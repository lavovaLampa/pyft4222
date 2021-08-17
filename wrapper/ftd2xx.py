from ctypes import POINTER, byref, create_string_buffer, Structure
from ctypes import c_uint, c_void_p, c_int, c_char_p, c_char, c_uint32

from enum import IntEnum, IntFlag, auto
from typing import Final, List, NamedTuple, Optional

from .dll_loader import ftlib
from . import FtHandle, Ok, Err, Result, SYSTEM_TYPE


class FtStatus(IntEnum):
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


class FtException(Exception):
    status: FtStatus
    msg: Optional[str]

    def __init__(self, status: FtStatus, msg: Optional[str] = None):
        self.status = status
        self.msg = msg

    def __str__(self) -> str:
        return f"""
Exception during call to FTD2XX library.
FT return code: {self.status.name}
Message: {self.msg}
        """

# DLL function protoypes declaration


_create_device_info_list = ftlib.FT_CreateDeviceInfoList
_create_device_info_list.argtypes = [POINTER(c_uint)]
_create_device_info_list.restype = FtStatus

_get_device_info_list = ftlib.FT_GetDeviceInfoList
_get_device_info_list.argtypes = []
_get_device_info_list.restype = FtStatus

_get_device_info_detail = ftlib.FT_GetDeviceInfoDetail
_get_device_info_detail.argtypes = []
_get_device_info_detail.restype = FtStatus

_open = ftlib.FT_Open
_open.argtypes = [c_int, POINTER(c_void_p)]
_open.restype = FtStatus

_open_ex = ftlib.FT_OpenEx
_open_ex.argtypes = [c_void_p, c_uint, POINTER(c_void_p)]
_open_ex.restype = FtStatus

_close = ftlib.FT_Close
_close.argtypes = [c_void_p]
_close.restype = FtStatus

_get_device_info = ftlib.FT_GetDeviceInfo
_get_device_info.argtypes = [c_void_p, POINTER(
    c_uint), POINTER(c_uint), c_char_p, c_char_p, c_void_p]
_get_device_info.restype = FtStatus

_get_driver_version = ftlib.FT_GetDriverVersion
_get_driver_version.argtypes = [c_void_p, POINTER(c_uint)]
_get_driver_version.restype = FtStatus

_purge = ftlib.FT_Purge
_purge.argtypes = [c_void_p, c_uint]
_purge.restype = FtStatus

_reset_device = ftlib.FT_ResetDevice
_reset_device.argtypes = [c_void_p]
_reset_device.restype = FtStatus

# Constants

# Max. length of C string containing D2XX device serial number (according to D2XX documentation)
SERIAL_NUMBER_MAX_LEN: Final[int] = 16
# Max. length of C string containing D2XX device description (according to D2XX documentation)
DESCRIPTION_MAX_LEN: Final[int] = 64

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
            serial_number=raw_node.serial_number.decode('utf-8'),
            description=raw_node.description.decode('utf-8'),
            handle=FtHandle(raw_node.handle)
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


def get_device_info_list() -> List[DeviceInfo]:
    """Return list containing details about connected D2XX devices.

    This function returns a device information list and the number of D2XX devices in the list.

    Args:
        dev_count:          Max. number of devices to construct list for

    Raises:
        FtException:        In case of unexpected error

    Return:
        List[DeviceInfo]:   List containing details about connected D2XX devices
    """
    dev_count = create_device_info_list()

    array_elems = c_uint(dev_count)
    raw_list = (_RawDeviceInfoListNode * dev_count)()

    result: FtStatus = _get_device_info_list(raw_list, byref(array_elems))

    if result != FtStatus.OK:
        raise FtException(result)

    return list(map(DeviceInfo.from_raw, raw_list))[:array_elems.value]


def get_device_info_detail(dev_id: int) -> Optional[DeviceInfo]:
    """This function returns an entry from the device information list.

    Args:
        dev_id:         Index of device in device info list (non-negative)

    Raises:
        FtException:    In case of unexpected error

    Returns:
        device details (if id exists)
    """
    assert 0 <= dev_id <= (2 ** 31) - 1,\
        "Device ID must be a non-negative integer"

    idx = c_uint(dev_id)
    flags = c_uint()
    type = c_uint()
    id = c_uint()
    loc_id = c_uint()
    serial_number = create_string_buffer(SERIAL_NUMBER_MAX_LEN)
    description = create_string_buffer(DESCRIPTION_MAX_LEN)
    handle = c_void_p()

    result: FtStatus = _get_device_info_detail(
        idx,
        byref(flags),
        byref(type),
        byref(id),
        byref(loc_id),
        serial_number,
        description,
        byref(handle)
    )

    if result == FtStatus.OK:
        return DeviceInfo(
            flags=DeviceFlags(flags.value),
            type=DeviceType(type.value),
            id=id.value,
            loc_id=loc_id.value,
            serial_number=serial_number.value.decode('utf-8'),
            description=description.value.decode('utf-8'),
            handle=FtHandle(handle)
        )
    elif result in {FtStatus.DEVICE_NOT_FOUND, FtStatus.INVALID_HANDLE}:
        return None
    else:
        raise FtException(result)


