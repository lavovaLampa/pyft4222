#! /usr/bin/env python3

from ctypes import *
from enum import IntEnum, IntFlag, auto
from typing import Final, List, NamedTuple, Optional

from ft_common import FTStatus, FtHandle

try:
    ftlib = cdll.LoadLibrary('./lib/libft4222.so.1.4.4.44')
except OSError as e:
    print("Unable to load shared library!")
    exit(1)

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

SERIAL_NUMBER_MAX_LEN: Final[int] = 16
DESCRIPTION_MAX_LEN: Final[int] = 64

# Data types


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


class _RawDeviceInfoListNode(Structure):
    _fields_ = [
        ('Flags', c_uint),
        ('Type', c_uint),
        ('ID', c_uint),
        ('LocId', c_uint),
        ('SerialNumber', c_char * SERIAL_NUMBER_MAX_LEN),
        ('Description', c_char * DESCRIPTION_MAX_LEN),
        ('Handle', c_void_p)
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
            flags=DeviceFlags(raw_node.Flags),
            type=DeviceType(raw_node.Type),
            id=raw_node.ID,
            loc_id=raw_node.LocId,
            serial_number=raw_node.SerialNumber,
            description=raw_node.Description,
            handle=raw_node.Handle
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
    dev_count = c_uint()
    result: FTStatus = _create_device_info_list(byref(dev_count))

    if result != FTStatus.OK:
        raise RuntimeError("TODO")

    return dev_count.value


def get_device_info_list(dev_count: int) -> List[DeviceInfo]:
    array_elems = c_uint(dev_count)
    raw_list = (_RawDeviceInfoListNode * dev_count)()
    result: FTStatus = _get_device_info_list(raw_list, byref(array_elems))

    if result != FTStatus.OK:
        raise RuntimeError("TODO")

    return list(map(DeviceInfo.from_raw, raw_list))[:array_elems.value]


def get_device_info_detail(dev_id: int) -> DeviceInfo:
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
    ft_handle = c_void_p()
    result: FTStatus = _open(dev_id, byref(ft_handle))

    if result != FTStatus.OK:
        raise RuntimeError("TODO")

    return FtHandle(ft_handle)


def open_by_serial(serial_num: str) -> Optional[FtHandle]:
    ft_handle = c_void_p()
    result: FTStatus = _open_ex(
        c_wchar_p(serial_num),
        _OpenExFlag.BY_SERIAL_NUMBER.value,
        byref(ft_handle)
    )

    if result != FTStatus.OK:
        raise RuntimeError("TODO")

    return FtHandle(ft_handle)


def open_by_description(dev_description: str) -> Optional[FtHandle]:
    ft_handle = c_void_p()
    result: FTStatus = _open_ex(
        c_wchar_p(dev_description),
        _OpenExFlag.BY_DESCRIPTION,
        byref(ft_handle)
    )

    if result != FTStatus.OK:
        raise RuntimeError("TODO")

    return FtHandle(ft_handle)


def open_by_location(location: int) -> Optional[FtHandle]:
    ft_handle = c_void_p()
    result: FTStatus = _open_ex(
        location,
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
    result: FTStatus = _close(ft_handle)

    if result != FTStatus.OK:
        raise RuntimeError("TODO")


def get_device_info(ft_handle: FtHandle) -> ShortDeviceInfo:
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


def get_driver_version(ft_handle: FtHandle) -> int:
    driver_version = c_uint()

    result: FTStatus = _get_driver_version(ft_handle, byref(driver_version))

    if result != FTStatus.OK:
        raise RuntimeError("TODO")

    return driver_version.value


def purge(ft_handle: FtHandle, purge_type_mask: PurgeType) -> None:
    result: FTStatus = _purge(ft_handle, purge_type_mask)

    if result != FTStatus.OK:
        raise RuntimeError("TODO")


def reset_device(ft_handle: FtHandle) -> None:
    result: FTStatus = _reset_device(ft_handle)

    if result != FTStatus.OK:
        raise RuntimeError("TODO")


def main() -> None:
    result = create_device_info_list()
    print(get_device_info_detail(0))


if __name__ == '__main__':
    main()
