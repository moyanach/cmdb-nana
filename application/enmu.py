from enum import IntEnum, Enum


class AppCostModeEnmu(str, Enum):
    计算型 = "cpu"
    内存型 = "memory"
    磁盘型 = "disk"


class AppLevelEnmu(IntEnum):
    S级 = 1
    A级 = 2
    B级 = 3


class AppTypeEnmu(IntEnum):
    物理应用 = 1
    虚拟应用 = 2


class DockerTypeEnmu(IntEnum):
    容器应用 = 1
    非容器应用 = 0


class AppLangEnmu(IntEnum):
    Java = 1
    Golang = 2
    PHP = 3
    Python = 4
    Node = 5
    C = 6

