# 클립보드 번역기 (Clipboard Translator)

이 프로그램은 클립보드에 복사된 영어 텍스트를 한국어로 번역하고, 주요 단어 목록과 함께 Markdown 또는 HTML 형식으로 출력하는 도구입니다.

## 주요 기능

- 클립보드 내용 자동 감지 및 표시
- 영어에서 한국어로 텍스트 번역
- 주요 단어 추출 및 번역
- Markdown 또는 HTML 형식으로 결과 출력
- 사용자 친화적인 GUI 인터페이스

## 설치 방법

1. Python 3.6 이상이 설치되어 있어야 합니다.

2. 필요한 라이브러리를 설치합니다:
   ```
   pip install deep-translator markdown pyperclip
   ```

3. 이 저장소를 클론하거나 소스 코드를 다운로드합니다.

## 사용 방법

1. 터미널에서 다음 명령어로 프로그램을 실행합니다:
   ```
   python clipboard_to_html.py
   ```

2. 프로그램이 실행되면 클립보드의 내용이 표시됩니다.

3. 다음 옵션 중 하나를 선택합니다:
   - Markdown: Markdown 파일로 출력
   - HTML: HTML 파일로 출력
   - 둘 다: Markdown과 HTML 파일 모두 출력
   - 취소: 프로그램 종료

4. 선택한 형식에 따라 `output.md` 또는 `output.html` 파일(또는 둘 다)이 생성됩니다.

## 주의사항

- 인터넷 연결이 필요합니다 (번역 기능 사용).
- 큰 텍스트의 경우 번역에 시간이 걸릴 수 있습니다.
- 번역 품질은 Google 번역 API에 의존합니다.

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 기여

버그 리포트, 기능 제안 또는 풀 리퀘스트는 언제나 환영합니다. 프로젝트에 기여하고 싶으시다면 이슈를 열어 논의를 시작해주세요.