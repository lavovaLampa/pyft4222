from ctypes import c_void_p, cdll, POINTER, c_uint8, c_uint16, c_bool, byref
from typing import NewType
from .. import FT4222Status
from ...ft_common import FtHandle

try:
    ftlib = cdll.LoadLibrary('./lib/libft4222.so.1.4.4.44')
except OSError as e:
    print("Unable to load shared library!")
    exit(1)

I2cSlaveHandle = NewType('I2cSlaveHandle', c_void_p)

# Function prototypes

_init = ftlib.FT4222_I2CSlave_Init
_init.argtypes = [c_void_p]
_init.restype = FT4222Status

_reset = ftlib.FT4222_I2CSlave_Reset
_reset.argtypes = [c_void_p]
_reset.restype = FT4222Status

_get_address = ftlib.FT4222_I2CSlave_GetAddress
_get_address.argtypes = [c_void_p, POINTER(c_uint8)]
_get_address.restype = FT4222Status

_set_address = ftlib.FT4222_I2CSlave_SetAddress
_set_address.argtypes = [c_void_p, c_uint8]
_set_address.restype = FT4222Status

_get_rx_status = ftlib.FT4222_I2CSlave_GetRxStatus
_get_rx_status.argtypes = [c_void_p, POINTER(c_uint16)]
_get_rx_status.restype = FT4222Status

_read = ftlib.FT4222_I2CSlave_Read
_read.argtypes = [c_void_p, POINTER(
    c_uint8), c_uint16, POINTER(c_uint16)]
_read.restype = FT4222Status

_write = ftlib.FT4222_I2CSlave_Write
_write.argtypes = [c_void_p, POINTER(
    c_uint8), c_uint16, POINTER(c_uint16)]
_write.restype = FT4222Status

_set_clock_stretch = ftlib.FT4222_I2CSlave_SetClockStretch
_set_clock_stretch.argtypes = [c_void_p, c_bool]
_set_clock_stretch.restype = FT4222Status

_set_resp_word = ftlib.FT4222_I2CSlave_SetRespWord
_set_resp_word.argtypes = [c_void_p, c_uint8]
_set_resp_word.restype = FT4222Status


def init(ft_handle: FtHandle) -> I2cSlaveHandle:
    """Initialized FT4222H as an I2C slave.

    After initialization, the I2C slave address is set to 0x40.

    Args:
        ft_handle:      Handle to an opened FT4222 device

    Raises:
        RuntimeError:   TODO

    Returns:
        I2cSlaveHandle: Handle to initialized FT4222 device in I2C Slave mode
    """
    result: FT4222Status = _init(ft_handle)

    if result != FT4222Status.OK:
        raise RuntimeError('TODO')

    return I2cSlaveHandle(ft_handle)


def reset(ft_handle: I2cSlaveHandle) -> None:
    """Reset the I2C slave device.

    This function will maintain the original i2c slave setting and clear all cache in the device.

    Args:
        ft_handle:      Handle to an initialized FT4222 device in I2C Slave mode

    Raises:
        RuntimeError:    TODO
    """
    result: FT4222Status = _reset(ft_handle)

    if result != FT4222Status.OK:
        raise RuntimeError('TODO')


def get_address(ft_handle: I2cSlaveHandle) -> int:
    """Get the address of the I2C slave device.

    Default address is 0x40.

    Args:
        ft_handle:      Handle to an initialized FT4222 device in I2C Slave mode

    Raises:
        RuntimeError:   TODO

    Returns:
        int:            Current I2C slave address
    """
    addr = c_uint8()

    result: FT4222Status = _get_address(
        ft_handle, byref(addr))

    if result != FT4222Status.OK:
        raise RuntimeError('TODO')

    return addr.value


def set_address(ft_handle: I2cSlaveHandle, addr: int) -> None:
    """Set the address of the I2C slave device.

    Args:
        ft_handle:      Handle to an initialized FT4222 device in I2C Slave mode
        addr:           Address to be set

    Raises:
        RuntimeError:   TODO
    """
    result: FT4222Status = _set_address(ft_handle, addr)

    if result != FT4222Status.OK:
        raise RuntimeError('TODO')


def get_rx_status(ft_handle: I2cSlaveHandle) -> int:
    """Get number of bytes in the receive queue.

    Args:
        ft_handle:      Handle to an initialized FT4222 device in I2C Slave mode

    Raises:
        RuntimeError:   TODO

    Returns:
        int:            Number of bytes in Rx queue
    """
    rx_size = c_uint16()

    result: FT4222Status = _get_rx_status(
        ft_handle, byref(rx_size))

    if result != FT4222Status.OK:
        raise RuntimeError('TODO')

    return rx_size.value


def read(ft_handle: I2cSlaveHandle, read_byte_count: int) -> bytes:
    """Read data from the buffer of the I2C slave device.

    Args:
        ft_handle:          Handle to an initialized FT4222 device in I2C Slave mode
        read_byte_count:    Number of bytes to read

    Raises:
        RuntimeError:   TODO

    Returns:
        bytes:              Read data
    """
    read_buffer = (c_uint8 * read_byte_count)()
    bytes_read = c_uint16()

    result: FT4222Status = _read(
        ft_handle,
        read_buffer,
        len(read_buffer),
        byref(bytes_read)
    )

    if result != FT4222Status.OK:
        raise RuntimeError('TODO')

    return bytes(read_buffer[:bytes_read.value])


def write(ft_handle: I2cSlaveHandle, write_data: bytes) -> int:
    """Write data to the buffer of I2C slave device.

    Args:
        ft_handle:      Handle to an initialized FT4222 device in I2C Slave mode
        write_data:     Data to write into Tx queue

    Raises:
        RuntimeError:   TODO

    Returns:
        int:            Number of bytes written
    """
    bytes_written = c_uint16()

    result: FT4222Status = _write(
        ft_handle,
        write_data,
        len(write_data),
        byref(bytes_written)
    )

    if result != FT4222Status.OK:
        raise RuntimeError('TODO')

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
        RuntimeError:   TODO
    """
    result: FT4222Status = _set_clock_stretch(
        ft_handle, enable)

    if result != FT4222Status.OK:
        raise RuntimeError('TODO')


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
        RuntimeError:   TODO
    """
    result: FT4222Status = _set_resp_word(
        ft_handle, response_word)

    if result != FT4222Status.OK:
        raise RuntimeError('TODO')
