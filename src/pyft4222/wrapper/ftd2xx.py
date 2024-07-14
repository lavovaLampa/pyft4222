from ctypes import (
    POINTER,
    Structure,
    byref,
    c_char,
    c_char_p,
    c_int,
    c_uint,
    c_uint32,
    c_void_p,
    create_string_buffer,
)
from enum import IntEnum, IntFlag, auto
from typing import Final, NamedTuple

from pyft4222.result import Err, Ok, Result
from pyft4222.wrapper import OS_TYPE, FtException, FtHandle, FtStatus
from pyft4222.wrapper.dll_loader import d2lib

# DLL function protoypes declaration


_create_device_info_list = d2lib.FT_CreateDeviceInfoList
_create_device_info_list.argtypes = [POINTER(c_uint)]
_create_device_info_list.restype = FtStatus

_get_device_info_list = d2lib.FT_GetDeviceInfoList
_get_device_info_list.argtypes = []
_get_device_info_list.restype = FtStatus

_get_device_info_detail = d2lib.FT_GetDeviceInfoDetail
_get_device_info_detail.argtypes = []
_get_device_info_detail.restype = FtStatus

_open = d2lib.FT_Open
_open.argtypes = [c_int, POINTER(c_void_p)]
_open.restype = FtStatus

_open_ex = d2lib.FT_OpenEx
_open_ex.argtypes = [c_void_p, c_uint, POINTER(c_void_p)]
_open_ex.restype = FtStatus

_close = d2lib.FT_Close
_close.argtypes = [c_void_p]
_close.restype = FtStatus

_get_device_info = d2lib.FT_GetDeviceInfo
_get_device_info.argtypes = [
    c_void_p,
    POINTER(c_uint),
    POINTER(c_uint),
    c_char_p,
    c_char_p,
    c_void_p,
]
_get_device_info.restype = FtStatus

_get_driver_version = d2lib.FT_GetDriverVersion
_get_driver_version.argtypes = [c_void_p, POINTER(c_uint)]
_get_driver_version.restype = FtStatus

_purge = d2lib.FT_Purge
_purge.argtypes = [c_void_p, c_uint]
_purge.restype = FtStatus

_reset_device = d2lib.FT_ResetDevice
_reset_device.argtypes = [c_void_p]
_reset_device.restype = FtStatus

# Constants

# Max. length of C string containing D2XX device serial number,
# according to the D2XX documentation
_SERIAL_NUMBER_MAX_LEN: Final[int] = 16
# Max. length of C string containing D2XX device description,
# according to the D2XX documentation
_DESCRIPTION_MAX_LEN: Final[int] = 64

# Data types


class _RawDeviceInfoListNode(Structure):
    _fields_ = [
        ("flags", c_uint),
        ("type", c_uint),
        ("id", c_uint),
        ("loc_id", c_uint),
        ("serial_number", c_char * _SERIAL_NUMBER_MAX_LEN),
        ("description", c_char * _DESCRIPTION_MAX_LEN),
        ("handle", c_void_p),
    ]


class DeviceFlags(IntFlag):
    """Class representing the D2XX 'device information flags' enum."""

    OPEN = 1
    """Device is currently opened."""
    HIGH_SPEED = 2
    """Device is using USB High-Speed signaling rate."""


class DeviceType(IntEnum):
    """Class representing the 'FT_DEVICE' D2XX enum."""

    DEV_BM = 0
    DEV_AM = auto()
    DEV_100AX = auto()
    DEV_UNKNOWN = auto()
    DEV_2232C = auto()
    DEV_232R = auto()
    DEV_2232H = auto()
    DEV_4232H = auto()
    DEV_232H = auto()
    DEV_X_SERIES = auto()
    DEV_4222H_0 = auto()
    DEV_4222H_1_2 = auto()
    DEV_4222H_3 = auto()
    DEV_4222_PROG = auto()
    DEV_900 = auto()
    DEV_930 = auto()
    DEV_UMFTPD3A = auto()


class DeviceInfo(NamedTuple):
    """NamedTuple encapsulating the 'FT_DEVICE_INFO_LIST_NODE' D2XX data struct."""

    flags: DeviceFlags
    """Special device flags. See 'DeviceFlags'."""
    dev_type: DeviceType
    """Device type. See 'DeviceType'."""
    idx: int
    """Device index in device information list."""
    loc_id: int
    """Device USB Location ID."""
    serial_number: str
    """Serial number of the device."""
    description: str
    """Device description."""
    handle: FtHandle
    """A C pointer to device handle; NULL if not opened"""

    @classmethod
    def from_raw(cls, raw_node: _RawDeviceInfoListNode) -> "DeviceInfo":
        return cls(
            flags=DeviceFlags(raw_node.flags),
            dev_type=DeviceType(raw_node.type),
            idx=raw_node.id,
            loc_id=raw_node.loc_id,
            serial_number=raw_node.serial_number.decode("utf-8"),
            description=raw_node.description.decode("utf-8"),
            handle=FtHandle(raw_node.handle),
        )


