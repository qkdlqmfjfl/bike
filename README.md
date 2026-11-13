# NEON RIDER 🏍️

Traffic Rider에서 영감을 받은 **2.5D 원근감 오토바이 회피 게임**입니다. Python과 Pygame으로 만들었으며, 일반 PC에서는 창으로 실행하고 GitHub Codespaces에서는 브라우저로 플레이할 수 있습니다.

## 게임 기능
- 지평선에서 가까워질수록 넓어지는 원근 도로와 움직이는 차선
- A/D 또는 방향키로 오토바이 좌우 이동
- 무작위 차선에 등장하는 차량과 충돌 판정
- 주행 거리, 점수, 속도 HUD
- 시작 화면, 플레이 화면, 게임오버 및 재시작
- 초보자가 읽기 쉬운 파일 분리와 한국어 주석

## 파일 구조
```text
bike/
├── .devcontainer/
│   └── devcontainer.json
├── entities.py       # 오토바이와 차량
├── game.py           # 게임 상태, 도로, 충돌, HUD
├── main.py           # 실행 및 이벤트 루프
├── settings.py       # 화면 크기와 색상
├── requirements.txt
└── README.md
```

## PC에서 실행
Python 3.10 이상을 권장합니다.

```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
python main.py
```

## GitHub Codespaces에서 브라우저로 실행
1. 저장소에서 **Code → Codespaces → Create codespace on feature/traffic-rider-game**를 선택합니다.
2. 터미널에서 의존성을 설치합니다: `pip install -r requirements.txt`
3. 다음 명령으로 브라우저용 게임을 실행합니다.

```bash
python -m pygbag .
```

4. 터미널에 표시되는 포트 **8000**의 주소를 열거나, VS Code의 **Ports** 탭에서 8000번 포트를 **Open in Browser**로 엽니다.

## 조작법
| 키 | 동작 |
|---|---|
| Enter / Space | 시작 |
| A / ← | 왼쪽 이동 |
| D / → | 오른쪽 이동 |
| R / Enter | 게임오버 후 재시작 |

## 개발 참고
이 프로젝트는 실제 3D 모델을 사용하는 게임이 아니라 Pygame 도형과 원근 투영을 이용한 2.5D 스타일입니다. 기능을 확장할 때는 차량 이미지, 엔진 사운드, 최고 기록 저장 등을 추가할 수 있습니다.
