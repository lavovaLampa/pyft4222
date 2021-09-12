from ..fixtures import *

import pyft4222.wrapper.common as ft


# TESTS


def test_set_get_clock(open_handle: FtHandle):
    for clock in ft.ClockRate:
        ft.set_clock(open_handle, clock)
        assert ft.get_clock(open_handle) == clock


def test_set_wakeup_interrupt(open_handle: FtHandle):
    for state in [True, False]:
        ft.set_wakeup_interrupt(open_handle, state)


def test_set_suspend_out(open_handle: FtHandle):
    for state in [True, False]:
        ft.set_suspend_out(open_handle, state)


def test_get_version(open_handle: FtHandle):
    result = ft.get_version(open_handle)
    assert result.chip_version == ft.ChipVersion.REV_D


def test_chip_reset(open_handle: FtHandle):
    ft.chip_reset(open_handle)
