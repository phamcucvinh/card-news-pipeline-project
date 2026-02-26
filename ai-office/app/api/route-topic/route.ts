import { routeTopic } from "../../lib/topic-router";

export async function POST(req: Request) {
  const { topic } = await req.json();

  if (!topic) {
    return new Response(JSON.stringify({ error: "주제가 필요합니다." }), {
      status: 400,
    });
  }

  const experts = routeTopic(topic);
  const expertIds = experts.map((e) => e.id);

  return new Response(JSON.stringify({ expertIds, experts }), {
    headers: { "Content-Type": "application/json" },
  });
}
