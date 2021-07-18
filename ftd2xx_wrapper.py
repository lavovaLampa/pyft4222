#! /usr/bin/env python3

from ctypes import *
from enum import IntEnum, IntFlag, auto
from typing import Final, List, NamedTuple, Optional
import platform

from ft_common import FtHandle

try:
    ftlib = cdll.LoadLibrary('./lib/libft4222.so.1.4.4.44')
except OSError as e:
    print("Unable to load shared library!")
    exit(1)


class FTStatus(IntEnum):
    OK = 0
    INVALID_HANDLE = auto()
    DEVICE_NOT_FOUND = auto()
    DEVICE_NOT_OPENED = auto()
    IO_ERROR = auto()
    INSUFFICIENT_RESOURCES = auto()
    INVALID_PARAMETER = auto()
    INVALID_BAUD_RATE = auto()
    DEVICE_NOT_OPENED_FOR_ERASE = auto()
    DEVICE_NOT_OPENED_FOR_WRITE = auto()
    FAILED_TO_WRITE_DEVICE = auto()
    EEPROM_READ_FAILED = auto()
    EEPROM_WRITE_FAILED = auto()
    EEPROM_ERASE_FAILED = auto()
    EEPROM_NOT_PRESENT = auto()
    EEPROM_NOT_PROGRAMMED = auto()
    INVALID_ARGS = auto()
    NOT_SUPPORTED = auto()
    OTHER_ERROR = auto()
    DEVICE_LIST_NOT_READY = auto()

# DLL function protoypes declaration


_create_device_info_list = ftlib.FT_CreateDeviceInfoList
_create_device_info_list.argtypes = [POINTER(c_uint)]
_create_device_info_list.restype = FTStatus

_get_device_info_list = ftlib.FT_GetDeviceInfoList
_get_device_info_list.argtypes = []
_get_device_info_list.restype = FTStatus

_get_device_info_detail = ftlib.FT_GetDeviceInfoDetail
_get_device_info_detail.argtypes = []
_get_device_info_detail.restype = FTStatus

_open = ftlib.FT_Open
_open.argtypes = [c_int, POINTER(c_void_p)]
_open.restype = FTStatus

_open_ex = ftlib.FT_OpenEx
_open_ex.argtypes = [c_void_p, c_uint, POINTER(c_void_p)]
_open_ex.restype = FTStatus

_close = ftlib.FT_Close
_close.argtypes = [c_void_p]
_close.restype = FTStatus

_get_device_info = ftlib.FT_GetDeviceInfo
_get_device_info.argtypes = [c_void_p, POINTER(
    c_uint), POINTER(c_uint), c_char_p, c_char_p, c_void_p]
_get_device_info.restype = FTStatus

_get_driver_version = ftlib.FT_GetDriverVersion
_get_driver_version.argtypes = [c_void_p, POINTER(c_uint)]
_get_driver_version.restype = FTStatus

_purge = ftlib.FT_Purge
_purge.argtypes = [c_void_p, c_uint]
_purge.restype = FTStatus

_reset_device = ftlib.FT_ResetDevice
_reset_device.argtypes = [c_void_p]
_reset_device.restype = FTStatus

# Constants

# Max. length of C string containing D2XX device serial number (according to D2XX documentation)
SERIAL_NUMBER_MAX_LEN: Final[int] = 16
# Max. length of C string containing D2XX device description (according to D2XX documentation)
DESCRIPTION_MAX_LEN: Final[int] = 64
SYSTEM_TYPE: Final[str] = platform.system()

# Data types


class _RawDeviceInfoListNode(Structure):
    _fields_ = [
        ('flags', c_uint),
        ('type', c_uint),
        ('id', c_uint),
        ('loc_id', c_uint),
        ('serial_number', c_char * SERIAL_NUMBER_MAX_LEN),
        ('description', c_char * DESCRIPTION_MAX_LEN),
        ('handle', c_void_p)
    ]


class DeviceFlags(IntFlag):
    OPEN = 1
    HIGH_SPEED = 2


class DeviceType(IntEnum):
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
    flags: DeviceFlags
    type: DeviceType
    id: int
    loc_id: int
    serial_number: str
    description: str
    handle: FtHandle

    @staticmethod
    def from_raw(raw_node: _RawDeviceInfoListNode) -> 'DeviceInfo':
        return DeviceInfo(
            flags=DeviceFlags(raw_node.flags),
            type=DeviceType(raw_node.type),
            id=raw_node.id,
            loc_id=raw_node.loc_id,
            serial_number=raw_node.serial_number,
            description=raw_node.description,
            handle=raw_node.handle
        )


