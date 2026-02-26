import { EXPERTS, Expert } from "../data/experts";

interface RoutingRule {
  keywords: string[];
  expertIds: string[];
}

const ROUTING_RULES: RoutingRule[] = [
  {
    keywords: ["노무", "노동", "근로", "임금", "해고", "퇴직", "4대보험", "주52시간", "야근", "연차", "인사", "단체협약", "노조", "산재"],
    expertIds: ["nomu", "lawyer", "union", "ceo", "hr", "official", "safety", "doctor", "mediator"],
  },
  {
    keywords: ["세금", "세무", "회계", "재무", "납세", "부가세", "법인세", "절세", "결산"],
    expertIds: ["taxman", "accountant", "finance", "ceo", "official", "investor", "mediator"],
  },
  {
    keywords: ["AI", "인공지능", "자동화", "IT", "기술", "디지털", "소프트웨어", "개발", "로봇", "플랫폼"],
    expertIds: ["ai_expert", "it", "data", "startup", "ceo", "professor", "ethicist", "journalist"],
  },
  {
    keywords: ["환경", "ESG", "탄소", "기후", "친환경", "지속가능", "탄소중립", "녹색"],
    expertIds: ["environment", "ceo", "official", "activist", "investor", "journalist", "urban"],
  },
  {
    keywords: ["건강", "의료", "질병", "스트레스", "번아웃", "과로", "정신건강", "산재", "직업병"],
    expertIds: ["doctor", "counselor", "safety", "official", "welfare", "nomu", "union"],
  },
  {
    keywords: ["취업", "채용", "실업", "청년", "일자리", "구직", "아르바이트", "인턴"],
    expertIds: ["hr", "student", "professor", "official", "journalist", "nomu", "startup", "welfare"],
  },
  {
    keywords: ["투자", "주식", "금융", "대출", "금리", "부동산", "자산"],
    expertIds: ["investor", "finance", "accountant", "taxman", "journalist", "ethicist"],
  },
  {
    keywords: ["국제", "글로벌", "해외", "수출", "무역", "OECD", "FTA", "외국"],
    expertIds: ["diplomat", "trade", "ceo", "official", "journalist", "startup"],
  },
  {
    keywords: ["복지", "취약계층", "장애", "노인", "빈곤", "사회안전망", "지원"],
    expertIds: ["welfare", "activist", "official", "counselor", "journalist", "legislator"],
  },
  {
    keywords: ["법안", "입법", "정책", "규제", "제도", "국회", "개혁", "법"],
    expertIds: ["legislator", "lawyer", "official", "journalist", "ethicist", "professor", "activist"],
  },
];

const DEFAULT_EXPERTS = ["professor", "ceo", "official", "lawyer", "mediator"];
const MIN_EXPERTS = 5;
const MAX_EXPERTS = 9;

export function routeTopic(topic: string): Expert[] {
  const topicLower = topic.toLowerCase();
  const scoreMap = new Map<string, number>();

  // 키워드 매칭으로 전문가 점수 계산
  for (const rule of ROUTING_RULES) {
    let ruleScore = 0;
    for (const kw of rule.keywords) {
      if (topicLower.includes(kw.toLowerCase())) {
        ruleScore += 1;
      }
    }
    if (ruleScore > 0) {
      for (const expertId of rule.expertIds) {
        scoreMap.set(expertId, (scoreMap.get(expertId) || 0) + ruleScore);
      }
    }
  }

  // 점수 순 정렬
  let selected: string[] = Array.from(scoreMap.entries())
    .sort((a, b) => b[1] - a[1])
    .map(([id]) => id);

  // 최소 인원 보장
  if (selected.length < MIN_EXPERTS) {
    for (const defaultId of DEFAULT_EXPERTS) {
      if (!selected.includes(defaultId)) {
        selected.push(defaultId);
      }
      if (selected.length >= MIN_EXPERTS) break;
    }
  }

  // 최대 인원 제한
  selected = selected.slice(0, MAX_EXPERTS);

  // 항상 중재자를 마지막에 배치
  if (!selected.includes("mediator")) {
    if (selected.length >= MAX_EXPERTS) selected.pop();
    selected.push("mediator");
  } else {
    const idx = selected.indexOf("mediator");
    selected.splice(idx, 1);
    selected.push("mediator");
  }

  // Expert 객체로 변환
  return selected
    .map(id => EXPERTS.find(e => e.id === id))
    .filter((e): e is Expert => e !== undefined);
}
