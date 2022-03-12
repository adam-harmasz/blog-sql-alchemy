from random import randrange


class ShowRepr:
    def __init__(self, some_string: str) -> None:
        self.some_string = some_string

    @property
    def my_props(self) -> str:
        return f"{randrange(100)}"

    def __repr__(self) -> str:
        return f"This is my string here: {self.some_string}"


x = ShowRepr(some_string="KAWA")

# print(x.my_props)
