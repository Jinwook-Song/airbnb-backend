# Airbnb with Django and React

| 프로젝트 기간 | 22.09.03 ~                            |
| ------------- | ------------------------------------- |
| 프로젝트 목적 | Django & React                        |
| Github        | ‣                                     |
| Docs          | https://docs.djangoproject.com/en/4.1 |

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

### inheritance, super

다른 클래스를 상속하려면 constructor(**init**) 함수를 호출 해야한다.

super()를 통해 접근할 수 있다.

```python
class Human:
    def __init__(self, name):
        print("Human initialization")
        self.name = name

    def hello(self):
        print(f"hello my name is {self.name}")

class Player(Human):
    def __init__(self, name="jinwook"):
        # Human class 에 대한 접근 권한을 준다.
        super().__init__(name)
        self.name = name

class Fan(Human):
    def __init__(self, name):
        super().__init__(name)
        self.name = name

user = Player("nico")
print(user.name)
user.hello()
```

---

## Django basic

`python manage.py runserver`

`python manage.py migrate`

⇒ database를 조작할 수 있는 코드들이 실제로 동작 가능하도록 database shape을 갖춰줌

---

## Django apps

`python manage.py startapp {app_name}`

새로 만든 app을 장고 project에 등록 시켜야 한다.

```python
config > settings.py

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "houses.apps.HousesConfig",
]
```

models

```python
from pydoc import describe
from django.db import models

# Create your models here.
class House(models.Model):
    """Model definition for House"""

    name = models.CharField(max_length=140)
    price = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=140)
```

migrate

`python mangae.py makemigrations`

`python mangae.py migrate`

---

## Admin pannel

```python
from django.contrib import admin
from houses.models import House

# Register your models here.

@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "address", "pets_allowed")
    list_filter = ("price", "pets_allowed")
    search_fields = ("address",)
```

---

## User model

[공식 문서](https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#substituting-a-custom-user-model)

Django user의 모든 기능을 상속

model.py

```python
# from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass
```

setting.py에 user를 생성한 custom user로 등록해준다

```python
CUSTOM_APPS = ["users.apps.UsersConfig"]

# AUTH
AUTH_USER_MODEL = "users.User"
```

admin.py

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User

# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass
```
