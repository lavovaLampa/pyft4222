from typing import Final

import pytest

from pyft4222.result import Ok
from pyft4222.wrapper.common import FtHandle
from pyft4222.wrapper.i2c import slave as i2c_slave
from tests.fixtures import open_serial_io_handle

_PERIPHERAL_ADDR: Final[int] = 0x10


@pytest.fixture
def i2c_perif_handle(open_serial_io_handle: FtHandle) -> i2c_slave.I2cSlaveHandle:
    result = i2c_slave.init(open_serial_io_handle)
    if isinstance(result, Ok):
        return result.val
    else:
        raise RuntimeError("Cannot initialize I2C Peripheral handle!")


def test_init(open_serial_io_handle: FtHandle):
    result = i2c_slave.init(open_serial_io_handle)
    assert isinstance(result, Ok)


def test_reset(i2c_perif_handle: i2c_slave.I2cSlaveHandle):
    i2c_slave.reset(i2c_perif_handle)


def test_get_setaddress(i2c_perif_handle: i2c_slave.I2cSlaveHandle):
    i2c_slave.set_address(i2c_perif_handle, _PERIPHERAL_ADDR)
    curr_addr = i2c_slave.get_address(i2c_perif_handle)
    assert curr_addr == _PERIPHERAL_ADDR


def test_get_rx_status(i2c_perif_handle: i2c_slave.I2cSlaveHandle):
    rx_bytes = i2c_slave.get_rx_status(i2c_perif_handle)
    assert rx_bytes == 0


def test_read(i2c_perif_handle: i2c_slave.I2cSlaveHandle):
    read_bytes_count = 1024
    read_data = i2c_slave.read(i2c_perif_handle, read_bytes_count)
    assert len(read_data) == 0


def test_write(i2c_perif_handle: i2c_slave.I2cSlaveHandle):
    write_data = bytes([0x01, 0xDE, 0xAD, 0xBE, 0xEF, 0xFF, 0x02, 0x03])
    bytes_written = i2c_slave.write(i2c_perif_handle, write_data)
    assert bytes_written == len(write_data)


def test_set_clock_stretch(i2c_perif_handle: i2c_slave.I2cSlaveHandle):
    for state in [True, False]:
        i2c_slave.set_clock_stretch(i2c_perif_handle, state)


def test_set_resp_word(i2c_perif_handle: i2c_slave.I2cSlaveHandle):
    i2c_slave.set_resp_word(i2c_perif_handle, 0x00)
