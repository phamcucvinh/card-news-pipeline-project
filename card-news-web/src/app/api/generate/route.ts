import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  const { topic, ratio, style, count } = await req.json();

  if (!topic) {
    return NextResponse.json({ error: "주제를 입력해주세요" }, { status: 400 });
  }

  const apiKey = process.env.ANTHROPIC_API_KEY || process.env.OPENAI_API_KEY;
  if (!apiKey) {
    // API 키 없으면 데모 데이터 반환
    return NextResponse.json(demoData(topic, count));
  }

  try {
    const prompt = `당신은 SNS 카드뉴스 전문 작가입니다.
주제: "${topic}"
비율: ${ratio}
스타일: ${style}
카드 수: ${count}장

위 주제로 ${count}장의 카드뉴스 내용을 작성해주세요.
각 카드는 핵심 내용 1가지를 담아야 합니다.
각 카드 내용은 2~3문장으로 간결하게 작성하세요.
한국어로 작성하세요.

응답 형식 (JSON):
{
  "title": "카드뉴스 제목",
  "cards": [
    "첫 번째 카드 내용...",
    "두 번째 카드 내용...",
    ...
  ]
}`;

    // Anthropic API 호출
    const response = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "x-api-key": process.env.ANTHROPIC_API_KEY || "",
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
      },
      body: JSON.stringify({
        model: "claude-haiku-4-5-20251001",
        max_tokens: 2000,
        messages: [{ role: "user", content: prompt }],
      }),
    });

    const data = await response.json();
    const text = data.content?.[0]?.text || "";
    const jsonMatch = text.match(/\{[\s\S]*\}/);
    if (!jsonMatch) throw new Error("JSON 파싱 실패");
    const parsed = JSON.parse(jsonMatch[0]);
    return NextResponse.json(parsed);
  } catch {
    return NextResponse.json(demoData(topic, count));
  }
}

function demoData(topic: string, count: number) {
  const cards = Array.from({ length: count }, (_, i) => {
    const demos = [
      `${topic}의 핵심 포인트 ${i + 1}번입니다. AI API 키를 설정하면 실제 내용이 생성됩니다.`,
      `두 번째 중요한 사항입니다. .env.local 파일에 ANTHROPIC_API_KEY를 추가해주세요.`,
      `세 번째 인사이트입니다. 카드뉴스가 자동으로 생성되어 SNS에 공유할 수 있습니다.`,
      `네 번째 팁입니다. 비율과 스타일을 선택해 다양한 형식으로 제작 가능합니다.`,
      `다섯 번째 정보입니다. Vercel에 배포하면 어디서든 사용 가능합니다.`,
      `여섯 번째 포인트입니다. 생성된 내용은 클립보드에 복사해 바로 활용하세요.`,
      `일곱 번째 내용입니다. 카드 수, 비율, 스타일을 자유롭게 조합할 수 있습니다.`,
      `여덟 번째 사항입니다. 지금 바로 API 키를 설정해 실제 AI 생성을 경험해보세요.`,
      `아홉 번째 팁입니다. 주제만 입력하면 전문적인 카드뉴스가 자동 완성됩니다.`,
      `열 번째 마무리입니다. AI 카드뉴스 생성기로 콘텐츠 제작 시간을 90% 단축하세요.`,
    ];
    return demos[i % demos.length];
  });
  return { title: `${topic} - AI 카드뉴스`, cards };
}
