#! /usr/bin/env python

from ctypes import c_void_p
from wrapper.ft4222.spi import ClkPhase, ClkPolarity, master
from wrapper import FtHandle, ResultTag
import wrapper.ftd2xx as ft

import wrapper.ft4222.spi.slave as slave

import ft4222 as pyft


def main() -> None:
    print(f"Create Device Info List: {ft.create_device_info_list()}")
    print(f"Get Device Info List: {ft.get_device_info_list()}")
    print(f"Get Device Info Detail: {ft.get_device_info_detail(0)}")
    print(f"Open: {ft.open(0)}")
    # print(f"Open By Serial: {ft.open_by_serial('SVF_0061-0003A')}")
    print(f"Open By Description: {ft.open_by_description('FT4222 B')}")
    # print(f"Open By Location: {ft.open_by_location(10)}")
    print(f"Close: {ft.close(FtHandle(c_void_p(None)))}")
    print(f"Get Device Info: {ft.get_device_info(FtHandle(c_void_p(None)))}")
    # print(f"Get Driver Version: {ft.get_driver_version(FtHandle(c_void_p(None)))}")
    print(
        f"Purge: {ft.purge(FtHandle(c_void_p(None)), ft.PurgeType.RX | ft.PurgeType.TX)}")
    print(f"Reset Device: {ft.reset_device(FtHandle(c_void_p(None)))}")


def test_positif() -> None:
    result = ft.open(0)
    if result.tag == ResultTag.OK:
        handle = result.result
        print(f"Get Device Info: {ft.get_device_info(handle)}")
        print(f"Purge: {ft.purge(handle, ft.PurgeType.RX)}")
        print(f"Reset Device: {ft.reset_device(handle)}")

def test_spi_slave() -> None:
    result = ft.open(0)
    if result.tag == ResultTag.OK:
        handle = result.result
        temp = slave.init_ex(handle, slave.IoProtocol.NO_PROTOCOL)

def test_spi_master() -> None:
    result = ft.open(0)
    if result.tag == ResultTag.OK:
        handle = result.result
        temp = master.init(
            handle, 
            master.IoMode.IO_DUAL,
            master.ClkDiv.CLK_DIV_2,
            ClkPolarity.CLK_IDLE_LOW,
            ClkPhase.CLK_LEADING,
            master.SsoMap.SS_0
        )


def new_one() -> None:
    pyft.open(0)


if __name__ == "__main__":
    # main()
    # test_positif()
    print(ft.get_device_info_list())
    new_one()
