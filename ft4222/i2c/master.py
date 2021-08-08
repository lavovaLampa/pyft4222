from typing import Optional

from wrapper import FtHandle
from wrapper.ft4222 import Ft4222Exception, Ft4222Status
from wrapper.ft4222.common import uninitialize
from wrapper.ft4222.i2c.master import I2cMasterHandle, Status, TransactionFlag
from wrapper.ft4222.i2c.master import get_status, read, read_ex, reset, reset_bus, write, write_ex


class I2CMaster:
    _handle: Optional[I2cMasterHandle]

    def __init__(self, ft_handle: I2cMasterHandle):
        self._handle = ft_handle

    def read(self, dev_address: int, read_byte_count: int) -> bytes:
        if self._handle is not None:
            return read(self._handle, dev_address, read_byte_count)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "I2C Master has been uninitialized!"
            )

    def write(self, dev_address: int, write_data: bytes) -> int:
        if self._handle is not None:
            return write(self._handle, dev_address, write_data)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "I2C Master has been uninitialized!"
            )

    def read_ex(
        self,
        dev_address: int,
        flag: TransactionFlag,
        read_byte_count: int
    ) -> bytes:
        if self._handle is not None:
            return read_ex(self._handle, dev_address, flag, read_byte_count)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "I2C Master has been uninitialized!"
            )

    def write_ex(
        self,
        dev_address: int,
        flag: TransactionFlag,
        write_data: bytes
    ) -> int:
        if self._handle is not None:
            return write_ex(self._handle, dev_address, flag, write_data)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "I2C Master has been uninitialized!"
            )

    def get_status(self) -> Status:
        if self._handle is not None:
            return get_status(self._handle)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "I2C Master has been uninitialized!"
            )

    def reset(self) -> None:
        if self._handle is not None:
            reset(self._handle)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "I2C Master has been uninitialized!"
            )

    def reset_bus(self) -> None:
        if self._handle is not None:
            reset_bus(self._handle)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "I2C Master has been uninitialized!"
            )

    def uninitialize(self) -> FtHandle:
        if self._handle is not None:
            handle = self._handle
            self._handle = None
            return uninitialize(handle)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "I2C Master has been uninitialized already!"
            )
