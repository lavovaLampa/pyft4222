from enum import IntEnum, auto


class DriveStrength(IntEnum):
    DS_4MA = 0
    DS_8MA = auto()
    DS_12MA = auto()
    DS_16MA = auto()


class ClkPolarity(IntEnum):
    CLK_IDLE_LOW = 0
    CLK_IDLE_HIGH = 1


class ClkPhase(IntEnum):
    CLK_LEADING = 0
    CLK_TRAILING = 1
