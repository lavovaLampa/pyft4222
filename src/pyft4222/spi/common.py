from abc import ABC
from typing import TypeVar

from pyft4222.handle import GenericProtocolHandle, StreamHandleType
from pyft4222.wrapper import Ft4222Exception, Ft4222Status
from pyft4222.wrapper.spi import DriveStrength
from pyft4222.wrapper.spi.common import (
    SpiHandle,
    TransactionIdx,
    reset,
    reset_transaction,
    set_driving_strength,
)

SpiHandleType = TypeVar("SpiHandleType", bound=SpiHandle)


class SpiCommon(GenericProtocolHandle[SpiHandleType, StreamHandleType], ABC):
    """A class encapsulating functions common to all SPI modes."""

    def reset_bus(self) -> None:
        """Reset the SPI bus.

        It is not necessary to initialize the SPI Master again.
        The chip retains all settings.

        Raises:
            Ft4222Exception:    In case of unexpected error
        """
        if self._handle is None:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "SPI Slave has been uninitialized!"
            )

        reset(self._handle)

    def reset_transaction(self, transaction_idx: TransactionIdx) -> None:
        """Purge transmit and received buffers, reset transaction state.

        Args:
            transaction_idx:    Index of SPI transaction (0 to 3),
            depending on the mode of the chip.

        Raises:
            Ft4222Exception:    In case of unexpected error
        """
        if self._handle is None:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "SPI Slave has been uninitialized!"
            )

        reset_transaction(self._handle, transaction_idx)

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
        if self._handle is None:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "SPI Slave has been uninitialized!"
            )

        set_driving_strength(self._handle, clk_strength, io_strength, sso_strength)
