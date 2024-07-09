import pyft4222.wrapper.ftd2xx as ftd
from pyft4222.result import Ok
from pyft4222.wrapper import FtHandle

from ..fixtures import *


def test_list_devices() -> None:
    devices = ftd.get_device_info_list()
    assert len(devices) > 0


class TestOpenFunctions:
    def test_device_info_detail(self, valid_dev: ftd.DeviceInfo):
        dev_info = ftd.get_device_info_detail(valid_dev.idx)
        assert isinstance(dev_info, Ok)
        assert dev_info.val.dev_type in FT4222_DEV_TYPES

    def test_open_by_idx(self, valid_dev_idx: int):
        handle = ftd.open_by_idx(valid_dev_idx)
        assert isinstance(handle, Ok)
        assert handle.val is not None

        # Cleanup
        ftd.close_handle(handle.val)

    def test_open_by_serial(self, valid_dev: ftd.DeviceInfo):
        handle = ftd.open_by_serial(valid_dev.serial_number)
        assert isinstance(handle, Ok)
        assert handle.val is not None

        # Cleanup
        ftd.close_handle(handle.val)

    def test_open_by_description(self, valid_dev: ftd.DeviceInfo):
        handle = ftd.open_by_description(valid_dev.description)
        assert isinstance(handle, Ok)
        assert handle.val is not None

        # Cleanup
        ftd.close_handle(handle.val)


def test_close_handle(open_handle: FtHandle):
    ftd.close_handle(open_handle)


def test_get_device_info(open_handle: FtHandle):
    result = ftd.get_device_info(open_handle)
    assert result is not None


def test_purge_buffers(open_handle: FtHandle):
    buftypes = [
        ftd.BufferType.RX,
        ftd.BufferType.TX,
        ftd.BufferType.RX | ftd.BufferType.TX,
    ]

    for buftype in buftypes:
        ftd.purge_buffers(open_handle, buftype)


def test_reset_device(open_handle: FtHandle):
    ftd.reset_device(open_handle)
