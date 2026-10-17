"""세 파일을 같은 폴더에 두고 Python 3로 실행: python start_local.py"""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import threading
import webbrowser

class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, max-age=0')
        super().end_headers()

    def log_message(self, *_args):
        pass


def main():
    folder = Path(__file__).resolve().parent
    for name in ('index.html', 'reset-password.html'):
        if not (folder / name).is_file():
            print(f'{name} 파일이 없습니다. 압축을 풀고 세 파일을 같은 폴더에 두세요.', flush=True)
            return
    if "new URL('reset-password.html'" not in (folder / 'index.html').read_text(encoding='utf-8'):
        print('index.html이 이전 버전입니다. 이번 압축파일의 index.html로 교체해주세요.', flush=True)
        return
    try:
        server = ThreadingHTTPServer(('127.0.0.1', 8000), partial(Handler, directory=str(folder)))
    except OSError:
        print('8000번 포트가 사용 중입니다. 이전 start_local.py 창에서 Ctrl+C로 종료한 후 다시 실행하세요.', flush=True)
        return
    print('로그인: http://localhost:8000/index.html', flush=True)
    print('재설정: http://localhost:8000/reset-password.html', flush=True)
    print('메일의 링크를 열 때도 이 창을 켜두세요. 종료: Ctrl+C', flush=True)
    threading.Timer(0.5, lambda: webbrowser.open('http://localhost:8000/index.html')).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

if __name__ == '__main__':
    main()
