from enum import IntEnum, IntFlag, auto
from typing import Final, Optional, Set


class Ft4222Status(IntEnum):
    OK = 0
    INVALID_HANDLE = auto()
    DEVICE_NOT_FOUND = auto()
    DEVICE_NOT_OPENED = auto()
    IO_ERROR = auto()
    INSUFFICIENT_RESOURCES = auto()
    INVALID_PARAMETER = auto()
    INVALID_BAUD_RATE = auto()
    DEVICE_NOT_OPENED_FOR_ERASE = auto()
    DEVICE_NOT_OPENED_FOR_WRITE = auto()
    FAILED_TO_WRITE_DEVICE = auto()
    EEPROM_READ_FAILED = auto()
    EEPROM_WRITE_FAILED = auto()
    EEPROM_ERASE_FAILED = auto()
    EEPROM_NOT_PRESENT = auto()
    EEPROM_NOT_PROGRAMMED = auto()
    INVALID_ARGS = auto()
    NOT_SUPPORTED = auto()
    OTHER_ERROR = auto()
    DEVICE_LIST_NOT_READY = auto()

    # FT_STATUS extending message
    DEVICE_NOT_SUPPORTED = 1000
    CLK_NOT_SUPPORTED = auto()
    VENDOR_CMD_NOT_SUPPORTED = auto()
    IS_NOT_SPI_MODE = auto()
    IS_NOT_I2C_MODE = auto()
    IS_NOT_SPI_SINGLE_MODE = auto()
    IS_NOT_SPI_MULTI_MODE = auto()
    WRONG_I2C_ADDR = auto()
    INVALID_FUNCTION = auto()
    INVALID_POINTER = auto()
    EXCEEDED_MAX_TRANSFER_SIZE = auto()
    FAILED_TO_READ_DEVICE = auto()
    I2C_NOT_SUPPORTED_IN_THIS_MODE = auto()
    GPIO_NOT_SUPPORTED_IN_THIS_MODE = auto()
    GPIO_EXCEEDED_MAX_PORTNUM = auto()
    GPIO_WRITE_NOT_SUPPORTED = auto()
    GPIO_PULLUP_INVALID_IN_INPUTMODE = auto()
    GPIO_PULLDOWN_INVALID_IN_INPUTMODE = auto()
    GPIO_OPENDRAIN_INVALID_IN_OUTPUTMODE = auto()
    INTERRUPT_NOT_SUPPORTED = auto()
    GPIO_INPUT_NOT_SUPPORTED = auto()
    EVENT_NOT_SUPPORTED = auto()
    FUN_NOT_SUPPORT = auto()


SOFT_ERROR_SET: Final[Set[Ft4222Status]] = {
    Ft4222Status.OK, Ft4222Status.INVALID_HANDLE,
    Ft4222Status.DEVICE_NOT_FOUND, Ft4222Status.DEVICE_NOT_OPENED,
}


class Ft4222Exception(Exception):
    """A class wrapping the FT4222 driver exception.
    """
    status: Ft4222Status
    msg: Optional[str]

    def __init__(self, status: Ft4222Status, msg: Optional[str] = None):
        self.status = status
        self.msg = msg

    def __str__(self) -> str:
        return f"""
Exception during call to LibFT4222 library.
FT return code: {self.status.name}
Message: {self.msg}
        """


class GpioTrigger(IntFlag):
    RISING = 0x01       # Trigger on rising edge
    FALLING = 0x02      # Trigger on falling edge
    LEVEL_HIGH = 0x04   # Trigger on high level
    LEVEL_LOW = 0X08    # Trigger on low level
