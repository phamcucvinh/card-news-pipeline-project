#!/bin/bash
# html_to_png.sh — HTML 슬라이드 → PNG/MP4 변환 (Playwright 사용)
# 사용: bash scripts/html_to_png.sh [슬라이드폴더] [출력폴더]
# 예시: bash scripts/html_to_png.sh output/slides output/images

set -e

SLIDES_DIR="${1:-output/slides}"
OUTPUT_DIR="${2:-output/images}"
RECORD_MP4="${3:-}"  # "--record-mp4" 옵션

# 색상
RED='\033[91m'
GREEN='\033[92m'
YELLOW='\033[93m'
CYAN='\033[96m'
RESET='\033[0m'
BOLD='\033[1m'

echo ""
echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "📦 HTML → PNG 변환 시작"
echo -e "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"

# 출력 폴더 생성
mkdir -p "$OUTPUT_DIR"

# Node.js / Playwright 설치 확인
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js가 설치되어 있지 않습니다.${RESET}"
    echo "설치: https://nodejs.org"
    exit 1
fi

# Playwright 변환 스크립트 (임시 생성)
SCRIPT=$(cat <<'NODEEOF'
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

async function convertSlides(slidesDir, outputDir, recordMp4) {
  const browser = await chromium.launch();
  const htmlFiles = fs.readdirSync(slidesDir)
    .filter(f => f.match(/^slide-.*\.html$/))
    .sort();

  let converted = 0;

  for (const file of htmlFiles) {
    const inputPath = path.resolve(slidesDir, file);
    const outputName = file.replace('.html', '.png');
    const outputPath = path.resolve(outputDir, outputName);
    const fileUrl = `file://${inputPath}`;

    const page = await browser.newPage();
    await page.setViewportSize({ width: 1080, height: 1080 });
    await page.goto(fileUrl, { waitUntil: 'networkidle' });

    // 폰트 로드 대기
    await page.waitForTimeout(500);

    await page.screenshot({
      path: outputPath,
      type: 'png',
      clip: { x: 0, y: 0, width: 1080, height: 1080 }
    });

    console.log(`  ✅ ${file} → ${outputName}`);
    converted++;
    await page.close();
  }

  // MP4 녹화 (표지 슬라이드, B시리즈)
  if (recordMp4 === '--record-mp4') {
    const coverFiles = htmlFiles.filter(f => f.match(/^slide-01-/));
    for (const file of coverFiles) {
      const inputPath = path.resolve(slidesDir, file);
      const outputName = file.replace('slide-01-', 'cover-').replace('.html', '.mp4');
      const outputPath = path.resolve(outputDir, outputName);

      const context = await browser.newContext({
        recordVideo: {
          dir: outputDir,
          size: { width: 1080, height: 1080 }
        }
      });
      const page = await context.newPage();
      await page.setViewportSize({ width: 1080, height: 1080 });
      await page.goto(`file://${inputPath}`, { waitUntil: 'networkidle' });
      await page.waitForTimeout(3000); // 3초 녹화

      await context.close(); // 비디오 저장
      console.log(`  🎬 ${file} → MP4 녹화 완료`);
    }
  }

  await browser.close();
  console.log(`\n총 ${converted}개 파일 변환 완료`);
  console.log(`저장 위치: ${outputDir}`);
}

const [,, slidesDir, outputDir, recordMp4] = process.argv;
convertSlides(slidesDir, outputDir, recordMp4).catch(e => {
  console.error('오류:', e.message);
  process.exit(1);
});
NODEEOF
)

# 임시 스크립트 파일 생성
TEMP_SCRIPT=$(mktemp /tmp/html_to_png_XXXXXX.js)
echo "$SCRIPT" > "$TEMP_SCRIPT"

# Playwright 설치 확인 및 실행
if node -e "require('playwright')" 2>/dev/null; then
    echo -e "${CYAN}Playwright 사용 중...${RESET}"
    node "$TEMP_SCRIPT" "$SLIDES_DIR" "$OUTPUT_DIR" "$RECORD_MP4"
else
    echo -e "${YELLOW}Playwright가 없습니다. 설치 중...${RESET}"
    npm install playwright 2>/dev/null || {
        echo -e "${RED}npm 설치 실패. 수동으로 설치해주세요:${RESET}"
        echo "  npm install playwright"
        echo "  npx playwright install chromium"
        rm -f "$TEMP_SCRIPT"
        exit 1
    }
    npx playwright install chromium
    node "$TEMP_SCRIPT" "$SLIDES_DIR" "$OUTPUT_DIR" "$RECORD_MP4"
fi

rm -f "$TEMP_SCRIPT"

echo ""
echo -e "${GREEN}${BOLD}✅ 변환 완료!${RESET}"
echo -e "📁 저장 위치: ${OUTPUT_DIR}/"
echo ""

# 변환된 파일 목록
ls -la "$OUTPUT_DIR"/*.png 2>/dev/null | awk '{print "  " $NF " (" $5 " bytes)"}' || true
