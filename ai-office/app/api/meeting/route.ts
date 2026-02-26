import { GoogleGenerativeAI } from "@google/generative-ai";
import { getExpertById } from "../../data/experts";

const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY || "");

export const maxDuration = 300;

export async function POST(req: Request) {
  const { topic, expertIds } = await req.json();

  if (!topic || !expertIds || expertIds.length === 0) {
    return new Response(JSON.stringify({ error: "주제와 전문가 목록이 필요합니다." }), {
      status: 400,
    });
  }

  const encoder = new TextEncoder();

  const readable = new ReadableStream({
    async start(controller) {
      const send = (data: object) => {
        controller.enqueue(
          encoder.encode(`data: ${JSON.stringify(data)}\n\n`)
        );
      };

      const previousStatements: { name: string; role: string; content: string }[] = [];

      for (let i = 0; i < expertIds.length; i++) {
        const expertId = expertIds[i];
        const expert = getExpertById(expertId);
        if (!expert) continue;

        send({
          type: "expert_start",
          expertId: expert.id,
          expertName: expert.name,
          expertRole: expert.role,
          expertEmoji: expert.emoji,
          expertColor: expert.color,
          index: i,
          total: expertIds.length,
        });

        let userContent = `【회의 안건】\n${topic}\n\n`;

        if (previousStatements.length > 0) {
          userContent += `【이전 발언자 의견】\n`;
          for (const stmt of previousStatements) {
            userContent += `[${stmt.name} ${stmt.role}]\n${stmt.content}\n\n`;
          }
          userContent += `위 의견들을 참고하여 당신의 입장을 발언해주세요.`;
        } else {
          userContent += `이 안건에 대해 당신의 전문 분야 관점에서 첫 번째로 의견을 제시해주세요.`;
        }

        let fullContent = "";

        try {
          const model = genAI.getGenerativeModel({
            model: "gemini-1.5-flash",
            systemInstruction: expert.systemPrompt,
          });

          const result = await model.generateContentStream(userContent);

          for await (const chunk of result.stream) {
            const text = chunk.text();
            if (text) {
              fullContent += text;
              send({ type: "token", text });
            }
          }
        } catch (err) {
          console.error(`Error for expert ${expertId}:`, err);
          const errMsg = "[ 발언 중 오류가 발생했습니다. ]";
          fullContent = errMsg;
          send({ type: "token", text: errMsg });
        }

        previousStatements.push({
          name: expert.name,
          role: expert.role,
          content: fullContent,
        });

        send({
          type: "expert_end",
          expertId: expert.id,
          content: fullContent,
        });

        if (i < expertIds.length - 1) {
          await new Promise((r) => setTimeout(r, 150));
        }
      }

      controller.enqueue(encoder.encode("data: [DONE]\n\n"));
      controller.close();
    },
  });

  return new Response(readable, {
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      Connection: "keep-alive",
    },
  });
}
