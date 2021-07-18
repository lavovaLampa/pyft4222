from ctypes import cdll, Structure, c_uint, c_void_p, POINTER, c_bool, c_uint16, byref
from enum import IntEnum, IntFlag, auto
from typing import NamedTuple, Union

from .spi import SpiHandle
from .spi.slave import SpiSlaveProtoHandle
from .i2c import I2cHandle
from .gpio import GpioHandle

from ..ft_common import FtHandle

try:
    ftlib = cdll.LoadLibrary('./lib/libft4222.so.1.4.4.44')
except OSError as e:
    print("Unable to load shared library!")
    exit(1)

InitializedHandle = Union[SpiHandle, I2cHandle, GpioHandle]


class FT4222Status(IntEnum):
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
    VENDER_CMD_NOT_SUPPORTED = auto()
    IS_NOT_SPI_MODE = auto()
    IS_NOT_I2C_MODE = auto()
    IS_NOT_SPI_SINGLE_MODE = auto()
    IS_NOT_SPI_MULTI_MODE = auto()
    WRONG_I2C_ADDR = auto()
    INVAILD_FUNCTION = auto()
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


class ClockRate(IntEnum):
    SYS_CLK_60 = 0
    SYS_CLK_24 = auto()
    SYS_CLK_48 = auto()
    SYS_CLK_80 = auto()


class GpioTrigger(IntFlag):
    RISING = 0x01
    FALLING = 0x02
    LEVEL_HIGH = 0x04
    LEVEL_LOW = 0X08


class EventType(IntFlag):
    EVENT_RXCHAR = 8


class _RawVersion(Structure):
    _fields_ = [
        ("chip_version", c_uint),
        ("dll_version", c_uint)
    ]


class Version(NamedTuple):
    chip_version: int
    dll_version: int

    @staticmethod
    def from_raw(raw_struct: _RawVersion) -> 'Version':
        return Version(
            raw_struct.chip_version,
            raw_struct.dll_version
        )


_uninitialize = ftlib.FT4222_UnInitialize
_uninitialize.argtypes = [c_void_p]
_uninitialize.restype = FT4222Status

_set_clock = ftlib.FT4222_SetClock
_set_clock.argtypes = [c_void_p, c_uint]
_set_clock.restype = FT4222Status

_get_clock = ftlib.FT4222_GetClock
_get_clock.argtypes = [c_void_p, POINTER(c_uint)]
_get_clock.restype = FT4222Status

_set_wakeup_interrupt = ftlib.FT4222_SetWakeUpInterrupt
_set_wakeup_interrupt.argtypes = [c_void_p, c_bool]
_set_wakeup_interrupt.restype = FT4222Status

_set_interrupt_trigger = ftlib.FT4222_SetInterruptTrigger
_set_interrupt_trigger.argtypes = [c_void_p, c_uint]
_set_interrupt_trigger.restype = FT4222Status

_set_suspend_out = ftlib.FT4222_SetSuspendOut
_set_suspend_out.argtypes = [c_void_p, c_bool]
_set_suspend_out.restype = FT4222Status

_get_max_transfer_size = ftlib.FT4222_GetMaxTransferSize
_get_max_transfer_size.argtypes = [c_void_p, POINTER(c_uint16)]
_get_max_transfer_size.restype = FT4222Status

_set_event_notification = ftlib.FT4222_SetEventNotification
_set_event_notification.argtypes = [c_void_p, c_uint, c_void_p]
_set_event_notification.restype = FT4222Status

_get_version = ftlib.FT4222_GetVersion
_get_version.argtypes = [c_void_p, POINTER(_RawVersion)]
_get_version.restype = FT4222Status

_chip_reset = ftlib.FT4222_ChipReset
_chip_reset.argtypes = [c_void_p]
_chip_reset.restype = FT4222Status


def uninitialize(ft_handle: InitializedHandle) -> FtHandle:
    """Release allocated resources.

    This functions should be called before calling 'close()'.

    Args:
        ft_handle:  Handle to an initialized FT4222 device

    Raises:
        RuntimeError:   TODO
    """
    retval: FT4222Status = _uninitialize(ft_handle)

    if retval != FT4222Status.OK:
        raise RuntimeError('TODO')

    return FtHandle(ft_handle)


def set_clock(ft_handle: FtHandle, clk_rate: ClockRate) -> None:
    """Set the system clock rate.

    The FT4222H supports 4 clock rates: 80MHz, 60MHz, 48MHz, or 24MHz.
    By default, the FT4222H runs at 60MHz clock rate.

    Args:
        ft_handle:  Handle to an opened FT4222 device
        clk_rate:   Desired system clock rate

    Raises:
        RuntimeError:   TODO
    """
    retval: FT4222Status = _set_clock(ft_handle, clk_rate)

    if retval != FT4222Status.OK:
        raise RuntimeError('TODO')


def get_clock(ft_handle: FtHandle) -> ClockRate:
    """Get the current system clock rate.

    Args:
        ft_handle:  Handle to an opened FT4222 device

    Raises:
        RuntimeError:   TODO

    Returns:
        ClockRate:  Current system clock rate
    """
    clk_rate = c_uint()
    retval: FT4222Status = _get_clock(ft_handle, byref(clk_rate))

    if retval != FT4222Status.OK:
        raise RuntimeError('TODO')

    return ClockRate(clk_rate.value)


