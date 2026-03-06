import http.server
import socketserver
import webbrowser
import os
import sys

# 포트 설정 (기본값: 8000)
PORT = 8000

# 현재 스크립트가 있는 디렉토리를 웹 루트로 설정
web_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(web_dir)

# 핸들러 설정
Handler = http.server.SimpleHTTPRequestHandler

def run_server():
    # 포트 재시도 로직 (포트가 이미 사용 중일 경우를 대비)
    port = PORT
    while True:
        try:
            with socketserver.TCPServer(("", port), Handler) as httpd:
                url = f"http://localhost:{port}"
                print(f"[INFO] Joy AI Server started successfully!")
                print(f"[LINK] Access URL: {url}")
                print(f"[HELP] Press Ctrl+C to stop the server.")
                
                # 브라우저 자동 실행
                webbrowser.open(url)
                
                # 서버 실행
                httpd.serve_forever()
        except OSError:
            # 포트가 사용 중이면 +1 하여 재시도
            print(f"[WARN] Port {port} is in use. Trying next port...")
            port += 1
        except KeyboardInterrupt:
            print("\n[STOP] Server stopped.")
            sys.exit(0)

if __name__ == "__main__":
    run_server()