def open(dev_id: int) -> Result[FtHandle, FtStatus]:
    """Open the device and return a handle which will be used for subsequent accesses.

    NOTE:
        Although this function can be used to open multiple devices by setting iDevice to 0, 1, 2 etc.
        there is no ability to open a specific device.
        To open named devices, use functions: 'open_by_serial', 'open_by_description', 'open_by_location'

    Args:
        dev_id:     ID of D2XX device to open

    Returns:
        D2XX device handle (optional)
    """
    assert 0 <= dev_id <= (2 ** 31) - 1,\
        "Device ID must be a non-negative integer"

    ft_handle = c_void_p()
    result: FtStatus = _open(dev_id, byref(ft_handle))

    if result == FtStatus.OK:
        return Ok(FtHandle(ft_handle))
    else:
        return Err(result)


def open_by_serial(serial_num: str) -> Result[FtHandle, FtStatus]:
    """Open the specified device and return a handle that will be used for subsequent accesses.
    The device is specified by its serial number.

    This function can also be used to open multiple devices simultaneously.

    Args:
        serial_num:     Serial number of the D2XX device

    Returns:
        D2XX device handle (optional)
    """
    ft_handle = c_void_p()
    result: FtStatus = _open_ex(
        serial_num.encode('utf-8'),
        _OpenExFlag.BY_SERIAL_NUMBER,
        byref(ft_handle)
    )

    if result == FtStatus.OK:
        return Ok(FtHandle(ft_handle))
    else:
        return Err(result)


def open_by_description(dev_description: str) -> Result[FtHandle, FtStatus]:
    """Open the specified device and return a handle that will be used for subsequent accesses.
    The device is specified by its description string.

    This function can also be used to open multiple devices simultaneously.

    Arguments:
        dev_description:    Description string of the D2XX device

    Return:
        D2XX device handle (optional)
    """
    ft_handle = c_void_p()
    result: FtStatus = _open_ex(
        dev_description.encode('utf-8'),
        _OpenExFlag.BY_DESCRIPTION,
        byref(ft_handle)
    )

    if result == FtStatus.OK:
        return Ok(FtHandle(ft_handle))
    else:
        return Err(result)


# This function is not supported on Linux and Windows CE
# REVIEW: Windows CE is unsupported by Python so no need to check?
if SYSTEM_TYPE != "Linux":
    def open_by_location(location_id: int) -> Result[FtHandle, FtStatus]:
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
        result: FtStatus = _open_ex(
            location_id,
            _OpenExFlag.BY_LOCATION,
            byref(ft_handle)
        )

        if result == FtStatus.OK:
            return Ok(FtHandle(ft_handle))
        else:
            return Err(result)


def close(ft_handle: FtHandle) -> None:
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


def get_device_info(ft_handle: FtHandle) -> Optional[ShortDeviceInfo]:
    """Get device information for an open device.

    Args:
        ft_handle:          Handle to an opened D2XX device

    Raises:
        FtException:        In case of unexpected error

    Returns:
        ShortDeviceInfo:    Short device info
    """
    dev_type = c_uint()
    dev_id = c_uint()
    serial_number = create_string_buffer(SERIAL_NUMBER_MAX_LEN)
    description = create_string_buffer(DESCRIPTION_MAX_LEN)

    result: FtStatus = _get_device_info(
        ft_handle,
        byref(dev_type),
        byref(dev_id),
        serial_number,
        description,
        None
    )

    if result == FtStatus.OK:
        return ShortDeviceInfo(
            dev_type=DeviceType(dev_type.value),
            dev_id=dev_id.value,
            serial_number=serial_number.value.decode('utf-8'),
            description=description.value.decode('utf-8')
        )
    elif result in {
        FtStatus.DEVICE_NOT_FOUND,
        FtStatus.DEVICE_NOT_OPENED,
        FtStatus.INVALID_HANDLE
    }:
        return None
    else:
        raise FtException(result)


class DriverVersion(NamedTuple):
    major: int
    minor: int
    build_version: int


if SYSTEM_TYPE == "Windows":
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

        result: FtStatus = _get_driver_version(
            ft_handle, byref(driver_version))

        if result != FtStatus.OK:
            raise FtException(result)

        return DriverVersion(
            build_version=driver_version.value & 0xFF,
            minor=(driver_version.value >> 8) & 0xFF,
            major=(driver_version.value >> 16) & 0xFF
        )


def purge(ft_handle: FtHandle, purge_type_mask: PurgeType) -> None:
    """This function purges receive and transmit buffers in the device.

    Args:
        ft_handle:          Handle to an opened D2XX device
        purge_type_mask:    Which buffers to purge (Tx and/or Rx)

    Raises:
        FtException:        In case of unexpected error
    """
    result: FtStatus = _purge(ft_handle, purge_type_mask)

    if result not in {
        FtStatus.OK, FtStatus.INVALID_HANDLE,
        FtStatus.DEVICE_NOT_FOUND, FtStatus.DEVICE_NOT_OPENED
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
        FtStatus.OK, FtStatus.INVALID_HANDLE,
        FtStatus.DEVICE_NOT_FOUND, FtStatus.DEVICE_NOT_OPENED
    }:
        raise FtException(result)
