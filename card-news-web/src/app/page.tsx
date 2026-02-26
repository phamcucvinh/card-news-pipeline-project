"use client";

import { useState, useRef } from "react";

const RATIOS = [
  { label: "1:1", value: "1:1", aspect: "aspect-square" },
  { label: "9:16", value: "9:16", aspect: "aspect-[9/16]" },
  { label: "16:9", value: "16:9", aspect: "aspect-video" },
  { label: "4:3", value: "4:3", aspect: "aspect-[4/3]" },
  { label: "Story", value: "Instagram Story", aspect: "aspect-[9/16]" },
  { label: "Twitter", value: "Twitter", aspect: "aspect-[16/9]" },
];

const STYLES: Record<string, { bg: string; text: string; num: string; border: string; tag: string }> = {
  modern:   { bg: "from-violet-600 via-purple-600 to-indigo-700", text: "text-white", num: "text-white/40", border: "border-white/20", tag: "bg-white/20 text-white" },
  minimal:  { bg: "from-gray-50 to-white", text: "text-gray-900", num: "text-gray-200", border: "border-gray-200", tag: "bg-gray-100 text-gray-600" },
  dark:     { bg: "from-gray-900 via-gray-800 to-black", text: "text-white", num: "text-white/20", border: "border-white/10", tag: "bg-white/10 text-gray-300" },
  colorful: { bg: "from-pink-500 via-orange-400 to-yellow-400", text: "text-white", num: "text-white/40", border: "border-white/20", tag: "bg-white/20 text-white" },
};

const CARD_COUNT = [3, 5, 7, 10];

function CardPreview({ text, index, total, style, title }: {
  text: string; index: number; total: number; style: string; title: string;
}) {
  const s = STYLES[style] || STYLES.modern;
  const isFirst = index === 0;
  const isLast = index === total - 1;

  return (
    <div className={`relative w-full bg-gradient-to-br ${s.bg} rounded-2xl p-8 flex flex-col justify-between shadow-2xl border ${s.border} min-h-[320px]`}>
      {/* 배경 장식 */}
      <div className="absolute top-0 right-0 w-40 h-40 rounded-full bg-white/5 -translate-y-1/2 translate-x-1/2" />
      <div className="absolute bottom-0 left-0 w-24 h-24 rounded-full bg-white/5 translate-y-1/2 -translate-x-1/2" />

      {/* 상단 */}
      <div className="relative">
        <div className="flex items-center justify-between mb-6">
          <span className={`text-xs font-bold px-3 py-1 rounded-full ${s.tag}`}>
            {isFirst ? "🚀 시작" : isLast ? "✅ 마무리" : `📌 포인트 ${index}`}
          </span>
          <span className={`text-sm font-medium ${s.text} opacity-60`}>{index + 1} / {total}</span>
        </div>
        {isFirst && (
          <h2 className={`text-2xl font-black leading-tight mb-4 ${s.text}`}>{title}</h2>
        )}
      </div>

      {/* 카드 번호 (배경) */}
      <div className={`absolute right-6 bottom-16 text-8xl font-black ${s.num} select-none`}>
        {String(index + 1).padStart(2, "0")}
      </div>

      {/* 본문 */}
      <div className="relative">
        <p className={`text-lg leading-relaxed font-medium ${s.text}`}>{text}</p>
      </div>

      {/* 하단 브랜드 */}
      <div className={`mt-6 pt-4 border-t ${s.border} flex items-center justify-between`}>
        <span className={`text-xs ${s.text} opacity-40 font-medium`}>AI 카드뉴스 생성기</span>
        <div className="flex gap-1">
          {Array.from({ length: total }).map((_, i) => (
            <div key={i} className={`w-1.5 h-1.5 rounded-full ${i === index ? "bg-white opacity-80" : "bg-white/30"}`} />
          ))}
        </div>
      </div>
    </div>
  );
}

