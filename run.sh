#!/bin/bash

# LangChain RAG 시스템 실행 스크립트

echo "🚀 LangChain RAG 시스템 시작"
echo "================================"

# 가상환경 활성화
if [ ! -d "venv" ]; then
    echo "❌ 가상환경이 없습니다. 먼저 설정해주세요."
    exit 1
fi

source venv/bin/activate

# Ollama 상태 확인
echo "📡 Ollama 서버 상태 확인 중..."
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  Ollama 서버가 실행되지 않았습니다."
    echo "다른 터미널에서 실행하세요: ollama serve"
    read -p "계속하시겠습니까? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ Ollama 서버 연결됨"
fi

# 필요한 패키지 확인
echo ""
echo "📦 필수 패키지 확인 중..."
python -c "import streamlit" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Streamlit이 설치되지 않았습니다. 설치 중..."
    pip install streamlit
fi

echo ""
echo "================================"
echo "서버 시작 중..."
echo "================================"
echo ""

# FastAPI 서버를 백그라운드에서 실행
echo "🔧 FastAPI 서버 시작 (포트 8000)..."
python main.py > fastapi.log 2>&1 &
FASTAPI_PID=$!
echo "FastAPI PID: $FASTAPI_PID"

# 서버가 시작될 때까지 대기
sleep 3

# Streamlit UI 실행
echo "🎨 Streamlit UI 시작 (포트 8501)..."
echo ""
echo "================================"
echo "✅ 시스템 실행 완료!"
echo "================================"
echo ""
echo "📍 FastAPI: http://localhost:8000/docs"
echo "📍 Streamlit UI: http://localhost:8501"
echo ""
echo "종료하려면 Ctrl+C를 누르세요."
echo ""

# Streamlit 실행 (포그라운드)
streamlit run ui_app.py

# 종료 시 FastAPI도 함께 종료
echo ""
echo "🛑 시스템 종료 중..."
kill $FASTAPI_PID 2>/dev/null
echo "✅ 종료 완료"

