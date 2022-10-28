# Airbnb with Django and React

| 프로젝트 기간 | 22.09.03 ~                            |
| ------------- | ------------------------------------- |
| 프로젝트 목적 | Django & React                        |
| Github        | ‣                                     |
| Docs          | https://docs.djangoproject.com/en/4.1 |

---

### Experiences (TODOS)

- [ ] POST /experiences
- [ ] GET PUT DELETE /experiences/1
- [x] GET /experiences/1/perks
- [x] GET POST /perks
- [ ] GET PUT DELETE /perks/1
- [ ] GET POST /experiences/1/bookings
- [ ] GET PUT DELETE /experiences/1/bookings/2

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

---

### More Admin

room의 review 평균 계산

```python
def rating(self):
        count = self.reviews.count()
        if count == 0:
            return "No Reviews"
        else:
            total_rating = 0
            # return dictionary of reviews
            for review in self.reviews.all().values("rating"):
                total_rating += review["rating"]
            return round(total_rating / count, 2)
```

---

### Search Admin

[docs](https://docs.djangoproject.com/en/4.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields)

| Prefix | Lookup     |
| ------ | ---------- |
| ^      | startswith |
| =      | iexact     |
| @      | search     |
| None   | icontains  |
|        |            |

`search_fields = ['foreign_key__related_fieldname']`

```python
search_fields = (
        "name",
        "^price",  # ^: startWith, default: contain
        "owner__username",
    )
```

---

### Admin action

```python
from django.contrib import admin

from rooms.models import Amenity, Room

@admin.action(description="Set all prices to zero")
def reset_prices(room_admin, request, querysets):
    print(room_admin)
    print(request)
    print(querysets)
    pass

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    actions = (reset_prices,)

```

- admin action은 3개의 input을 갖는다.
  model admin, request, queryset

```python
@admin.action(description="Set all prices to zero")
def reset_prices(room_admin, request, querysets):
    for room in querysets.all():
        room.price = 0
        room.save()
    pass
```

---

### Custom filters

foreign key를 통해서도 필터를 구현할 수 있다.

foreign key는 한단계만 되는것이 아니라 계속해서 적용할 수 있다.

```python
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("__str__", "payload")

    list_filter = (
        "rating",
        "user__is_host",
        "room__category__kind",
    )
```

기본으로 제공하는 필터 이외의 커스텀 필터도 가능하다

```python
class WorldFilter(admin.SimpleListFilter):
    title = "Filter by words"

    # URL Query
    parameter_name = "word"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("bad", "Bad"),
        ]

    def queryset(self, request, queryset):
        word = self.value()
        if word:
            return queryset.filter(payload__contains=word)
        else:
            queryset

class RatingFilter(admin.SimpleListFilter):
    title = "Filter by 🌟x3"

    parameter_name = "star"

    def lookups(self, request, model_admin):
        return [
            ("3", "🌟x3 👆"),
        ]

    def queryset(self, request, queryset):
        stars = self.value()
        if stars:
            return queryset.filter(rating__gte=stars)
        else:
            queryset
```

---

### URLs & Views

config > urls.py : 유저가 특정 url로 접근했을 때 장고가 해야할 일을 명시

```python
from django.contrib import admin
from django.urls import path
from rooms import views as room_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("rooms", room_views.say_hello),
]
```

view: 유저가 특정 url에 접근했을때 실행되는 함수

view.py

```python
from django.shortcuts import render
from django.http import HttpResponse

def say_hello(req):
    print(req)
    return HttpResponse("hello")
```

---

### urls with include

config > urls.py

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("rooms", include("rooms.urls")),
]
```

rooms > urls.py

```python
from django.urls import path
from rooms import views

urlpatterns = [
    path("/", views.say_hello),  # root
]
```

### Url arguments

config > urls.py

타입을 지정해줄 수 있다. <int> , <str>

```python
from django.urls import path
from rooms import views

