#!/usr/bin/env python3
"""
단일 DOCX 파일을 MP3 음성 파일로 변환
"""

import os
from docx import Document
from gtts import gTTS

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
        print(f"❌ 텍스트 추출 오류: {e}")
        return None

def convert_to_mp3(text, output_path, lang='ko'):
    """텍스트를 MP3로 변환"""
    try:
        print(f"🔊 음성 생성 중...")
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(output_path)
        print(f"✅ 완료: {output_path}")
        return True
    except Exception as e:
        print(f"❌ MP3 변환 오류: {e}")
        return False

# 파일 경로
docx_file = "automate_youtube_shorts_설명.docx"
mp3_file = "automate_youtube_shorts_설명.mp3"

print(f"{'='*60}")
print(f"📄 변환 중: {docx_file}")
print(f"{'='*60}\n")

# 텍스트 추출
print(f"📖 텍스트 추출 중...")
text = extract_text_from_docx(docx_file)

if text and len(text.strip()) > 0:
    print(f"📝 추출된 텍스트 길이: {len(text)} 문자\n")

    # MP3 변환
    if convert_to_mp3(text, mp3_file):
        file_size = os.path.getsize(mp3_file) / 1024  # KB
        print(f"💾 파일 크기: {file_size:.1f} KB")
        print(f"\n🎉 변환 완료!")
    else:
        print(f"\n❌ 변환 실패")
else:
    print(f"⚠️  텍스트를 추출할 수 없습니다.")