class _OpenExFlag(IntEnum):
    BY_SERIAL_NUMBER = 1
    BY_DESCRIPTION = 2
    BY_LOCATION = 4


class PurgeType(IntFlag):
    RX = 1
    TX = 2


class ShortDeviceInfo(NamedTuple):
    dev_type: DeviceType
    dev_id: int
    serial_number: str
    description: str


def create_device_info_list() -> int:
    """Create a device info list.

    This function builds a device information list and returns the number of D2XX devices connected to the system.
    The list contains information about both unopened and open devices.

    An application can use this function to get the number of devices attached to the system.
    It can then allocate space for the device information list and retrieve the list using get_device_info_list.
    If the devices connected to the system change,
    the device info list will not be updated until create_device_info_list is called again.

    Return:
        number of connected D2XX devices
    """
    dev_count = c_uint()
    result: FTStatus = _create_device_info_list(byref(dev_count))

    if result != FTStatus.OK:
        raise RuntimeError("TODO")

    return dev_count.value


def get_device_info_list(dev_count: int) -> List[DeviceInfo]:
    """Return list containing details about connected D2XX devices.

    This function returns a device information list and the number of D2XX devices in the list.

    NOTE: function 'create_device_info_list' must be called beforehand, to update the list!

    Return:
        list containing details about connected D2XX devices
    """
    array_elems = c_uint(dev_count)
    raw_list = (_RawDeviceInfoListNode * dev_count)()
    result: FTStatus = _get_device_info_list(raw_list, byref(array_elems))

    if result != FTStatus.OK:
        raise RuntimeError("TODO")

    return list(map(DeviceInfo.from_raw, raw_list))[:array_elems.value]


def get_device_info_detail(dev_id: int) -> DeviceInfo:
    """This function returns an entry from the device information list.

    Parameters:
        dev_id:     index of device in device info list

    Return:
        device details (if id exists)

    """
    idx = c_uint(dev_id)
    flags = c_uint()
    type = c_uint()
    id = c_uint()
    loc_id = c_uint()
    serial_number = create_string_buffer(SERIAL_NUMBER_MAX_LEN)
    description = create_string_buffer(DESCRIPTION_MAX_LEN)
    handle = c_void_p()

    result: FTStatus = _get_device_info_detail(
        idx,
        byref(flags),
        byref(type),
        byref(id),
        byref(loc_id),
        serial_number,
        description,
        byref(handle)
    )

    if result != FTStatus.OK:
        raise RuntimeError("TODO")

    return DeviceInfo(
        flags=DeviceFlags(flags.value),
        type=DeviceType(type.value),
        id=id.value,
        loc_id=loc_id.value,
        serial_number=serial_number.value,
        description=description.value,
        handle=FtHandle(handle)
    )


def open(dev_id: int) -> Optional[FtHandle]:
    """Open the device and return a handle which will be used for subsequent accesses.

    NOTE:
        Although this function can be used to open multiple devices by setting iDevice to 0, 1, 2 etc.
        there is no ability to open a specific device.
        To open named devices, use functions: 'open_by_serial', 'open_by_description', 'open_by_location'

    Parameters:
        dev_id:     ID of D2XX device to open

    Return:
        D2XX device handle (optional)
    """
    ft_handle = c_void_p()
    result: FTStatus = _open(dev_id, byref(ft_handle))

    if result != FTStatus.OK:
        raise RuntimeError("TODO")

    return FtHandle(ft_handle)


def open_by_serial(serial_num: str) -> Optional[FtHandle]:
    """Open the specified device and return a handle that will be used for subsequent accesses.
    The device is specified by its serial number.

    This function can also be used to open multiple devices simultaneously.

    Arguments:
        serial_num:     Serial number of the D2XX device

    Return:
        D2XX device handle (optional)
    """
    ft_handle = c_void_p()
    result: FTStatus = _open_ex(
        c_wchar_p(serial_num),
        _OpenExFlag.BY_SERIAL_NUMBER,
        byref(ft_handle)
    )

    if result != FTStatus.OK:
        raise RuntimeError("TODO")

    return FtHandle(ft_handle)


