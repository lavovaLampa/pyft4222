from abc import ABC
from ctypes import c_void_p
from enum import Enum, auto
from typing import Any, Generic, Literal, TypeVar, Union

from pyft4222.handle import GenericProtocolHandle, StreamHandleType
from pyft4222.wrapper import Ft4222Exception, Ft4222Status
from pyft4222.wrapper.spi import ClkPhase, ClkPolarity, DriveStrength
from pyft4222.wrapper.spi.common import (
    TransactionIdx,
    reset,
    reset_transaction,
    set_driving_strength,
)
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
SpiSlaveType = TypeVar("SpiSlaveType", "SpiSlaveRaw[Any]", "SpiSlaveProto[Any]")


class SpiModeTag(Enum):
    RAW = auto()
    PROTO = auto()


class SpiSlaveCommon(
    Generic[SpiSlaveHandleType, SpiSlaveType, StreamHandleType],
    GenericProtocolHandle[SpiSlaveHandleType, SpiSlaveType, StreamHandleType],
    ABC,
):
    """A class encapsulating functions common to all SPI Slave modes."""

    def __init__(self, ft_handle: SpiSlaveHandleType, stream_handle: StreamHandleType):
        """Initialize the class with given FT4222 handle and a mode class type.

        Args:
            ft_handle:      FT4222 handle initialized in any SPI Slave mode
            stream_handle:  Calling stream mode handle. Used in 'uninitialize()' method.
        """
        super().__init__(ft_handle, stream_handle)

    # FIXME: De-duplicate with SPI Master
    def reset_bus(self) -> None:
        """Reset the SPI bus.

        It is not necessary to initialize the SPI Master again.
        The chip retains all settings.

        Raises:
            Ft4222Exception:    In case of unexpected error
        """
        if self._handle is not None:
            reset(self._handle)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "SPI Slave has been uninitialized!"
            )

    # FIXME: De-duplicate with SPI Master
    def reset_transaction(self, transaction_idx: TransactionIdx) -> None:
        """Purge transmit and received buffers, reset transaction state.

        Args:
            transaction_idx:    Index of SPI transaction (0 to 3),
            depending on the mode of the chip.

        Raises:
            Ft4222Exception:    In case of unexpected error
        """
        if self._handle is not None:
            reset_transaction(self._handle, transaction_idx)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "SPI Slave has been uninitialized!"
            )

    # FIXME: De-duplicate with SPI Master
    def set_driving_strength(
        self,
        clk_strength: DriveStrength,
        io_strength: DriveStrength,
        sso_strength: DriveStrength,
    ) -> None:
        """Set driving strength of clk, io and sso pins.

        Note:
            Default driving strength is 4mA.

        Args:
            clk_strength:   Driving strength of the clk pin
            io_strength:    Driving strength of the I/O pins (MISO, MOSI, IO2, IO3)
            sso_strength:   Driving strength of the slave select pins (SSO0, SSO1, SSO2, SSO3)

        Raises:
            Ft4222Exception:    In case of unexpected error
        """
        if self._handle is not None:
            set_driving_strength(self._handle, clk_strength, io_strength, sso_strength)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "SPI Slave has been uninitialized!"
            )

    def set_mode(self, clk_polarity: ClkPolarity, clk_phase: ClkPhase) -> None:
        """Set SPI clock polarity and phase.

        Args:
            clk_polarity:       Clock polarity
            clk_phase:          Clock phase

        Raises:
            Ft4222Exception:    In case of unexpected error
        """
        if self._handle is not None:
            set_mode(self._handle, clk_polarity, clk_phase)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "SPI Slave has been uninitialized!"
            )

    def get_rx_status(self) -> int:
        """Get number of bytes in the Rx queue.

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            int:                Number of bytes in the Rx queue
        """
        if self._handle is not None:
            return get_rx_status(self._handle)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "SPI Slave has been uninitialized!"
            )

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
        if self._handle is not None:
            if 0 < read_byte_count < (2 ** 16):
                return read(self._handle, read_byte_count)
            else:
                raise ValueError("read_byte_count must be in range <1, 65_535>.")
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "SPI Slave has been uninitialized!"
            )

    def write(self, write_data: bytes) -> int:
        """Write data into Tx queue.

        Args:
            write_data:     Non-empty list of bytes to write, length <1, 65_535>

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            int:            Number of bytes written
        """
        if self._handle is not None:
            if 0 < len(write_data) < (2 ** 16):
                return write(self._handle, write_data)
            else:
                raise ValueError("write_data length must be in range <1, 65_535>.")
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "SPI Slave has been uninitialized!"
            )


class SpiSlaveProto(
    Generic[StreamHandleType],
    SpiSlaveCommon[SpiSlaveProtoHandle, "SpiSlaveProto", StreamHandleType],
):
    """A class encapsulating the SPI Slave protocol mode.

    Attributes:
        tag:    Can be used to disambiguate between SPI Slave in raw/protocol mode
    """

    tag: Literal[SpiModeTag.PROTO]

    def __init__(self, ft_handle: SpiSlaveProtoHandle, stream_handle: StreamHandleType):
        """Initialize the class with given FT4222 handle and a mode class type.

        Args:
            ft_handle:  FT4222 handle initialized in protocol SPI Slave mode
            mode_handle:    Calling stream mode handle. Used in 'uninitialize()' method.
        """
        super().__init__(ft_handle, stream_handle)
        self.tag = SpiModeTag.PROTO

    # FIXME: Proper typing
    def set_event_notification(self, mask: EventType, param: c_void_p) -> None:
        raise NotImplementedError(
            "Unfortunately this function is yet to be implemented!"
        )
        """TODO: Implement and document"""
        pass


class SpiSlaveRaw(
    Generic[StreamHandleType],
    SpiSlaveCommon[SpiSlaveRawHandle, "SpiSlaveRaw", StreamHandleType],
):
    """A class encapsulating the SPI Slave in raw mode.

    Attributes:
        tag:    Can be used to disambiguate between SPI Slave in raw/protocol mode
    """

    tag: Literal[SpiModeTag.RAW]

    def __init__(self, ft_handle: SpiSlaveRawHandle, stream_handle: StreamHandleType):
        """Initialize the class with given FT4222 handle and a mode class type.

        Args:
            ft_handle:      FT4222 handle initialized in raw SPI Slave mode
            stream_handle:  Calling stream mode handle. Used in 'uninitialize()' method.
        """
        super().__init__(ft_handle, stream_handle)
        self.tag = SpiModeTag.RAW


SpiSlave = Union[SpiSlaveProto[StreamHandleType], SpiSlaveRaw[StreamHandleType]]