urlpatterns = [
    path("", views.see_all_rooms),  # root
    path("<int:room_id>", views.see_one_room),  # root
]
```

rooms > urls.py

```python
from django.http import HttpResponse

def see_all_rooms(req):
    return HttpResponse("see all rooms")

def see_one_room(req, room_id):
    return HttpResponse(f"see {room_id} room")
```

### Render templates

app > templates > page_name.html

render는 (request: HttpRequest, template_name: str | Sequence[str], ccontext: Mapping[str, Any]

```python
from django.shortcuts import render
from django.http import HttpResponse
from rooms.models import Room

def see_all_rooms(req):
    rooms = Room.objects.all()
    return render(
        req,
        "all_rooms.html",
        {
            "title": "Comes from Django",
            "rooms": rooms,
        },
    )
```

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>
  <body>
    <header>{{title}}</header>
    <main>
      <ul>
        {% for room in rooms %}
        <li>
          <a href="/rooms/{{room.pk}}">
            {{room.name}}
            <hr />
            {% for amenity in room.amenities.all %}
            <span>{{amenity.name}}</span>
            <p>{{amenity.description}}</p>
            {% endfor %}
          </a>
        </li>
        {% endfor %}
      </ul>
    </main>
  </body>
</html>
```

### Not Found (404)

```python
def see_one_room(req, room_id):
    try:
        room = Room.objects.get(pk=room_id)
        return render(
            req,
            "room_detail.html",
            {
                "room": room,
            },
        )
    except Room.DoesNotExist:
        return render(
            req,
            "room_detail.html",
            {
                "not_found": True,
            },
        )
```

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>
  <body>
    {% if not not_found %}
    <header>
      <h1>{{room.name}}</h1>
    </header>
    <main>
      <div>
        <h3>price: {{room.price}}</h3>
        <h5>{{room.category.name}}</h5>
        <p>{{room.description}}</p>
      </div>
    </main>
    {% else %}
    <h2>Room Not Found.</h2>
    {% endif %}
  </body>
</html>
```

## Django REST Framwork

[docs](https://www.django-rest-framework.org/#installation)

`poetry add djangorestframework`

config.py > settings.py

third party app 등록

```python
THIRD_PARTY_APPS = [
    "rest_framework",
]

CUSTOM_APPS = [
    "common.apps.CommonConfig",
    "users.apps.UsersConfig",
    "rooms.apps.RoomsConfig",
    "experiences.apps.ExperiencesConfig",
    "categories.apps.CategoriesConfig",
    "reviews.apps.ReviewsConfig",
    "wishlists.apps.WishlistsConfig",
    "bookings.apps.BookingsConfig",
    "medias.apps.MediasConfig",
    "direct_messages.apps.DirectMessagesConfig",
]

SYSTEM_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

INSTALLED_APPS = SYSTEM_APPS + CUSTOM_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
```

Queryset → Json 으로의 변환 과정 필요

```python
from django.http import JsonResponse
from categories.models import Category

def categories(req):
    all_categories = Category.objects.all()
    return JsonResponse(
        {
            "ok": True,
            # ERROR OCCUR: Object of type QuerySet is not JSON serializable
            # Need to translate(serialize) QuerySet to JSON
            "categories": all_categories,
        },
    )
```

Serialize

[docs](https://docs.djangoproject.com/en/4.1/topics/serialization/#serializing-django-objects)

```python
from django.http import JsonResponse
from django.core import serializers
from categories.models import Category

def categories(req):
    all_categories = Category.objects.all()
    return JsonResponse(
        {
            "ok": True,
            "categories": serializers.serialize("json", all_categories),
        },
    )
