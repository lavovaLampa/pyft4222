#! /usr/bin/env python

from wrapper import ResType, ftd2xx as ftd

from wrapper.ft4222.common import ClockRate, set_wakeup_interrupt, set_suspend_out, set_clock
from wrapper.ft4222 import gpio

from wrapper.ft4222.spi import ClkPhase, ClkPolarity, master as spi_master
from wrapper.ft4222.gpio import Direction, PortId

import sys


def mode_test():
    result0 = ftd.open(0)
    result1 = ftd.open(1)

    if result0.tag == ResType.OK and result1.tag == ResType.OK:
        handle0 = result0.result
        handle1 = result1.result

        print(ftd.get_device_info(handle0))
        print(ftd.get_device_info(handle1))

        set_clock(handle0, ClockRate.SYS_CLK_24)
        set_wakeup_interrupt(handle1, False)
        set_suspend_out(handle1, False)
        spim_handle = spi_master.init(
            handle0,
            spi_master.IoMode.IO_SINGLE,
            spi_master.ClkDiv.CLK_DIV_512,
            ClkPolarity.CLK_IDLE_LOW,
            ClkPhase.CLK_TRAILING,
            spi_master.SsoMap.SS_0
        )
        gpio_handle = gpio.init(
            handle1,
            (
                gpio.Direction.OUTPUT,
                gpio.Direction.OUTPUT,
                gpio.Direction.OUTPUT,
                gpio.Direction.OUTPUT
            )
        )

        if spim_handle.tag == ResType.OK:
            handle = spim_handle.result
            print("Spi Master initialized OK")
            temp = spi_master.single_write(handle, bytes([0x00] * 256))
            print(temp)
        else:
            print(
                f"Spi Master failed to initialize. Reason: {spim_handle.err}", file=sys.stderr)

        if gpio_handle.tag == ResType.OK:
            handle = gpio_handle.result
            print("GPIO initialized OK")

            # result = gpio.read(handle, gpio.PortId.PORT_3)
            # print(result)
            # gpio.write(handle, gpio.PortId.PORT_0, False);
            # gpio.write(handle, gpio.PortId.PORT_1, False);
            # gpio.write(handle, gpio.PortId.PORT_3, True)

            result = gpio.read(handle, gpio.PortId.PORT_3)
            print(result)

            result = gpio.get_trigger_status(handle, gpio.PortId.PORT_0)
            print(result)

            result = gpio.read_trigger_queue(handle, gpio.PortId.PORT_0, 100)
            print(result)

            gpio.set_waveform_mode(handle, False)
        else:
            print(
                f"Spi Slave failed to initialize. Reason: {gpio_handle.err}", file=sys.stderr)

    else:
        print("Invalid device ID", file=sys.stderr)


def spi_mode_test():
    for i in ftd.get_device_info_list():
        print(i)

    handle3 = ftd.open(0)
    if handle3.tag == ResType.OK:
        handle = handle3.result

        set_wakeup_interrupt(handle, False)
        set_suspend_out(handle, False)

        result = gpio.init(
            handle,
            (
                Direction.OUTPUT,
                Direction.OUTPUT,
                Direction.OUTPUT,
                Direction.OUTPUT
            )
        )

        if result.tag == ResType.OK:
            handle = result.result
            gpio.write(handle, PortId.PORT_3, True)
        else:
            print("Failed to initialize GPIO!", file=sys.stderr)

    else:
        print("OMEGALUL")


if __name__ == "__main__":
    # spi_mode_test()
    mode_test()
