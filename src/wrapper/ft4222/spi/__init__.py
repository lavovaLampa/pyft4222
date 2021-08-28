from enum import IntEnum, auto


class DriveStrength(IntEnum):
    """Enum defining all possible I/O drive strength values."""
    DS_4MA = 0
    """4 mA"""
    DS_8MA = auto()
    """8 mA"""
    DS_12MA = auto()
    """12 mA"""
    DS_16MA = auto()
    """16 mA"""


class ClkPolarity(IntEnum):
    """Enum defining SPI clock polarity."""
    CLK_IDLE_LOW = 0
    CLK_IDLE_HIGH = 1


class ClkPhase(IntEnum):
    """Enum defining SPI clock phase."""
    CLK_LEADING = 0
    CLK_TRAILING = 1
