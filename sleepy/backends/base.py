class BaseBackend:
    def __init__(self, name):
        self.name = name

    def log(self, message):
        print(f"{self.name}: {message}")
