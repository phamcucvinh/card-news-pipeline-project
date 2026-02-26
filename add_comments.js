/**
 * AI 기반 코드 주석 자동 추가 프로그램
 *
 * 폴더 내의 모든 소스 파일을 스캔하고, AI를 사용하여 상세한 주석을 자동으로 추가합니다.
 * 지원 파일: .mq4, .mq5, .mqh, .js, .ts, .jsx, .tsx
 *
 * 사용법:
 *   node add_comments.js <대상_폴더> [옵션]
 *
 * 옵션:
 *   --output <폴더>     출력 폴더 지정 (기본값: 원본 파일 덮어쓰기)
 *   --backup            원본 파일 백업 (.bak 확장자로 저장)
 *   --exclude <패턴>    제외할 파일/폴더 패턴 (쉼표로 구분)
 *   --dry-run           실제 파일 수정 없이 미리보기만
 */

const fs = require('fs').promises;
const path = require('path');
const Anthropic = require('@anthropic-ai/sdk');

// 설정
const CONFIG = {
  apiKey: process.env.ANTHROPIC_API_KEY || '',
  model: 'claude-sonnet-4-5-20250929',
  maxTokens: 4000,
  supportedExtensions: ['.mq4', '.mq5', '.mqh', '.js', '.ts', '.jsx', '.tsx'],
  excludePatterns: ['node_modules', 'dist', 'build', '.git', 'coverage'],
  backupExtension: '.bak'
};

class CommentAdder {
  constructor(options = {}) {
    this.options = {
      targetDir: options.targetDir || process.cwd(),
      outputDir: options.outputDir || null,
      backup: options.backup || false,
      excludePatterns: options.excludePatterns || CONFIG.excludePatterns,
      dryRun: options.dryRun || false
    };

    if (!CONFIG.apiKey) {
      throw new Error('ANTHROPIC_API_KEY 환경 변수가 설정되지 않았습니다.');
    }

    this.client = new Anthropic({ apiKey: CONFIG.apiKey });
    this.stats = {
      totalFiles: 0,
      processedFiles: 0,
      failedFiles: 0,
      skippedFiles: 0
    };
  }

  /**
   * 파일이 처리 대상인지 확인
   */
  shouldProcessFile(filePath) {
    const ext = path.extname(filePath).toLowerCase();
    if (!CONFIG.supportedExtensions.includes(ext)) {
      return false;
    }

    // 제외 패턴 확인
    for (const pattern of this.options.excludePatterns) {
      if (filePath.includes(pattern)) {
        return false;
      }
    }

    return true;
  }

  /**
   * 디렉토리를 재귀적으로 스캔하여 파일 목록 수집
   */
  async scanDirectory(dirPath) {
    const files = [];

    try {
      const entries = await fs.readdir(dirPath, { withFileTypes: true });

      for (const entry of entries) {
        const fullPath = path.join(dirPath, entry.name);

        // 제외 패턴 확인
        if (this.options.excludePatterns.some(pattern => entry.name.includes(pattern))) {
          continue;
        }

        if (entry.isDirectory()) {
          // 재귀적으로 하위 디렉토리 스캔
          const subFiles = await this.scanDirectory(fullPath);
          files.push(...subFiles);
        } else if (entry.isFile() && this.shouldProcessFile(fullPath)) {
          files.push(fullPath);
        }
      }
    } catch (error) {
      console.error(`❌ 디렉토리 스캔 오류 (${dirPath}):`, error.message);
    }

    return files;
  }

