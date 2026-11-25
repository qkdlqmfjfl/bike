# NEON RIDER 🏍️

Traffic Rider에서 영감을 받은 초보자용 **2.5D 오토바이 회피 게임**입니다. Python과 Pygame으로 제작하며, 일반 PC에서는 게임 창으로, GitHub Codespaces에서는 브라우저로 실행할 수 있습니다.

## 현재 구현된 기능

- 지평선에서 가까워질수록 넓어지는 원근감 있는 도로
- 움직이는 차선 표시와 도로 주변 풍경
- A/D 또는 방향키로 오토바이 좌우 이동
- 세 개 차선에 등장하는 교통 차량
- 차량과 부딪히면 게임 종료
- 주행 거리, 점수, 속도 표시
- 시작 화면, 플레이 화면, 게임 오버 화면
- 게임 오버 후 재시작
- Shift 키 니트로 부스트와 충전 게이지
- 근접 회피 보너스와 시각 효과
- P 키 일시정지 및 재개
- 난이도에 따라 빨라지는 교통 차량과 도로 속도감
- 초보자가 읽기 쉽도록 기능별 파일 분리 및 한국어 주석

> 이 게임은 실제 3D 모델을 사용하는 게임이 아니라 Pygame 도형으로 원근감을 표현한 2.5D 게임입니다.

## 파일 구조

```text
bike/
├── .devcontainer/
│   └── devcontainer.json
├── entities.py       # 플레이어 오토바이와 교통 차량
├── game.py           # 도로, 게임 진행, 충돌, 점수와 화면
├── main.py           # 게임 실행 및 이벤트 처리
├── settings.py       # 화면 크기와 색상 설정
├── requirements.txt  # 필요한 Python 패키지
└── README.md         # 프로젝트 설명과 실행 방법
```

## 자동 검사

GitHub Actions가 코드를 변경할 때마다 Python 문법 검사와 기본 게임 스모크 테스트를 실행합니다.

```bash
python -m compileall -q .
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy python -m unittest discover -s tests -v
```

## GitHub Codespaces에서 실행하기

1. GitHub 저장소의 **Code** 버튼을 누릅니다.
2. **Codespaces** 탭을 선택합니다.
3. **Create codespace on main**을 눌러 `main` 브랜치에서 Codespace를 만듭니다.
4. Codespace가 열리면 아래 명령을 터미널에 입력합니다.

```bash
python -m pip install -r requirements.txt
```

5. 설치가 끝나면 브라우저 실행 명령을 입력합니다.

```bash
python -m pygbag .
```

6. VS Code 아래쪽의 **Ports** 탭에서 `8000` 포트를 찾고 **Open in Browser**를 누릅니다. 포트가 자동으로 열리면 표시되는 주소를 눌러도 됩니다.

## 내 컴퓨터에서 실행하기

Python 3.10 이상을 권장합니다.

```bash
python -m pip install -r requirements.txt
python main.py
```

## 조작 방법

| 키 | 동작 |
|---|---|
| Enter 또는 Space | 시작 |
| A 또는 ← | 왼쪽 이동 |
| D 또는 → | 오른쪽 이동 |
| Shift | 니트로 부스트 |
| P | 일시정지 / 재개 |
| R 또는 Enter | 게임 오버 후 재시작 |

## 팀 개발 안내

- `settings.py`: 화면 크기와 색상 등 공통 설정
- `entities.py`: 오토바이와 다른 차량
- `game.py`: 도로, 충돌, 점수, 화면 구성
- `main.py`: 프로그램 시작과 입력 처리

각 파일을 나누어 맡아 수정하면 5명이 함께 작업하기 편리합니다. 수정하기 전에는 GitHub에서 최신 `main` 브랜치를 기준으로 작업하세요.
