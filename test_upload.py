"""
문서 업로드 기능 직접 테스트
"""
import sys
import traceback

# 테스트 파일 생성
test_content = "이것은 테스트 문서입니다. RAG 시스템이 이 내용을 학습할 것입니다."
with open("data/test_doc.txt", "w", encoding="utf-8") as f:
    f.write(test_content)

print("📄 테스트 파일 생성 완료: data/test_doc.txt\n")

try:
    print("1️⃣ 문서 처리 모듈 import...")
    from rag.document_loader import document_processor
    from rag.vector_store import vector_store_manager
    print("   ✅ Import 성공\n")
    
    print("2️⃣ 문서 로드 및 분할 중...")
    chunks = document_processor.process_document("data/test_doc.txt")
    print(f"   ✅ {len(chunks)}개 청크 생성\n")
    
    print("3️⃣ 벡터 스토어에 추가 중...")
    vector_store_manager.add_documents(chunks)
    print("   ✅ 벡터화 완료\n")
    
    print("4️⃣ 검색 테스트...")
    results = vector_store_manager.search("테스트", k=1)
    if results:
        print(f"   ✅ 검색 성공!")
        print(f"   내용: {results[0].page_content[:50]}...\n")
    else:
        print("   ⚠️  검색 결과 없음\n")
    
    print("🎉 모든 테스트 성공!")
    
except Exception as e:
    print(f"\n❌ 오류 발생!")
    print(f"타입: {type(e).__name__}")
    print(f"메시지: {str(e)}\n")
    print("=" * 60)
    print("상세 스택 트레이스:")
    print("=" * 60)
    traceback.print_exc()
    sys.exit(1)

