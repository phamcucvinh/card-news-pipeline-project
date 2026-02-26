#!/usr/bin/env python3
"""
preview_server.py — 카드뉴스 슬라이드 로컬 프리뷰 서버
사용: python scripts/preview_server.py
브라우저: http://localhost:8080
"""

import http.server
import socketserver
import os
import sys
import webbrowser
from pathlib import Path

PORT = 8080
BASE_DIR = Path(__file__).parent.parent  # 프로젝트 루트

class CardNewsHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def do_GET(self):
        # 루트 접속 시 갤러리 페이지 자동 생성
        if self.path == "/" or self.path == "":
            self.send_gallery()
            return
        super().do_GET()

    def send_gallery(self):
        """슬라이드 갤러리 HTML 자동 생성"""
        slides_dir = BASE_DIR / "output" / "slides"
        html_files = sorted(slides_dir.glob("slide-*.html")) if slides_dir.exists() else []

        gallery_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>카드뉴스 프리뷰 갤러리</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:#0a0a0f; color:#e0e0e0; font-family:sans-serif; padding:40px; }}
  h1 {{ color:#fff; font-size:28px; margin-bottom:8px; }}
  .subtitle {{ color:#666; margin-bottom:40px; font-size:15px; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(220px,1fr)); gap:20px; }}
  .card {{ background:#13131b; border:1px solid #1e1e2a; border-radius:12px; overflow:hidden;
            transition:border-color 0.2s; cursor:pointer; }}
  .card:hover {{ border-color:#444; }}
  .preview {{ width:100%; aspect-ratio:1; background:#0d1117; position:relative; overflow:hidden; }}
  .preview iframe {{ width:1080px; height:1080px; border:none;
                     transform:scale(0.2); transform-origin:top left;
                     pointer-events:none; }}
  .card-info {{ padding:12px 16px; }}
  .card-name {{ font-size:13px; color:#888; word-break:break-all; }}
  .no-slides {{ text-align:center; padding:80px; color:#555; }}
  .refresh {{ display:inline-block; margin-bottom:20px; padding:8px 20px;
               background:rgba(99,102,241,0.12); border:1px solid rgba(99,102,241,0.25);
               color:#818cf8; border-radius:8px; cursor:pointer; font-size:14px;
               text-decoration:none; }}
</style>
</head>
<body>
<h1>🎴 카드뉴스 프리뷰 갤러리</h1>
<div class="subtitle">output/slides/ 폴더의 슬라이드 목록 |
  <a href="/" class="refresh">🔄 새로고침</a>
</div>

<div class="grid">
"""
        if html_files:
            for f in html_files:
                rel_path = f.relative_to(BASE_DIR)
                gallery_html += f"""
  <div class="card" onclick="window.open('/{rel_path}', '_blank')">
    <div class="preview">
      <iframe src="/{rel_path}" scrolling="no"></iframe>
    </div>
    <div class="card-info">
      <div class="card-name">{f.name}</div>
    </div>
  </div>
"""
        else:
            gallery_html += """
  <div class="no-slides">
    <div style="font-size:48px;margin-bottom:16px">📭</div>
    <div>슬라이드가 없습니다</div>
    <div style="margin-top:8px;font-size:13px">output/slides/ 폴더에 slide-*.html 파일을 추가하세요</div>
  </div>
"""

        gallery_html += """
</div>
</body>
</html>"""

        content = gallery_html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", len(content))
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, format, *args):
        # 정적 파일 요청 로그 숨기기 (슬라이드 iframe 요청 등)
        if args and str(args[0]).startswith("GET /output"):
            return
        super().log_message(format, *args)

def main():
    os.chdir(BASE_DIR)

    with socketserver.TCPServer(("", PORT), CardNewsHandler) as httpd:
        print(f"\n✅ 프리뷰 서버 시작!")
        print(f"🌐 브라우저 열기: http://localhost:{PORT}")
        print(f"📁 루트 디렉토리: {BASE_DIR}")
        print(f"\nCtrl+C로 종료\n")

        # 브라우저 자동 열기
        webbrowser.open(f"http://localhost:{PORT}")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n서버 종료.")

if __name__ == "__main__":
    main()