class DriverVersion(NamedTuple):
    """NamedTuple encapsulating the driver version information."""

    major: int
    minor: int
    build_version: int


class _OpenExFlag(IntEnum):
    BY_SERIAL_NUMBER = 1
    BY_DESCRIPTION = 2
    BY_LOCATION = 4


class BufferType(IntFlag):
    """Enum for selecting the buffer purge type."""

    RX = 1
    """Purge receive buffers."""
    TX = 2
    """Purge transmit buffers."""


class ShortDeviceInfo(NamedTuple):
    """NamedTuple encapsulating the short device information."""

    dev_type: DeviceType
    """Device type. See 'DeviceType' enum."""
    dev_idx: int
    """Device index in device information list."""
    serial_number: str
    """Device serial number."""
    description: str
    """Device description"""


def create_device_info_list() -> int:
    """Create a device info list.

    This function builds a device information list and returns
    the number of D2XX devices connected to the system.
    The list contains information about both unopened and open devices.

    An application can use this function to get the number
    of devices attached to the system.
    It can then allocate space for the device information list
    and retrieve the list using get_device_info_list.
    If the devices connected to the system change,
    the device info list will not be updated until
    'create_device_info_list()' is called again.

    Raises:
        FtException:    In case of unexpected error

    Returns:
        int:            Number of connected D2XX devices
    """
    dev_count = c_uint()
    result: FtStatus = _create_device_info_list(byref(dev_count))

    if result != FtStatus.OK:
        raise FtException(result)

    return dev_count.value


def get_device_info_list() -> list[DeviceInfo]:
    """Return list containing details about connected D2XX devices.

    This function returns a device information list containing information
    about all connected D2XX devices.

    Args:
        dev_count:          Max. number of devices to construct list for

    Raises:
        FtException:        In case of unexpected error

    Returns:
        list[DeviceInfo]:   List containing details about connected D2XX devices
    """
    dev_count = create_device_info_list()

    array_elem_count = c_uint(dev_count)
    raw_list = (_RawDeviceInfoListNode * dev_count)()

    result: FtStatus = _get_device_info_list(raw_list, byref(array_elem_count))

    if result != FtStatus.OK:
        raise FtException(result)

    return list(map(DeviceInfo.from_raw, raw_list))[: array_elem_count.value]


def get_device_info_detail(dev_idx: int) -> Result[DeviceInfo, FtStatus]:
    """This function returns an entry from the device information list.

    Args:
        dev_id:         Index of device in device info list (non-negative)

    Raises:
        FtException:    In case of unexpected error

    Returns:
        device details (if id exists)
    """
    assert 0 <= dev_idx <= (2**31) - 1, "Device ID must be a non-negative integer"

    idx = c_uint(dev_idx)
    flags = c_uint()
    dev_type = c_uint()
    idx = c_uint()
    loc_id = c_uint()
    serial_number = create_string_buffer(_SERIAL_NUMBER_MAX_LEN)
    description = create_string_buffer(_DESCRIPTION_MAX_LEN)
    handle = c_void_p()

    result: FtStatus = _get_device_info_detail(
        idx,
        byref(flags),
        byref(dev_type),
        byref(idx),
        byref(loc_id),
        serial_number,
        description,
        byref(handle),
    )

    if result != FtStatus.OK:
        return Err(result)

    return Ok(
        DeviceInfo(
            flags=DeviceFlags(flags.value),
            dev_type=DeviceType(dev_type.value),
            idx=idx.value,
            loc_id=loc_id.value,
            serial_number=serial_number.value.decode("utf-8"),
            description=description.value.decode("utf-8"),
            handle=FtHandle(handle),
        )
    )


def open_by_idx(dev_idx: int) -> Result[FtHandle, FtStatus]:
    """Open the device using 'device index' and return a device handle.

    NOTE:
        Although this function can be used to open multiple devices
        by setting iDevice to 0, 1, 2 etc., there is no ability to open
        a specific device.
        To open named devices, use functions: 'open_by_serial()',
        'open_by_description()', 'open_by_location()'.

    Args:
        dev_id:     D2XX device index

    Returns:
        D2XX device handle (optional)
    """
    assert 0 <= dev_idx <= (2**31) - 1, "Device ID must be a non-negative integer"

    ft_handle = c_void_p()
    result: FtStatus = _open(dev_idx, byref(ft_handle))

    if result != FtStatus.OK:
        return Err(result)

    return Ok(FtHandle(ft_handle))


def open_by_serial(serial_num: str) -> Result[FtHandle, FtStatus]:
    """Open the specified device using 'serial number' and return a device handle.

    The device is specified by its serial number.

    This function can also be used to open multiple devices simultaneously.

    Args:
        serial_num:     Serial number of the D2XX device

    Returns:
        D2XX device handle (optional)
    """
    ft_handle = c_void_p()
    result: FtStatus = _open_ex(
        serial_num.encode("utf-8"), _OpenExFlag.BY_SERIAL_NUMBER, byref(ft_handle)
    )

    if result != FtStatus.OK:
        return Err(result)

    return Ok(FtHandle(ft_handle))


