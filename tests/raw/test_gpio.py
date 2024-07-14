import itertools
from ctypes import c_void_p
from functools import reduce

import pytest

from pyft4222.result import Err, Ok
from pyft4222.wrapper import Ft4222Status, FtHandle, GpioTrigger, gpio
from pyft4222.wrapper import common as ft_common

from ..fixtures import *


@pytest.fixture
def gpio_output_handle(open_gpio_handle: FtHandle) -> gpio.GpioHandle:
    handle = gpio.init(
        open_gpio_handle,
        (
            gpio.Direction.OUTPUT,
            gpio.Direction.OUTPUT,
            gpio.Direction.OUTPUT,
            gpio.Direction.OUTPUT,
        ),
    )

    if isinstance(handle, Ok):
        ft_common.set_suspend_out(handle.val, False)
        ft_common.set_wakeup_interrupt(handle.val, False)

        return handle.val
    else:
        raise RuntimeError("Cannot initialize GPIO handle!")


@pytest.fixture
def gpio_input_handle(open_gpio_handle: FtHandle) -> gpio.GpioHandle:
    handle = gpio.init(
        open_gpio_handle,
        (
            gpio.Direction.INPUT,
            gpio.Direction.INPUT,
            gpio.Direction.INPUT,
            gpio.Direction.INPUT,
        ),
    )

    if isinstance(handle, Ok):
        ft_common.set_suspend_out(handle.val, False)
        ft_common.set_wakeup_interrupt(handle.val, False)

        return handle.val
    else:
        raise RuntimeError("Cannot initialize GPIO handle!")


def test_invalid_init():
    handle = gpio.init(
        FtHandle(c_void_p(None)),
        (
            gpio.Direction.OUTPUT,
            gpio.Direction.OUTPUT,
            gpio.Direction.OUTPUT,
            gpio.Direction.OUTPUT,
        ),
    )

    assert isinstance(handle, Err)
    # Why this status? Go ask FTDI i guess...
    assert handle.err == Ft4222Status.DEVICE_NOT_SUPPORTED


def test_read_write(gpio_output_handle: gpio.GpioHandle):
    for port in gpio.PortId:
        for val in [True, False]:
            gpio.write(gpio_output_handle, port, val)
            assert gpio.read(gpio_output_handle, port) == val


def test_input_trigger(gpio_input_handle: gpio.GpioHandle):
    for port in gpio.PortId:
        states = itertools.product(*[(None, x) for x in GpioTrigger])
        for state in states:
            if state == (None, None, None, None):
                continue
            state = filter(lambda x: x is not None, state)
            trigger = reduce(lambda acc, x: acc | x, state)
            gpio.set_input_trigger(gpio_input_handle, port, trigger)


def test_get_trigger_status(gpio_input_handle: gpio.GpioHandle):
    for port in gpio.PortId:
        result = gpio.get_trigger_status(gpio_input_handle, port)
        assert result == 0


def test_read_trigger_queue(gpio_input_handle: gpio.GpioHandle):
    for port in gpio.PortId:
        result = gpio.read_trigger_queue(gpio_input_handle, port)
        assert len(result) == 0


def test_set_waveform_mode(gpio_input_handle: gpio.GpioHandle):
    for state in [True, False]:
        gpio.set_waveform_mode(gpio_input_handle, state)
