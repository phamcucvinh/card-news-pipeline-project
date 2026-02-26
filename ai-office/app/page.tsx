"use client";

import { useState, useRef, useEffect } from "react";
import { EXPERTS } from "./data/experts";
import ExpertCard from "./components/ExpertCard";

interface Statement {
  expertId: string;
  expertName: string;
  expertRole: string;
  expertEmoji: string;
  expertColor: string;
  content: string;
  isStreaming: boolean;
  index: number;
}

interface Meeting {
  topic: string;
  expertIds: string[];
  statements: Statement[];
  status: "idle" | "running" | "done";
  currentIndex: number;
}

const SAMPLE_TOPICS = [
  "주 52시간 예외 조항 확대 논란",
  "AI 도입으로 인한 일자리 감소 대책",
  "최저임금 인상이 자영업에 미치는 영향",
  "청년 취업난과 대기업 채용 축소",
];

export default function VirtualOffice() {
  const [meeting, setMeeting] = useState<Meeting>({
    topic: "",
    expertIds: [],
    statements: [],
    status: "idle",
    currentIndex: -1,
  });
  const [input, setInput] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [meeting.statements]);

  const startMeeting = async () => {
    const topic = input.trim();
    if (!topic || meeting.status === "running") return;

    // 주제 분석 → 전문가 선발 (클라이언트에서 직접 계산)
    const expertIds = await getExpertIdsForTopic(topic);

    const newMeeting: Meeting = {
      topic,
      expertIds,
      statements: [],
      status: "running",
      currentIndex: 0,
    };
    setMeeting(newMeeting);
    setInput("");

    // SSE 스트리밍 시작
    await runMeeting(topic, expertIds);
  };

  const getExpertIdsForTopic = async (topic: string): Promise<string[]> => {
    const res = await fetch("/api/route-topic", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic }),
    });
    const data = await res.json();
    return data.expertIds as string[];
  };

  const runMeeting = async (topic: string, expertIds: string[]) => {
    try {
      const res = await fetch("/api/meeting", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic, expertIds }),
      });

      const reader = res.body?.getReader();
      const decoder = new TextDecoder();
      if (!reader) return;

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split("\n");

        for (const line of lines) {
          if (line === "data: [DONE]") {
            setMeeting((prev) => ({ ...prev, status: "done", currentIndex: -1 }));
            return;
          }
          if (line.startsWith("data: ")) {
            try {
              const data = JSON.parse(line.slice(6));

              if (data.type === "expert_start") {
                setMeeting((prev) => ({
                  ...prev,
                  currentIndex: data.index,
                  statements: [
                    ...prev.statements,
                    {
                      expertId: data.expertId,
                      expertName: data.expertName,
                      expertRole: data.expertRole,
                      expertEmoji: data.expertEmoji,
                      expertColor: data.expertColor,
                      content: "",
                      isStreaming: true,
                      index: data.index,
                    },
                  ],
                }));
              } else if (data.type === "token") {
                setMeeting((prev) => {
                  const stmts = [...prev.statements];
                  if (stmts.length > 0) {
                    stmts[stmts.length - 1] = {
                      ...stmts[stmts.length - 1],
                      content: stmts[stmts.length - 1].content + data.text,
                    };
                  }
                  return { ...prev, statements: stmts };
                });
              } else if (data.type === "expert_end") {
                setMeeting((prev) => {
                  const stmts = [...prev.statements];
                  if (stmts.length > 0) {
                    stmts[stmts.length - 1] = {
                      ...stmts[stmts.length - 1],
                      isStreaming: false,
                      content: data.content,
                    };
                  }
                  return { ...prev, statements: stmts };
                });
              }
            } catch {
              // ignore
            }
          }
        }
      }
    } catch (err) {
      console.error(err);
      setMeeting((prev) => ({ ...prev, status: "idle" }));
    }
  };

  const resetMeeting = () => {
    setMeeting({
      topic: "",
      expertIds: [],
      statements: [],
      status: "idle",
      currentIndex: -1,
    });
    setInput("");
  };

  const activeExperts = meeting.expertIds
    .map((id) => EXPERTS.find((e) => e.id === id))
    .filter(Boolean);

  const progress =
    meeting.expertIds.length > 0
      ? Math.round(
          (meeting.statements.filter((s) => !s.isStreaming).length /
            meeting.expertIds.length) *
            100
        )
      : 0;

  return (
    <div className="flex flex-col h-screen bg-gray-950 text-gray-100">
      {/* 헤더 */}
      <header className="flex items-center justify-between px-6 py-3 border-b border-gray-800 bg-gray-900 shrink-0">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-orange-500 flex items-center justify-center text-lg">
            🏢
          </div>
          <div>
            <h1 className="font-bold text-white text-base">가상사무실</h1>
            <p className="text-xs text-gray-400">30인 전문가 · Powered by Claude</p>
          </div>
        </div>
        <button
          onClick={resetMeeting}
          disabled={meeting.status === "running"}
          className="text-xs text-gray-400 hover:text-gray-200 px-3 py-1.5 rounded-lg hover:bg-gray-800 transition-colors disabled:opacity-40"
        >
          회의 초기화
        </button>
      </header>

      <div className="flex flex-1 overflow-hidden">
        {/* 왼쪽: 출근자 사이드바 */}
        <aside className="w-52 shrink-0 border-r border-gray-800 bg-gray-900 flex flex-col">
          <div className="px-4 py-3 border-b border-gray-800">
            <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider">
              {meeting.status === "idle" ? "전문가 30인" : `오늘의 출근자 ${activeExperts.length}명`}
            </p>
          </div>

          <div className="flex-1 overflow-y-auto py-2">
            {meeting.status === "idle" ? (
              // 아이들 상태: 전체 전문가 목록
              <div className="space-y-0.5 px-2">
                {EXPERTS.map((expert) => (
                  <div
                    key={expert.id}
                    className="flex items-center gap-2 px-2 py-1.5 rounded-lg text-gray-500"
                  >
                    <span className="text-base">{expert.emoji}</span>
                    <div className="min-w-0">
                      <p className="text-xs text-gray-400 truncate">{expert.role}</p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              // 회의 중: 참가 전문가
              <div className="space-y-1 px-2">
                {activeExperts.map((expert, idx) => {
                  if (!expert) return null;
                  const stmt = meeting.statements.find(
                    (s) => s.expertId === expert.id
                  );
                  const isDone = stmt && !stmt.isStreaming;
                  const isSpeaking = stmt?.isStreaming;
                  const isPending = !stmt;

                  return (
                    <div
                      key={expert.id}
                      className={`flex items-center gap-2 px-2 py-2 rounded-lg transition-colors ${
                        isSpeaking
                          ? "bg-orange-500/20 border border-orange-500/30"
                          : isDone
                          ? "bg-gray-800/50"
                          : "opacity-50"
                      }`}
                    >
                      <span className="text-base shrink-0">{expert.emoji}</span>
                      <div className="min-w-0 flex-1">
                        <p className="text-xs font-medium text-gray-200 truncate">
                          {expert.name}
                        </p>
                        <p className="text-xs text-gray-500 truncate">{expert.role}</p>
                      </div>
                      <span className="shrink-0 text-xs">
                        {isSpeaking ? "🔴" : isDone ? "✅" : "⏳"}
                      </span>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </aside>

        {/* 오른쪽: 회의실 */}
        <main className="flex-1 flex flex-col overflow-hidden">
          {/* 회의실 본문 */}
          <div className="flex-1 overflow-y-auto px-6 py-6">
            {meeting.status === "idle" && meeting.statements.length === 0 && (
              <div className="flex flex-col items-center justify-center h-full gap-5 text-center">
                <div className="w-20 h-20 rounded-3xl bg-orange-500/10 flex items-center justify-center text-4xl">
                  🏢
                </div>
                <div>
                  <h2 className="text-2xl font-bold text-white mb-2">
                    가상사무실
                  </h2>
                  <p className="text-gray-400 text-sm max-w-md">
                    주제를 입력하면 관련 분야 전문가들이 자동으로 소집되어
                    순차적으로 의견을 나눕니다.
                  </p>
                </div>
                <div className="grid grid-cols-2 gap-2 max-w-lg w-full mt-2">
                  {SAMPLE_TOPICS.map((t) => (
                    <button
                      key={t}
                      onClick={() => setInput(t)}
                      className="text-sm text-gray-300 bg-gray-800 hover:bg-gray-700 px-4 py-3 rounded-xl transition-colors text-left border border-gray-700 hover:border-gray-600"
                    >
                      💬 {t}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* 안건 헤더 */}
            {meeting.topic && (
              <div className="mb-6 p-4 bg-gray-800/50 rounded-xl border border-gray-700">
                <p className="text-xs text-gray-400 mb-1">📋 회의 안건</p>
                <p className="text-white font-semibold">{meeting.topic}</p>
                {meeting.status !== "idle" && (
                  <div className="mt-3">
                    <div className="flex justify-between text-xs text-gray-400 mb-1">
                      <span>토론 진행 중...</span>
                      <span>
                        {meeting.statements.filter((s) => !s.isStreaming).length} /{" "}
                        {meeting.expertIds.length}
                      </span>
                    </div>
                    <div className="w-full bg-gray-700 rounded-full h-1.5">
                      <div
                        className="bg-orange-500 h-1.5 rounded-full transition-all duration-500"
                        style={{ width: `${progress}%` }}
                      />
                    </div>
                  </div>
                )}
                {meeting.status === "done" && (
                  <p className="mt-2 text-xs text-green-400">✅ 회의가 종료되었습니다.</p>
                )}
              </div>
            )}

            {/* 전문가 발언 목록 */}
            <div className="space-y-2">
              {meeting.statements.map((stmt, i) => (
                <ExpertCard
                  key={`${stmt.expertId}-${i}`}
                  emoji={stmt.expertEmoji}
                  name={stmt.expertName}
                  role={stmt.expertRole}
                  color={stmt.expertColor}
                  content={stmt.content}
                  isStreaming={stmt.isStreaming}
                  index={stmt.index}
                  total={meeting.expertIds.length}
                />
              ))}
            </div>

            <div ref={bottomRef} />
          </div>

          {/* 입력창 */}
          <div className="px-6 py-4 border-t border-gray-800 bg-gray-900 shrink-0">
            <div className="flex gap-3 items-end max-w-3xl mx-auto">
              <div className="flex-1 bg-gray-800 rounded-2xl border border-gray-700 focus-within:border-orange-500/50 transition-colors">
                <textarea
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && !e.shiftKey) {
                      e.preventDefault();
                      startMeeting();
                    }
                  }}
                  placeholder="회의 안건을 입력하세요... (Enter: 회의 시작)"
                  rows={1}
                  disabled={meeting.status === "running"}
                  className="w-full bg-transparent px-4 py-3 text-sm text-gray-100 placeholder-gray-500 resize-none outline-none max-h-32 disabled:opacity-50"
                  style={{ minHeight: "44px" }}
                  onInput={(e) => {
                    const el = e.currentTarget;
                    el.style.height = "auto";
                    el.style.height = Math.min(el.scrollHeight, 128) + "px";
                  }}
                />
              </div>
              <button
                onClick={startMeeting}
                disabled={meeting.status === "running" || !input.trim()}
                className="px-4 h-11 rounded-xl bg-orange-500 hover:bg-orange-400 disabled:bg-gray-700 disabled:cursor-not-allowed transition-colors flex items-center gap-2 shrink-0 text-sm font-medium"
              >
                {meeting.status === "running" ? (
                  <>
                    <svg className="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                    </svg>
                    회의 중
                  </>
                ) : (
                  <>🚀 회의 시작</>
                )}
              </button>
            </div>
            <p className="text-center text-xs text-gray-600 mt-2">
              가상사무실 · 30인 전문가 토론 시스템 by Claude
            </p>
          </div>
        </main>
      </div>
    </div>
  );
}
