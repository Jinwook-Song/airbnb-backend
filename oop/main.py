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
        # super().__init__(name)
        self.name = name


user = Player("nico")
print(user.name)
user.hello()

user2 = Fan("nico")
print(user2.name)
user2.hello()
