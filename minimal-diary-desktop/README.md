# 🗒️ Minimal Diary Desktop

> 미니멀한 디자인의 데스크톱 일기장 애플리케이션

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)
![Version](https://img.shields.io/badge/version-1.0.0-green.svg)

## 📖 소개

Minimal Diary Desktop은 단순함과 집중에 초점을 맞춘 일기장 애플리케이션입니다. 복잡한 기능 대신 글쓰기에만 집중할 수 있도록 설계되었습니다.

### ✨ 핵심 가치

- **단순함**: 불필요한 기능 없이 글쓰기에만 집중
- **프라이버시**: 모든 데이터는 로컬에 저장
- **미니멀 디자인**: 깔끔하고 방해받지 않는 인터페이스
- **크로스 플랫폼**: Windows, macOS, Linux 지원

## 🎯 주요 기능

- ✍️ **일기 작성**: 날짜별 일기 작성 및 편집
- 📅 **달력 보기**: 월간 달력으로 일기 확인
- 🔍 **검색**: 전체 일기 내용 검색
- ⚙️ **설정**: 글꼴, 줄 간격 등 개인화
- 💾 **자동 저장**: 3초마다 자동으로 저장
- 🔐 **프라이버시**: 로컬 저장, 외부 서버 불필요

## 🖼️ 스크린샷

_추후 추가 예정_

## 🚀 시작하기

### 필수 요구사항

- Node.js 18 이상
- npm 또는 yarn

### 설치 방법

```bash
# 저장소 클론
git clone https://github.com/yourusername/minimal-diary-desktop.git

# 디렉토리 이동
cd minimal-diary-desktop

# 의존성 설치
npm install

# 개발 모드 실행
npm run dev
```

### 빌드

```bash
# 모든 플랫폼용 빌드
npm run build

# Windows용 빌드
npm run build:win

# macOS용 빌드
npm run build:mac

# Linux용 빌드
npm run build:linux
```

## 📁 프로젝트 구조

```
minimal-diary-desktop/
├── docs/                 # 문서
│   └── DESIGN.md        # 설계 문서
├── src/                 # 소스 코드
│   ├── main/           # Electron 메인 프로세스
│   ├── renderer/       # React 렌더러 프로세스
│   │   ├── components/ # React 컴포넌트
│   │   ├── contexts/   # React Context
│   │   ├── hooks/      # 커스텀 훅
│   │   ├── styles/     # 스타일
│   │   └── utils/      # 유틸리티
│   └── shared/         # 공유 타입 및 상수
├── tests/              # 테스트
├── package.json
└── README.md
```

## 🛠️ 기술 스택

- **Frontend**: React 18 + TypeScript
- **Desktop**: Electron
- **상태 관리**: React Context API
- **스타일링**: CSS Modules
- **빌드**: Webpack
- **테스트**: Jest + React Testing Library

## 📚 문서

자세한 설계 문서는 [DESIGN.md](./docs/DESIGN.md)를 참고하세요.

## 🤝 기여하기

기여를 환영합니다! 다음 단계를 따라주세요:

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참고하세요.

## 📧 연락처

프로젝트 관련 문의: [이메일 주소]

프로젝트 링크: [https://github.com/yourusername/minimal-diary-desktop](https://github.com/yourusername/minimal-diary-desktop)

## 🙏 감사의 글

- [Electron](https://www.electronjs.org/)
- [React](https://react.dev/)
- [TypeScript](https://www.typescriptlang.org/)

## 🗺️ 로드맵

- [x] 기본 설계 완료
- [ ] 프로젝트 초기 설정
- [ ] UI 컴포넌트 구현
- [ ] 핵심 기능 구현
- [ ] 테스트 작성
- [ ] v1.0.0 릴리스
- [ ] 다크 모드 추가
- [ ] 클라우드 백업 (선택적)

---

**Made with ❤️ by [Your Name]**
