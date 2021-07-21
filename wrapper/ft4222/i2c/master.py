from ctypes import cdll
from ctypes import POINTER, byref
from ctypes import c_void_p, c_uint32, c_uint8, c_uint16

from enum import IntEnum, IntFlag
from pathlib import Path
from typing import Final, NewType

from .. import Ft4222Status, Ft4222Exception
from ... import FtHandle, Result, Ok, Err

MODULE_PATH: Final[Path] = Path(__file__).parent

try:
    ftlib = cdll.LoadLibrary(
        str(MODULE_PATH / '..' / '..' / 'dlls' / 'libft4222.so.1.4.4.44'))
except OSError as e:
    print("Unable to load shared library!")
    exit(1)

I2cMasterHandle = NewType('I2cMasterHandle', c_void_p)


class TransactionFlag(IntEnum):
    NONE = 0x80
    START = 0x02
    REPEATED_START = 0x03  # Repeated_START will not send master code in HS mode
    STOP = 0x04
    START_AND_STOP = 0x06  # START condition followed by SEND and STOP condition


class Status(IntFlag):
    CONTROLLER_BUSY = 1 << 0    # Controller busy; all other status bits are invalid
    ERROR = 1 << 1              # Error condition
    SLAVE_ADDR_NACK = 1 << 2    # Slave address was not acknowledged during last operation
    DATA_NACK = 1 << 3          # Data not acknowledged during last operation
    ARBITRATION_LOST = 1 << 4   # Arbitration lost during last operation
    IDLE = 1 << 5               # Controller idle
    BUS_BUSY = 1 << 6           # Bus busy


_init = ftlib.FT4222_I2CMaster_Init
_init.argtypes = [c_void_p, c_uint32]
_init.restype = Ft4222Status

_read = ftlib.FT4222_I2CMaster_Read
_read.argtypes = [c_void_p, c_uint16, POINTER(
    c_uint8), c_uint16, POINTER(c_uint16)]
_read.restype = Ft4222Status

_write = ftlib.FT4222_I2CMaster_Write
_write.argtypes = [c_void_p, c_uint16, POINTER(
    c_uint8), c_uint16, POINTER(c_uint16)]
_write.restype = Ft4222Status

_read_ex = ftlib.FT4222_I2CMaster_ReadEx
_read_ex.argtypes = [c_void_p, c_uint16, c_uint8,
                     POINTER(c_uint8), c_uint16, POINTER(c_uint16)]
_read_ex.restype = Ft4222Status

_write_ex = ftlib.FT4222_I2CMaster_WriteEx
_write_ex.argtypes = [c_void_p, c_uint16, c_uint8,
                      POINTER(c_uint8), c_uint16, POINTER(c_uint16)]
_write_ex.restype = Ft4222Status

_reset = ftlib.FT4222_I2CMaster_Reset
_reset.argtypes = [c_void_p]
_reset.restype = Ft4222Status

_get_status = ftlib.FT4222_I2CMaster_GetStatus
_get_status.argtypes = [c_void_p, POINTER(c_uint8)]
_get_status.restype = Ft4222Status

_reset_bus = ftlib.FT4222_I2CMaster_ResetBus
_reset_bus.argtypes = [c_void_p]
_reset_bus.restype = Ft4222Status


# FIXME: Check kbps typing?
def init(ft_handle: FtHandle, kbps: int) -> Result[I2cMasterHandle, Ft4222Status]:
    """Initialize the FT4222H as an I2C master with the requested I2C speed. 

    Args:
        ft_handle:          Handle to an opened FT4222 device
        kbps:               I2C transmission speed (60K - 3400K)

    Returns:
        Result:    Handle to initialized FT4222 device in I2C Master mode
    """
    result: Ft4222Status = _init(
        ft_handle,
        kbps
    )

    if result == Ft4222Status.OK:
        return Ok(I2cMasterHandle(ft_handle))
    else:
        return Err(result)


def read(
    ft_handle: I2cMasterHandle,
    dev_address: int,
    read_byte_count: int
) -> bytes:
    """Read data from the specified I2C slave device with START and STOP conditions.

    Args:
        ft_handle:          Handle to an initialized FT4222 device in I2C Master mode
        dev_address:        Address of the target I2C slave
        read_byte_count:    Number of bytes to read

    Raises:
        Ft4222Exception:    In case of unexpected error

    Returns:
        bytes:              Read data
    """
    read_buffer = (c_uint8 * read_byte_count)()
    bytes_read = c_uint16()

    result: Ft4222Status = _read(
        ft_handle,
        dev_address,
        read_buffer,
        len(read_buffer),
        byref(bytes_read)
    )

    if result != Ft4222Status.OK:
        raise Ft4222Exception(result)

    return bytes(read_buffer[:bytes_read.value])


