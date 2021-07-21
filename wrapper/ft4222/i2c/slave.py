from ctypes import cdll
from ctypes import POINTER, byref
from ctypes import c_void_p, c_uint8, c_uint16, c_bool
from pathlib import Path

from typing import Final, NewType

from .. import Ft4222Exception, Ft4222Status
from ... import FtHandle, Result, Ok, Err

MODULE_PATH: Final[Path] = Path(__file__).parent

try:
    ftlib = cdll.LoadLibrary(
        str(MODULE_PATH / '..' / '..' / 'dlls' / 'libft4222.so.1.4.4.44'))
except OSError as e:
    print("Unable to load shared library!")
    exit(1)

I2cSlaveHandle = NewType('I2cSlaveHandle', c_void_p)

# Function prototypes

_init = ftlib.FT4222_I2CSlave_Init
_init.argtypes = [c_void_p]
_init.restype = Ft4222Status

_reset = ftlib.FT4222_I2CSlave_Reset
_reset.argtypes = [c_void_p]
_reset.restype = Ft4222Status

_get_address = ftlib.FT4222_I2CSlave_GetAddress
_get_address.argtypes = [c_void_p, POINTER(c_uint8)]
_get_address.restype = Ft4222Status

_set_address = ftlib.FT4222_I2CSlave_SetAddress
_set_address.argtypes = [c_void_p, c_uint8]
_set_address.restype = Ft4222Status

_get_rx_status = ftlib.FT4222_I2CSlave_GetRxStatus
_get_rx_status.argtypes = [c_void_p, POINTER(c_uint16)]
_get_rx_status.restype = Ft4222Status

_read = ftlib.FT4222_I2CSlave_Read
_read.argtypes = [c_void_p, POINTER(
    c_uint8), c_uint16, POINTER(c_uint16)]
_read.restype = Ft4222Status

_write = ftlib.FT4222_I2CSlave_Write
_write.argtypes = [c_void_p, POINTER(
    c_uint8), c_uint16, POINTER(c_uint16)]
_write.restype = Ft4222Status

_set_clock_stretch = ftlib.FT4222_I2CSlave_SetClockStretch
_set_clock_stretch.argtypes = [c_void_p, c_bool]
_set_clock_stretch.restype = Ft4222Status

_set_resp_word = ftlib.FT4222_I2CSlave_SetRespWord
_set_resp_word.argtypes = [c_void_p, c_uint8]
_set_resp_word.restype = Ft4222Status


def init(ft_handle: FtHandle) -> Result[I2cSlaveHandle, Ft4222Status]:
    """Initialized FT4222H as an I2C slave.

    After initialization, the I2C slave address is set to 0x40.

    Args:
        ft_handle:      Handle to an opened FT4222 device

    Returns:
        Result:         Handle to initialized FT4222 device in I2C Slave mode
    """
    result: Ft4222Status = _init(ft_handle)

    if result == Ft4222Status.OK:
        return Ok(I2cSlaveHandle(ft_handle))
    else:
        return Err(result)


def reset(ft_handle: I2cSlaveHandle) -> None:
    """Reset the I2C slave device.

    This function will maintain the original i2c slave setting and clear all cache in the device.

    Args:
        ft_handle:      Handle to an initialized FT4222 device in I2C Slave mode

    Raises:
        Ft4222Exception:    In case of unexpected error
    """
    result: Ft4222Status = _reset(ft_handle)

    if result != Ft4222Status.OK:
        raise Ft4222Exception(result)


def get_address(ft_handle: I2cSlaveHandle) -> int:
    """Get the address of the I2C slave device.

    Default address is 0x40.

    Args:
        ft_handle:      Handle to an initialized FT4222 device in I2C Slave mode

    Raises:
        Ft4222Exception:    In case of unexpected error

    Returns:
        int:            Current I2C slave address
    """
    addr = c_uint8()

    result: Ft4222Status = _get_address(
        ft_handle, byref(addr))

    if result != Ft4222Status.OK:
        raise Ft4222Exception(result)

    return addr.value


def set_address(ft_handle: I2cSlaveHandle, addr: int) -> None:
    """Set the address of the I2C slave device.

    Args:
        ft_handle:      Handle to an initialized FT4222 device in I2C Slave mode
        addr:           Address to be set

    Raises:
        Ft4222Exception:    In case of unexpected error
    """
    result: Ft4222Status = _set_address(ft_handle, addr)

    if result != Ft4222Status.OK:
        raise Ft4222Exception(result)


def get_rx_status(ft_handle: I2cSlaveHandle) -> int:
    """Get number of bytes in the receive queue.

    Args:
        ft_handle:      Handle to an initialized FT4222 device in I2C Slave mode

    Raises:
        Ft4222Exception:    In case of unexpected error

    Returns:
        int:            Number of bytes in Rx queue
    """
    rx_size = c_uint16()

    result: Ft4222Status = _get_rx_status(
        ft_handle, byref(rx_size))

    if result != Ft4222Status.OK:
        raise Ft4222Exception(result)

    return rx_size.value


def read(ft_handle: I2cSlaveHandle, read_byte_count: int) -> bytes:
    """Read data from the buffer of the I2C slave device.

    Args:
        ft_handle:          Handle to an initialized FT4222 device in I2C Slave mode
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
        read_buffer,
        len(read_buffer),
        byref(bytes_read)
    )

    if result != Ft4222Status.OK:
        raise Ft4222Exception(result)

    return bytes(read_buffer[:bytes_read.value])


def write(ft_handle: I2cSlaveHandle, write_data: bytes) -> int:
    """Write data to the buffer of I2C slave device.

    Args:
        ft_handle:      Handle to an initialized FT4222 device in I2C Slave mode
        write_data:     Data to write into Tx queue

    Raises:
        Ft4222Exception:    In case of unexpected error

    Returns:
        int:            Number of bytes written
    """
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


def set_clock_stretch(ft_handle: I2cSlaveHandle, enable: bool) -> None:
    """Enable or disable Clock Stretch.

    The default setting of clock stretching is disabled.

    Clock stretch is as a flow-control mechanism for slaves.
    An addressed slave device may hold the clock line (SCL) low after receiving (or sending) a byte,
    indicating that it is not yet ready to process more data.
    The master that is communicating with the slave may not finish the transmission of the current bit,
    but must wait until the clock line actually goes high.

    Args:
        ft_handle:      Handle to an initialized FT4222 device in I2C Slave mode
        enable:         Enable clock stretching?

    Raises:
        Ft4222Exception:    In case of unexpected error
    """
    result: Ft4222Status = _set_clock_stretch(
        ft_handle, enable)

    if result != Ft4222Status.OK:
        raise Ft4222Exception(result)


def set_resp_word(ft_handle: I2cSlaveHandle, response_word: int) -> None:
    """Set the response word in case of empty Tx queue.

    Default value is 0xFF.

    This function only takes effect when Clock Stretch is disabled.
    When data is requested by an I2C master and the device is not ready to respond,
    the device will respond with a default value.

    Args:
        ft_handle:      Handle to an initialized FT4222 device in I2C Slave mode
        response_word:  Response word to be set

    Raises:
        Ft4222Exception:    In case of unexpected error
    """
    result: Ft4222Status = _set_resp_word(
        ft_handle, response_word)

    if result != Ft4222Status.OK:
        raise Ft4222Exception(result)
