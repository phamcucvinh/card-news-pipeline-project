#!/usr/bin/env python3
"""
DOCX 파일을 MP3 음성 파일로 변환하는 스크립트
"""

import os
import glob
from docx import Document
from gtts import gTTS
import time

def extract_text_from_docx(docx_path):
    """DOCX 파일에서 텍스트 추출"""
    try:
        doc = Document(docx_path)
        text = []

        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text.append(paragraph.text)

        full_text = '\n'.join(text)
        return full_text
    except Exception as e:
        print(f"❌ 텍스트 추출 오류 ({docx_path}): {e}")
        return None

def convert_to_mp3(text, output_path, lang='ko'):
    """텍스트를 MP3로 변환"""
    try:
        print(f"🔊 음성 생성 중: {os.path.basename(output_path)}")
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(output_path)
        print(f"✅ 완료: {os.path.basename(output_path)}")
        return True
    except Exception as e:
        print(f"❌ MP3 변환 오류: {e}")
        return False

def main():
    """메인 실행 함수"""
    # 현재 디렉토리의 모든 DOCX 파일 찾기
    docx_files = glob.glob("*_설명.docx")

    if not docx_files:
        print("❌ DOCX 파일을 찾을 수 없습니다.")
        return

    print(f"📂 발견된 DOCX 파일: {len(docx_files)}개\n")

    success_count = 0
    fail_count = 0

    for docx_file in sorted(docx_files):
        print(f"\n{'='*60}")
        print(f"📄 처리 중: {docx_file}")
        print(f"{'='*60}")

        # MP3 파일명 생성
        mp3_file = docx_file.replace('.docx', '.mp3')

        # 이미 존재하는 경우 건너뛰기
        if os.path.exists(mp3_file):
            print(f"⏭️  이미 존재함: {mp3_file}")
            continue

        # 텍스트 추출
        print(f"📖 텍스트 추출 중...")
        text = extract_text_from_docx(docx_file)

        if text and len(text.strip()) > 0:
            print(f"📝 추출된 텍스트 길이: {len(text)} 문자")

            # MP3 변환
            if convert_to_mp3(text, mp3_file):
                success_count += 1
                file_size = os.path.getsize(mp3_file) / 1024  # KB
                print(f"💾 파일 크기: {file_size:.1f} KB")
            else:
                fail_count += 1

            # API 제한 방지를 위한 대기
            time.sleep(1)
        else:
            print(f"⚠️  텍스트를 추출할 수 없습니다.")
            fail_count += 1

    # 최종 결과
    print(f"\n{'='*60}")
    print(f"🎉 변환 완료!")
    print(f"{'='*60}")
    print(f"✅ 성공: {success_count}개")
    print(f"❌ 실패: {fail_count}개")
    print(f"📁 총 파일: {len(docx_files)}개")

    # 생성된 MP3 파일 목록
    mp3_files = glob.glob("*_설명.mp3")
    if mp3_files:
        print(f"\n📂 생성된 MP3 파일:")
        total_size = 0
        for mp3_file in sorted(mp3_files):
            size = os.path.getsize(mp3_file) / 1024  # KB
            total_size += size
            print(f"  - {mp3_file} ({size:.1f} KB)")
        print(f"\n💾 총 용량: {total_size/1024:.1f} MB")

if __name__ == "__main__":
    main()
