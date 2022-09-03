# Airbnb with Django and React

| 프로젝트 기간 | 22.09.03 ~     |
| ------------- | -------------- |
| 프로젝트 목적 | Django & React |
| Github        | ‣              |

---

## Setup

pyenv로 nvm과 같이 python version을 관리하고 python 가상 환경을 생성

poetry로 npm 과 같이 모듈 관리

`pip install poetry`

`poetry init`

`django-admin startproject config .`

---

## OOP

### init

javascript constructor method는 class가 생성될때 호출되는 함수

python에서는 `__init__(self)`함수가 대신한다

self는 class의 instance를 가리킨다. (javascript의 this)

```python
class Player:
    def __init__(self, name="jinwook"):
        self.name = name

    def hello(self):
        print(f"hello {self.name}~")

user = Player("nico")
print(user.name)
user.hello()
```