  /**
   * AI를 사용하여 코드 분석 및 주석 생성
   */
  async generateComments(code, filePath) {
    const ext = path.extname(filePath).toLowerCase();
    const language = this.getLanguageName(ext);

    const prompt = `다음 ${language} 코드를 분석하고, 상세한 주석을 추가해주세요.

요구사항:
1. 파일 상단에 헤더 주석 추가 (파일명, 설명, 작성일자, 주요 기능)
2. 모든 함수/메서드에 설명 주석 추가 (목적, 매개변수, 반환값, 사용 예시)
3. 복잡한 로직에 인라인 주석 추가
4. 주석은 ${language === 'MQL4/MQL5' ? '영어' : '한국어'}로 작성
5. 원본 코드는 수정하지 말고 주석만 추가
6. ${language === 'MQL4/MQL5' ? '// 스타일' : '// 또는 /* */ 스타일'} 주석 사용

파일: ${path.basename(filePath)}

코드:
\`\`\`${language.toLowerCase()}
${code}
\`\`\`

주석이 추가된 완전한 코드를 제공해주세요. 설명이나 다른 텍스트 없이 코드만 출력하세요.`;

    try {
      const message = await this.client.messages.create({
        model: CONFIG.model,
        max_tokens: CONFIG.maxTokens,
        messages: [{
          role: 'user',
          content: prompt
        }]
      });

      const responseText = message.content[0].text;

      // 코드 블록 추출 (```로 감싸진 경우)
      const codeBlockMatch = responseText.match(/```(?:\w+)?\n([\s\S]+?)\n```/);
      if (codeBlockMatch) {
        return codeBlockMatch[1];
      }

      return responseText;
    } catch (error) {
      console.error(`❌ AI 주석 생성 오류:`, error.message);
      throw error;
    }
  }

  /**
   * 파일 확장자에서 언어명 추출
   */
  getLanguageName(ext) {
    const languageMap = {
      '.mq4': 'MQL4',
      '.mq5': 'MQL5',
      '.mqh': 'MQL4/MQL5',
      '.js': 'JavaScript',
      '.jsx': 'JavaScript',
      '.ts': 'TypeScript',
      '.tsx': 'TypeScript'
    };
    return languageMap[ext] || 'Unknown';
  }

  /**
   * 단일 파일 처리
   */
  async processFile(filePath) {
    console.log(`\n📄 처리 중: ${path.relative(this.options.targetDir, filePath)}`);

    try {
      // 파일 읽기
      const originalCode = await fs.readFile(filePath, 'utf-8');

      // 이미 주석이 많이 있는지 확인
      const commentLines = originalCode.split('\n').filter(line =>
        line.trim().startsWith('//') || line.trim().startsWith('/*') || line.trim().startsWith('*')
      ).length;
      const totalLines = originalCode.split('\n').length;
      const commentRatio = commentLines / totalLines;

      if (commentRatio > 0.3) {
        console.log(`   ⏭️  건너뜀: 이미 충분한 주석이 있음 (${(commentRatio * 100).toFixed(1)}%)`);
        this.stats.skippedFiles++;
        return;
      }

      // AI로 주석 생성
      console.log(`   🤖 AI 분석 중...`);
      const commentedCode = await this.generateComments(originalCode, filePath);

      if (this.options.dryRun) {
        console.log(`   ✅ [DRY-RUN] 처리 완료 (실제 파일 수정 안 함)`);
        this.stats.processedFiles++;
        return;
      }

      // 출력 경로 결정
      let outputPath = filePath;
      if (this.options.outputDir) {
        const relativePath = path.relative(this.options.targetDir, filePath);
        outputPath = path.join(this.options.outputDir, relativePath);

        // 출력 디렉토리 생성
        await fs.mkdir(path.dirname(outputPath), { recursive: true });
      }

      // 백업 생성
      if (this.options.backup && !this.options.outputDir) {
        const backupPath = filePath + CONFIG.backupExtension;
        await fs.copyFile(filePath, backupPath);
        console.log(`   💾 백업 생성: ${path.basename(backupPath)}`);
      }

      // 주석이 추가된 코드 저장
      await fs.writeFile(outputPath, commentedCode, 'utf-8');

      const addedComments = commentedCode.split('\n').filter(line =>
        line.trim().startsWith('//') || line.trim().startsWith('/*') || line.trim().startsWith('*')
      ).length - commentLines;

      console.log(`   ✅ 완료: ${addedComments}개의 주석 추가됨`);
      this.stats.processedFiles++;

    } catch (error) {
      console.error(`   ❌ 오류:`, error.message);
      this.stats.failedFiles++;
    }
  }

