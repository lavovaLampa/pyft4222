from ctypes import POINTER, byref, c_char_p
from ctypes import c_void_p, c_uint, c_uint8, c_uint16, c_bool, c_uint32

from enum import IntEnum, IntFlag, auto
from typing import Literal, NewType, Optional, Union, overload

from . import ClkPhase, ClkPolarity
from .. import FtHandle, Result, Ok, Err, Ft4222Status, Ft4222Exception
from ..dll_loader import ftlib

SpiMasterSingleHandle = NewType("SpiMasterSingleHandle", FtHandle)
SpiMasterMultiHandle = NewType("SpiMasterMultiHandle", FtHandle)
SpiMasterHandle = Union[SpiMasterSingleHandle, SpiMasterMultiHandle]


class IoMode(IntEnum):
    """Enum representing possible SPI data I/O modes/counts."""

    SINGLE = 1
    """Data are transferred full-duplex using MISO/MOSI lines."""
    DUAL = 2
    """Data are transferred half-duplex using MISO, MOSI lines (bit0, bit1)."""
    QUAD = 4
    """Data are transferred half-duples using
    MISO, MOSI, IO2, IO3 lines (bit0, bit1, bit2, bit3).
    """


class ClkDiv(IntEnum):
    """Enum representing possible clock divisors in SPI Master mode."""

    CLK_NONE = 0
    CLK_DIV_2 = auto()  # 1/2   System Clock
    CLK_DIV_4 = auto()  # 1/4   System Clock
    CLK_DIV_8 = auto()  # 1/8   System Clock
    CLK_DIV_16 = auto()  # 1/16  System Clock
    CLK_DIV_32 = auto()  # 1/32  System Clock
    CLK_DIV_64 = auto()  # 1/64  System Clock
    CLK_DIV_128 = auto()  # 1/128 System Clock
    CLK_DIV_256 = auto()  # 1/256 System Clock
    CLK_DIV_512 = auto()  # 1/512 System Clock


class CsPolarity(IntEnum):
    """Enum representing possible chip_select signal polarities."""

    ACTIVE_LOW = 0
    """Active-low chip select (DEFAULT)."""
    ACTIVE_HIGH = auto()
    """Active-high chip select."""


class SsoMap(IntFlag):
    """Enum representing a slave select mapping flag."""

    SS_0 = 1
    SS_1 = 2
    SS_2 = 4
    SS_3 = 8


_init = ftlib.FT4222_SPIMaster_Init
_init.argtypes = [c_void_p, c_uint, c_uint, c_uint, c_uint, c_uint8]
_init.restype = Ft4222Status

_set_cs = ftlib.FT4222_SPIMaster_SetCS
_set_cs.argtypes = [c_void_p, c_uint]
_set_cs.restype = Ft4222Status

_set_lines = ftlib.FT4222_SPIMaster_SetLines
_set_lines.argtypes = [c_void_p, c_uint]
_set_lines.restype = Ft4222Status

_single_read = ftlib.FT4222_SPIMaster_SingleRead
_single_read.argtypes = [
    c_void_p,
    POINTER(c_uint8),
    c_uint16,
    POINTER(c_uint16),
    c_bool,
]
_single_read.restype = Ft4222Status

_single_write = ftlib.FT4222_SPIMaster_SingleWrite
_single_write.argtypes = [c_void_p, c_char_p, c_uint16, POINTER(c_uint16), c_bool]
_single_write.restype = Ft4222Status

_single_read_write = ftlib.FT4222_SPIMaster_SingleReadWrite
_single_read_write.argtypes = [
    c_void_p,
    POINTER(c_uint8),
    c_char_p,
    c_uint16,
    POINTER(c_uint16),
    c_bool,
]
_single_read_write.restype = Ft4222Status

_multi_read_write = ftlib.FT4222_SPIMaster_MultiReadWrite
_multi_read_write.argtypes = [
    c_void_p,
    POINTER(c_uint8),
    POINTER(c_uint8),
    c_uint8,
    c_uint16,
    c_uint16,
    POINTER(c_uint32),
]
_multi_read_write.restype = Ft4222Status


@overload
def init(
    ft_handle: FtHandle,
    io_mode: Literal[IoMode.SINGLE],
    clock_div: ClkDiv,
    clk_polarity: ClkPolarity,
    clk_phase: ClkPhase,
    sso_map: SsoMap,
) -> Result[SpiMasterSingleHandle, Ft4222Status]:
    ...


@overload
def init(
    ft_handle: FtHandle,
    io_mode: Union[Literal[IoMode.DUAL], Literal[IoMode.QUAD]],
    clock_div: ClkDiv,
    clk_polarity: ClkPolarity,
    clk_phase: ClkPhase,
    sso_map: SsoMap,
) -> Result[SpiMasterMultiHandle, Ft4222Status]:
    ...


