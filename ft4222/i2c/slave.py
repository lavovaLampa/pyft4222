from typing import Optional
from wrapper.ft4222.common import uninitialize
from wrapper.ft4222 import Ft4222Exception, Ft4222Status
from wrapper import FtHandle

from wrapper.ft4222.i2c.slave import I2cSlaveHandle, get_address, get_rx_status, read, reset, set_address, set_clock_stretch, set_resp_word, write


class I2CSlave:
    _handle: Optional[I2cSlaveHandle]

    def __init__(self, ft_handle: I2cSlaveHandle):
        self._handle = ft_handle

    def reset(self) -> None:
        if self._handle is not None:
            reset(self._handle)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "I2C Slave has been uninitialized!"
            )

    def get_address(self) -> int:
        if self._handle is not None:
            return get_address(self._handle)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "I2C Slave has been uninitialized!"
            )

    def set_address(self, addr: int) -> None:
        if self._handle is not None:
            set_address(self._handle, addr)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "I2C Slave has been uninitialized!"
            )

    def get_rx_status(self) -> int:
        if self._handle is not None:
            return get_rx_status(self._handle)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "I2C Slave has been uninitialized!"
            )

    def read(self, read_byte_count: int) -> bytes:
        if self._handle is not None:
            return read(self._handle, read_byte_count)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "I2C Slave has been uninitialized!"
            )

    def write(self, write_data: bytes) -> int:
        if self._handle is not None:
            return write(self._handle, write_data)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "I2C Slave has been uninitialized!"
            )

    def set_clock_stretch(self, enable: bool) -> None:
        if self._handle is not None:
            set_clock_stretch(self._handle, enable)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "I2C Slave has been uninitialized!"
            )

    def set_resp_word(self, response_word: int) -> None:
        if self._handle is not None:
            set_resp_word(self._handle, response_word)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "I2C Slave has been uninitialized!"
            )

    def uninitialize(self) -> FtHandle:
        if self._handle is not None:
            handle = self._handle
            self._handle = None
            return uninitialize(handle)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "I2C Slave has been uninitialized!"
            )
