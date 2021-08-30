from abc import ABC
from enum import Enum, auto
from typing import Generic, Literal, Optional, Type, TypeVar, Union, overload

from pyft4222.handle import GenericHandle

from pyft4222.wrapper import FtHandle, Ft4222Exception, Ft4222Status
from pyft4222.wrapper.common import uninitialize
from pyft4222.wrapper.spi import DriveStrength
from pyft4222.wrapper.spi.master import (
    CsPolarity, IoMode, SpiMasterHandle,
    SpiMasterSingleHandle, SpiMasterMultiHandle,
    multi_read_write, set_cs_polarity, single_read,
    single_read_write, single_write
)
from pyft4222.wrapper.spi.common import (
    TransactionIdx,
    reset, reset_transaction, set_driving_strength
)


T = TypeVar('T', bound=GenericHandle[FtHandle])
U = TypeVar('U', bound=SpiMasterHandle)


class SpiModeTag(Enum):
    SINGLE = auto()
    MULTI = auto()


class SpiMasterCommon(Generic[T, U], GenericHandle[U], ABC):
    """An abstract class encapsulating functions
    common to all SPI Master modes.
    """
    _mode_class: Type[T]

    def __init__(self, ft_handle: U, mode_class: Type[T]):
        """Initialize the class with given FT4222 handle and a mode class type.

        Args:
            ft_handle:      FT4222 handle initialized in any SPI Master mode
            mode_class:     Calling class type. Used in 'uninitialize()' method.
        """
        super().__init__(ft_handle)
        self._mode_class = mode_class

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
                Ft4222Status.DEVICE_NOT_OPENED,
                "SPI Master has been uninitialized!"
            )

    def reset_transaction(self, transaction_idx: TransactionIdx) -> None:
        """Purge transmit and receive buffers, reset transaction state.

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
                Ft4222Status.DEVICE_NOT_OPENED,
                "SPI Master has been uninitialized!"
            )

    def set_driving_strength(
        self,
        clk_strength: DriveStrength,
        io_strength: DriveStrength,
        sso_strength: DriveStrength
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
            set_driving_strength(
                self._handle,
                clk_strength,
                io_strength,
                sso_strength
            )
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "SPI Master has been uninitialized!"
            )

    def set_cs_polarity(self, cs_polarity: CsPolarity) -> None:
        """Set chip select signal polarity.

        Args:
            cs_polarity:        Chip select signal polarity

        Raises:
            Ft4222Exception:    In case of unexpected error
        """
        if self._handle is not None:
            set_cs_polarity(self._handle, cs_polarity)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "SPI Master has been uninitialized!"
            )

    @overload
    def set_io_mode(
        self,
        io_mode: Literal[IoMode.SINGLE]
    ) -> 'SpiMasterSingle[T]': ...

    @overload
    def set_io_mode(
        self,
        io_mode: Literal[IoMode.DUAL, IoMode.QUAD]
    ) -> 'SpiMasterMulti[T]': ...

    @overload
    def set_io_mode(
        self,
        io_mode: IoMode
    ) -> Union['SpiMasterSingle[T]', 'SpiMasterMulti[T]']: ...

    def set_io_mode(
        self,
        io_mode: IoMode
    ) -> Union['SpiMasterSingle[T]', 'SpiMasterMulti[T]']:
        """Set I/O mode of the SPI Master (i.e., single, dual, quad)

        Note:
            Dual and quad modes are half-duplex (duh).

        Args:
            io_mode:            I/O mode to be set

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            SpiMaster:          A class encapsulating the selected mode
        """
        if self._handle is not None:
            temp_handle = self._handle
            self._handle = None

            if io_mode == IoMode.SINGLE:
                return SpiMasterSingle(
                    SpiMasterSingleHandle(temp_handle),
                    self._mode_class
                )
            else:
                return SpiMasterMulti(
                    SpiMasterMultiHandle(temp_handle),
                    self._mode_class
                )
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "SPI Master has been uninitialized!"
            )

    def close(self) -> None:
        """Uninitialize and close the owned handle.

        Note:
            A new handle must be opened and initialized
            after calling this method.

        Raises:
            Ft4222Exception:    In case of unexpected error
        """
        self.uninitialize().close()

    def uninitialize(self) -> T:
        """Uninitialize the owned handle from SPI Master mode.

        The handle can be initialized into any other supported mode.

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            T:                  A class encapsulating the opened stream type
        """
        if self._handle is not None:
            handle = self._handle
            self._handle = None
            return self._mode_class(uninitialize(handle))
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "SPI Master has been uninitialized already!"
            )


class SpiMasterSingle(Generic[T], SpiMasterCommon[T, SpiMasterSingleHandle]):
    """A class encapsulating the SPI Master in single I/O (full-duplex) mode.

    Attributes:
        tag:    Can be used to disambiguate between SPI Master in single/multi IO mode
    """
    tag: Literal[SpiModeTag.SINGLE]

    def __init__(self, ft_handle: SpiMasterSingleHandle, mode_class: Type[T]):
        """Initialize the class with given FT4222 handle and a mode class type.

        Args:
            ft_handle:  FT4222 handle initialized in single SPI Master mode
            mode_class: Calling class type. Used in 'uninitialize()' method.
        """
        super().__init__(ft_handle, mode_class)
        self.tag = SpiModeTag.SINGLE

    def single_read(self, read_byte_count: int, end_transaction: bool = True) -> bytes:
        """Read data from an SPI slave.

        Args:
            read_byte_count:    Non-zero number of bytes to read (1 - 65_535)
            end_transaction:    De-assert slave select after a read?

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            bytes:              Read data
        """
        if self._handle is not None:
            if 0 < read_byte_count < (2 ** 16):
                return single_read(self._handle, read_byte_count, end_transaction)
            else:
                raise ValueError(
                    "read_byte_count value must be in range <1, 65_535>."
                )
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "SPI Master has been uninitialized!"
            )

    def single_write(self, write_data: bytes, end_transaction: bool = True) -> int:
        """Write data to an SPI slave.

        Args:
            write_data:         Non-empty list of data to write
            end_transaction:    De-assert slave select after a write?

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            int:                Number of bytes written
        """
        if self._handle is not None:
            if 0 < len(write_data) < (2 ** 16):
                return single_write(self._handle, write_data, end_transaction)
            else:
                raise ValueError(
                    "write_data length must be in range <1, 65_535>."
                )
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "SPI Master has been uninitialized!"
            )

    def single_read_write(self, write_data: bytes, end_transaction: bool = True) -> bytes:
        """Write and read data concurrently (i.e., full-duplex) from an SPI slave.

        Args:
            write_data:         Non-empty list of data to write, length <1, 65_535>
            end_transaction:    De-assert slave select after a write?

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            bytes:              Read data
        """
        if self._handle is not None:
            if 0 < len(write_data) < (2 ** 16):
                return single_read_write(self._handle, write_data, end_transaction)
            else:
                raise ValueError(
                    "write_data length must be in range <1, 65_535>."
                )
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "SPI Master has been uninitialized!"
            )


class SpiMasterMulti(Generic[T], SpiMasterCommon[T, SpiMasterMultiHandle]):
    """A class encapsulating the SPI Master in dual or quad I/O (half-duplex) mode.

    Attributes:
        tag:    Can be used to disambiguate between SPI Master in single/multi IO mode
    """

    tag: Literal[SpiModeTag.MULTI]

    def __init__(self, ft_handle: SpiMasterMultiHandle, mode_class: Type[T]):
        """Initialize the class with given FT4222 handle and a mode class type.

        Args:
            ft_handle:  FT4222 handle initialized in dual or quad SPI Master mode
            mode_class: Calling class type.  Used in 'uninitialize()' method.
        """
        super().__init__(ft_handle, mode_class)
        self.tag = SpiModeTag.MULTI

    def multi_read_write(
        self,
        write_data: Optional[bytes],
        single_write_byte_count: int,
        multi_write_byte_count: int,
        multi_read_byte_count: int
    ) -> bytes:
        """Write and read data from an SPI slave.

        Note:
            The data are written and read in 3 phases.

        First, the given number of bytes is written using single I/O line. This
        is used mostly for commands (e.g., for EEPROMs, flash memories, etc.).

        Second, the given number of bytes is written using multiple I/O lines.

        Third, the given number of bytes is read using multiple I/O lines.

        Number of bytes to write can be zero.
        Number of bytes to read can be zero.
        But both cannot be zero at the same time.

        The total number of bytes to write cannot be larger than length of
        given data.

        Args:
            write_data:                 Data to be write
                length <0, 65_535>
            single_write_byte_count:    Number of bytes to write using single I/O line,
                length <0, 15>              (1st phase)
            multi_write_byte_count:     Number of bytes to write using multiple I/O lines,
                length <0, 65_535>          (2nd phase)
            multi_read_byte_count:      Number of bytes to read using multi I/O lines
                length <0, 65_535>          (3rd phase)

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            bytes:              Read data
        """
        if self._handle is not None:
            if not (0 <= single_write_byte_count < (2 ** 4)):
                raise ValueError(
                    "single_write_bytes must be in range <0, 15>."
                )
            if not (0 <= multi_write_byte_count < (2 ** 16)):
                raise ValueError(
                    "multi_write_bytes must be in range <0, 65_535>."
                )
            if not (0 <= multi_read_byte_count < (2 ** 16)):
                raise ValueError(
                    "multi_read_bytes must be in range <0, 65_535>."
                )
            if (
                single_write_byte_count +
                multi_write_byte_count +
                multi_read_byte_count
            ) <= 0:
                raise ValueError(
                    "Total number of bytes to read and write must be non-zero."
                )
            if write_data is None:
                if (single_write_byte_count + multi_write_byte_count) != 0:
                    raise ValueError(
                        "Number of bytes to write must be zero if the write_data are None."
                    )
            else:
                if not (0 <= len(write_data) < (2 ** 16)):
                    raise ValueError(
                        "Length of write_data must be in range <0, 65_535>."
                    )
                if (single_write_byte_count + multi_write_byte_count) > len(write_data):
                    raise ValueError(
                        "Number of bytes to write is larger than write_data length."
                    )

            return multi_read_write(
                self._handle,
                write_data,
                single_write_byte_count,
                multi_write_byte_count,
                multi_read_byte_count
            )
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "SPI Master has been uninitialized!"
            )


SpiMaster = Union[SpiMasterSingle[T], SpiMasterMulti[T]]