@overload
def init(
    ft_handle: FtHandle,
    io_mode: IoMode,
    clock_div: ClkDiv,
    clk_polarity: ClkPolarity,
    clk_phase: ClkPhase,
    sso_map: SsoMap,
) -> Union[
    Result[SpiMasterSingleHandle, Ft4222Status],
    Result[SpiMasterMultiHandle, Ft4222Status],
]:
    ...


def init(
    ft_handle: FtHandle,
    io_mode: IoMode,
    clock_div: ClkDiv,
    clk_polarity: ClkPolarity,
    clk_phase: ClkPhase,
    sso_map: SsoMap,
) -> Union[
    Result[SpiMasterSingleHandle, Ft4222Status],
    Result[SpiMasterMultiHandle, Ft4222Status],
]:
    """Initialize the FT4222H as an SPI master.

    Args:
        ft_handle:      Handle to an open FT4222 device
        io_mode:        Data transmission mode (single, dual, quad)
        clock_div:      SPI clock rate division ratio (spi_clock = (sys_clk / clock_div))
        clk_polarity:   Clock polarity (idle low/high)
        clk_phase:      Clock phase (data sampled on the leading [first] or trailing [second] clock edge)
        sso_map:        Slave selection output pin map

    Returns:
        Result:         Handle to initialized SPI Master FT4222 device
    """
    result: Ft4222Status = _init(
        ft_handle, io_mode, clock_div, clk_polarity, clk_phase, sso_map
    )

    if result == Ft4222Status.OK:
        if io_mode == IoMode.SINGLE:
            return Ok(SpiMasterSingleHandle(ft_handle))
        elif io_mode in {IoMode.DUAL, IoMode.QUAD}:
            return Ok(SpiMasterMultiHandle(ft_handle))
        else:
            return Err(result)
    else:
        return Err(result)


def set_cs_polarity(ft_handle: SpiMasterHandle, cs_polarity: CsPolarity) -> None:
    """Change polarity of chip select signal.

    Default chip select is active low.

    Args:
        ft_handle:      Handle to an initialized FT4222 device in SPI Master mode
        cs_polarity:    Polarity of chip select signal

    Raises:
        Ft4222Exception:    In case of unexpected error
    """
    result: Ft4222Status = _set_cs(ft_handle, cs_polarity)

    if result != Ft4222Status.OK:
        raise Ft4222Exception(result)


@overload
def set_lines(
    ft_handle: SpiMasterHandle, io_mode: Literal[IoMode.SINGLE]
) -> SpiMasterSingleHandle:
    ...


@overload
def set_lines(
    ft_handle: SpiMasterHandle, io_mode: Literal[IoMode.DUAL, IoMode.QUAD]
) -> SpiMasterMultiHandle:
    ...


@overload
def set_lines(ft_handle: SpiMasterHandle, io_mode: IoMode) -> SpiMasterHandle:
    ...


def set_lines(ft_handle: SpiMasterHandle, io_mode: IoMode) -> SpiMasterHandle:
    """Switch the FT4222H SPI Master to single, dual, or quad mode.

    This overrides the mode passed to 'SPI.Master.init()' function.
    This might be needed if a device accepts commands in single mode but data transfer is using dual or quad mode.

    Args:
        ft_handle:  Handle to an initialized FT4222 device in SPI Master mode
        io_mode:    Desired IO mode (single, dual, quad)

    Raises:
        Ft4222Exception:    In case of unexpected error

    Returns:
        SpiMasterHandle:    Handle to an initialized FT4222 device in SPI Master mode with selected io setting
    """
    result: Ft4222Status = _set_lines(ft_handle, io_mode)

    if result != Ft4222Status.OK:
        raise Ft4222Exception(result)

    if io_mode == IoMode.SINGLE:
        return SpiMasterSingleHandle(ft_handle)
    elif io_mode in [IoMode.DUAL, IoMode.QUAD]:
        return SpiMasterMultiHandle(ft_handle)
    else:
        raise Ft4222Exception(result, "Invalid IoMode! Cannot use 'IoMode.NONE'.")


def single_read(
    ft_handle: SpiMasterSingleHandle, read_byte_count: int, end_transaction: bool = True
) -> bytes:
    """Under SPI single mode, read data from an SPI slave.

    Args:
        ft_handle:          Handle to an initialized FT4222 device in SPI Master mode with 'IoMode.IO_SINGLE' setting
        read_byte_count:    Positive number of bytes to read
        end_transaction:    De-assert slave select pin at the end of transaction?

    Raises:
        Ft4222Exception:    In case of unexpected error

    Returns:
        bytes:              Read data (length can be lower than requested)
    """
    assert (
        0 < read_byte_count < (2 ** 16)
    ), "Number of bytes to read must be positive and less than 2^16"

    buffer = (c_uint8 * read_byte_count)()
    bytes_transferred = c_uint16()

    result: Ft4222Status = _single_read(
        ft_handle, buffer, read_byte_count, byref(bytes_transferred), end_transaction
    )

    if result != Ft4222Status.OK:
        raise Ft4222Exception(result)

    return bytes(buffer)


