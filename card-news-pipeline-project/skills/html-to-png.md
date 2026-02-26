# html-to-png — HTML → PNG 변환 스킬

## 역할
Playwright를 사용해 HTML 슬라이드를 1080x1080 PNG로 변환한다.

## 실행 방법
```bash
bash scripts/html_to_png.sh output/slides/ output/images/
```

## 출력
`output/images/slide-[번호]-[주제].png`

---

## B시리즈 MP4 녹화

B시리즈 표지는 커서 깜빡임 애니메이션이 있으므로 MP4로도 저장:

```bash
# 3초 녹화
bash scripts/html_to_png.sh --record-mp4 output/slides/slide-01-[주제].html output/images/
```

출력: `output/images/cover-[주제].mp4`

---

## 변환 품질 설정

```javascript
// Playwright 설정
await page.setViewportSize({ width: 1080, height: 1080 });
await page.screenshot({
  path: outputPath,
  type: 'png',
  fullPage: false
});
```

## 설치 필요사항
```bash
npm install playwright
npx playwright install chromium
```
