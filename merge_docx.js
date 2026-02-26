/**
 * DOCX 파일 병합 도구 (페이지 번호 포함)
 * 사용법:
 *   merge_docx.exe <파일/폴더> [...] [-o 출력파일.docx]
 *
 * 예시:
 *   merge_docx.exe file1.docx file2.docx
 *   merge_docx.exe 01문서/                       ← 폴더 내 모든 .docx 병합
 *   merge_docx.exe 01문서/ short/ -o 전체병합.docx
 *   merge_docx.exe file1.docx 01문서/ -o 결과.docx
 */

const fs = require('fs');
const path = require('path');
const DocxMerger = require('docx-merger');
const JSZip = require('jszip');

// 폴더에서 .docx 파일 수집 (하위 폴더 포함)
function collectDocx(dirPath) {
  const results = [];
  const items = fs.readdirSync(dirPath);
  for (const item of items) {
    const fullPath = path.join(dirPath, item);
    const stat = fs.statSync(fullPath);
    if (stat.isDirectory()) {
      results.push(...collectDocx(fullPath));
    } else if (item.toLowerCase().endsWith('.docx') && !item.startsWith('~$')) {
      results.push(fullPath);
    }
  }
  return results;
}

// docx 파일 유효성 검사 (ZIP 시그니처 확인)
function isValidDocx(filePath) {
  try {
    const fd = fs.openSync(filePath, 'r');
    const buf = Buffer.alloc(4);
    fs.readSync(fd, buf, 0, 4, 0);
    fs.closeSync(fd);
    return buf[0] === 0x50 && buf[1] === 0x4B && buf[2] === 0x03 && buf[3] === 0x04;
  } catch {
    return false;
  }
}

// 병합된 docx에 페이지 번호 추가 (하단 중앙, 검은색, 12pt, 진하게)
function addPageNumbers(docxBuffer, callback) {
  var zip = new JSZip(docxBuffer);

  // footer XML: 하단 중앙, 검은색(000000), 12pt(24 half-pt), 굵게
  var footerXml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' +
    '<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"' +
    ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">' +
    '<w:p>' +
    '<w:pPr><w:jc w:val="center"/></w:pPr>' +
    '<w:r>' +
    '<w:rPr><w:b/><w:sz w:val="24"/><w:szCs w:val="24"/><w:color w:val="000000"/></w:rPr>' +
    '<w:fldChar w:fldCharType="begin"/>' +
    '</w:r>' +
    '<w:r>' +
    '<w:rPr><w:b/><w:sz w:val="24"/><w:szCs w:val="24"/><w:color w:val="000000"/></w:rPr>' +
    '<w:instrText> PAGE </w:instrText>' +
    '</w:r>' +
    '<w:r>' +
    '<w:rPr><w:b/><w:sz w:val="24"/><w:szCs w:val="24"/><w:color w:val="000000"/></w:rPr>' +
    '<w:fldChar w:fldCharType="end"/>' +
    '</w:r>' +
    '</w:p>' +
    '</w:ftr>';

  // footer 파일 추가
  zip.file('word/footer1.xml', footerXml);

  // document.xml에서 모든 sectPr에 footer 참조 추가
  var docXml = zip.file('word/document.xml').asText();

  // 기존 footerReference 제거 후 새로 추가
  docXml = docXml.replace(/<w:footerReference[^/]*\/>/g, '');

  // 모든 sectPr에 footer 참조 삽입
  docXml = docXml.replace(/<w:sectPr([^>]*)>/g,
    '<w:sectPr$1><w:footerReference w:type="default" r:id="rIdFooter1"/>');

  zip.file('word/document.xml', docXml);

  // [Content_Types].xml에 footer 등록
  var contentTypes = zip.file('[Content_Types].xml').asText();
  if (contentTypes.indexOf('footer1.xml') === -1) {
    contentTypes = contentTypes.replace('</Types>',
      '<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/></Types>');
    zip.file('[Content_Types].xml', contentTypes);
  }

  // word/_rels/document.xml.rels에 footer 관계 추가
  var relsFile = 'word/_rels/document.xml.rels';
  var rels = zip.file(relsFile).asText();
  if (rels.indexOf('rIdFooter1') === -1) {
    rels = rels.replace('</Relationships>',
      '<Relationship Id="rIdFooter1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/></Relationships>');
    zip.file(relsFile, rels);
  }

  var buf = zip.generate({ type: 'nodebuffer' });
  callback(buf);
}