def single_write(
    ft_handle: SpiMasterSingleHandle, write_data: bytes, end_transaction: bool = True
) -> int:
    """Under SPI single mode, write data to an SPI slave.

    Args:
        ft_handle:          Handle to an initialized FT4222 device in SPI Master mode with 'IoMode.IO_SINGLE' setting
        write_data:         Non-empty list of bytes to be written
        end_transaction:    De-assert slave select pin at the end of transaction?

    Raises:
        Ft4222Exception:    In case of unexpected error

    Returns:
        int:                Number of transmitted bytes
    """
    assert (
        0 < len(write_data) < (2 ** 16)
    ), "Data to be written must be non-empty and contain less than 2^16 bytes"

    bytes_transferred = c_uint16()
    result: Ft4222Status = _single_write(
        ft_handle,
        write_data,
        len(write_data),
        byref(bytes_transferred),
        end_transaction,
    )

    if result != Ft4222Status.OK:
        raise Ft4222Exception(result)

    return bytes_transferred.value


def single_read_write(
    ft_handle: SpiMasterSingleHandle, write_data: bytes, end_transaction: bool = True
) -> bytes:
    """Under SPI single mode, full-duplex write data to and read data from an SPI slave.

    Args:
        ft_handle:          Handle to an initialized FT4222 device in SPI Master mode with 'IoMode.IO_SINGLE' setting
        write_data:         Non-empty list of data to be written
        end_transaction:    De-assert slave select pin at the end of transaction?

    Raises:
        Ft4222Exception:    In case of unexpected error

    Returns:
        bytes:              Received data
    """
    assert (
        0 < len(write_data) < (2 ** 16)
    ), "Data to be written must be non-empty and contain less than 2^16 bytes"

    bytes_transferred = c_uint16()
    read_buffer = (c_uint8 * len(write_data))()

    result: Ft4222Status = _single_read_write(
        ft_handle,
        read_buffer,
        write_data,
        len(write_data),
        byref(bytes_transferred),
        end_transaction,
    )

    if result != Ft4222Status.OK:
        raise Ft4222Exception(result)

    return bytes(read_buffer)


def multi_read_write(
    ft_handle: SpiMasterMultiHandle,
    write_data: Optional[bytes],
    single_write_byte_count: int,
    multi_write_byte_count: int,
    multi_read_byte_count: int,
) -> bytes:
    """Under SPI dual or quad mode, write data to and read data from an SPI slave.

    It is a mixed protocol initiated with a single write transmission,
    which may be an SPI command and dummy cycles,
    and followed by multi-io-write and multi-io-read transmission that use 2/4 signals in parallel for the data.
    All three parts of the protocol are optional.

    Args:
        ft_handle:                  Handle to an initialized FT4222 device in SPI Master mode with 'IoMode.IO_DUAL' or 'IoMode'IO_QUAD' setting
        write_data:                 Data to be written
        single_write_byte_count:    Number of bytes to be written out using single IO line      (1st phase)
        multi_write_byte_count:     Number of bytes to be written out using multi IO lines      (2nd phase)
        multi_read_byte_count:      Number of bytes to be read using multi IO lines             (3rd phase)

    Raises:
        Ft4222Exception:            In case of unexpected error

    Returns:
        bytes:                      Read data (if any)
    """
    assert (
        0 <= single_write_byte_count < (2 ** 4)
    ), "Number of single-write bytes must be non-negative and less than 16"
    assert (
        0 <= multi_write_byte_count < (2 ** 16)
    ), "Number of multi-write bytes must be non-negative and less than 2^16 (65 536)"
    assert (
        0 <= multi_read_byte_count < (2 ** 16)
    ), "Number of multi-read bytes must be non-negative and less than 2^16 (65 536)"
    assert (
        single_write_byte_count + multi_write_byte_count + multi_read_byte_count
    ) > 0, "Total number of bytes written/read must be non-zero"
    if write_data is None:
        assert (
            single_write_byte_count + multi_write_byte_count
        ) == 0, "Number of bytes to write must be zero in case the write data are None"
    else:
        assert len(write_data) < (
            2 ** 16
        ), "Data to be written must have size less than 2^16 bytes"
        assert (single_write_byte_count + multi_write_byte_count) <= len(
            write_data
        ), "Length of data to write is longer than given data"

    read_buffer = (c_uint8 * multi_read_byte_count)()
    bytes_read = c_uint16()
    result: Ft4222Status = _multi_read_write(
        ft_handle,
        read_buffer,
        write_data,
        single_write_byte_count,
        multi_write_byte_count,
        multi_read_byte_count,
        byref(bytes_read),
    )

    if result != Ft4222Status.OK:
        raise Ft4222Exception(result)

    return bytes(read_buffer[:bytes_read])