export default function Home() {
  const [topic, setTopic] = useState("");
  const [ratio, setRatio] = useState("1:1");
  const [style, setStyle] = useState("modern");
  const [count, setCount] = useState(7);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ cards: string[]; title: string } | null>(null);
  const [error, setError] = useState("");
  const [activeCard, setActiveCard] = useState(0);
  const resultRef = useRef<HTMLDivElement>(null);

  const selectedRatio = RATIOS.find(r => r.value === ratio) || RATIOS[0];

  async function generate() {
    if (!topic.trim()) { setError("주제를 입력해주세요"); return; }
    setError("");
    setLoading(true);
    setResult(null);
    setActiveCard(0);
    try {
      const res = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic, ratio, style, count }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "생성 실패");
      setResult(data);
      setTimeout(() => resultRef.current?.scrollIntoView({ behavior: "smooth" }), 100);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "오류가 발생했습니다");
    } finally {
      setLoading(false);
    }
  }

  function copyAll() {
    if (!result) return;
    navigator.clipboard.writeText(result.cards.map((c, i) => `[${i+1}] ${c}`).join("\n\n"));
    alert("클립보드에 복사되었습니다!");
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="max-w-5xl mx-auto px-4 py-12">

        {/* 헤더 */}
        <div className="text-center mb-10">
          <div className="inline-flex items-center gap-2 bg-white/10 rounded-full px-4 py-2 mb-4 text-purple-300 text-sm font-medium">
            ✨ AI 자동 생성
          </div>
          <h1 className="text-5xl font-black text-white mb-3 tracking-tight">
            카드뉴스 생성기
          </h1>
          <p className="text-purple-300 text-lg">주제만 입력하면 AI가 바로 만들어드립니다</p>
        </div>

        {/* 입력 폼 */}
        <div className="bg-white/10 backdrop-blur-md rounded-3xl p-8 mb-8 border border-white/20 shadow-xl">

          {/* 주제 */}
          <div className="mb-6">
            <label className="block text-white/80 text-sm font-semibold mb-2 uppercase tracking-wider">주제 입력</label>
            <input
              type="text"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && generate()}
              placeholder="예: 2026년 SNS 마케팅 트렌드, 건강한 식습관의 비밀..."
              className="w-full px-5 py-4 rounded-2xl bg-white/10 border border-white/20 text-white placeholder-white/30 focus:outline-none focus:border-purple-400 focus:bg-white/15 text-lg transition-all"
            />
          </div>

          {/* 옵션 3열 */}
          <div className="grid grid-cols-3 gap-6 mb-8">
            {/* 비율 */}
            <div>
              <label className="block text-white/80 text-sm font-semibold mb-3 uppercase tracking-wider">비율</label>
              <div className="flex flex-col gap-2">
                {RATIOS.map((r) => (
                  <button key={r.value} onClick={() => setRatio(r.value)}
                    className={`px-3 py-2 rounded-xl border text-sm font-medium transition-all text-left ${
                      ratio === r.value ? "bg-purple-500 border-purple-400 text-white" : "bg-white/5 border-white/10 text-white/60 hover:bg-white/15"
                    }`}>
                    {r.label}
                  </button>
                ))}
              </div>
            </div>

            {/* 스타일 */}
            <div>
              <label className="block text-white/80 text-sm font-semibold mb-3 uppercase tracking-wider">스타일</label>
              <div className="flex flex-col gap-2">
                {Object.entries(STYLES).map(([k]) => (
                  <button key={k} onClick={() => setStyle(k)}
                    className={`px-3 py-2 rounded-xl border text-sm font-medium transition-all text-left ${
                      style === k ? "bg-purple-500 border-purple-400 text-white" : "bg-white/5 border-white/10 text-white/60 hover:bg-white/15"
                    }`}>
                    {k === "modern" ? "🌈 모던" : k === "minimal" ? "⬜ 미니멀" : k === "dark" ? "🌑 다크" : "🎨 컬러풀"}
                  </button>
                ))}
              </div>
            </div>

            {/* 카드 수 */}
            <div>
              <label className="block text-white/80 text-sm font-semibold mb-3 uppercase tracking-wider">카드 수</label>
              <div className="grid grid-cols-2 gap-2">
                {CARD_COUNT.map((n) => (
                  <button key={n} onClick={() => setCount(n)}
                    className={`py-3 rounded-xl border text-xl font-black transition-all ${
                      count === n ? "bg-purple-500 border-purple-400 text-white" : "bg-white/5 border-white/10 text-white/60 hover:bg-white/15"
                    }`}>
                    {n}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {error && <p className="text-red-400 mb-4 text-sm bg-red-400/10 rounded-xl px-4 py-3">⚠️ {error}</p>}

          <button onClick={generate} disabled={loading}
            className="w-full py-5 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-black text-xl rounded-2xl hover:from-purple-600 hover:to-pink-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-purple-500/30 hover:scale-[1.01]">
            {loading ? (
              <span className="flex items-center justify-center gap-3">
                <svg className="animate-spin h-6 w-6" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
                </svg>
                AI가 카드뉴스를 생성 중...
              </span>
            ) : "✨ 카드뉴스 생성하기"}
          </button>
        </div>

        {/* 결과 */}
        {result && (
          <div ref={resultRef} className="animate-fadeIn">
            {/* 헤더 */}
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-2xl font-black text-white">{result.title}</h2>
                <p className="text-purple-300 text-sm mt-1">{result.cards.length}장 생성 완료</p>
              </div>
              <button onClick={copyAll}
                className="px-5 py-2.5 bg-white/10 hover:bg-white/20 text-white rounded-xl text-sm font-medium transition-all border border-white/20">
                📋 전체 복사
              </button>
            </div>

            {/* 레이아웃: 썸네일 + 미리보기 */}
            <div className="grid grid-cols-[200px_1fr] gap-6">
              {/* 썸네일 목록 */}
              <div className="flex flex-col gap-3 max-h-[600px] overflow-y-auto pr-1 scrollbar-thin">
                {result.cards.map((card, i) => (
                  <button key={i} onClick={() => setActiveCard(i)}
                    className={`text-left p-3 rounded-xl border transition-all ${
                      activeCard === i ? "bg-purple-500/30 border-purple-400" : "bg-white/5 border-white/10 hover:bg-white/10"
                    }`}>
                    <span className="block text-xs font-black text-purple-400 mb-1">{String(i+1).padStart(2,"0")}</span>
                    <span className="text-white/70 text-xs leading-relaxed line-clamp-3">{card}</span>
                  </button>
                ))}
              </div>

              {/* 카드 미리보기 */}
              <div className="flex flex-col gap-4">
                <div className={`w-full ${selectedRatio.aspect} max-h-[560px]`}>
                  <div className="w-full h-full">
                    <CardPreview
                      text={result.cards[activeCard]}
                      index={activeCard}
                      total={result.cards.length}
                      style={style}
                      title={result.title}
                    />
                  </div>
                </div>
                {/* 이전/다음 */}
                <div className="flex gap-3">
                  <button onClick={() => setActiveCard(Math.max(0, activeCard - 1))}
                    disabled={activeCard === 0}
                    className="flex-1 py-3 bg-white/10 hover:bg-white/20 text-white rounded-xl font-medium disabled:opacity-30 transition-all">
                    ← 이전
                  </button>
                  <button onClick={() => setActiveCard(Math.min(result.cards.length - 1, activeCard + 1))}
                    disabled={activeCard === result.cards.length - 1}
                    className="flex-1 py-3 bg-white/10 hover:bg-white/20 text-white rounded-xl font-medium disabled:opacity-30 transition-all">
                    다음 →
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
