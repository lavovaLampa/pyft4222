from ft4222 import CommonHandle
from typing import Generic, Optional, Type, TypeVar, Union

from wrapper import FtHandle
from wrapper.ft4222 import Ft4222Exception, Ft4222Status
from wrapper.ft4222.common import uninitialize
from wrapper.ft4222.spi import DriveStrength
from wrapper.ft4222.spi.common import TransactionIdx
from wrapper.ft4222.spi.master import CsPolarity, IoMode, SpiMasterHandle, SpiMasterSingleHandle, SpiMasterMultiHandle
from wrapper.ft4222.spi.common import reset, reset_transaction, set_driving_strength
from wrapper.ft4222.spi.master import multi_read_write, set_cs_polarity, single_read, single_read_write, single_write


T = TypeVar('T', bound=CommonHandle[FtHandle])
U = TypeVar('U', bound=SpiMasterHandle)


class SpiMasterCommon(Generic[T, U], CommonHandle[U]):
    _mode_class: Type[T]

    def __init__(self, ft_handle: U, mode_class: Type[T]):
        super().__init__(ft_handle)
        self._mode_class = mode_class

    def reset_bus(self) -> None:
        if self._handle is not None:
            reset(self._handle)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "SPI Master has been uninitialized!"
            )

    def reset_transaction(self, transaction_idx: TransactionIdx) -> None:
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
        if self._handle is not None:
            set_cs_polarity(self._handle, cs_polarity)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "SPI Master has been uninitialized!"
            )

    # FIXME: Correct typing & implementation
    def set_lines(self, io_mode: IoMode) -> None:
        pass

    def close(self) -> None:
        self.uninitialize().close()

    def uninitialize(self) -> T:
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
    def __init__(self, ft_handle: SpiMasterSingleHandle, mode_class: Type[T]):
        super().__init__(ft_handle, mode_class)

    def single_read(self, read_byte_count: int, end_transaction: bool = True) -> bytes:
        if self._handle is not None:
            return single_read(self._handle, read_byte_count, end_transaction)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "SPI Master has been uninitialized!"
            )

    def single_write(self, write_data: bytes, end_transaction: bool = True) -> int:
        if self._handle is not None:
            return single_write(self._handle, write_data, end_transaction)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "SPI Master has been uninitialized!"
            )

    def single_read_write(self, write_data: bytes, end_transaction: bool = True) -> bytes:
        if self._handle is not None:
            return single_read_write(self._handle, write_data, end_transaction)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "SPI Master has been uninitialized!"
            )


class SpiMasterMulti(Generic[T], SpiMasterCommon[T, SpiMasterMultiHandle]):
    def __init__(self, ft_handle: SpiMasterMultiHandle, mode_class: Type[T]):
        super().__init__(ft_handle, mode_class)

    def multi_read_write(
        self,
        write_data: Optional[bytes],
        single_write_byte_count: int,
        multi_write_byte_count: int,
        multi_read_byte_count: int
    ) -> bytes:
        if self._handle is not None:
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