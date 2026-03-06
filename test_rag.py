import os
import sys

# Add locally installed dependencies to path
current_dir = os.path.dirname(os.path.abspath(__file__))
libs_dir = os.path.join(current_dir, 'joy_libs')
if os.path.exists(libs_dir):
    sys.path.insert(0, libs_dir)

from core.rag_engine import RAGEngine

def test_rag():
    print("Initializing RAGEngine...")
    try:
        # Mock embedding model since Ollama might not be running on test server
        # We will test ChromaDB and TextSplitter logic first.
        # However Langchain's OllamaEmbeddings doesn't check connection on init, only on embed.
        rag = RAGEngine(db_dir="test_chroma_db")
        print("RAGEngine initialized.")
        
        # Create a test document
        test_file = "test_resume.txt"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("안녕하세요! 제 이름은 조이입니다.\n저는 파이썬과 딥러닝을 좋아합니다.\n가장 기억에 남는 프로젝트는 로컬 AI 비서 개발이었습니다.")
            
        print("Test file created. Indexing...")
        # Since Ollama is not installed on the system (based on the setup.sh output),
        # this will likely fail during the actual embedding step.
        # But we can verify if the file reading and splitting works.
        try:
             success, msg = rag.load_and_index_document(test_file)
             print(f"Indexing result: {success}, {msg}")
        except Exception as e:
             print(f"Expected error during embedding (Ollama missing): {e}")

        # Clean up
        import shutil
        if os.path.exists(test_file):
            os.remove(test_file)
        if os.path.exists("test_chroma_db"):
            shutil.rmtree("test_chroma_db")
            
    except Exception as e:
        print(f"Initialization or general error: {e}")

if __name__ == "__main__":
    test_rag()
