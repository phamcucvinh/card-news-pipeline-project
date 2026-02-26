/**
 * 일기장 애플리케이션 공유 타입 정의
 */

/**
 * 일기 항목
 */
export interface DiaryEntry {
  /** 고유 ID (UUID v4) */
  id: string;
  /** 일기 날짜 (YYYY-MM-DD) */
  date: string;
  /** 생성 시간 (Unix timestamp, ms) */
  createdAt: number;
  /** 수정 시간 (Unix timestamp, ms) */
  updatedAt: number;
  /** 본문 내용 */
  content: string;
  /** 단어 수 */
  wordCount: number;
}

/**
 * 애플리케이션 설정
 */
export interface Settings {
  /** 설정 버전 */
  version: string;
  /** 외관 설정 */
  appearance: AppearanceSettings;
  /** 편집기 설정 */
  editor: EditorSettings;
  /** 프라이버시 설정 */
  privacy: PrivacySettings;
}

/**
 * 외관 설정
 */
export interface AppearanceSettings {
  /** 글꼴 크기 (px) */
  fontSize: number;
  /** 줄 간격 */
  lineHeight: number;
  /** 글꼴 패밀리 */
  fontFamily: string;
}

/**
 * 편집기 설정
 */
export interface EditorSettings {
  /** 자동 저장 활성화 */
  autoSave: boolean;
  /** 자동 저장 간격 (ms) */
  saveInterval: number;
  /** 맞춤법 검사 활성화 */
  spellCheck: boolean;
}

/**
 * 프라이버시 설정
 */
export interface PrivacySettings {
  /** 삭제 시 확인 메시지 표시 */
  confirmDelete: boolean;
}

/**
 * 검색 결과 항목
 */
export interface SearchResult {
  /** 일기 항목 */
  entry: DiaryEntry;
  /** 일치하는 텍스트 스니펫 */
  snippet: string;
  /** 일치하는 위치들 */
  matches: number[];
}

/**
 * 날짜 범위
 */
export interface DateRange {
  /** 시작 날짜 */
  start: Date;
  /** 종료 날짜 */
  end: Date;
}

/**
 * 파일 시스템 오류 타입
 */
export enum FileSystemErrorType {
  NOT_FOUND = 'NOT_FOUND',
  PERMISSION_DENIED = 'PERMISSION_DENIED',
  ALREADY_EXISTS = 'ALREADY_EXISTS',
  INVALID_FORMAT = 'INVALID_FORMAT',
  UNKNOWN = 'UNKNOWN',
}

/**
 * 파일 시스템 오류
 */
export interface FileSystemError {
  type: FileSystemErrorType;
  message: string;
  path?: string;
}

/**
 * API 응답
 */
export type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };
