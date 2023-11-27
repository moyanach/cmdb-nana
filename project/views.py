# Create your views here.
from typing_extensions import Self

from django.utils.dateparse import parse_datetime


def test_parse_datetime():
    datetime_str = "2023-03-22 11:06:34"
    datetime_obj = parse_datetime(datetime_str)
    print(datetime_obj)


class TestClassGetAttr:

    def __init__(self) -> None:
        pass

    def voice(self, voice: str):
        print(f'voice: {voice}')


class TestMagicClass:

    def __new__(cls, *args, **kwargs) -> Self:
        print('__new__')
        return super().__new__(cls)

    def __init__(self) -> None:
        print(f'__init__, dir(self): {dir(self)}')

    def __getattr__(self, name):
        aa = TestClassGetAttr()
        return getattr(aa, name)


if __name__ == "__main__":
    magic = TestMagicClass()
    print(magic.voice('ww'))
