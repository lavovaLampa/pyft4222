from ctypes import c_void_p, c_uint8, c_uint

from typing import Literal, Union
from .slave import SpiSlaveHandle
from .master import SpiMasterHandle

from . import DriveStrength
from ...dll_loader import ftlib
from .. import Ft4222Exception, Ft4222Status, SOFT_ERROR_SET

SpiHandle = Union[SpiMasterHandle, SpiSlaveHandle]

TransactionIdx = Literal[0, 1, 2, 3]


_reset = ftlib.FT4222_SPI_Reset
_reset.argtypes = [c_void_p]
_reset.restype = Ft4222Status

_reset_transaction = ftlib.FT4222_SPI_ResetTransaction
_reset_transaction.argtypes = [c_void_p, c_uint8]
_reset_transaction.restype = Ft4222Status

_set_driving_strength = ftlib.FT4222_SPI_SetDrivingStrength
_set_driving_strength.argtypes = [c_void_p, c_uint, c_uint, c_uint]
_set_driving_strength.restype = Ft4222Status


def reset(ft_handle: SpiHandle) -> None:
    """Reset the SPI master or slave device.

    If the SPI bus encounters errors or works abnormally, this function will reset the SPIdevice.
    It is not necessary to call SPI init function again after calling this reset function.
    It retains all original setting of SPI.

    Args:
        ft_handle:          Handle to an initialized FT4222 device in SPI Master/Slave mode

    Raises:
        Ft4222Exception:    In case of unexpected error
    """
    result: Ft4222Status = _reset(ft_handle)

    if result not in SOFT_ERROR_SET:
        raise Ft4222Exception(result)


def reset_transaction(ft_handle: SpiHandle, spi_idx: TransactionIdx) -> None:
    """Reset the SPI transaction.

    Purge receive and transmit buffers in the device and reset the transaction state.

    Args:
        ft_handle:  Handle to an initialized FT4222 device in SPI Master/Slave mode
        spi_idx:    Index of SPI transaction (0 - 3), depending on the mode of the chip

    Raises:
        Ft4222Exception:    In case of unexpected error
    """
    assert 0 <= spi_idx <= 3, "Invalid SPI transaction index (0 - 3)"

    result: Ft4222Status = _reset_transaction(ft_handle, spi_idx)

    if result not in SOFT_ERROR_SET:
        raise Ft4222Exception(result)


def set_driving_strength(
    ft_handle: SpiHandle,
    clk_strength: DriveStrength,
    io_strength: DriveStrength,
    sso_strength: DriveStrength
) -> None:
    """Set the driving strength of clk, io, and sso pins.

    Default driving strength of all spi pins is 'SPI.DriveStrength.DS_4MA'.
    Unless there is some hardware wiring requirement for device,
    setting driving strength to 4 mA should be enough.

    Args:
        ft_handle:  Handle to an initialized FT4222 device in SPI Master/Slave mode

    Raises:
        Ft4222Exception:    In case of unexpected error
    """
    result: Ft4222Status = _set_driving_strength(
        ft_handle,
        clk_strength,
        io_strength,
        sso_strength
    )

    if result not in SOFT_ERROR_SET:
        raise Ft4222Exception(result)