def open_by_description(dev_description: str) -> Result[FtHandle, FtStatus]:
    """Open the specified device using 'device description' and return a device handle.

    The device is specified by its description string.

    This function can also be used to open multiple devices simultaneously.

    Arguments:
        dev_description:    Description string of the D2XX device

    Return:
        D2XX device handle (optional)
    """
    ft_handle = c_void_p()
    result: FtStatus = _open_ex(
        dev_description.encode("utf-8"), _OpenExFlag.BY_DESCRIPTION, byref(ft_handle)
    )

    if result != FtStatus.OK:
        return Err(result)

    return Ok(FtHandle(ft_handle))


# This function is not supported on Linux and Windows CE
# REVIEW: Windows CE is unsupported by Python so no need to check?
if OS_TYPE != "Linux":

    def open_by_location(location_id: int) -> Result[FtHandle, FtStatus]:
        """Open the specified device using 'location ID' and return a device handle.

        The device is specified by its location ID.

        This function can also be used to open multiple devices simultaneously.

        Note:
            This method is not supported on Windows CE and Linux.

        Arguments:
            location_id:    Location ID of the D2XX device

        Returns:
            Result[FtHandle, FtStatus]: D2XX device handle (if location exists)
        """
        ft_handle = c_void_p()
        result: FtStatus = _open_ex(
            location_id, _OpenExFlag.BY_LOCATION, byref(ft_handle)
        )

        if result != FtStatus.OK:
            return Err(result)

        return Ok(FtHandle(ft_handle))


def close_handle(ft_handle: FtHandle) -> None:
    """Close an open device.

    Args:
        ft_handle:      Handle to an opened D2XX device

    Raises:
        FtException:    In case of unexpected error
    """
    result: FtStatus = _close(ft_handle)

    if result not in [
        FtStatus.OK,
        FtStatus.DEVICE_NOT_OPENED,
        FtStatus.INVALID_HANDLE,
        FtStatus.DEVICE_NOT_FOUND,
    ]:
        raise FtException(result)


def get_device_info(ft_handle: FtHandle) -> Result[ShortDeviceInfo, FtStatus]:
    """Get device information for an opened device.

    Args:
        ft_handle:          Handle to an opened D2XX device

    Raises:
        FtException:        In case of unexpected error

    Returns:
        ShortDeviceInfo:    Short device info
    """
    dev_type = c_uint()
    dev_id = c_uint()
    serial_number = create_string_buffer(_SERIAL_NUMBER_MAX_LEN)
    description = create_string_buffer(_DESCRIPTION_MAX_LEN)

    result: FtStatus = _get_device_info(
        ft_handle, byref(dev_type), byref(dev_id), serial_number, description, None
    )

    if result != FtStatus.OK:
        return Err(result)

    return Ok(
        ShortDeviceInfo(
            dev_type=DeviceType(dev_type.value),
            dev_idx=dev_id.value,
            serial_number=serial_number.value.decode("utf-8"),
            description=description.value.decode("utf-8"),
        )
    )


if OS_TYPE == "Windows":

    def get_driver_version(ft_handle: FtHandle) -> DriverVersion:
        """This function returns the D2XX driver version number.

        Args:
            ft_handle:      Handle to an opened D2XX device

        Raises:
            FtException:    In case of unexpected error

        Returns:
            DriverVersion:  Tuple containing detailed driver version information
        """
        driver_version = c_uint32()

        result: FtStatus = _get_driver_version(ft_handle, byref(driver_version))

        if result != FtStatus.OK:
            raise FtException(result)

        return DriverVersion(
            build_version=driver_version.value & 0xFF,
            minor=(driver_version.value >> 8) & 0xFF,
            major=(driver_version.value >> 16) & 0xFF,
        )


def purge_buffers(ft_handle: FtHandle, purge_type_mask: BufferType) -> None:
    """This function purges receive and transmit buffers in the device.

    Args:
        ft_handle:          Handle to an opened D2XX device
        purge_type_mask:    Which buffers to purge (Tx and/or Rx)

    Raises:
        FtException:        In case of unexpected error
    """
    result: FtStatus = _purge(ft_handle, purge_type_mask)

    if result not in {
        FtStatus.OK,
        FtStatus.INVALID_HANDLE,
        FtStatus.DEVICE_NOT_FOUND,
        FtStatus.DEVICE_NOT_OPENED,
    }:
        raise FtException(result)


def reset_device(ft_handle: FtHandle) -> None:
    """This function sends a reset command to the device.

    Args:
        ft_handle:      Handle to an opened D2XX device

    Raises:
        FtException:    In case of unexpected error
    """
    result: FtStatus = _reset_device(ft_handle)

    if result not in {
        FtStatus.OK,
        FtStatus.INVALID_HANDLE,
        FtStatus.DEVICE_NOT_FOUND,
        FtStatus.DEVICE_NOT_OPENED,
    }:
        raise FtException(result)