def set_wakeup_interrupt(ft_handle: FtHandle, enable: bool) -> None:
    """Enable or disable wakeup/interrupt.
    By default, wake-up/interrupt function is on.

    When Wake up/Interrupt function is on, GPIO3 pin acts as an input pin for wakeup/interrupt.
    While system is in normal mode, GPIO3 acts as an interrupt pin.
    While system is in suspend mode, GPIO3 acts as a wakeup pin.

    Args:
        ft_handle:  Handle to an opened FT4222 device
        enable:     Enable wakeup/interrupt function?

    Raises:
        RuntimeError:   TODO
    """
    retval: FT4222Status = _set_wakeup_interrupt(ft_handle, enable)

    if retval != FT4222Status.OK:
        raise RuntimeError('TODO')


def set_interrupt_trigger(ft_handle: FtHandle, trigger: GpioTrigger) -> None:
    """Set trigger condition for the pin wakeup/interrupt.
    By default, the trigger condition is 'GpioTrigger.RISING'.

    This function configures trigger condition for wakeup/interrupt.

    When GPIO3 acts as wakeup pin, the ft4222H device has the capability to wake up the host.
    Only 'GpioTrigger.RISING' and 'GpioTrigger.FALLING' are valid when GPIO3 act as a wakeup pin.
    It is not necessary to call 'GPIO.init()' function to set up wake-up function.

    When GPIO3 acts as interrupt pin, all trigger conditions can be set.
    The result of trigger status can be inquired by 'GPIO.read_trigger_queue()' or 'GPIO.read()' functions.
    This is because the trigger status is provided by the GPIO pipe.
    Therefore it is necessary to call 'GPIO.init()' function to set up interrupt function.

    For GPIO triggering conditions: 'GpioTrigger.LEVEL_HIGH' and 'GpioTrigger.LEVEL_LOW',
    that can be configured when GPIO3 behaves as an interrupt pin, when the system enters suspend mode,
    these two configurations will act as 'GpioTrigger.RISING' and 'GpioTrigger.FALLING' respectively.

    Args:
        ft_handle:  Handle to an opened FT4222 device
        trigger:    WakeUp/Interrupt condition to set

    Raises:
        RuntimeError:   TODO
    """
    retval: FT4222Status = _set_interrupt_trigger(
        ft_handle, trigger.value)

    if retval != FT4222Status.OK:
        raise RuntimeError('TODO')


def set_suspend_out(ft_handle: FtHandle, enable: bool) -> None:
    """Enable or disable suspend out, which will emit a signal when FT4222H enters suspend mode.

    Please note that the suspend-out pin is not available under mode 2.
    By default, suspend-out function is on.
    GPIO2 will be used as an GPIO in output mode for emitting a suspend-out signal.

    When suspend-out function is on, suspend-out pin emits signal according to suspend-out polarity.
    The default value of suspend-out polarity is active high.
    It means suspend-out pin output low in normal mode and output high in suspend mode.
    Suspend-out polarity only can be adjusted by FT_PROG.

    Args:
        ft_handle:  Handle to an opened FT4222 device
        enable:     Enable suspend-out signaling?

    Raises:
        RuntimeError:   TODO
    """
    retval: FT4222Status = _set_suspend_out(ft_handle, enable)

    if retval != FT4222Status.OK:
        raise RuntimeError('TODO')


def get_max_transfer_size(ft_handle: FtHandle) -> int:
    """Get the maximum packet size in a transaction.

    It will be affected by different bus speeds, chip modes, and functions.
    The maximum transfer size is maximum size in writing path.

    Args:
        ft_handle:  Handle to an opened FT4222 device

    Raises:
        RuntimeError:   TODO

    Returns:
        int:    Maximum packet size in a transaction
    """
    max_size = c_uint16()
    retval: FT4222Status = _get_max_transfer_size(
        ft_handle, byref(max_size))

    if retval != FT4222Status.OK:
        raise RuntimeError('TODO')

    return max_size.value


# FIXME: Proper typing
def set_event_notification(
    ft_handle: SpiSlaveProtoHandle,
    mask: EventType,
    param: c_void_p
) -> None:
    """Sets conditions for event notification.

    An application can use this function to setup conditions which allow a thread to block until one of the conditions is met.
    Typically, an application will create an event, call this function, and then block on the event.
    When the conditions are met, the event is set, and the application thread unblocked.
    Usually, the event is set to notify the application to check the condition.
    The application needs to check the condition again before it goes to handle the condition.
    The API is only valid when the device acts as SPI slave and SPI slave protocol is not 'IoProtocol.No_PROTOCOL'. 

    Args:
        ft_handle:  Handle to an initialized FT4222 device in SPI Slave mode
        mask:       Event mask (i.e. select which events to react to)
        param:      TODO

    Raises:
        RuntimeError:   TODO
    """
    retval: FT4222Status = _set_event_notification(
        ft_handle, mask.value, param)

    if retval != FT4222Status.OK:
        raise RuntimeError('TODO')


# FIXME: Add enum for chip version?
def get_version(ft_handle: FtHandle) -> Version:
    """Get the version of FT4222H chip and LibFT4222 library.

    Args:
        ft_handle:  Handle to an opened FT4222 device

    Raises:
        RuntimeError:   TODO

    Returns:
        Version:    NamedTuple containing version information
    """
    version_struct = _RawVersion()
    retval: FT4222Status = _get_version(
        ft_handle, byref(version_struct))

    if retval != FT4222Status.OK:
        raise RuntimeError('TODO')

    return Version.from_raw(version_struct)


def chip_reset(ft_handle: FtHandle) -> None:
    """Software reset for a device.

    This function is used to attempt to recover system after a failure.
    It is a software reset for device.

    Args:
        ft_handle:  Handle to an opened FT4222 device

    Raises:
        RuntimeError:   TODO
    """
    retval: FT4222Status = _chip_reset(ft_handle)

    if retval != FT4222Status.OK:
        raise RuntimeError('TODO')
