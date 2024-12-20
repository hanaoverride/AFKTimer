[English Version](README-en.md)


## 목차
1. [프로젝트 소개](#afk-timer)
2. [만든 목적](#만든-목적)
3. [주요 기능](#주요-기능)
4. [설치 및 실행](#설치-및-실행)
5. [사용법](#사용법)
6. [데이터 저장](#데이터-저장)
7. [언인스톨 방법](#언인스톨-방법)
8. [문제 해결](#문제-해결)
9. [라이선스](#라이선스)


# AFK Timer

![AFK Timer Image](https://private-user-images.githubusercontent.com/192361273/397818950-53c9889a-ee03-4700-b084-c04b83cbfc59.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzQ3MTYzOTIsIm5iZiI6MTczNDcxNjA5MiwicGF0aCI6Ii8xOTIzNjEyNzMvMzk3ODE4OTUwLTUzYzk4ODlhLWVlMDMtNDcwMC1iMDg0LWMwNGI4M2NiZmM1OS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQxMjIwJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MTIyMFQxNzM0NTJaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT01NDNjZDFlN2VjNThjZGRhMTQzZTQ1MzViNzNkN2NmMTU3YTJjMDYyZjhkOTc2Yjc1MzIzM2Y5MTBlMmIyOGJjJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.J1xmX1xhV8hPjzrKWilZm2WmnllEkXv8RTj2UjxK7pc)

AFK Timer는 Windows 환경에서 유휴(AFK, Away From Keyboard) 시간을 추적하는 간단하고 직관적인 타이머 프로그램입니다.

코드 작성 및 테스트까지 제작시간 약 4시간 이내로 완성했습니다.
(초안을 Claude 3.5 Sonnet으로 빠르게 잡은 뒤 기능 추가 및 수정을 했습니다.)

---

## 만든 목적

생산성 관리 앱은 많으나 저는 딱 유휴시간만 체크해서 심리적 **Procrastination(지연 현상)** 을 줄이는데 활용하고 싶었는데
그런 앱이 없어서 간단하게 만들어봤습니다.

**'아, 씻어야 하는데 씻기 싫다...'** 고 생각하며 휴대폰을 보다가 몇 시간씩 안 씻고 휴대폰에 열중하느라 시간을 허비하거나

**'이 유튜브 영상만 보고 진짜로 과제 한다.'** 라고 생각하며 유튜브 알고리즘 자동재생만 열심히 본 적 있으신가요?

네. 그걸 스스로 **단죄**하고, 좀 더 시간을 효율적으로 활용하고 싶을때 사용하는 프로그램입니다.

상용 프로그램 중에서는 이 목적만을 위해 사용할 수 있는 프로그램은 잘 없더라고요.

저는 주로 생산적인 활동을 컴퓨터 앞에서 하기 때문에, 컴퓨터가 켜져있는 시간동안 지연 현상에 허비한 시간을 재고 및 반성할 수 있다면
좀 더 효율적인 하루를 보낼 수 있을 것이라 생각했습니다. 

만약 운동이나 산책, 스포츠 경기 관람 혹은 독서 등의 다른 활동을 한다면 간단하게 Pause 버튼을 눌러두고, 다시 컴퓨터에서 활동할때 Resume 하면 그만이죠!


## 주요 기능
- **유휴 시간 추적**: 마우스와 키보드 활동을 감지하여 3분 이상 미활동 시 유휴 시간을 기록.
- **일시정지/재개**: 필요에 따라 AFK 시간 측정을 일시정지 및 재개.
- **데이터 저장**: 일일 AFK 데이터를 기록하고 최근 7일간의 데이터를 그래프로 시각화.
- **자동 시작 설정**: 시작 프로그램으로 등록하여 자동 실행 가능.
- **자정 리셋**: 자정마다 타이머가 자동 리셋되고 데이터가 저장.

---

## 설치 및 실행

### 1. 시스템 요구 사항
- Windows 10 이상
- Python 3.7 이상 (소스 코드 사용 시)
- 종속 라이브러리:
  - `tkinter`
  - `matplotlib`
  - `pynput`
  - `win32api`, `win32con`, `win32gui`, `winreg`

### 2. 설치 방법
#### A. 실행 파일 사용 (권장)
1. Github Release에서 실행 파일을 다운로드합니다.
2. 실행 파일을 더블 클릭하여 프로그램을 실행합니다.

#### B. 소스 코드 실행
1. 이 저장소를 클론합니다:
   ```bash
   git clone https://github.com/username/afk-timer.git
   cd afk-timer

## 사용법

1. **프로그램 실행** 후, 상단에 떠 있는 작은 위젯에서 유휴 시간을 실시간으로 확인할 수 있습니다.
2. **Pause/Resume 버튼**: 유휴 시간 측정을 일시정지하거나 재개합니다.
3. **Exit 버튼**: 현재 데이터를 저장하고 프로그램을 종료합니다. 재실행시 종료했던 위치에 위젯이 그대로 떠있습니다.
4. **그래프**: 최근 7일간의 AFK 데이터를 시각화하여 표시됩니다.


### 데이터 저장

#### AFK 데이터 및 설정 파일은 다음 경로에 저장됩니다:
        Documents/AFKTimer/afk_history.json
        Documents/AFKTimer/widget_config.ini

## 언인스톨 방법

1. `uninstall_afktimer.reg` 파일을 실행하여 시작 프로그램 레지스트리 설정을 제거합니다.
2. 프로그램 실행 파일과 관련 데이터(`Documents/AFKTimer` 폴더)를 삭제합니다. (후자는 재설치 목적이 있을 시 남겨두셔도 좋습니다.)

### 문제 해결

짧은 시간 내에 만들어서 제가 잡지 못한 버그가 많을 것이라고 생각합니다.

사실 일단은 제가 사용하려고 만들었고, 아이디어 자체는 좋다고 생각해서 일단 배포한다음 실제로 사용하는 사람이 많아지면 버그를 수정하자고 생각했거든요.

Discussion을 열어주시면 확인 후 수정하도록 하겠습니다.

버그 리포트시 다음과 같은 예시 양식을 따라 작성해주시면 도움이 됩니다!

# 🐞 버그 리포트 템플릿

## 1. 버그 요약 (Summary)
- 문제가 무엇인지 간단히 설명해주세요.
  - 예: "Pause 버튼을 누르면 AFK 타이머가 멈추지 않음."

---

## 2. 재현 단계 (Steps to Reproduce)
- 버그를 재현하기 위한 단계를 하나씩 적어주세요.
  1. **첫 번째 단계**: 예) 프로그램 실행
  2. **두 번째 단계**: 예) Pause 버튼 클릭
  3. **세 번째 단계**: 예) 마우스와 키보드 사용을 멈춤
  4. **네 번째 단계**: 예) AFK 타이머가 계속 증가하는 것을 확인

---

## 3. 예상 동작 (Expected Behavior)
- 정상적으로 동작해야 하는 방법을 설명해주세요.
  - 예: "Pause 버튼을 누르면 AFK 타이머가 멈춰야 합니다."

---

## 4. 실제 동작 (Actual Behavior)
- 현재 발생한 문제를 설명해주세요.
  - 예: "Pause 버튼을 눌러도 AFK 타이머가 계속 작동합니다."

---

## 5. 스크린샷 또는 로그 (Optional)
- 문제가 나타나는 화면의 스크린샷을 첨부해주세요. 노콘솔로 패키징하여 로그는 따로 없으나, 심각한 오류의 경우 Traceback이 별도로 뜨기 때문에 그 메시지를 주시면 도움이 됩니다...

---

## 6. 사용 환경 (Environment)
- 문제가 발생한 환경을 구체적으로 적어주세요:
  - **운영 체제**: 예) Windows 10 / Windows 11
  - **Python 버전** (소스 코드 사용 시): 예) Python 3.9
  - **AFK Timer 버전**: 예) v1.0.1
  - **다중 모니터 사용 여부**: 예) Yes / No

---

## 7. 기타 (Additional Context)
- 문제가 발생하기 전에 특별히 수행한 작업이 있다면 적어주세요.

## Q&A

#### Q: 프로그램이 시작 프로그램으로 자동 실행되지 않습니다.

    프로그램 실행 시 autostart_afktimer.reg 파일을 생성합니다.
    해당 파일을 실행하여 시작 프로그램으로 등록할 수 있습니다.

#### Q: 프로그램 실행 중 그래프가 제대로 보이지 않습니다.
1. `matplotlib`가 올바르게 설치되었는지 확인하세요:
   ```bash
   pip install matplotlib


### 라이선스

이 프로젝트는 **MIT 라이선스**를 따릅니다.

여러분은 이 소프트웨어를 자유롭게 **사용, 수정, 배포, 상업적 활용**할 수 있습니다!
다만, 원저작자를 명시해야 하고, 소프트웨어 사용으로 인한 책임은 사용자에게 있습니다.
