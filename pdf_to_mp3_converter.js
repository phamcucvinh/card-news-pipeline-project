const fs = require('fs');
const path = require('path');
const pdf = require('pdf-parse');
const gtts = require('gtts');

/**
 * PDF to MP3 Converter
 * PDF 파일에서 텍스트를 추출하여 MP3 음성 파일로 변환
 */

class PDFtoMP3Converter {
    constructor(options = {}) {
        this.language = options.language || 'ko'; // 기본 언어: 한국어
        this.outputDir = options.outputDir || './output';

        // 출력 디렉토리 생성
        if (!fs.existsSync(this.outputDir)) {
            fs.mkdirSync(this.outputDir, { recursive: true });
        }
    }

    /**
     * PDF 파일에서 텍스트 추출
     */
    async extractTextFromPDF(pdfPath) {
        try {
            console.log(`📄 PDF 파일 읽기: ${pdfPath}`);
            const dataBuffer = fs.readFileSync(pdfPath);
            const data = await pdf(dataBuffer);

            console.log(`✅ 텍스트 추출 완료 (${data.numpages}페이지, ${data.text.length}자)`);
            return data.text;
        } catch (error) {
            console.error('❌ PDF 텍스트 추출 실패:', error.message);
            throw error;
        }
    }

    /**
     * 텍스트를 청크로 분할 (TTS API 제한 고려)
     */
    splitTextIntoChunks(text, maxLength = 5000) {
        const sentences = text.match(/[^.!?]+[.!?]+/g) || [text];
        const chunks = [];
        let currentChunk = '';

        for (const sentence of sentences) {
            if ((currentChunk + sentence).length > maxLength) {
                if (currentChunk) {
                    chunks.push(currentChunk.trim());
                    currentChunk = sentence;
                } else {
                    // 단일 문장이 maxLength보다 긴 경우
                    chunks.push(sentence.trim());
                }
            } else {
                currentChunk += sentence;
            }
        }

        if (currentChunk) {
            chunks.push(currentChunk.trim());
        }

        return chunks;
    }

    /**
     * 텍스트를 MP3로 변환
     */
    async textToMP3(text, outputPath) {
        return new Promise((resolve, reject) => {
            try {
                console.log(`🔊 음성 변환 시작...`);
                const tts = new gtts(text, this.language);

                tts.save(outputPath, (err) => {
                    if (err) {
                        reject(err);
                    } else {
                        console.log(`✅ MP3 저장 완료: ${outputPath}`);
                        resolve(outputPath);
                    }
                });
            } catch (error) {
                reject(error);
            }
        });
    }

    /**
     * PDF를 MP3로 변환 (메인 함수)
     */
    async convert(pdfPath) {
        try {
            const startTime = Date.now();
            console.log('\n=== PDF to MP3 변환 시작 ===\n');

            // 1. PDF에서 텍스트 추출
            const text = await this.extractTextFromPDF(pdfPath);

            if (!text || text.trim().length === 0) {
                throw new Error('PDF에서 텍스트를 추출할 수 없습니다.');
            }

            // 2. 텍스트 정리
            const cleanText = text
                .replace(/\s+/g, ' ')
                .replace(/\n+/g, '\n')
                .trim();

            // 3. 출력 파일명 생성
            const pdfFileName = path.basename(pdfPath, '.pdf');
            const outputPath = path.join(this.outputDir, `${pdfFileName}.mp3`);

            // 4. 텍스트가 너무 긴 경우 청크로 분할
            const chunks = this.splitTextIntoChunks(cleanText);
            console.log(`📝 텍스트를 ${chunks.length}개 청크로 분할`);

            if (chunks.length === 1) {
                // 단일 파일로 변환
                await this.textToMP3(cleanText, outputPath);
            } else {
                // 여러 파일로 변환
                console.log('⚠️  텍스트가 길어 여러 파일로 분할합니다.');
                for (let i = 0; i < chunks.length; i++) {
                    const chunkOutputPath = path.join(
                        this.outputDir,
                        `${pdfFileName}_part${i + 1}.mp3`
                    );
                    await this.textToMP3(chunks[i], chunkOutputPath);
                }
            }

            const endTime = Date.now();
            const duration = ((endTime - startTime) / 1000).toFixed(2);

            console.log('\n=== 변환 완료 ===');
            console.log(`⏱️  소요 시간: ${duration}초`);
            console.log(`📁 출력 디렉토리: ${this.outputDir}\n`);

            return true;
        } catch (error) {
            console.error('\n❌ 변환 실패:', error.message);
            throw error;
        }
    }

    /**
     * 디렉토리 내 모든 PDF 파일 변환
     */
    async convertDirectory(dirPath) {
        try {
            const files = fs.readdirSync(dirPath);
            const pdfFiles = files.filter(file => file.toLowerCase().endsWith('.pdf'));

            if (pdfFiles.length === 0) {
                console.log('PDF 파일이 없습니다.');
                return;
            }

            console.log(`📚 ${pdfFiles.length}개의 PDF 파일을 찾았습니다.\n`);

            for (const pdfFile of pdfFiles) {
                const pdfPath = path.join(dirPath, pdfFile);
                await this.convert(pdfPath);
            }

            console.log('🎉 모든 파일 변환 완료!');
        } catch (error) {
            console.error('디렉토리 변환 실패:', error.message);
            throw error;
        }
    }
}

// CLI 사용
if (require.main === module) {
    const args = process.argv.slice(2);

    if (args.length === 0) {
        console.log(`
사용법:
  단일 파일 변환:
    node pdf_to_mp3_converter.js <PDF파일경로> [언어코드]

  디렉토리 변환:
    node pdf_to_mp3_converter.js --dir <디렉토리경로> [언어코드]

예시:
  node pdf_to_mp3_converter.js document.pdf
  node pdf_to_mp3_converter.js document.pdf ko
  node pdf_to_mp3_converter.js document.pdf en
  node pdf_to_mp3_converter.js --dir ./pdfs ko

지원 언어:
  ko - 한국어 (기본값)
  en - 영어
  ja - 일본어
  zh - 중국어
  es - 스페인어
  fr - 프랑스어
        `);
        process.exit(0);
    }

    const language = args[args.length - 1].match(/^(ko|en|ja|zh|es|fr|de|it|ru)$/)
        ? args.pop()
        : 'ko';

    const converter = new PDFtoMP3Converter({
        language: language,
        outputDir: './mp3_output'
    });

    if (args[0] === '--dir') {
        const dirPath = args[1];
        if (!dirPath) {
            console.error('❌ 디렉토리 경로를 지정해주세요.');
            process.exit(1);
        }
        converter.convertDirectory(dirPath);
    } else {
        const pdfPath = args[0];
        if (!fs.existsSync(pdfPath)) {
            console.error('❌ PDF 파일을 찾을 수 없습니다:', pdfPath);
            process.exit(1);
        }
        converter.convert(pdfPath);
    }
}

module.exports = PDFtoMP3Converter;