```

Response example

```json
{
ok: true,
categories: "[{"model": "categories.category", "pk": 1, "fields": {"created_at": "2022-09-15T10:12:23.104Z", "updated_at": "2022-09-15T10:12:23.104Z", "name": "tiny homes", "kind": "rooms"}}, {"model": "categories.category", "pk": 2, "fields": {"created_at": "2022-09-15T10:12:49.437Z", "updated_at": "2022-09-15T10:12:49.437Z", "name": "food and drink", "kind": "experiences"}}]"
}
```

---

### Django Rest Framework

`api_view` decorators를 통해 아래와 같은 response를 받을 수 있다.

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/cdad9c1f-fff3-4779-9d09-f70090a4a818/Untitled.png)

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view()
def categories(req):
    return Response(
        {
            "ok": True,
        },
    )
```

app > serializer.py

```python
from rest_framework import serializers

class CategorySerializer(serializers.Serializer):

    # Customizable
    # How & What
    pk = serializers.IntegerField(required=True)
    name = serializers.CharField(required=True)
    kind = serializers.CharField()
```

app > views.py

```python
from categories.models import Category
from categories.serializers import CategorySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view()
def categories(req):
    all_categories = Category.objects.all()
    # CategorySerializer는 하나의 category에 대해서 번역을 하고 있기 때문에
    # 리스트를 번역하기 위해 many 옵션 필요
    serializers = CategorySerializer(all_categories, many=True)
    return Response(
        {
            "ok": True,
            "categories": serializers.data,
        },
    )
```

### POST request

decorator에 method를 지정해주기만 하면 된다

```python
@api_view(["GET", "POST"])
def categories(req):
    if req.method == "GET":
        all_categories = Category.objects.all()
        serializers = CategorySerializer(all_categories, many=True)
        return Response(serializers.data)

    elif req.method == "POST":
        print(req.data)
        return Response({"created": True})
```

### Is_valid

views.py

```python
@api_view(["GET", "POST"])
def categories(req):
    if req.method == "GET":
        all_categories = Category.objects.all()
        serializers = CategorySerializer(all_categories, many=True)
        return Response(serializers.data)

    elif req.method == "POST":
        # Serializer know data shape
        serializers = CategorySerializer(data=req.data)
        if serializers.is_valid():
            return Response({"created": True})
        else:
            return Response(serializers.errors)
```

serializer.py

read_only for POST request

```python
from rest_framework import serializers

class CategorySerializer(serializers.Serializer):

    # Customizable
    # How & What
    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True)
    kind = serializers.CharField()
```

### Save

view.py

```python
@api_view(["GET", "POST"])
def categories(req):
    if req.method == "GET":
        all_categories = Category.objects.all()
        serializers = CategorySerializer(all_categories, many=True)
        return Response(serializers.data)

    elif req.method == "POST":
        # Serializer know data shape
        serializers = CategorySerializer(data=req.data)
        if serializers.is_valid():
            # if save called, automatically call create method
            # create method definition is our job
            new_category = serializers.save()
            serializers = CategorySerializer(new_category)
            return Response(serializers.data)
        else:
            return Response(serializers.errors)
```

serializer.py

```python
def create(self, validated_data):
        # python unpacking
        return Category.objects.create(**validated_data)
```

### Update

view.py

```python
@api_view(["GET", "PUT"])
def category(req, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        raise NotFound

    if req.method == "GET":
        serializers = CategorySerializer(category)
        return Response(serializers.data)
    elif req.method == "PUT":
        serializers = CategorySerializer(
            category,
            data=req.data,
            # because only for update
            partial=True,
        )
        if serializers.is_valid():
            # in this case, serializers call update method
            updated_category = serializers.save()
            serializers = CategorySerializer(updated_category)
            return Response(serializers.data)
        else:
            return Response(serializers.errors)
```

serilizer.py

```python
def update(self, instance, validated_data):
        # second args return defualt value
        instance.name = validated_data.get("name", instance.name)
        instance.kind = validated_data.get("kind", instance.kind)
        instance.save()
        return instance
```

### Delete

view.py