def open_by_description(dev_description: str) -> Optional[FtHandle]:
    """Open the specified device and return a handle that will be used for subsequent accesses.
    The device is specified by its description string.

    This function can also be used to open multiple devices simultaneously.

    Arguments:
        dev_description:    Description string of the D2XX device

    Return:
        D2XX device handle (optional)
    """
    ft_handle = c_void_p()
    result: FTStatus = _open_ex(
        c_wchar_p(dev_description),
        _OpenExFlag.BY_DESCRIPTION,
        byref(ft_handle)
    )

    if result != FTStatus.OK:
        raise RuntimeError("TODO")

    return FtHandle(ft_handle)


# This function is not supported on Linux and Windows CE
# REVIEW: Windows CE is unsupported by Python so no need to check?
if SYSTEM_TYPE != "Linux":
    def open_by_location(location_id: int) -> Optional[FtHandle]:
        """Open the specified device and return a handle that will be used for subsequent accesses.
        The device is specified by its location ID.

        This function can also be used to open multiple devices simultaneously.

        NOTE: This method is not supported on Windows CE and Linux.

        Arguments:
            location_id:    Location ID of the D2XX device

        Return:
            D2XX device handle (optional)
        """
        ft_handle = c_void_p()
        result: FTStatus = _open_ex(
            location_id,
            _OpenExFlag.BY_LOCATION,
            byref(ft_handle)
        )

        no_err_set = set([
            FTStatus.DEVICE_NOT_FOUND,
            FTStatus.INVALID_ARGS,
            FTStatus.NOT_SUPPORTED,
            FTStatus.INVALID_PARAMETER
        ])
        if result == FTStatus.OK:
            return FtHandle(ft_handle)
        elif result in no_err_set:
            return None
        else:
            raise RuntimeError("TODO")


def close(ft_handle: FtHandle) -> None:
    """Close an open device.

    Arguments:
        ft_handle:  Handle to an opened D2XX device
    """
    result: FTStatus = _close(ft_handle)

    if result != FTStatus.OK:
        raise RuntimeError("TODO")


def get_device_info(ft_handle: FtHandle) -> ShortDeviceInfo:
    """Get device information for an open device.

    Arguments:
        ft_handle:  Handle to an opened D2XX device

    Return:
        Short device info
    """
    dev_type = c_uint()
    dev_id = c_uint()
    serial_number = create_string_buffer(SERIAL_NUMBER_MAX_LEN)
    description = create_string_buffer(DESCRIPTION_MAX_LEN)

    result: FTStatus = _get_device_info(
        ft_handle,
        byref(dev_type),
        byref(dev_id),
        byref(serial_number),
        byref(description),
        None
    )

    if result != FTStatus.OK:
        raise RuntimeError("TODO")

    return ShortDeviceInfo(
        dev_type=DeviceType(dev_type.value),
        dev_id=dev_id.value,
        serial_number=serial_number.value,
        description=description.value
    )


class DriverVersion(NamedTuple):
    major: int
    minor: int
    build_version: int


if SYSTEM_TYPE == "Windows":
    def get_driver_version(ft_handle: FtHandle) -> DriverVersion:
        """This function returns the D2XX driver version number.

        Arguments:
            ft_handle:  Handle to an opened D2XX device

        Return:
            NamedTuple containing driver version information
        """
        driver_version = c_uint32()

        result: FTStatus = _get_driver_version(
            ft_handle, byref(driver_version))

        if result != FTStatus.OK:
            raise RuntimeError("TODO")

        return DriverVersion(
            build_version=driver_version.value & 0xFF,
            minor=(driver_version.value >> 8) & 0xFF,
            major=(driver_version.value >> 16) & 0xFF
        )


def purge(ft_handle: FtHandle, purge_type_mask: PurgeType) -> None:
    """This function purges receive and transmit buffers in the device.

    Arguments:
        ft_handle:  Handle to an opened D2XX device
    """
    result: FTStatus = _purge(ft_handle, purge_type_mask)

    if result != FTStatus.OK:
        raise RuntimeError("TODO")


def reset_device(ft_handle: FtHandle) -> None:
    """This function sends a reset command to the device.

    Arguments:
        ft_handle:  Handle to an opened D2XX device

    """
    result: FTStatus = _reset_device(ft_handle)

    if result != FTStatus.OK:
        raise RuntimeError("TODO")


def main() -> None:
    result = create_device_info_list()
    if result > 0:
        detail = get_device_info_detail(0)
        print(detail)


if __name__ == '__main__':
    main()
