from ctypes import c_void_p
from typing import Optional, Union
from wrapper.ft4222.common import uninitialize

from wrapper.ft4222.spi import ClkPhase, ClkPolarity, DriveStrength
from wrapper.ft4222 import Ft4222Exception, Ft4222Status
from wrapper.ft4222.spi.common import TransactionIdx, reset, reset_transaction, set_driving_strength
from wrapper import FtHandle

from wrapper.ft4222.spi.slave import EventType, SpiSlaveHandle, SpiSlaveProtoHandle, get_rx_status, read, set_mode, write


class SpiSlaveCommon():
    _handle: Optional[SpiSlaveHandle]

    def reset_bus(self) -> None:
        if self._handle is not None:
            reset(self._handle)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "SPI Slave has been uninitialized!"
            )

    def reset_transaction(self, transaction_idx: TransactionIdx) -> None:
        if self._handle is not None:
            reset_transaction(self._handle, transaction_idx)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "SPI Slave has been uninitialized!"
            )

    def set_driving_strength(
        self,
        clk_strength: DriveStrength,
        io_strength: DriveStrength,
        sso_strength: DriveStrength
    ) -> None:
        if self._handle is not None:
            set_driving_strength(
                self._handle,
                clk_strength,
                io_strength,
                sso_strength
            )
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "SPI Slave has been uninitialized!"
            )

    def set_mode(self, clk_polarity: ClkPolarity, clk_phase: ClkPhase) -> None:
        if self._handle is not None:
            set_mode(self._handle, clk_polarity, clk_phase)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "SPI Slave has been uninitialized!"
            )

    def get_rx_status(self) -> int:
        if self._handle is not None:
            return get_rx_status(self._handle)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "SPI Slave has been uninitialized!"
            )

    def read(self, read_byte_count: int) -> bytes:
        if self._handle is not None:
            return read(self._handle, read_byte_count)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "SPI Slave has been uninitialized!"
            )

    def write(self, write_data: bytes) -> int:
        if self._handle is not None:
            return write(self._handle, write_data)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "SPI Slave has been uninitialized!"
            )

    def uninitialize(self) -> FtHandle:
        if self._handle is not None:
            handle = self._handle
            self._handle = None
            return uninitialize(handle)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "SPI Slave has been uninitialized already!"
            )


class SpiSlaveProto(SpiSlaveCommon):
    _handle: Optional[SpiSlaveProtoHandle]

    def __init__(self, ft_handle: SpiSlaveProtoHandle):
        self._handle = ft_handle

    # FIXME: Proper typing
    def set_event_notification(self, mask: EventType, param: c_void_p) -> None:
        pass


SpiSlave = Union[SpiSlaveProto, SpiSlaveCommon]
