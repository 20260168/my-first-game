# Week 11 실습
## 오늘 한 것
1. PyInstaller 설치 및 빌드
2. resource_path() 함수 추가
3. --add-data 옵션으로 에셋 포함
4. snake.exe (중간 과제 변경 사항) 실행 확인

## resource_path() 를 써야 하는 이유
상대 경로로 작성한 소스 코드는 CWD와 game이 있는 폴더 파일의 위치가 같다.
하지만 빌드 후, CWD와 game이 실행하는 실제 위치는 Desktop에서 실행되어 서로 실행하는 폴더 위치가 달라서 실행되지 않는다.
이를 같은 경로로 수정을 해주는 resource_path()를 사용한다.

## 사용한 빌드 명령어
pyinstaller --onefile game.py
pyinstaller --add-data "asset;asset" snake.py

## AI 활용 내역
1. 불러오는 모든 이미지 파일과 사운드 파일을 한 번에 관리할 수 있게 만들고, 다른 컴퓨터에서 py.game 다운로드 없이 플레이가 가능하도록(이미지와 사운드가 적용되도록) resource_path()를 사용해서 이미지 및 사운드 부분 소스 코드를 변경해줘
-> 모든 이미지 및 사운드 파일을 (예시) 0, 1로 정의하여 0이면 수정 전, (.exe)1이면 수정 후 작동하도록 변경했다.

2. pyinstaller --add-data "asset;asset" snake.py 로 사용하면 불러올 수 있던데 다른 --onefile을 사용하는 이유가 뭐야?
-> 첫 실행 속도가 느린 것을 방지한다.

3. 내가 asset을 넣어둔 폴더에 여러 개의 폴더를 세부적으로 정리하기 편하게 만들어놨는데, 여러 개면 "fonts;fonts" 나 "sound;sound" 도 해야해?
-> asset안에 넣어둔 파일이라면 괜찮습니다.	
