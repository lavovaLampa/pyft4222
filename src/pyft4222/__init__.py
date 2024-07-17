"""TODO: Add module information

"""

from __future__ import annotations

from typing import Callable, Final, Union

from typing_extensions import TypeAlias

from pyft4222.result import Err, Ok, Result
from pyft4222.stream import GpioStream, ProtocolStream, SpiStream
from pyft4222.wrapper import OS_TYPE, FtHandle, FtStatus
from pyft4222.wrapper import ftd2xx as ftd
from pyft4222.wrapper import gpio as wgpio
from pyft4222.wrapper.common import uninitialize

_DEFAULT_GPIO_DIRS: Final[wgpio.DirTuple] = (
    wgpio.Direction.INPUT,
    wgpio.Direction.INPUT,
    wgpio.Direction.INPUT,
    wgpio.Direction.INPUT,
)


def _disambiguate_modes(handle: FtHandle) -> GpioStream | SpiStream:
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


_Ft4222HandleType: TypeAlias = Union[
    type[ProtocolStream],
    type[GpioStream],
    type[SpiStream],
    Callable[[FtHandle], Union[GpioStream, SpiStream]],
]

Ft4222Handle: TypeAlias = Union[ProtocolStream, GpioStream, SpiStream]

_MODE_MAP: Final[dict[tuple[str, ftd.DeviceType], _Ft4222HandleType]] = {
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


def _get_mode_handle(ft_handle: FtHandle) -> Result[Ft4222Handle, FtStatus]:
    """Resolve and instantiate a correct device configuration class.

    Args:
        ft_handle:  Handle to open FT4222 device stream

    Returns:
        Result[Ft4222Handle, FtError]:
    """
    dev_details = ftd.get_device_info(ft_handle)

    if isinstance(dev_details, Err):
        return dev_details

    handle_type = _MODE_MAP.get((dev_details.val.description, dev_details.val.dev_type))
    assert handle_type is not None
    return Ok(handle_type(ft_handle))


def _is_dev_idx_valid(dev_idx: int) -> bool:
    """Validate given D2XX device index.

    Args:
        dev_idx:    D2XX device index

    Returns:
        bool:       Is given device index valid?
    """
    return 0 <= dev_idx < (2**31)


def get_device_info_list() -> list[ftd.DeviceInfo]:
    """Get list containing information about available (connected) D2XX devices.

    Raises:
        FtException:        In case of unexpected error

    Returns:
        list[DeviceInfo]:   List containing details about connected D2XX devices
    """
    return ftd.get_device_info_list()


def get_device_info_detail(dev_idx: int) -> Result[ftd.DeviceInfo, FtStatus]:
    """Get information about device at the given index (if any).

    Args:
        dev_idx:        Zero-base index of the device (0 to (2^31 - 1))

    Raises:
        FtException:    In case of unexpected error

    Returns:
        Result[DeviceInfo, FtError]:    Structure containing information
        about the device
    """
    if not _is_dev_idx_valid(dev_idx):
        return Err(FtStatus.INVALID_ARGS)

    return ftd.get_device_info_detail(dev_idx)


def open_by_idx(dev_idx: int) -> Result[Ft4222Handle, FtStatus]:
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
    if not _is_dev_idx_valid(dev_idx):
        return Err(FtStatus.INVALID_ARGS)

    return ftd.open_by_idx(dev_idx).flat_map(_get_mode_handle)


def open_by_serial(serial_num: str) -> Result[Ft4222Handle, FtStatus]:
    """Open FT4222 device stream using 'device serial number'.

    Args:
        serial_num:     A device serial number string

    Returns:
        Result[Ft4222Handle, FtError]:
    """
    return ftd.open_by_serial(serial_num).flat_map(_get_mode_handle)


def open_by_description(dev_description: str) -> Result[Ft4222Handle, FtStatus]:
    """Open FT4222 device stream using 'device description'.

    Args:
        dev_description:    Device description string

    Returns:
        Result[Ft4222Handle, FtError]:
    """
    return ftd.open_by_description(dev_description).flat_map(_get_mode_handle)


if OS_TYPE != "Linux":

    def open_by_location(location_id: int) -> Result[Ft4222Handle, FtStatus]:
        """Open FT4222 device stream using 'device USB location ID'.

        Args:
            location_id:    Device USB location ID

        Returns:
            Result[Ft4222Handle, FtError]:
        """
        return ftd.open_by_location(location_id).flat_map(_get_mode_handle)