```python
elif req.method == "DELETE":
        category.delete()
        return Response(status=HTTP_204_NO_CONTENT)
```

## Refactor

urls.py

```python
from django.urls import path
from categories import views

urlpatterns = [
    path("", views.Categories.as_view()),
    path("<int:pk>", views.CategoryDetail.as_view()),
]
```

views.py

```python
from categories.models import Category
from categories.serializers import CategorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT

class Categories(APIView):
    def get(self, req):
        all_categories = Category.objects.all()
        serializers = CategorySerializer(all_categories, many=True)
        return Response(serializers.data)

    def post(self, req):
        # Serializer know data shape
        serializers = CategorySerializer(data=req.data)
        if serializers.is_valid():
            # if save called, automatically call create method
            # create method definition is our job
            new_category = serializers.save()
            serializers = CategorySerializer(new_category)
            return Response(serializers.data)
        else:
            return Response(serializers.errors)

class CategoryDetail(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise NotFound

    def get(self, req, pk):
        serializers = CategorySerializer(self.get_object(pk))
        return Response(serializers.data)

    def put(self, req, pk):
        serializers = CategorySerializer(
            self.get_object(pk),
            data=req.data,
            # because only for update
            partial=True,
        )
        if serializers.is_valid():
            # in this case, serializers call update method
            updated_category = serializers.save()
            serializers = CategorySerializer(updated_category)
            return Response(serializers.data)
        else:
            return Response(serializers.errors)

    def delete(self, req, pk):
        self.get_object(pk).delete()
        return Response(status=HTTP_204_NO_CONTENT)
```

### ModelSerializer

- A set of default fields are automatically populated.
- A set of default validators are automatically populated.
- Default `.create()` and `.update()` implementations are provided.

serializer.py

```python
from rest_framework import serializers
from categories.models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        # exclude
```

### ModelViewSet

