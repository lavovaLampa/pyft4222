"""TODO: Add module information

"""

from enum import Enum, auto
from typing import Callable, Dict, Final, List, Tuple, Type, Union

from koda import Err, Ok, Result

from pyft4222.stream import GpioStream, ProtocolStream, SpiStream
from pyft4222.wrapper import OS_TYPE, FtHandle
from pyft4222.wrapper import ftd2xx as ftd
from pyft4222.wrapper import gpio as wgpio
from pyft4222.wrapper.common import uninitialize

VERSION: Final = "0.1.2"

_DEFAULT_GPIO_DIRS: Final[wgpio.DirTuple] = (
    wgpio.Direction.INPUT,
    wgpio.Direction.INPUT,
    wgpio.Direction.INPUT,
    wgpio.Direction.INPUT,
)


def _disambiguate_modes(handle: FtHandle) -> Union[GpioStream, SpiStream]:
    """Disambiguate between chip configuration mode 1 and 2.

    Args:
        handle:             Handle to an opened FT4222 interface (in mode_1_2)

    Raises:
        Ft4222Exception:    In case of unexpected error

    Returns:
        Union[GpioHandle, SpiMasterHandle]:     Returns disambiguated handle
    """
    result = wgpio.init(handle, _DEFAULT_GPIO_DIRS)
    if isinstance(result, Ok):
        return GpioStream(uninitialize(result.val))
    else:
        return SpiStream(handle)


_Ft4222HandleType = Union[
    Type[ProtocolStream],
    Type[GpioStream],
    Type[SpiStream],
    Callable[[FtHandle], Union[GpioStream, SpiStream]],
]

Ft4222Handle = Union[ProtocolStream, GpioStream, SpiStream]

_MODE_MAP: Final[Dict[Tuple[str, ftd.DeviceType], _Ft4222HandleType]] = {
    # Mode 0
    ("FT4222 A", ftd.DeviceType.DEV_4222H_0): ProtocolStream,
    ("FT4222 B", ftd.DeviceType.DEV_4222H_0): GpioStream,
    # Mode 1 or Mode 2
    ("FT4222 A", ftd.DeviceType.DEV_4222H_1_2): SpiStream,
    ("FT4222 B", ftd.DeviceType.DEV_4222H_1_2): SpiStream,
    ("FT4222 C", ftd.DeviceType.DEV_4222H_1_2): SpiStream,
    ("FT4222 D", ftd.DeviceType.DEV_4222H_1_2): _disambiguate_modes,
    # Mode 3
    ("FT4222", ftd.DeviceType.DEV_4222H_3): ProtocolStream,
}


class FtError(Enum):
    INVALID_MODE = auto()
    INVALID_IDX = auto()
    INVALID_HANDLE = auto()
    UNKNOWN_FAILURE = auto()


def _get_mode_handle(ft_handle: FtHandle) -> Result[Ft4222Handle, FtError]:
    """Resolve and instantiate a correct device configuration class.

    Args:
        ft_handle:  Handle to open FT4222 device stream

    Returns:
        Result[Ft4222Handle, FtError]:
    """
    dev_details = ftd.get_device_info(ft_handle)
    if dev_details is not None:
        handle_type = _MODE_MAP.get((dev_details.description, dev_details.dev_type))
        if handle_type is not None:
            return Ok(handle_type(ft_handle))
        else:
            return Err(FtError.INVALID_MODE)
    else:
        return Err(FtError.INVALID_HANDLE)


def _validate_dev_idx(dev_idx: int) -> bool:
    """Validate given D2XX device index.

    Args:
        dev_idx:    D2XX device index

    Returns:
        bool:       Is given device index valid?
    """
    return 0 <= dev_idx < (2**31)


def get_device_info_list() -> List[ftd.DeviceInfo]:
    """Get list containing information about available (connected) D2XX devices.

    Raises:
        FtException:        In case of unexpected error

    Returns:
        List[DeviceInfo]:   List containing details about connected D2XX devices
    """
    return ftd.get_device_info_list()


def get_device_info_detail(dev_idx: int) -> Result[ftd.DeviceInfo, FtError]:
    """Get information about device at the given index (if any).

    Args:
        dev_idx:        Zero-base index of the device (0 to (2^31 - 1))

    Raises:
        FtException:    In case of unexpected error

    Returns:
        Result[DeviceInfo, FtError]:    Structure containing information
        about the device
    """
    if _validate_dev_idx(dev_idx):
        result = ftd.get_device_info_detail(dev_idx)
        if result is not None:
            return Ok(result)

    return Err(FtError.INVALID_IDX)


def open_by_idx(dev_idx: int) -> Result[Ft4222Handle, FtError]:
    """Open FT4222 device stream using 'device index'.

    The device index is 0-based and can be found by calling
    'get_device_info_list()' for example.

    Args:
        dev_id:         Device index

    Raises:
        FtException:    In case of unexpected error

    Returns:
        Ft4222Handle:   Handle encapsulating modes available in the
        current device configuration mode
    """
    if _validate_dev_idx(dev_idx):
        ft_handle = ftd.open_by_idx(dev_idx)
        if isinstance(ft_handle, Ok):
            return _get_mode_handle(ft_handle.val)
        else:
            return Err(FtError.INVALID_HANDLE)
    else:
        return Err(FtError.INVALID_IDX)


def open_by_serial(serial_num: str) -> Result[Ft4222Handle, FtError]:
    """Open FT4222 device stream using 'device serial number'.

    Args:
        serial_num:     A device serial number string

    Returns:
        Result[Ft4222Handle, FtError]:
    """
    ft_handle = ftd.open_by_serial(serial_num)
    if isinstance(ft_handle, Ok):
        return _get_mode_handle(ft_handle.val)
    else:
        return Err(FtError.INVALID_HANDLE)


def open_by_description(dev_description: str) -> Result[Ft4222Handle, FtError]:
    """Open FT4222 device stream using 'device description'.

    Args:
        dev_description:    Device description string

    Returns:
        Result[Ft4222Handle, FtError]:
    """
    ft_handle = ftd.open_by_description(dev_description)
    if isinstance(ft_handle, Ok):
        return _get_mode_handle(ft_handle.val)
    else:
        return Err(FtError.INVALID_HANDLE)


if OS_TYPE != "Linux":

    def open_by_location(location_id: int) -> Result[Ft4222Handle, FtError]:
        """Open FT4222 device stream using 'device USB location ID'.

        Args:
            location_id:    Device USB location ID

        Returns:
            Result[Ft4222Handle, FtError]:
        """
        ft_handle = ftd.open_by_location(location_id)
        if isinstance(ft_handle, Ok):
            return _get_mode_handle(ft_handle.val)
        else:
            return Err(FtError.INVALID_HANDLE)
