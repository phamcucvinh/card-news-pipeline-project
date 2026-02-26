#!/usr/bin/env python3
"""Simple MP3 Player using pygame"""

import pygame
import sys
import os

def play_mp3(file_path):
    """Play an MP3 file"""
    if not os.path.exists(file_path):
        print(f"❌ 파일을 찾을 수 없습니다: {file_path}")
        return

    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)

        print(f"▶️  재생 중: {os.path.basename(file_path)}")
        pygame.mixer.music.play()

        # Wait for music to finish
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        print("✅ 재생 완료")
    except Exception as e:
        print(f"❌ 재생 오류: {e}")
    finally:
        pygame.mixer.quit()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python3 play_mp3.py <mp3파일경로>")
        print("\n예시:")
        print('  python3 play_mp3.py "./12_기타/Chad_Hobson_-_Magical_Moment_(Hydr0.org).mp3"')
        sys.exit(1)

    play_mp3(sys.argv[1])
