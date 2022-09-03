class Player:
    def __init__(self, name="jinwook"):
        self.name = name

    def hello(self):
        print(f"hello {self.name}~")


user = Player("nico")
print(user.name)
user.hello()
