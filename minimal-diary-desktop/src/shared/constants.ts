/**
 * 애플리케이션 상수
 */

/**
 * 애플리케이션 정보
 */
export const APP_INFO = {
  NAME: 'Minimal Diary',
  VERSION: '1.0.0',
  DESCRIPTION: '미니멀한 디자인의 데스크톱 일기장',
} as const;

/**
 * 기본 설정값
 */
export const DEFAULT_SETTINGS = {
  version: '1.0.0',
  appearance: {
    fontSize: 16,
    lineHeight: 1.8,
    fontFamily: 'Pretendard',
  },
  editor: {
    autoSave: true,
    saveInterval: 3000, // 3초
    spellCheck: true,
  },
  privacy: {
    confirmDelete: true,
  },
} as const;

/**
 * UI 상수
 */
export const UI = {
  SIDEBAR_WIDTH: 240,
  EDITOR_MAX_WIDTH: 800,
  EDITOR_PADDING: 48,
  WINDOW_MIN_WIDTH: 1024,
  WINDOW_MIN_HEIGHT: 768,
} as const;

/**
 * 타이밍 상수
 */
export const TIMING = {
  AUTO_SAVE_INTERVAL: 3000, // 3초
  SEARCH_DEBOUNCE: 300, // 300ms
  ANIMATION_DURATION: 200, // 200ms
} as const;

/**
 * 날짜 형식
 */
export const DATE_FORMATS = {
  FILE: 'yyyy-MM-dd', // 파일명용
  DISPLAY: 'yyyy년 M월 d일', // 화면 표시용
  ISO: 'yyyy-MM-dd', // ISO 8601
} as const;

/**
 * 파일 경로
 */
export const PATHS = {
  APP_DATA: 'MinimalDiary',
  DATA: 'data',
  CONFIG: 'config',
  BACKUPS: 'backups',
  SETTINGS_FILE: 'settings.json',
} as const;

/**
 * 검증 규칙
 */
export const VALIDATION = {
  MAX_CONTENT_LENGTH: 1000000, // 1MB
  MIN_FONT_SIZE: 14,
  MAX_FONT_SIZE: 24,
  MIN_LINE_HEIGHT: 1.4,
  MAX_LINE_HEIGHT: 2.0,
} as const;

/**
 * 키보드 단축키
 */
export const SHORTCUTS = {
  NEW_ENTRY: 'CommandOrControl+N',
  SAVE: 'CommandOrControl+S',
  SEARCH: 'CommandOrControl+F',
  SETTINGS: 'CommandOrControl+,',
  QUIT: 'CommandOrControl+Q',
} as const;
