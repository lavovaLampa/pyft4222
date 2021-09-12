import pytest
import itertools
from typing import Tuple, Final

from tests.fixtures import open_serial_io_handle

from pyft4222.wrapper.common import uninitialize
from pyft4222.wrapper.spi import slave as spi_periph
from pyft4222.wrapper.common import FtHandle
from pyft4222 import ResType


@pytest.fixture
def spi_periph_raw_handle(
    open_serial_io_handle: FtHandle,
) -> spi_periph.SpiSlaveRawHandle:
    result = spi_periph.init_ex(
        open_serial_io_handle, spi_periph.IoProtocol.NO_PROTOCOL
    )
    if result.tag == ResType.OK:
        yield result.ok

        uninitialize(result.ok)
    else:
        raise RuntimeError("Unable to initialize SPI Peripheral handle!")


def test_init(open_serial_io_handle: FtHandle):
    result = spi_periph.init(open_serial_io_handle)
    assert result.tag == ResType.OK


def test_init_ex(open_serial_io_handle: FtHandle):
    for proto_mode in spi_periph.IoProtocol:
        result = spi_periph.init_ex(open_serial_io_handle, proto_mode)
        assert result.tag == ResType.OK

        uninitialize(result.ok)


def test_set_mode(spi_periph_raw_handle: spi_periph.SpiSlaveRawHandle):
    args = itertools.product(spi_periph.ClkPolarity, spi_periph.ClkPhase)
    for arg in args:
        spi_periph.set_mode(spi_periph_raw_handle, *arg)


def test_get_rx_status(spi_periph_raw_handle: spi_periph.SpiSlaveRawHandle):
    rx_bytes = spi_periph.get_rx_status(spi_periph_raw_handle)
    assert rx_bytes == 0


# FIXME: Reads are blocking it seems
@pytest.mark.skip
def test_read(spi_periph_raw_handle: spi_periph.SpiSlaveRawHandle):
    read_byte_count = 20
    read_data = spi_periph.read(spi_periph_raw_handle, read_byte_count)
    assert len(read_data) == 0


def test_write(spi_periph_raw_handle: spi_periph.SpiSlaveRawHandle):
    write_data = bytes([0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08])
    bytes_written = spi_periph.write(spi_periph_raw_handle, write_data)
    assert bytes_written == len(write_data)
