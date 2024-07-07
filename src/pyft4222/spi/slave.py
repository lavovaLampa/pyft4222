from abc import ABC
from ctypes import c_void_p
from typing import TypeVar, Union

from pyft4222.handle import StreamHandleType
from pyft4222.spi.common import SpiCommon
from pyft4222.wrapper import Ft4222Exception, Ft4222Status
from pyft4222.wrapper.spi import ClkPhase, ClkPolarity
from pyft4222.wrapper.spi.slave import (
    EventType,
    SpiSlaveHandle,
    SpiSlaveProtoHandle,
    SpiSlaveRawHandle,
    get_rx_status,
    read,
    set_mode,
    write,
)

SpiSlaveHandleType = TypeVar("SpiSlaveHandleType", bound=SpiSlaveHandle)


class SpiSlaveCommon(SpiCommon[SpiSlaveHandleType, StreamHandleType], ABC):
    """A class encapsulating functions common to all SPI Slave modes."""

    def set_mode(self, clk_polarity: ClkPolarity, clk_phase: ClkPhase) -> None:
        """Set SPI clock polarity and phase.

        Args:
            clk_polarity:       Clock polarity
            clk_phase:          Clock phase

        Raises:
            Ft4222Exception:    In case of unexpected error
        """
        if self._handle is None:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "SPI Slave has been uninitialized!"
            )

        set_mode(self._handle, clk_polarity, clk_phase)

    def get_rx_status(self) -> int:
        """Get number of bytes in the Rx queue.

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            int:                Number of bytes in the Rx queue
        """
        if self._handle is None:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "SPI Slave has been uninitialized!"
            )

        return get_rx_status(self._handle)

    def read(self, read_byte_count: int) -> bytes:
        """Read data from the Rx queue.

        Note:
            The FT4222 library adds a zero byte at the beginning.
            FIXME: Is this correct?

        Args:
            read_byte_count:    Number of bytes to read, length <1, 65_535>

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            bytes:              Read data
        """
        if self._handle is None:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "SPI Slave has been uninitialized!"
            )

        if 0 < read_byte_count < (2**16):
            return read(self._handle, read_byte_count)
        else:
            raise ValueError("read_byte_count must be in range <1, 65_535>.")

    def write(self, write_data: bytes) -> int:
        """Write data into Tx queue.

        Args:
            write_data:     Non-empty list of bytes to write, length <1, 65_535>

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            int:            Number of bytes written
        """
        if self._handle is None:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "SPI Slave has been uninitialized!"
            )

        if 0 < len(write_data) < (2**16):
            return write(self._handle, write_data)
        else:
            raise ValueError("write_data length must be in range <1, 65_535>.")


class SpiSlaveProto(SpiSlaveCommon[SpiSlaveProtoHandle, StreamHandleType]):
    """A class encapsulating the SPI Slave protocol mode."""

    # FIXME: Proper typing
    def set_event_notification(self, mask: EventType, param: c_void_p) -> None:
        raise NotImplementedError(
            "Unfortunately this function is yet to be implemented!"
        )
        """TODO: Implement and document"""
        pass


class SpiSlaveRaw(SpiSlaveCommon[SpiSlaveRawHandle, StreamHandleType]):
    """A class encapsulating the SPI Slave in raw mode."""


SpiSlave = Union[SpiSlaveProto[StreamHandleType], SpiSlaveRaw[StreamHandleType]]
