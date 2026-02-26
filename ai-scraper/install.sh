#!/bin/bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install
echo ""
echo "설치 완료! 실행 방법:"
echo "  source venv/bin/activate"
echo "  python app.py"
