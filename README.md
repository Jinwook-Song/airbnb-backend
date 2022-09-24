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

customize admin.py
[공식 문서](https://docs.djangoproject.com/en/4.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.fieldsets)

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User

# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (
            "Profile",
            {
                "fields": ("username", "password", "email", "name", "is_host"),
                "classes": ("wide",),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Important dates",
            {
                "fields": ("last_login", "date_joined"),
                "classes": ("collapse",),
            },
        ),
    )

    list_display = ("username", "email", "name", "is_host")
```

---

## Foreign key

[공식 문서](https://docs.djangoproject.com/en/4.1/topics/db/models/#relationships)

```python
from django.db import models
from users.models import User

# Create your models here.

class House(models.Model):
    """Model definition for House"""

    name = models.CharField(max_length=140)
    price = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=140)
    pets_allowed = models.BooleanField(default=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
```

---

### User model (more)

```python
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    class Genders(models.TextChoices):
        MALE = ("male", "Male")  # database value, admin pannel label
        FEMALE = ("female", "Female")

    class Languagues(models.TextChoices):
        KR = ("kr", "Korean")
        EN = ("en", "English")

    class Currencies(models.TextChoices):
        KRW = ("krw", "Korean ₩")
        USD = ("usd", "Dollar $")

    avatar = models.ImageField(
        blank=True, # blank는 database가 아닌 form level이다.
    )
    gender = models.CharField(
        max_length=10,
        choices=Genders.choices,
        default=Genders.MALE,
    )
    language = models.CharField(
        max_length=2,
        choices=Languagues.choices,
        default=Languagues.KR,
    )
    currency = models.CharField(
        max_length=3,
        choices=Currencies.choices,
        default=Currencies.KRW,
    )
```

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User

# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (
            "Profile",
            {
                "fields": (
                    "avatar",
                    "username",
                    "password",
                    "email",
                    "name",
                    "gender",
                    "language",
                    "currency",
                    "is_host",
                ),
                "classes": ("wide",),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Important dates",
            {
                "fields": ("last_login", "date_joined"),
                "classes": ("collapse",),
            },
        ),
    )

    list_display = ("username", "email", "name", "is_host")
```

---

Common Model

```python
from django.db import models

# Create your models here.

class CommonModel(models.Model):
    """Common model definition, blueprint for other models"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Django dosen't create database about this model
    class Meta:
        abstract = True
```

```python
from django.db import models
from common.models import CommonModel

from users.models import User

# Create your models here.

class Rooms(CommonModel):
    """Room Model Definition"""

    class RoomKindChoices(models.TextChoices):
        ENTIRE_PLACE = ("entire_place", "Entire Place")
        PRIVATE_ROOM = ("private_room", "Private Room")
        SHARED_ROOM = ("shared_room", "Shared Room")

    country = models.CharField(max_length=50, default="Korea")
    city = models.CharField(max_length=50, default="Seoul")
    price = models.PositiveBigIntegerField()
    rooms = models.PositiveBigIntegerField()
    toilets = models.PositiveBigIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=250)
    pet_allowed = models.BooleanField(default=True)
    kind = models.CharField(max_length=50, choices=RoomKindChoices.choices)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    amenities = models.ManyToManyField("rooms.Amenity")

class Amenity(CommonModel):
    """Amenity Model"""

    name = models.CharField(max_length=150)
    description = models.CharField(max_length=150, null=True)
```

---

### Room admin

```python
from django.contrib import admin

from rooms.models import Amenity, Room

# Register your models here.

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "kind",
        "owner",
    )

    list_filter = (
        "country",
        "city",
        "price",
        "rooms",
        "toilets",
        "pet_allowed",
        "kind",
        "amenities",
    )

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
```

---

### Category

```python
from django.db import models

from common.models import CommonModel

# Create your models here.

class Category(CommonModel):

    """Room or Experience category"""

    class CategoryKindChoices(models.TextChoices):
        ROOMS = ("rooms", "Rooms")
        EXPERIENCES = ("experiences", "Experiences")

    name = models.CharField(max_length=50)
    kind = models.CharField(max_length=15, choices=CategoryKindChoices.choices)

    def __str__(self) -> str:
        return f"{self.kind.title()}: {self.name}"

    class Meta:
        verbose_name_plural = "Categories"
```

---

### Media

OneToOneField: 특정 모델에 종속되지만 고유한 값을 갖도록 하기 위해

예를들어 결제 정보를 저장할 때, 유저에 대해 하나의 결제 정보만 갖도록

```jsx
from django.db import models
from common.models import CommonModel

# Create your models here.

class Photo(CommonModel):
    """Photo model definition"""

    file = models.ImageField()
    description = models.CharField(max_length=150)
    room = models.ForeignKey(
        "rooms.Room",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

class Video(CommonModel):
    """Video model definition"""

    file = models.FileField()
    experience = models.OneToOneField(
        "experiences.Experience",
        on_delete=models.CASCADE,
    )
```

---

## ORM

[docs](https://docs.djangoproject.com/en/4.1/topics/db/queries/#retrieving-objects)

`python manage.py shell`

모델은 단순히 데이터의 형태만 표현하는 것이 아닌 실제 데이터와의 연결 통로가 된다.

ex) 사용 예시

```python
from rooms.models import Room

# Room.objects 를 통해 다양한 method를 사용할 수 있다.

Room.objects.all() # get all
Room.objects.get(name='room_name') # get with name
room = Room.objects.get(name='room_name')
room.owner # get user with foreinkey
room.price = 2000 # update data
room.save() # save for db
```

filler , exclude chaining

```python
>>> Entry.objects.filter(
...     headline__startswith='What'
... ).exclude(
...     pub_date__gte=datetime.date.today()
... ).filter(
...     pub_date__gte=datetime.date(2005, 1, 30)
... )
```

create

```python
<Entry: New Lennon Biography>
>>> Entry.objects.create(
...     blog=beatles,
...     headline='New Lennon Biography in Paperback',
...     pub_date=date(2009, 6, 1),
... )
```

delete

```python
>>> Entry.objects.filter(pub_date__year=2005).delete()
(5, {'webapp.Entry': 5})
```

---

### Admin methods

in admin:

```python
def total_amenities(self, room):
        return room.amenities.count()
```

in model:

```python
def total_amenities(self):
        return self.amenities.count()
```

---

### Reverse Access with reverse accessors

기본적으로 foreignkey를 생성하면 해당 모델은 \_set을 통해 접근이 가능하다

room.user로 foreignkey 관계를 형성하면

user.room_set을 통해 접근 가능하다

room_set은 related_name으로 변경 가능

ex) room.user ↔  user.rooms

→ room은 하나의 user를 가질 수 있다. user는 여러개의 room을 가질 수 있다

```python
# Room Model
owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="rooms",
    )
```
