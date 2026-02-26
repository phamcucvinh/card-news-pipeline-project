# PDF to MP3 Converter

PDF 파일을 음성(MP3) 파일로 변환하는 Node.js 프로그램입니다.

## 기능

- ✅ PDF 파일에서 텍스트 자동 추출
- ✅ 텍스트를 음성(TTS)으로 변환
- ✅ MP3 파일로 저장
- ✅ 여러 언어 지원 (한국어, 영어, 일본어 등)
- ✅ 긴 텍스트 자동 분할 처리
- ✅ 디렉토리 일괄 변환 지원

## 설치

### 1. 필요한 패키지 설치

```bash
npm install
```

또는 개별 설치:

```bash
npm install pdf-parse gtts
```

## 사용법

### 단일 파일 변환

```bash
# 기본 사용 (한국어)
node pdf_to_mp3_converter.js document.pdf

# 영어로 변환
node pdf_to_mp3_converter.js document.pdf en

# 일본어로 변환
node pdf_to_mp3_converter.js document.pdf ja
```

### 디렉토리 일괄 변환

```bash
# 디렉토리 내 모든 PDF 파일 변환
node pdf_to_mp3_converter.js --dir ./pdfs

# 특정 언어로 변환
node pdf_to_mp3_converter.js --dir ./pdfs en
```

### 프로그래밍 방식 사용

```javascript
const PDFtoMP3Converter = require('./pdf_to_mp3_converter');

// 변환기 생성
const converter = new PDFtoMP3Converter({
    language: 'ko',           // 언어 설정
    outputDir: './mp3_output' // 출력 디렉토리
});

// 단일 파일 변환
await converter.convert('document.pdf');

// 디렉토리 변환
await converter.convertDirectory('./pdfs');
```

## 지원 언어

| 코드 | 언어 |
|------|------|
| ko   | 한국어 |
| en   | 영어 |
| ja   | 일본어 |
| zh   | 중국어 |
| es   | 스페인어 |
| fr   | 프랑스어 |
| de   | 독일어 |
| it   | 이탈리아어 |
| ru   | 러시아어 |

## 출력

- 변환된 MP3 파일은 `mp3_output` 디렉토리에 저장됩니다.
- 긴 텍스트는 자동으로 여러 파일로 분할됩니다. (예: `document_part1.mp3`, `document_part2.mp3`)

## 예제

### 예제 1: 한국어 PDF를 MP3로 변환

```bash
node pdf_to_mp3_converter.js "01문서/매뉴얼.pdf"
```

### 예제 2: 영어 문서 변환

```bash
node pdf_to_mp3_converter.js README.pdf en
```

### 예제 3: 여러 파일 일괄 변환

```bash
node pdf_to_mp3_converter.js --dir 01문서 ko
```

## 주의사항

1. **PDF 형식**: 텍스트 기반 PDF만 지원합니다. 이미지 기반 PDF는 OCR이 필요합니다.
2. **텍스트 길이**: 매우 긴 문서는 자동으로 여러 파일로 분할됩니다.
3. **인터넷 연결**: Google TTS API를 사용하므로 인터넷 연결이 필요합니다.

## 문제 해결

### PDF 텍스트 추출 실패
- PDF가 이미지 기반인 경우 텍스트 추출이 불가능합니다.
- OCR 도구(Tesseract 등)를 사용하여 먼저 텍스트로 변환하세요.

### 음성 변환 실패
- 인터넷 연결을 확인하세요.
- 텍스트에 특수문자가 많은 경우 정리가 필요할 수 있습니다.

### 파일이 너무 큰 경우
- 프로그램이 자동으로 분할하지만, 수동으로 PDF를 분할할 수도 있습니다.

## 라이선스

MIT License
