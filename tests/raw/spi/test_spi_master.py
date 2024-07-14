import itertools
from typing import Final, Tuple

import pytest

from pyft4222.result import Ok
from pyft4222.wrapper.common import FtHandle, uninitialize
from pyft4222.wrapper.spi import master as spi_ctrl

from ...fixtures import *

_DEFAULT_CTRL_PARAMS: Final[
    Tuple[spi_ctrl.ClkDiv, spi_ctrl.ClkPolarity, spi_ctrl.ClkPhase, spi_ctrl.SsoMap]
] = (
    spi_ctrl.ClkDiv.CLK_DIV_2,
    spi_ctrl.ClkPolarity.CLK_IDLE_LOW,
    spi_ctrl.ClkPhase.CLK_LEADING,
    spi_ctrl.SsoMap.SS_0,
)


@pytest.fixture
def spi_ctrl_single_handle(
    open_serial_io_handle: FtHandle,
) -> spi_ctrl.SpiMasterSingleHandle:
    result = spi_ctrl.init(
        open_serial_io_handle, spi_ctrl.IoMode.SINGLE, *_DEFAULT_CTRL_PARAMS
    )
    if isinstance(result, Ok):
        return result.val
    else:
        raise RuntimeError("Cannot initialize SPI controller handle!")


@pytest.fixture
def spi_ctrl_dual_handle(
    open_serial_io_handle: FtHandle,
) -> spi_ctrl.SpiMasterMultiHandle:
    result = spi_ctrl.init(
        open_serial_io_handle, spi_ctrl.IoMode.DUAL, *_DEFAULT_CTRL_PARAMS
    )
    if isinstance(result, Ok):
        return result.val
    else:
        raise RuntimeError("Cannot initialize SPI controller handle!")


@pytest.fixture
def spi_ctrl_quad_handle(
    open_serial_io_handle: FtHandle,
) -> spi_ctrl.SpiMasterMultiHandle:
    result = spi_ctrl.init(
        open_serial_io_handle, spi_ctrl.IoMode.QUAD, *_DEFAULT_CTRL_PARAMS
    )
    if isinstance(result, Ok):
        return result.val
    else:
        raise RuntimeError("Cannot initialize SPI controller handle!")


def test_init(open_serial_io_handle: FtHandle):
    args = itertools.product(
        spi_ctrl.IoMode,
        spi_ctrl.ClkDiv,
        spi_ctrl.ClkPolarity,
        spi_ctrl.ClkPhase,
        spi_ctrl.SsoMap,
    )

    for arg in args:
        # TODO: Implement better
        if arg[4] != spi_ctrl.SsoMap.SS_0:
            continue
        result = spi_ctrl.init(open_serial_io_handle, *arg)
        assert isinstance(result, Ok)

        uninitialize(result.val)


def test_set_cs(spi_ctrl_single_handle: spi_ctrl.SpiMasterSingleHandle):
    for polarity in spi_ctrl.CsPolarity:
        spi_ctrl.set_cs_polarity(spi_ctrl_single_handle, polarity)


def test_set_lines(spi_ctrl_single_handle: spi_ctrl.SpiMasterSingleHandle):
    for io_mode in spi_ctrl.IoMode:
        handle = spi_ctrl.set_lines(spi_ctrl_single_handle, io_mode)
        assert handle is not None


def test_single_read(spi_ctrl_single_handle: spi_ctrl.SpiMasterSingleHandle):
    read_byte_count = 400
    for trans_end in [False, True]:
        read_data = spi_ctrl.single_read(
            spi_ctrl_single_handle, read_byte_count, trans_end
        )
        assert len(read_data) == read_byte_count


def test_single_read_write(spi_ctrl_single_handle: spi_ctrl.SpiMasterSingleHandle):
    write_data = bytes([0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06])
    for trans_end in [False, True]:
        read_data = spi_ctrl.single_read_write(
            spi_ctrl_single_handle, write_data, trans_end
        )
        assert len(read_data) == len(write_data)


def test_multi_read_write(spi_ctrl_quad_handle: spi_ctrl.SpiMasterMultiHandle):
    write_data = bytes([0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06])
    read_data = spi_ctrl.multi_read_write(spi_ctrl_quad_handle, None, 0, 0, 100)
    assert len(read_data) == 100

    read_data = spi_ctrl.multi_read_write(
        spi_ctrl_quad_handle, write_data, 0, len(write_data), 100
    )
    assert len(read_data) == 100

    read_data = spi_ctrl.multi_read_write(
        spi_ctrl_quad_handle, write_data, len(write_data), 0, 0
    )
    assert len(read_data) == 0
