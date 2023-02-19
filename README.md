# 인스타그램 게시물 python으로 가져오기
---
⚠️ 인스타그램의 상황에 따라 스크래핑이 안될 수도 있습니다.

- 크롬 디버그모드 실행
  - macos
    ```shell
    /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="~/ChromeProfile"
    ```
    - alias로 저장해두면 편합니다.(rc파일에 입력하고 source 하면 `chrome` 명령어만으로 실행)
    ```shell
    alias chrome='/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="~/ChromeProfile"'
    ```
  - windows (cmd)
    ```shell
    `C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --remote-debugging-port=8989 --user-data-dirs="C:\chromeprofileDebug`
    ```
    - doskey로 저장해두면 편합니다. `%windir%\system32\cmd.exe /k 파일위치\aliases.cmd`
    - aliases.cmd에 추가할 내용
        ```shell
        doskey chrome=`C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dirs="C:\chromeprofileDebug`
        ```
     
- `.env` 커스터마이징
  - `DRIVER_PATH`: 크롬드라이버의 경로
  - `FILEPATH`: 다운로드 받은 파일이 저장될 경로
  - `ID`: 인스타그램 아이디
  - `PASSWORD`: 인스타그램 비밀번호
  - `PAUSE_TIME`: 게시물의 링크를 가져올 때의 스크롤 대기 시간
  - `TARGET_PAGE`: 게시물을 가져올 페이지(인스타그램 유저페이지 or 해시태그 결과)