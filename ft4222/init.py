from enum import Enum, auto
from typing import Callable, Union, Final, Dict, Tuple, Type

from .ft4222 import ProtocolHandle, GpioHandle, SpiMasterHandle
from wrapper import Err, FtHandle, Ok, Result, ResultTag, ftd2xx as ftd
from wrapper.dll_loader import OS_TYPE
from wrapper.ftd2xx import DeviceType
from wrapper.ft4222 import gpio
from wrapper.ft4222.common import uninitialize


_DEFAULT_GPIO_DIRS: Final[gpio.DirTuple] = (
    gpio.Direction.INPUT,
    gpio.Direction.INPUT,
    gpio.Direction.INPUT,
    gpio.Direction.INPUT
)


def _disambiguate_modes(handle: FtHandle) -> Union[GpioHandle, SpiMasterHandle]:
    """Disambiguate between FT4222 in mode 1 and 2.

    Args:
        handle:     Handle to an opened FT4222 interface (in mode_1_2)

    Raises:
        Ft4222Exception:        In case of unexpected error

    Returns:
        TODO
    """
    result = gpio.init(handle, _DEFAULT_GPIO_DIRS)
    if result.tag == ResultTag.OK:
        gpio_handle = result.result
        open_handle = uninitialize(gpio_handle)
        return GpioHandle(open_handle)
    else:
        return SpiMasterHandle(handle)


Ft4222HandleType = Union[
    Type[ProtocolHandle],
    Type[GpioHandle],
    Type[SpiMasterHandle],
    Callable[[FtHandle], Union[GpioHandle, SpiMasterHandle]]
]

Ft4222Handle = Union[
    ProtocolHandle,
    GpioHandle,
    SpiMasterHandle
]

MODE_MAP: Final[Dict[Tuple[str, DeviceType], Ft4222HandleType]] = {
    # Mode 0
    ("FT4222 A", DeviceType.DEV_4222H_0): ProtocolHandle,
    ("FT4222 B", DeviceType.DEV_4222H_0): GpioHandle,

    # Mode 1 or Mode 2
    ("FT4222 A", DeviceType.DEV_4222H_1_2): SpiMasterHandle,
    ("FT4222 B", DeviceType.DEV_4222H_1_2): SpiMasterHandle,
    ("FT4222 C", DeviceType.DEV_4222H_1_2): SpiMasterHandle,
    ("FT4222 D", DeviceType.DEV_4222H_1_2): _disambiguate_modes,

    # Mode 3
    ("FT4222", DeviceType.DEV_4222H_3): ProtocolHandle
}


class FtError(Enum):
    INVALID_MODE = auto()
    INVALID_ID = auto()
    INVALID_HANDLE = auto()
    UNKNOWN_FAILURE = auto()


def get_mode_handle(ft_handle: FtHandle) -> Result[Ft4222Handle, FtError]:
    dev_details = ftd.get_device_info(ft_handle)
    if dev_details is not None:
        handle_type = MODE_MAP.get((
            dev_details.description,
            dev_details.dev_type
        ))
        if handle_type is not None:
            return Ok(handle_type(ft_handle))
        else:
            return Err(FtError.INVALID_MODE)
    else:
        return Err(FtError.INVALID_HANDLE)


def open(dev_id: int) -> Result[Ft4222Handle, FtError]:
    id_valid = 0 <= dev_id < (2 ** 31) - 1

    if id_valid:
        ft_handle = ftd.open(dev_id)
        if ft_handle.tag == ResultTag.OK:
            return get_mode_handle(ft_handle.result)
        else:
            return Err(FtError.INVALID_HANDLE)
    else:
        return Err(FtError.INVALID_ID)


def open_by_serial(serial_num: str) -> Result[Ft4222Handle, FtError]:
    ft_handle = ftd.open_by_serial(serial_num)
    if ft_handle.tag == ResultTag.OK:
        return get_mode_handle(ft_handle.result)
    else:
        return Err(FtError.INVALID_HANDLE)


def open_by_description(dev_description: str) -> Result[Ft4222Handle, FtError]:
    ft_handle = ftd.open_by_description(dev_description)
    if ft_handle.tag == ResultTag.OK:
        return get_mode_handle(ft_handle.result)
    else:
        return Err(FtError.INVALID_HANDLE)


if OS_TYPE != 'Linux':
    def open_by_location(location_id: int) -> Result[Ft4222Handle, FtError]:
        ft_handle = ftd.open_by_location(location_id)
        if ft_handle.tag == ResultTag.OK:
            return get_mode_handle(ft_handle.result)
        else:
            return Err(FtError.INVALID_HANDLE)
