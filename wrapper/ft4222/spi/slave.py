from ctypes import POINTER, byref
from ctypes import c_void_p, c_uint, c_uint16, c_uint8

from enum import IntEnum, IntFlag, auto
from typing import Literal, NewType, Union, overload

from . import ClkPhase, ClkPolarity
from .. import Ft4222Exception, Ft4222Status
from ...dll_loader import ftlib
from ... import FtHandle, Result, Ok, Err

SpiSlaveRawHandle = NewType('SpiSlaveRawHandle', FtHandle)
SpiSlaveProtoHandle = NewType('SpiSlaveProtoHandle', FtHandle)
SpiSlaveHandle = Union[SpiSlaveRawHandle, SpiSlaveProtoHandle]


class IoProtocol(IntEnum):
    WITH_PROTOCOL = 0
    NO_PROTOCOL = auto()
    NO_ACK = auto()


class EventType(IntFlag):
    EVENT_RXCHAR = 8


_init = ftlib.FT4222_SPISlave_Init
_init.argtypes = [c_void_p]
_init.restype = Ft4222Status

_init_ex = ftlib.FT4222_SPISlave_InitEx
_init_ex.argtypes = [c_void_p, c_uint]
_init_ex.restype = Ft4222Status

_set_mode = ftlib.FT4222_SPISlave_SetMode
_set_mode.argtypes = [c_void_p, c_uint, c_uint]
_set_mode.restype = Ft4222Status

_get_rx_status = ftlib.FT4222_SPISlave_GetRxStatus
_get_rx_status.argtypes = [c_void_p, POINTER(c_uint16)]
_get_rx_status.restype = Ft4222Status

_read = ftlib.FT4222_SPISlave_Read
_read.argtypes = [c_void_p, POINTER(
    c_uint8), c_uint16, POINTER(c_uint16)]
_read.restype = Ft4222Status

_write = ftlib.FT4222_SPISlave_Write
_write.argtypes = [c_void_p, POINTER(
    c_uint8), c_uint16, POINTER(c_uint16)]
_write.restype = Ft4222Status

_set_event_notification = ftlib.FT4222_SetEventNotification
_set_event_notification.argtypes = [c_void_p, c_uint, c_void_p]
_set_event_notification.restype = Ft4222Status


def init(ft_handle: FtHandle) -> Result[SpiSlaveProtoHandle, Ft4222Status]:
    """Initialize the FT4222H as an SPI slave.

    Default SPI Slave protocol is 'IoProtocol.WITH_PROTOCOL'.

    Args:
        ft_handle:  Handle to an open FT4222 device

    Returns:
        Result:     Handle to FT4222 device in SPI Slave mode with protocol
    """
    result: Ft4222Status = _init(ft_handle)

    if result == Ft4222Status.OK:
        return Ok(SpiSlaveProtoHandle(ft_handle))
    else:
        return Err(result)


@overload
def init_ex(
    ft_handle: FtHandle,
    protocol: Literal[IoProtocol.NO_PROTOCOL]
) -> Result[SpiSlaveRawHandle, Ft4222Status]: ...


@overload
def init_ex(
    ft_handle: FtHandle,
    protocol: Literal[IoProtocol.WITH_PROTOCOL, IoProtocol.NO_ACK]
) -> Result[SpiSlaveProtoHandle, Ft4222Status]: ...


def init_ex(
    ft_handle: FtHandle,
    protocol: IoProtocol
) -> Union[
        Result[SpiSlaveProtoHandle, Ft4222Status],
        Result[SpiSlaveRawHandle, Ft4222Status]
]:
    """Initialize the FT4222H as an SPI slave.

    Similar to 'spi.slave.init()' function, but with parameters to define the transmission protocol.

    Args:
        ft_handle:      Handle to an open FT4222 device
        protocol:       Protocol to be used for communication (if any)

    Returns:
        Result: Handle to FT4222 device in selected protocol mode
    """
    result: Ft4222Status = _init_ex(ft_handle, protocol)

    if result == Ft4222Status.OK:
        if protocol == IoProtocol.NO_PROTOCOL:
            return Ok(SpiSlaveRawHandle(ft_handle))
        else:
            return Ok(SpiSlaveProtoHandle(ft_handle))
    else:
        return Err(result)


def set_mode(
    ft_handle: SpiSlaveHandle,
    clk_polarity: ClkPolarity,
    clk_phase: ClkPhase
) -> None:
    """Set clock polarity and phase.

    Args:
        ft_handle:          Handle to an initialized FT4222 device in SPI Slave mode
        clk_polarity:       Clock polarity (idle low/high)
        clk_phase:          Clock phase

    Raises:
        Ft4222Exception:    In case of unexpected error
    """
    result: Ft4222Status = _set_mode(
        ft_handle,
        clk_polarity,
        clk_phase
    )

    if result != Ft4222Status.OK:
        raise Ft4222Exception(result)


def get_rx_status(ft_handle: SpiSlaveHandle) -> int:
    """Get number of bytes in the receive queue.

    Args:
        ft_handle:          Handle to an initialized FT4222 device in SPI Slave mode

    Raises:
        Ft4222Exception:    In case of unexpected error

    Returns:
        int:                Number of bytes in the receive queue
    """
    rx_size = c_uint16()

    result: Ft4222Status = _get_rx_status(
        ft_handle,
        byref(rx_size)
    )

    if result != Ft4222Status.OK:
        raise Ft4222Exception(result)

    return rx_size.value


def read(ft_handle: SpiSlaveHandle, read_byte_count: int) -> bytes:
    """Read data from the receive queue of the SPI slave device.

    Args:
        ft_handle:          Handle to an initialized FT4222 device in SPI Slave mode
        read_byte_count:    Positive number of bytes to read from Rx queue

    Raises:
        Ft4222Exception:    In case of unexpected error

    Returns:
        bytes:              Read data (if any)
    """
    assert 0 < read_byte_count < (2 ** 16),\
        "Number of bytes to read must be positive and less than 2^16"

    read_buffer = (c_uint8 * read_byte_count)()
    bytes_read = c_uint16()

    result: Ft4222Status = _read(
        ft_handle,
        read_buffer,
        len(read_buffer),
        byref(bytes_read)
    )

    if result != Ft4222Status.OK:
        raise Ft4222Exception(result)

    return bytes(read_buffer[:bytes_read.value])


def write(ft_handle: SpiSlaveHandle, write_data: bytes) -> int:
    """Write data to the transmit queue of the SPI slave device.

    NOTE: For some reasons, support lib will append a dummy byte (0x00) at the first byte automatically.
    This additional byte exists at all of the three transfer methods.

    Args:
        ft_handle:          Handle to an initialized FT4222 device in SPI Slave mode
        write_data:         Non-empty list of bytes to be written into Tx queue

    Raises:
        Ft4222Exception:    In case of unexpected error

    Returns:
        int:                Number of bytes written into Tx queue
    """
    assert 0 < len(write_data) < (2 ** 16),\
        "Data to be written must be non-empty and contain less than 2^16 bytes"

    bytes_written = c_uint16()

    result: Ft4222Status = _write(
        ft_handle,
        write_data,
        len(write_data),
        byref(bytes_written)
    )

    if result != Ft4222Status.OK:
        raise Ft4222Exception(result)

    return bytes_written.value


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
        Ft4222Exception:    In case of unexpected error
    """
    result: Ft4222Status = _set_event_notification(
        ft_handle, mask.value, param)

    if result != Ft4222Status.OK:
        raise Ft4222Exception(result)
