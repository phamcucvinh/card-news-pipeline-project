"use client";

interface ExpertCardProps {
  emoji: string;
  name: string;
  role: string;
  color: string;
  content: string;
  isStreaming?: boolean;
  index: number;
  total: number;
}

export default function ExpertCard({
  emoji,
  name,
  role,
  color,
  content,
  isStreaming = false,
  index,
  total,
}: ExpertCardProps) {
  return (
    <div className="flex gap-3 animate-fadeIn">
      {/* 아바타 */}
      <div className="shrink-0 flex flex-col items-center gap-1">
        <div
          className={`w-10 h-10 rounded-xl ${color} flex items-center justify-center text-xl shadow-md`}
        >
          {emoji}
        </div>
        {/* 발언 순서 라인 */}
        {index < total - 1 && (
          <div className="w-0.5 flex-1 bg-gray-700 min-h-[20px]" />
        )}
      </div>

      {/* 발언 내용 */}
      <div className="flex-1 mb-4">
        {/* 헤더 */}
        <div className="flex items-center gap-2 mb-1.5">
          <span className="font-semibold text-white text-sm">{name}</span>
          <span className="text-xs text-gray-400 bg-gray-800 px-2 py-0.5 rounded-full">
            {role}
          </span>
          {isStreaming && (
            <span className="flex items-center gap-1 text-xs text-orange-400">
              <span className="w-1.5 h-1.5 bg-orange-400 rounded-full animate-pulse" />
              발언 중
            </span>
          )}
          {!isStreaming && content && (
            <span className="text-xs text-gray-600">
              {index + 1} / {total}
            </span>
          )}
        </div>

        {/* 발언 버블 */}
        <div className="bg-gray-800 rounded-2xl rounded-tl-sm px-4 py-3 text-sm text-gray-100 leading-relaxed whitespace-pre-wrap border border-gray-700">
          {content || (
            isStreaming ? (
              <span className="inline-flex gap-1">
                <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce [animation-delay:0ms]" />
                <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce [animation-delay:150ms]" />
                <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce [animation-delay:300ms]" />
              </span>
            ) : null
          )}
        </div>
      </div>
    </div>
  );
}
