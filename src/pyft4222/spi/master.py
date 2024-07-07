from abc import ABC
from typing import Generic, Literal, Optional, TypeVar, Union, overload

from pyft4222.handle import StreamHandleType
from pyft4222.spi.common import SpiCommon
from pyft4222.wrapper import Ft4222Exception, Ft4222Status
from pyft4222.wrapper.spi.master import (
    CsPolarity,
    IoMode,
    SpiMasterHandle,
    SpiMasterMultiHandle,
    SpiMasterSingleHandle,
    multi_read_write,
    set_cs_polarity,
    single_read,
    single_read_write,
    single_write,
)

SpiMasterHandleType = TypeVar("SpiMasterHandleType", bound=SpiMasterHandle)


class SpiMasterCommon(SpiCommon[SpiMasterHandleType, StreamHandleType], ABC):
    """An abstract class encapsulating functions
    common to all SPI Master modes.
    """

    def set_cs_polarity(self, cs_polarity: CsPolarity) -> None:
        """Set chip select signal polarity.

        Args:
            cs_polarity:        Chip select signal polarity

        Raises:
            Ft4222Exception:    In case of unexpected error
        """
        if self._handle is None:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "SPI Master has been uninitialized!"
            )

        set_cs_polarity(self._handle, cs_polarity)

    @overload
    def set_io_mode(
        self, io_mode: Literal[IoMode.SINGLE]
    ) -> "SpiMasterSingle[StreamHandleType]": ...

    @overload
    def set_io_mode(
        self, io_mode: Literal[IoMode.DUAL, IoMode.QUAD]
    ) -> "SpiMasterMulti[StreamHandleType]": ...

    @overload
    def set_io_mode(
        self, io_mode: IoMode
    ) -> Union[
        "SpiMasterSingle[StreamHandleType]", "SpiMasterMulti[StreamHandleType]"
    ]: ...

    def set_io_mode(
        self, io_mode: IoMode
    ) -> Union["SpiMasterSingle[StreamHandleType]", "SpiMasterMulti[StreamHandleType]"]:
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
        if self._handle is None:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "SPI Master has been uninitialized!"
            )

        temp_handle = self._handle
        self._handle = None

        if io_mode == IoMode.SINGLE:
            return SpiMasterSingle(
                SpiMasterSingleHandle(temp_handle), self._stream_handle
            )
        else:
            return SpiMasterMulti(
                SpiMasterMultiHandle(temp_handle), self._stream_handle
            )


class SpiMasterSingle(
    Generic[StreamHandleType],
    SpiMasterCommon[SpiMasterSingleHandle, StreamHandleType],
):
    """A class encapsulating the SPI Master in single I/O (full-duplex) mode."""

    def single_read(self, read_byte_count: int, end_transaction: bool = True) -> bytes:
        """Read data from an SPI slave.

        Args:
            read_byte_count:    Non-zero number of bytes to read (1 - 65_535)
            end_transaction:    De-assert chip select after a read?

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            bytes:              Read data
        """
        if self._handle is None:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "SPI Master has been uninitialized!"
            )

        result: bytes = bytes()

        while read_byte_count > 0:
            read_len: int = min(read_byte_count, (2**16) - 1)
            trans_end: bool = end_transaction if read_len < (2**16) else False
            result += single_read(self._handle, read_len, trans_end)

            read_byte_count -= read_len

        return result

    def single_write(self, write_data: bytes, end_transaction: bool = True) -> int:
        """Write data to an SPI slave.

        NOTE:
            Data larger than 2^16 - 1 bytes will be done using multiple driver calls.

        Args:
            write_data:         Non-empty list of data to write
            end_transaction:    De-assert slave select after a write?

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            int:                Number of bytes written
        """
        if self._handle is None:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "SPI Master has been uninitialized!"
            )

        write_len: int = len(write_data)
        offset: int = 0
        result: int = 0

        while write_len > 0:
            write_amount: int = min(write_len, (2**16) - 1)
            trans_end: bool = end_transaction if write_len < (2**16) else False
            result += single_write(
                self._handle, write_data[offset : offset + write_amount], trans_end
            )

            write_len -= write_amount
            offset += write_amount

        return result

    def single_read_write(
        self, write_data: bytes, end_transaction: bool = True
    ) -> bytes:
        """Write and read data concurrently (i.e., full-duplex) from an SPI slave.

        NOTE:
            Data larger than 2^16 - 1 bytes will be done using multiple driver calls.

        Args:
            write_data:         Non-empty list of data to write, length
            end_transaction:    De-assert slave select after a write?

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            bytes:              Read data
        """
        if self._handle is None:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "SPI Master has been uninitialized!"
            )

        write_len: int = len(write_data)
        offset: int = 0
        result: bytes = bytes()

        while write_len > 0:
            write_amount: int = min(write_len, (2**16) - 1)
            trans_end: bool = end_transaction if write_len < (2**16) else False
            result += single_read_write(
                self._handle, write_data[offset : offset + write_amount], trans_end
            )

            write_len -= write_amount
            offset += write_amount

        return result


class SpiMasterMulti(
    Generic[StreamHandleType],
    SpiMasterCommon[SpiMasterMultiHandle, StreamHandleType],
):
    """A class encapsulating the SPI Master in dual or quad I/O (half-duplex) mode."""

    def multi_read_write(
        self,
        single_write_data: Optional[bytes] = None,
        multi_write_data: Optional[bytes] = None,
        multi_read_byte_count: int = 0,
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
            single_write_data:          Data to write using single I/O line,
                length <0, 15>              (1st phase)
            multi_write_data:           Data to write using multiple I/O lines,
                length <0, 65_535>          (2nd phase)
            multi_read_byte_count:      Number of bytes to read using multi I/O lines
                length <0, 65_535>          (3rd phase)

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            bytes:              Read data
        """
        single_write_bytes: bytes = (
            single_write_data if single_write_data is not None else bytes()
        )
        multi_write_bytes: bytes = (
            multi_write_data if multi_write_data is not None else bytes()
        )
        write_data_cat: bytes = single_write_bytes + multi_write_bytes

        if self._handle is None:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "SPI Master has been uninitialized!"
            )

        if not (0 <= len(single_write_bytes) < (2**4)):
            raise ValueError("single_write_bytes must be in range <0, 15>.")
        if not (0 <= len(multi_write_bytes) < (2**16)):
            raise ValueError("multi_write_bytes must be in range <0, 65_535>.")
        if not (0 <= multi_read_byte_count < (2**16)):
            raise ValueError("multi_read_bytes must be in range <0, 65_535>.")
        if (
            len(single_write_bytes) + len(multi_write_bytes) + multi_read_byte_count
        ) <= 0:
            raise ValueError(
                "Total number of bytes to read and write must be non-zero."
            )

        return multi_read_write(
            self._handle,
            write_data_cat,
            len(single_write_bytes),
            len(multi_write_bytes),
            multi_read_byte_count,
        )


SpiMaster = Union[SpiMasterSingle[StreamHandleType], SpiMasterMulti[StreamHandleType]]