  /**
   * 전체 프로세스 실행
   */
  async run() {
    console.log('🚀 AI 기반 코드 주석 자동 추가 시작\n');
    console.log('설정:');
    console.log(`  대상 폴더: ${this.options.targetDir}`);
    console.log(`  출력 폴더: ${this.options.outputDir || '원본 파일 덮어쓰기'}`);
    console.log(`  백업: ${this.options.backup ? '활성화' : '비활성화'}`);
    console.log(`  제외 패턴: ${this.options.excludePatterns.join(', ')}`);
    console.log(`  Dry Run: ${this.options.dryRun ? '예' : '아니오'}`);
    console.log();

    // 파일 스캔
    console.log('📂 파일 스캔 중...');
    const files = await this.scanDirectory(this.options.targetDir);
    this.stats.totalFiles = files.length;

    if (files.length === 0) {
      console.log('\n⚠️  처리할 파일이 없습니다.');
      return;
    }

    console.log(`✅ ${files.length}개 파일 발견\n`);
    console.log('─'.repeat(60));

    // 각 파일 처리
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      console.log(`\n[${i + 1}/${files.length}]`);
      await this.processFile(file);

      // API Rate Limit 방지를 위한 딜레이
      if (i < files.length - 1) {
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
    }

    // 결과 출력
    console.log('\n' + '─'.repeat(60));
    console.log('\n📊 처리 결과:');
    console.log(`  전체 파일: ${this.stats.totalFiles}`);
    console.log(`  처리 완료: ${this.stats.processedFiles}`);
    console.log(`  건너뜀: ${this.stats.skippedFiles}`);
    console.log(`  실패: ${this.stats.failedFiles}`);
    console.log(`  성공률: ${((this.stats.processedFiles / this.stats.totalFiles) * 100).toFixed(1)}%`);
    console.log();
  }
}

/**
 * CLI 인자 파싱
 */
function parseArguments() {
  const args = process.argv.slice(2);
  const options = {
    targetDir: null,
    outputDir: null,
    backup: false,
    excludePatterns: CONFIG.excludePatterns,
    dryRun: false
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];

    if (arg === '--output' && args[i + 1]) {
      options.outputDir = path.resolve(args[++i]);
    } else if (arg === '--backup') {
      options.backup = true;
    } else if (arg === '--exclude' && args[i + 1]) {
      const patterns = args[++i].split(',').map(p => p.trim());
      options.excludePatterns = [...CONFIG.excludePatterns, ...patterns];
    } else if (arg === '--dry-run') {
      options.dryRun = true;
    } else if (arg === '--help' || arg === '-h') {
      printHelp();
      process.exit(0);
    } else if (!arg.startsWith('--') && !options.targetDir) {
      options.targetDir = path.resolve(arg);
    }
  }

  if (!options.targetDir) {
    console.error('❌ 대상 폴더를 지정해주세요.\n');
    printHelp();
    process.exit(1);
  }

  return options;
}

/**
 * 도움말 출력
 */
function printHelp() {
  console.log(`
AI 기반 코드 주석 자동 추가 프로그램

사용법:
  node add_comments.js <대상_폴더> [옵션]

옵션:
  --output <폴더>     출력 폴더 지정 (기본값: 원본 파일 덮어쓰기)
  --backup            원본 파일 백업 (.bak 확장자로 저장)
  --exclude <패턴>    제외할 파일/폴더 패턴 (쉼표로 구분)
  --dry-run           실제 파일 수정 없이 미리보기만
  --help, -h          도움말 출력

예시:
  # 기본 사용
  node add_comments.js ./src

  # 백업 파일 생성하며 처리
  node add_comments.js ./src --backup

  # 다른 폴더에 결과 저장
  node add_comments.js ./src --output ./src_commented

  # 특정 폴더 제외
  node add_comments.js ./src --exclude "test,spec"

  # Dry-run 모드로 미리보기
  node add_comments.js ./src --dry-run

환경 변수:
  ANTHROPIC_API_KEY   Claude API 키 (필수)

지원 파일 형식:
  .mq4, .mq5, .mqh    MetaTrader 프로그램
  .js, .jsx           JavaScript
  .ts, .tsx           TypeScript
`);
}

/**
 * 메인 실행
 */
async function main() {
  try {
    const options = parseArguments();
    const adder = new CommentAdder(options);
    await adder.run();

    console.log('✅ 모든 작업이 완료되었습니다.\n');
    process.exit(0);
  } catch (error) {
    console.error('\n❌ 오류 발생:', error.message);
    process.exit(1);
  }
}

// 프로그램 실행
if (require.main === module) {
  main();
}

module.exports = { CommentAdder };
