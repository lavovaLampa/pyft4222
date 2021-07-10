#! /usr/bin/env python3

from ctypes import *
from enum import IntEnum, IntFlag, auto
from typing import Final, NamedTuple, Optional

from .ft_common import FTStatus, FtHandle

try:
    ftlib = cdll.LoadLibrary('./lib/libft4222.so.1.4.4.44')
except OSError as e:
    print("Unable to load shared library!")
    exit(1)


_create_device_info_list = ftlib.FT_CreateDeviceInfo_list
_create_device_info_list.argtypes = [POINTER(c_uint)]
_create_device_info_list.restype = FTStatus


def create_device_info_list() -> int:
    dev_count = c_uint()
    result: FTStatus = _create_device_info_list(byref(dev_count))

    if result != FTStatus.OK:
        raise RuntimeError("TODO")

    return dev_count.value


class DeviceInfoListNode(NamedTuple):
    flags: int
    type: int
    id: int
    loc_id: int
    serial_number: str
    description: str
    handle: FtHandle


_get_device_info_list = ftlib.FT_GetDeviceInfoList
_get_device_info_list.argtypes = []
_get_device_info_list.restype = FTStatus


def get_device_info_list() -> None:
    pass


_get_device_info_detail = ftlib.FT_GetDeviceInfoDetail
_get_device_info_detail.argtypes = []
_get_device_info_detail.restype = FTStatus


def get_device_info_detail() -> None:
    pass


_open = ftlib.FT_Open
_open.argtypes = [c_int, POINTER(c_void_p)]
_open.restype = FTStatus


def open(dev_id: int) -> Optional[FtHandle]:
    ft_handle = c_void_p()
    result: FTStatus = _open(dev_id, byref(ft_handle))

    if result != FTStatus.OK:
        raise RuntimeError("TODO")

    return FtHandle(ft_handle)


class _OpenExFlag(IntEnum):
    BY_SERIAL_NUMBER = 1
    BY_DESCRIPTION = 2
    BY_LOCATION = 4


_open_ex = ftlib.FT_OpenEx
_open_ex.argtypes = [c_void_p, c_uint, POINTER(c_void_p)]
_open_ex.restype = FTStatus


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

    if result != FTStatus.OK:
        raise RuntimeError("TODO")

    return FtHandle(ft_handle)


_close = ftlib.FT_Close
_close.argtypes = [c_void_p]
_close.restype = FTStatus


def close(ft_handle: FtHandle) -> None:
    pass


class FtDeviceType(IntEnum):
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
    dev_type: FtDeviceType
    dev_id: int
    serial_number: str
    description: str


DESCRIPTION_MAX_LEN: Final[int] = 64
SERIAL_NUMBER_MAX_LEN: Final[int] = 16


_get_device_info = ftlib.FT_GetDeviceInfo
_get_device_info.argtypes = [c_void_p, POINTER(
    c_uint), POINTER(c_uint), c_char_p, c_char_p, c_void_p]
_get_device_info.restype = FTStatus


def get_device_info(ft_handle: FtHandle, ) -> DeviceInfo:
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

    return DeviceInfo(
        dev_type=FtDeviceType(dev_type.value),
        dev_id=dev_id.value,
        serial_number=serial_number.value,
        description=description.value
    )


_get_driver_version = ftlib.FT_GetDriverVersion
_get_driver_version.argtypes = [c_void_p, POINTER(c_uint)]
_get_driver_version.restype = FTStatus


def get_driver_version(ft_handle: FtHandle) -> int:
    driver_version = c_uint()

    result: FTStatus = _get_driver_version(ft_handle, byref(driver_version))

    if result != FTStatus.OK:
        raise RuntimeError("TODO")

    return driver_version.value


class PurgeType(IntFlag):
    RX = 1
    TX = 2


_purge = ftlib.FT_Purge
_purge.argtypes = [c_void_p, c_uint]
_purge.restype = FTStatus


def purge(ft_handle: FtHandle, purge_type_mask: PurgeType) -> None:
    result: FTStatus = _purge(FtHandle, purge_type_mask)

    if result != FTStatus.OK:
        raise RuntimeError("TODO")


_reset_device = ftlib.FT_ResetDevice
_reset_device.argtypes = [c_void_p]
_reset_device.restype = FTStatus


def reset_device(ft_handle: FtHandle) -> None:
    result: FTStatus = _reset_device(ft_handle)

    if result != FTStatus.OK:
        raise RuntimeError("TODO")
