from ctypes import cdll
from ctypes import c_void_p, c_uint8, c_uint

from enum import IntEnum, auto
from typing import Union

from .master import SpiMasterHandle
from .slave import SpiSlaveHandle

from .. import FT4222Status

try:
    ftlib = cdll.LoadLibrary('../../dlls/libft4222.so.1.4.4.44')
except OSError as e:
    print("Unable to load shared library!")
    exit(1)

SpiHandle = Union[SpiMasterHandle, SpiSlaveHandle]


class DriveStrength(IntEnum):
    DS_4MA = 0
    DS_8MA = auto()
    DS_12MA = auto()
    DS_16MA = auto()


class ClkPolarity(IntEnum):
    CLK_IDLE_LOW = 0
    CLK_IDLE_HIGH = 1


class ClkPhase(IntEnum):
    CLK_LEADING = 0
    CLK_TRAILING = 1


_reset = ftlib.FT4222_SPI_Reset
_reset.argtypes = [c_void_p]
_reset.restype = FT4222Status

_reset_transaction = ftlib.FT4222_SPI_ResetTransaction
_reset_transaction.argtypes = [c_void_p, c_uint8]
_reset_transaction.restype = FT4222Status

_set_driving_strength = ftlib.FT4222_SPI_SetDrivingStrength
_set_driving_strength.argtypes = [c_void_p, c_uint, c_uint, c_uint]
_set_driving_strength.restype = FT4222Status


def reset(ft_handle: SpiHandle) -> None:
    """Reset the SPI master or slave device.

    If the SPI bus encounters errors or works abnormally, this function will reset the SPIdevice.
    It is not necessary to call SPI init function again after calling this reset function.
    It retains all original setting of SPI.

    Args:
        ft_handle:  Handle to an initialized FT4222 device in SPI Master/Slave mode

    Raises:
        RuntimeError:   TODO
    """
    result: FT4222Status = _reset(ft_handle)

    if result != FT4222Status.OK:
        raise RuntimeError('TODO')


def reset_transaction(ft_handle: SpiHandle, spi_idx: int) -> None:
    """Reset the SPI transaction.

    Purge receive and transmit buffers in the device and reset the transaction state.

    Args:
        ft_handle:  Handle to an initialized FT4222 device in SPI Master/Slave mode
        spi_idx:    Index of SPI transaction (0 - 3), depending on the mode of the chip

    Raises:
        RuntimeError:   TODO
    """
    result: FT4222Status = _reset_transaction(ft_handle, spi_idx)

    if result != FT4222Status.OK:
        raise RuntimeError('TODO')


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
    """
    result: FT4222Status = _set_driving_strength(
        ft_handle,
        clk_strength,
        io_strength,
        sso_strength
    )

    if result != FT4222Status.OK:
        raise RuntimeError('TODO')