[docs](https://www.django-rest-framework.org/api-guide/viewsets/#viewset-actions)

urls.py

```python
from django.urls import path
from categories import views

# https://www.django-rest-framework.org/api-guide/viewsets/#viewset-actions
urlpatterns = [
    path(
        "",
        views.CategoryViewSet.as_view(
            # connect http methods and class methods
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path(
        "<int:pk>",
        views.CategoryViewSet.as_view(
            {
                "get": "retrieve",
                "put": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
]
```

views.py

```python
from categories.models import Category
from categories.serializers import CategorySerializer
from rest_framework.viewsets import ModelViewSet

class CategoryViewSet(ModelViewSet):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
```

### Depth

```python
class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
        depth = 1
```

관계가 연결된 데이터의 정보를 가져온다.

### Populate Serializer

```python
class RoomSerializer(ModelSerializer):

    # populate: name, username, avatar
    owner = BriefUserSerializer()
    # populate: name, description
    amenities = AmenitySerializer(many=True)
    # populate: name, kind
    category = CategorySerializer()

    class Meta:
        model = Room
        fields = "__all__"
```

### Create Room with Authenticated Owner

serializer.py

nest 모델은 read_only를 설정

```python
class RoomSerializer(ModelSerializer):

    # populate: name, username, avatar
    owner = BriefUserSerializer(read_only=True)
    # populate: name, description
    amenities = AmenitySerializer(read_only=True, many=True)
    # populate: name, kind
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Room
        fields = "__all__"
```

view.py

req.user.is_authenticated로 로그인 된 유저를 검증하고

save method에 serializer.save(owner=req.user) owner를 넘겨준다.

```python
class Rooms(APIView):
    def get(self, req):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(all_rooms, many=True)
        return Response(serializer.data)

    def post(self, req):
        if req.user.is_authenticated:
            serializer = RoomSerializer(data=req.data)
            if serializer.is_valid():
                room = serializer.save(owner=req.user)
                return Response(RoomSerializer(room).data)
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated
```

### Room Category

category pk를 통해 category를 찾고, 전달해주는 방식

```python
def post(self, req):
        if req.user.is_authenticated:
            serializer = RoomSerializer(data=req.data)
            if serializer.is_valid():
                category_pk = req.data.get("category")
                if not category_pk:
                    raise ParseError("Category is required.")
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The category kind should be rooms.")
                except Category.DoesNotExist:
                    raise ParseError("Category not found.")
                room = serializer.save(owner=req.user, category=category)
                return Response(RoomSerializer(room).data)
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated
```

### Room Amenities (many to many)

```python
def post(self, req):
        if req.user.is_authenticated:
            serializer = RoomSerializer(data=req.data)
            if serializer.is_valid():
                category_pk = req.data.get("category")
                if not category_pk:
                    raise ParseError("Category is required.")
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The category kind should be rooms.")
                except Category.DoesNotExist:
                    raise ParseError("Category not found.")
                amenities = req.data.get("amenities")
                room = serializer.save(owner=req.user, category=category)
                for amenity_pk in amenities:
                    try:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                    except Amenity.DoesNotExist:
                        room.delete()
                        raise ParseError(f"Amenity with id {amenity_pk} not found.")
                    room.amenities.add(amenity)
                return Response(RoomSerializer(room).data)
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated
```

many to many의 경우 데이터를 추가할 때, room.amenities.add(amenity)과 같은 방식으로 추가해준다.

따라서 room이 생성되고 amenity를 추가하는 방식이기 때문에 amenity error가 발생하는 경우 생성된 room을 삭제한다. (optional)

### Transaction

django는 즉각적으로 query를 실행시킨다. 따라서 room을 생성하고 삭제하게되는 경우, 불필요한 query가 실행되기도 하고, 생성으로 인한 id가 계속해서 증가하기도 한다.

이를 방지하기 위해 transaction은 query가 한번에 실행되도록 나누고, 에러가 없는 경우 db에 push 한다.

```python
def post(self, req):
        if req.user.is_authenticated:
            serializer = RoomSerializer(data=req.data)
            if serializer.is_valid():
                category_pk = req.data.get("category")
                if not category_pk:
                    raise ParseError("Category is required.")
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The category kind should be rooms.")
                except Category.DoesNotExist:
                    raise ParseError("Category not found.")
                try:
                    with transaction.atomic():
                        room = serializer.save(owner=req.user, category=category)
                        amenities = req.data.get("amenities")
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            room.amenities.add(amenity)
                        return Response(RoomSerializer(room).data)
                except Exception:
                    raise ParseError("Amenity not found.")
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated
```

### Room Delete

check authenticated & owner of rooom

```python
class RoomListSerializer(ModelSerializer):

    rating = SerializerMethodField()

    class Meta:
        model = Room
        fields = ["pk", "name", "country", "city", "price", "rating"]

    # method name is mandatory(get_[field])
    def get_rating(self, room):
        return room.rating()
```

### \***\*Serializer Context\*\***

view.py

```python
class Rooms(APIView):
    def get(self, req):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(
            all_rooms,
            many=True,
            context={"req": req},
        )
        return Response(serializer.data)
```

serializers.py

```python
class RoomListSerializer(ModelSerializer):

    rating = SerializerMethodField()
    is_owner = SerializerMethodField()

    class Meta:
        model = Room
        fields = [
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
        ]

    # method name is mandatory(get_[field])
    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        req = self.context["req"]
        return req.user == room.owner
```

### Reverse \***\*Serializers\*\***

review > serializers.py

```python
from rest_framework import serializers
from reviews.models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
```

room > serializers.py

```python
class RoomSerializer(ModelSerializer):

    # populate: name, username, avatar
    owner = BriefUserSerializer(read_only=True)
    # populate: name, description
    amenities = AmenitySerializer(read_only=True, many=True)
    # populate: name, kind
    category = CategorySerializer(read_only=True)

    rating = SerializerMethodField()
    is_owner = SerializerMethodField()

    # Reverse Serializers
    # review has fk of room
    # room can access reviews pointing themself with related_name
    reviews = ReviewSerializer(read_only=True, many=True)

    class Meta:
        model = Room
        fields = "__all__"

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        req = self.context["req"]
        return req.user == room.owner
```

### Pagination

[docs](https://docs.djangoproject.com/en/4.1/topics/db/queries/#limiting-querysets)

모든 review를 load한 후 자르는것이 아닌 offset과 limit을 통해 요청

```python
def get(self, req, pk):
        try:
            page = req.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        take = 5
        start = (page - 1) * take
        end = page * take

        room = self.get_object(pk)
        serializer = ReviewSerializer(
            room.reviews.all()[start:end],
            many=True,
        )
        return Response(serializer.data)
```

### Global Constant

어디서든 접근 가능

config > settings.py

```python
# PAGINATION
TAKE_SIZE = 5
```

room > views.py

```python
from django.conf import settings

take = settings.TAKE_SIZE
```

### Files + Static

[docs](https://docs.djangoproject.com/en/4.1/howto/static-files/#serving-static-files-during-development)

개발 모드에서만 적합한 방식이다.

config > settings.py

```python
# MEDIA

# 실제 위치
MEDIA_ROOT = "uploads"
# 노출되는 위치 (Browser)
MEDIA_URL = "user-uploads/"
```

config > urls.py

```python
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/rooms/", include("rooms.urls")),
    path("api/v1/categories/", include("categories.urls")),
    path("api/v1/experiences/", include("experiences.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Upload photo

```python
class RoomPhotos(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def post(self, req, pk):
        room = self.get_object(pk)
        if not req.user.is_authenticated:
            raise NotAuthenticated
        if req.user != room.owner:
            raise PermissionDenied

        serializer = PhotoSerializer(data=req.data)
        if serializer.is_valid():
            photo = serializer.save(room=room)
            return Response(PhotoSerializer(photo).data)
        else:
            return Response(serializer.errors)
```

### permission_classes

room > view.py

인증에 관한 부분을 한 줄의 코드로 대신할 수 있다.

`permission_classes = [IsAuthenticatedOrReadOnly]`

```python
class RoomPhotos(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def post(self, req, pk):
        room = self.get_object(pk)
        if req.user != room.owner:
            raise PermissionDenied

        serializer = PhotoSerializer(data=req.data)
        if serializer.is_valid():
            photo = serializer.save(room=room)
            return Response(PhotoSerializer(photo).data)
        else:
            return Response(serializer.errors)
```

### Wishlists (toggle)

wishlists > urls.py

```python
urlpatterns = [
    path("", Wishlists.as_view()),
    path("<int:pk>", WishlistDetail.as_view()),
    path("<int:pk>/rooms/<int:room_pk>", WishlistToggle.as_view()),
]
```

wishlists > views.py

```python
class WishlistToggle(APIView):
    def get_wishlist(self, pk, user):
        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound

    def get_room(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def put(self, req, pk, room_pk):
        wishilist = self.get_wishlist(pk, req.user)
        room = self.get_room(room_pk)

        if wishilist.rooms.filter(pk=room.pk).exists():
            wishilist.rooms.remove(room)
        else:
            wishilist.rooms.add(room)
        return Response(status=HTTP_200_OK)
```

### is_on_wishlist

room > serializers.py

```python
class RoomSerializer(ModelSerializer):

    is_on_wishlist = SerializerMethodField()

    def get_is_on_wishlist(self, room):
        req = self.context["req"]
        return Wishlist.objects.filter(user=req.user, rooms__pk=room.pk).exists()
```

### Bookings

django util: timezone

```python
from django.utils import timezone

class RoomBookings(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, req, pk):
        room = self.get_object(pk)
        now = timezone.localtime().date()
        print(now)
        # room pk를 통해 bookings을 가져올 수도 있다.
        # 하지만 이 경우, room이 존재 하지 않는 경우와 booking이 존재하지 않는 경우가
        # 동일하게 빈 배열을 return 하게된다.
        # bookings = Booking.objects.filter(room__pk=pk)
        bookings = Booking.objects.filter(
            room=room,
            kind=Booking.BookingKindChoices.ROOM,
            check_in__gt=now,
        )
        serializer = PublicBookingSerializer(bookings, many=True)
        return Response(serializer.data)
```

### Custom validation

is_valid의 유효성 검사 customize

````python
class CreateRoomBookingSerializer(serializers.ModelSerializer):
    """
    Booking model에서 check_in, check_out 필드가 optional 하기떄문에
    오직 booking 생성을 위한 serializer
    """

    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = [
            "check_in",
            "check_out",
            "guests",
        ]

# custum validation method
    def validate_check_in(self, value):
        now = timezone.localtime().date()
        if value > now:
            return value
        else:
            raise serializers.ValidationError("Can't book in the past")

    def validate_check_out(self, value):
        now = timezone.localtime().date()
        if value > now:
            return value
        else:
            raise serializers.ValidationError("Can't book in the past")

    def validate(self, data):
        if data["check_in"] >= data["check_out"]:
            raise serializers.ValidationError(
                "Check in should be smaller than check out."
            )

        if Booking.objects.filter(
            check_in__lte=data["check_out"],
            check_out__gte=data["check_in"],
        ).exists():
            raise serializers.ValidationError(
                "Those (or some) of dates are already taken."
            )

        return data
```class CreateRoomBookingSerializer(serializers.ModelSerializer):
    """
    Booking model에서 check_in, check_out 필드가 optional 하기떄문에
    오직 booking 생성을 위한 serializer
    """

    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = [
            "check_in",
            "check_out",
            "guests",
        ]

    # custum validation method
    def validate_check_in(self, value):
        now = timezone.localtime().date()
        if value > now:
            return value
        else:
            raise serializers.ValidationError("Can't book in the past")

    def validate_check_out(self, value):
        now = timezone.localtime().date()
        if value > now:
            return value
        else:
            raise serializers.ValidationError("Can't book in the past")
````

### Create User

user.set_password → password를 알아서 hash 해줌

```python
class Users(APIView):
    def post(self, req):
        password = req.data.get("password")
        if not password:
            raise exceptions.ParseError("password is required.")

        serializer = PrivateUserSerializer(data=req.data)

        if serializer.is_valid():
            user = serializer.save()
            # hash the password
            user.set_password(password)
            user.save()
            serializer = PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
```

### Routing Caution

string을 인자로 받기 때문에 url 순서가 중요.

username이 `me`일 수 있기 때문에 @로 구분

```python
urlpatterns = [
    path("", views.Users.as_view()),
    path("me", views.Me.as_view()),
    path("@<str:username>", views.PublicUser.as_view()),
]
```

### Change Password

check_password를 통해 검증

```python
class ChangePassword(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, req):
        user = req.user
        old_password = req.data.get("old_password")
        new_password = req.data.get("new_password")

        if not old_password or not new_password:
            raise exceptions.ParseError

        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            raise exceptions.ParseError
```

### Log-in & Log-out

```python
from django.contrib.auth import authenticate, login, logout

class LogIn(APIView):
    def post(self, req):
        username = req.data.get("username")
        password = req.data.get("password")

        if not username or not password:
            raise exceptions.ParseError

        user = authenticate(
            req,
            username=username,
            password=password,
        )

        if not user:
            return Response({"error": "wrong passwrod"})
        else:
            login(req, user)
            return Response({"ok": "log-in succeed"})

class LogOut(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, req):
        logout(req)
        return Response({"ok": "log-out succeed"})
```