def write(
    ft_handle: I2cMasterHandle,
    dev_address: int,
    write_data: bytes
) -> int:
    """Write data to the specified I2C slave device with START and STOP conditions.

    Args:
        ft_handle:      Handle to an initialized FT4222 device in I2C Master mode
        dev_address:    Address of the target I2C slave
        write_data:     Data to write

    Raises:
        Ft4222Exception:    In case of unexpected error

    Returns:
        int:            Number of bytes written
    """
    bytes_written = c_uint16()

    result: Ft4222Status = _write(
        ft_handle,
        dev_address,
        write_data,
        len(write_data),
        byref(bytes_written)
    )

    if result != Ft4222Status.OK:
        raise Ft4222Exception(result)

    return bytes_written.value


def read_ex(
    ft_handle: I2cMasterHandle,
    dev_address: int,
    flag: TransactionFlag,
    read_byte_count: int
) -> bytes:
    """Read data from the specified I2C slave device with the specified I2C condition.

    NOTE: This function is supported by the rev. B FT4222H or later!

    Args:
        ft_handle:          Handle to an initialized FT4222 device in SPI Master mode
        dev_address:        Address of target I2C slave device
        flag:               I2C transaction condition flag
        read_byte_count:    Number of bytes to read

    Raises:
        Ft4222Exception:    In case of unexpected error

    Returns:
        bytes:              Read data
    """
    read_buffer = (c_uint8 * read_byte_count)()
    bytes_read = c_uint16()

    result: Ft4222Status = _read_ex(
        ft_handle,
        dev_address,
        flag,
        read_buffer,
        len(read_buffer),
        byref(bytes_read)
    )

    if result != Ft4222Status.OK:
        raise Ft4222Exception(result)

    return bytes(read_buffer[:bytes_read.value])


def write_ex(
    ft_handle: I2cMasterHandle,
    dev_address: int,
    flag: TransactionFlag,
    write_data: bytes
) -> int:
    """Write data to a specified I2C slave device with the specified I2C condition.

    NOTE: This function is supported by the rev. B FT4222H or later!

    Args:
        ft_handle:      Handle to an initialized FT4222 device in I2C Master mode
        dev_address:    Address of target I2C slave device
        flag:           I2C transaction condition flag
        write_data:     Data to write

    Raises:
        Ft4222Exception:    In case of unexpected error

    Returns:
        int:            Number of bytes written
    """
    bytes_written = c_uint16()

    result: Ft4222Status = _write_ex(
        ft_handle,
        dev_address,
        flag,
        write_data,
        len(write_data),
        byref(bytes_written)
    )

    if result != Ft4222Status.OK:
        raise Ft4222Exception(result)

    return bytes_written.value


def reset(ft_handle: I2cMasterHandle) -> None:
    """Reset the I2C master device.

    If the I2C bus encounters errors or works abnormally, this function will reset the I2C device.
    It is not necessary to call 'I2C.Master.Init()' again after calling this reset function.
    This function will maintain the original I2C master setting and clear all cache in the device.

    Args:
        ft_handle:      Handle to an initialized FT4222 device in I2C Master mode

    Raises:
        Ft4222Exception:    In case of unexpected error
    """
    result: Ft4222Status = _reset(ft_handle)

    if result != Ft4222Status.OK:
        raise Ft4222Exception(result)


def get_status(ft_handle: I2cMasterHandle) -> Status:
    """Read the status of the I2C master controller.

    This can be used to poll a slave after I2C transmission is complete.

    Args:
        ft_handle:          Handle to an initialized FT4222 device in I2C Master mode

    Raises:
        Ft4222Exception:    In case of unexpected error

    Returns:
        Status:  Controller status
    """
    status = c_uint8()

    result: Ft4222Status = _get_status(
        ft_handle, byref(status))

    if result != Ft4222Status.OK:
        raise Ft4222Exception(result)

    return Status(status.value)


def reset_bus(ft_handle: I2cMasterHandle) -> None:
    """Reset I2C bus.

    If the data line (SDA) is stuck LOW by the slave device, this function will make the master send nine SCK clocks to recover the I2C bus.
    The slave device that held the data line (SDA) LOW will release it within these nine clocks.
    If not, then use the HW reset or cycle power to clear the bus.

    Args:
        ft_handle:      Handle to an initialized FT4222 device in I2C Master mode

    Raises:
        Ft4222Exception:    In case of unexpected error
    """
    result: Ft4222Status = _reset_bus(ft_handle)

    if result != Ft4222Status.OK:
        raise Ft4222Exception(result)