// 인자 파싱
const args = process.argv.slice(2);

if (args.length === 0) {
  console.log('=== DOCX 파일 병합 도구 ===');
  console.log('');
  console.log('사용법: merge_docx.exe <파일/폴더> [...] [-o 출력파일.docx]');
  console.log('');
  console.log('예시:');
  console.log('  merge_docx.exe a.docx b.docx c.docx');
  console.log('  merge_docx.exe 01문서/                    (폴더 내 모든 .docx 병합)');
  console.log('  merge_docx.exe 01문서/ short/ -o 전체.docx');
  console.log('  merge_docx.exe a.docx 폴더/ -o 결과.docx  (파일+폴더 혼합)');
  console.log('');
  console.log('* 페이지 번호 자동 추가 (하단 중앙, 12pt, 굵게)');
  process.exit(0);
}

let outputFile = null;
const inputs = [];

for (let i = 0; i < args.length; i++) {
  if (args[i] === '-o' && i + 1 < args.length) {
    outputFile = args[++i];
  } else {
    inputs.push(args[i]);
  }
}

// 파일/폴더 → docx 파일 목록으로 변환
let inputFiles = [];
for (const input of inputs) {
  if (!fs.existsSync(input)) {
    console.error(`오류: 경로를 찾을 수 없습니다 → ${input}`);
    process.exit(1);
  }
  const stat = fs.statSync(input);
  if (stat.isDirectory()) {
    const found = collectDocx(input).sort();
    if (found.length === 0) {
      console.warn(`경고: 폴더에 .docx 파일이 없습니다 → ${input}`);
    }
    inputFiles.push(...found);
  } else if (input.toLowerCase().endsWith('.docx')) {
    inputFiles.push(input);
  } else {
    console.warn(`건너뜀 (docx 아님): ${input}`);
  }
}

// 중복 제거
inputFiles = [...new Set(inputFiles)];

// 출력 파일명 기본값
if (!outputFile) {
  outputFile = 'merged_' + Date.now() + '.docx';
}

// 출력 파일이 입력에 포함되면 제외
inputFiles = inputFiles.filter(f => path.resolve(f) !== path.resolve(outputFile));

// 손상된 파일 제외
const skipped = [];
inputFiles = inputFiles.filter(f => {
  if (!isValidDocx(f)) {
    skipped.push(f);
    return false;
  }
  return true;
});

if (skipped.length > 0) {
  console.log(`\n⚠ 손상/비정상 파일 ${skipped.length}개 제외:`);
  skipped.forEach(f => console.log(`  - ${f}`));
}

if (inputFiles.length < 2) {
  console.error('오류: 병합하려면 최소 2개 이상의 정상 .docx 파일이 필요합니다.');
  console.error(`  찾은 파일: ${inputFiles.length}개`);
  process.exit(1);
}

// 파일 읽기
console.log(`\n병합할 파일 ${inputFiles.length}개:`);
const buffers = [];
const loaded = [];
for (let i = 0; i < inputFiles.length; i++) {
  const f = inputFiles[i];
  const size = (fs.statSync(f).size / 1024).toFixed(1);
  try {
    buffers.push(fs.readFileSync(f, 'binary'));
    loaded.push(f);
    console.log(`  ${loaded.length}. ${f} (${size} KB)`);
  } catch (err) {
    console.warn(`  ⚠ 읽기 실패, 건너뜀: ${f} (${err.message})`);
  }
}

if (loaded.length < 2) {
  console.error('오류: 읽기 성공한 파일이 2개 미만입니다.');
  process.exit(1);
}

// 병합 실행
console.log('\n병합 중...');
try {
  const merger = new DocxMerger({}, buffers);
  merger.save('nodebuffer', (mergedData) => {
    // 페이지 번호 추가
    console.log('페이지 번호 추가 중...');
    addPageNumbers(mergedData, (finalData) => {
      fs.writeFileSync(outputFile, finalData);
      const outSize = (fs.statSync(outputFile).size / 1024).toFixed(1);
      console.log(`\n완료! → ${outputFile} (${outSize} KB)`);
      console.log(`  총 ${loaded.length}개 파일 병합됨`);
      console.log(`  페이지 번호: 하단 중앙, 12pt, 굵게`);
    });
  });
} catch (err) {
  console.error('병합 실패:', err.message);
  process.exit(1);
}
