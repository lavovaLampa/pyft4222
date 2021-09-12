import pytest
from typing import Final

from tests.fixtures import open_serial_io_handle

from pyft4222.wrapper.i2c import master as i2c_master
from pyft4222.wrapper.common import FtHandle
from pyft4222 import ResType

_TEST_DEVICE_ADDR: Final[int] = 0x40


@pytest.fixture
def i2c_master_handle(open_serial_io_handle: FtHandle) -> i2c_master.I2cMasterHandle:
    result = i2c_master.init(open_serial_io_handle, 3400)
    if result.tag == ResType.OK:
        return result.ok
    else:
        raise RuntimeError("Cannot initialize I2C Master handle!")


def test_init(open_serial_io_handle: FtHandle):
    result = i2c_master.init(open_serial_io_handle, 3400)
    assert result.tag == ResType.OK


def test_read(i2c_master_handle: i2c_master.I2cMasterHandle):
    read_data = i2c_master.read(i2c_master_handle, _TEST_DEVICE_ADDR, 300)
    assert len(read_data) == 300


def test_write(i2c_master_handle: i2c_master.I2cMasterHandle):
    data_to_write = bytes([0xFF, 0x01, 0x02, 0x03, 0xDE, 0xAD, 0xBE, 0xEF])
    bytes_written = i2c_master.write(
        i2c_master_handle, _TEST_DEVICE_ADDR, data_to_write
    )
    assert bytes_written == len(data_to_write)


def test_read_ex(i2c_master_handle: i2c_master.I2cMasterHandle):
    read_length = 40
    read_data = i2c_master.read_ex(
        i2c_master_handle,
        _TEST_DEVICE_ADDR,
        i2c_master.TransactionFlag.NONE,
        read_length,
    )
    assert len(read_data) == read_length


def test_write_ex(i2c_master_handle: i2c_master.I2cMasterHandle):
    data_to_write = bytes([0xFF, 0x01, 0x02, 0x03, 0xDE, 0xAD, 0xBE, 0xEF])
    bytes_written = i2c_master.write_ex(
        i2c_master_handle,
        _TEST_DEVICE_ADDR,
        i2c_master.TransactionFlag.NONE,
        data_to_write,
    )
    assert bytes_written == len(data_to_write)


def test_get_status(i2c_master_handle: i2c_master.I2cMasterHandle):
    status = i2c_master.get_status(i2c_master_handle)
    assert status == i2c_master.CtrlStatus.IDLE


def test_reset(i2c_master_handle: i2c_master.I2cMasterHandle):
    i2c_master.reset(i2c_master_handle)


def test_reset_bus(i2c_master_handle: i2c_master.I2cMasterHandle):
    i2c_master.reset_bus(i2c_master_handle)
