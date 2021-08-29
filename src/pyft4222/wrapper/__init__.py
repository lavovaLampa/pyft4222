from enum import Enum, IntEnum, IntFlag, auto
from typing import Final, Generic, Literal, NewType, Optional, TypeVar, Union
from ctypes import c_void_p

import platform

OS_TYPE: Final = platform.system()

FtHandle = NewType('FtHandle', c_void_p)


class ResType(Enum):
    OK = auto()
    ERR = auto()


T = TypeVar('T')
E = TypeVar('E')


class Ok(Generic[T]):
    tag: Literal[ResType.OK] = ResType.OK
    result: T

    def __init__(self, result: T):
        self.result = result


class Err(Generic[E]):
    tag: Literal[ResType.ERR] = ResType.ERR
    err: E

    def __init__(self, err: E):
        self.err = err


Result = Union[Ok[T], Err[E]]


class FtStatus(IntEnum):
    """Class representing a D2XX 'FT_RESULT' enum.
    """
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


class FtException(Exception):
    """A class wrapping the D2XX driver exceptions.

    Attributes:
        status:     D2XX result enum
        msg:        Optional human-readable message
    """
    status: FtStatus
    msg: Optional[str]

    def __init__(self, status: FtStatus, msg: Optional[str] = None):
        super().__init__()
        self.status = status
        self.msg = msg

    def __str__(self) -> str:
        return f"""
Exception during call to FTD2XX library.
FT return code: {self.status.name}
Message: {self.msg}
        """


class Ft4222Status(IntEnum):
    """Enum representing the 'FT4222_STATUS' enum from ft4222 library.

    This enum 'extends' the 'FT_STATUS' enum.
    """
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

    # FtStatus extending message
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

    @classmethod
    def from_ft_status(cls, ft_status: FtStatus) -> 'Ft4222Status':
        return Ft4222Status(int(ft_status))


class Ft4222Exception(Exception):
    """A class wrapping the FT4222 driver exceptions.

    Params:
        status:     FT4222 result enum
        msg:        Optional human-readable message
    """
    status: Ft4222Status
    msg: Optional[str]

    def __init__(self, status: Ft4222Status, msg: Optional[str] = None):
        super().__init__()
        self.status = status
        self.msg = msg

    def __str__(self) -> str:
        return f"""
Exception during call to LibFT4222 library.
FT return code: {self.status.name}
Message: {self.msg}
        """


class GpioTrigger(IntFlag):
    """Enum representing possible GPIO triggers types."""
    RISING = 0x01
    """Trigger on rising edge."""
    FALLING = 0x02
    """Trigger on falling edge."""
    LEVEL_HIGH = 0x04
    """Trigger on high level."""
    LEVEL_LOW = 0X08
    """Trigger on low level."""
