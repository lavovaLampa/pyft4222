from typing import Final, Mapping, Tuple
import pytest

from enum import Enum, auto

from pyft4222.wrapper import FtHandle, ResType, ftd2xx as ftd

FT4222_DEV_TYPES = {
    ftd.DeviceType.DEV_4222H_0,
    ftd.DeviceType.DEV_4222H_1_2,
    ftd.DeviceType.DEV_4222H_3,
}


class InterfaceType(Enum):
    GPIO = auto()
    SERIAL_IO = auto()
    SPI_MASTER = auto()
    ANY = auto()


DEV_INTERFACE_MAP: Final[Mapping[Tuple[InterfaceType, ftd.DeviceType], str]] = {
    # GPIO interface
    (InterfaceType.GPIO, ftd.DeviceType.DEV_4222H_0): "FT4222 B",
    # Serial I/O interface
    (InterfaceType.SERIAL_IO, ftd.DeviceType.DEV_4222H_0): "FT4222 A",
    (InterfaceType.SERIAL_IO, ftd.DeviceType.DEV_4222H_3): "FT4222",
    # SPI Master interface
    (InterfaceType.SPI_MASTER, ftd.DeviceType.DEV_4222H_0): "FT4222 A",
    (InterfaceType.SPI_MASTER, ftd.DeviceType.DEV_4222H_1_2): "FT4222 A",
    (InterfaceType.SPI_MASTER, ftd.DeviceType.DEV_4222H_3): "FT4222",
    # Any interface
    (InterfaceType.ANY, ftd.DeviceType.DEV_4222H_0): "FT4222 A",
    (InterfaceType.ANY, ftd.DeviceType.DEV_4222H_1_2): "FT4222 A",
    (InterfaceType.ANY, ftd.DeviceType.DEV_4222H_3): "FT4222",
}


def _find_suitable_device(intf_type: InterfaceType) -> Tuple[int, ftd.DeviceInfo]:
    devices = ftd.get_device_info_list()
    devices = enumerate(devices)
    devices = filter(
        lambda x: x[1].description == DEV_INTERFACE_MAP.get((intf_type, x[1].dev_type)),
        devices,
    )
    devices = list(devices)

    if len(devices) > 0:
        return devices[0]
    else:
        raise RuntimeError("Couldn't find an FT4222 device supporting given interface!")


@pytest.fixture
def valid_dev() -> ftd.DeviceInfo:
    return _find_suitable_device(InterfaceType.ANY)[1]


@pytest.fixture
def valid_dev_idx() -> int:
    return _find_suitable_device(InterfaceType.ANY)[0]


@pytest.fixture
def open_handle(valid_dev_idx: int) -> FtHandle:
    result = ftd.open_by_idx(valid_dev_idx)
    if result.tag == ResType.OK:
        yield result.ok

        ftd.close_handle(result.ok)
    else:
        raise RuntimeError("Cannot obtain an FT4222 device handle!")


@pytest.fixture
def open_gpio_handle() -> FtHandle:
    device = _find_suitable_device(InterfaceType.GPIO)
    result = ftd.open_by_idx(device[0])
    if result.tag == ResType.OK:
        yield result.ok

        ftd.close_handle(result.ok)
    else:
        raise RuntimeError("Cannot obtain a valid GPIO handle!")


@pytest.fixture
def open_serial_io_handle() -> FtHandle:
    device = _find_suitable_device(InterfaceType.SERIAL_IO)
    result = ftd.open_by_idx(device[0])
    if result.tag == ResType.OK:
        yield result.ok

        ftd.close_handle(result.ok)
    else:
        raise RuntimeError("Cannot obtain a valid GPIO handle!")
