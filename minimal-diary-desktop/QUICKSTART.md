# 🚀 빠른 시작 가이드

## 설치 및 실행

### 1단계: 의존성 설치

```bash
cd /mnt/c/Users/SAMSUNG/Desktop/저작권/minimal-diary-desktop
npm install
```

### 2단계: 애플리케이션 실행

```bash
npm start
```

## 실행 방법

### 방법 1: 간단한 실행 (권장)
```bash
npm start
```
- 빌드 후 Electron 앱을 바로 실행합니다
- 가장 빠르고 간단한 방법입니다

### 방법 2: 개발 모드 (핫 리로드)
```bash
npm run dev
```
- 코드 변경 시 자동으로 다시 로드됩니다
- 개발할 때 사용하세요

### 방법 3: 프로덕션 빌드
```bash
npm run build
electron .
```
- 최적화된 프로덕션 빌드를 생성합니다

## 문제 해결

### 오류: "Cannot find module"
```bash
# node_modules 삭제 후 재설치
rm -rf node_modules package-lock.json
npm install
```

### 오류: "webpack command not found"
```bash
# webpack-cli 재설치
npm install --save-dev webpack-cli
```

### 오류: "Electron failed to start"
```bash
# dist 폴더 삭제 후 재빌드
rm -rf dist
npm run build:dev
npm start
```

## 현재 구현된 기능

✅ 기본 Electron 창 띄우기
✅ React 기반 UI
✅ 미니멀 디자인 레이아웃
✅ 사이드바 네비게이션
✅ 일기 에디터 텍스트 영역
✅ 글자 수 카운터

## 다음 구현 예정

⏳ 일기 저장 기능
⏳ 날짜별 일기 로드
⏳ 달력 뷰
⏳ 검색 기능
⏳ 설정 기능

## 개발 팁

- `Ctrl+Shift+I` (Windows/Linux) 또는 `Cmd+Option+I` (macOS): 개발자 도구 열기
- 코드 수정 후 `npm start` 재실행으로 변경사항 확인
- `src/renderer/App.tsx`에서 UI 수정
- `src/renderer/App.css`에서 스타일 수정

## 폴더 구조

```
src/
├── main/           # Electron 메인 프로세스
│   └── index.ts    # 앱 진입점
├── renderer/       # React UI
│   ├── index.tsx   # React 진입점
│   ├── App.tsx     # 메인 앱 컴포넌트
│   ├── App.css     # 앱 스타일
│   ├── index.html  # HTML 템플릿
│   └── styles/     # 글로벌 스타일
└── shared/         # 공유 코드
    ├── types.ts    # TypeScript 타입
    └── constants.ts # 상수
```

## 도움이 필요하신가요?

- 설계 문서: [docs/DESIGN.md](docs/DESIGN.md)
- README: [README.md](README.md)
