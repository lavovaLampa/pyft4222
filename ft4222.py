from enum import Enum, auto
from typing import Dict, Final, Literal, Optional, Tuple, Type, Union
from abc import ABC

import wrapper.ftd2xx as ftd
from wrapper.ftd2xx import DeviceType

from wrapper import Err, FtHandle, Ok, Result, ResultTag, SYSTEM_TYPE
from wrapper.ft4222 import Ft4222Exception, Ft4222Status

from wrapper.ft4222.spi import slave as spi_slave
from wrapper.ft4222.spi import master as spi_master

from wrapper.ft4222.i2c import slave as i2c_slave
from wrapper.ft4222.i2c import master as i2c_master

from wrapper.ft4222 import gpio


class SpiMasterCommon(ABC):
    pass


class SpiMasterSingle(SpiMasterCommon):
    _handle: Optional[spi_master.SpiMasterSingleHandle]

    def __init__(self, ft_handle: spi_master.SpiMasterSingleHandle):
        pass


class SpiMasterMulti(SpiMasterCommon):
    _handle: Optional[spi_master.SpiMasterMultiHandle]

    def __init__(self, ft_handle: spi_master.SpiMasterMultiHandle):
        pass


SpiMaster = Union[SpiMasterSingle, SpiMasterMulti]


class SpiSlaveCommon(ABC):
    pass


class SpiSlaveRaw(SpiSlaveCommon):
    _handle: Optional[spi_slave.SpiSlaveRawHandle]

    def __init__(self, ft_handle: spi_slave.SpiSlaveRawHandle):
        self._handle = ft_handle
        pass


class SpiSlaveProto(SpiSlaveCommon):
    _handle: Optional[spi_slave.SpiSlaveProtoHandle]

    def __init__(self, ft_handle: spi_slave.SpiSlaveProtoHandle):
        self._handle = ft_handle


SpiSlave = Union[SpiSlaveRaw, SpiSlaveProto]


class I2CMaster:
    _handle: Optional[i2c_master.I2cMasterHandle]

    def __init__(self, ft_handle: i2c_master.I2cMasterHandle):
        self._handle = ft_handle


class I2CSlave:
    _handle: Optional[i2c_slave.I2cSlaveHandle]

    def __init__(self, ft_handle: i2c_slave.I2cSlaveHandle):
        self._handle = ft_handle


class Gpio:
    _handle: Optional[gpio.GpioHandle]

    def __init__(self, ft_handle: gpio.GpioHandle):
        self._handle = ft_handle


class ModeType(Enum):
    ANY_PROTOCOL = auto()
    GPIO = auto()
    GPIO_SPI_MASTER_COMBO = auto()
    SPI_MASTER = auto()


class ProtocolHandle:
    tag: Literal[ModeType.ANY_PROTOCOL]

    _handle: Optional[FtHandle]

    def __init__(self, ft_handle: FtHandle):
        self._handle = ft_handle
        self.tag = ModeType.ANY_PROTOCOL

    def init_single_spi_master(
        self,
        clk_div: spi_master.ClkDiv,
        clk_polarity: spi_master.ClkPolarity,
        clk_phase: spi_master.ClkPhase,
        sso_map: spi_master.SsoMap
    ) -> SpiMasterSingle:
        if self._handle is not None:
            result = spi_master.init(
                self._handle,
                spi_master.IoMode.IO_SINGLE,
                clk_div,
                clk_polarity,
                clk_phase,
                sso_map
            )
            if result.tag == ResultTag.OK:
                self._handle = None
                return SpiMasterSingle(result.result)
            else:
                raise Ft4222Exception(result.err)
        else:
            raise Ft4222Exception(Ft4222Status.INVALID_HANDLE)

    def init_dual_spi_master(
        self,
        clk_div: spi_master.ClkDiv,
        clk_polarity: spi_master.ClkPolarity,
        clk_phase: spi_master.ClkPhase,
        sso_map: spi_master.SsoMap
    ) -> SpiMasterMulti:
        if self._handle is not None:
            result = spi_master.init(
                self._handle,
                spi_master.IoMode.IO_DUAL,
                clk_div,
                clk_polarity,
                clk_phase,
                sso_map
            )
            if result.tag == ResultTag.OK:
                self._handle = None
                return SpiMasterMulti(result.result)
            else:
                raise Ft4222Exception(result.err)
        else:
            raise Ft4222Exception(Ft4222Status.INVALID_HANDLE)

    def init_quad_spi_master(
        self,
        clk_div: spi_master.ClkDiv,
        clk_polarity: spi_master.ClkPolarity,
        clk_phase: spi_master.ClkPhase,
        sso_map: spi_master.SsoMap
    ) -> SpiMasterMulti:
        if self._handle is not None:
            result = spi_master.init(
                self._handle,
                spi_master.IoMode.IO_QUAD,
                clk_div,
                clk_polarity,
                clk_phase,
                sso_map
            )
            if result.tag == ResultTag.OK:
                self._handle = None
                return SpiMasterMulti(result.result)
            else:
                raise Ft4222Exception(result.err)
        else:
            raise Ft4222Exception(Ft4222Status.INVALID_HANDLE)

    def init_raw_spi_slave(self) -> SpiSlaveRaw:
        if self._handle is not None:
            result = spi_slave.init_ex(
                self._handle,
                spi_slave.IoProtocol.NO_PROTOCOL,
            )
            if result.tag == ResultTag.OK:
                self._handle = None
                return SpiSlaveRaw(result.result)
            else:
                raise Ft4222Exception(result.err)
        else:
            raise Ft4222Exception(Ft4222Status.INVALID_HANDLE)

    def init_proto_spi_slave(
        self,
        proto_type: Union[
            Literal[spi_slave.IoProtocol.NO_ACK],
            Literal[spi_slave.IoProtocol.WITH_PROTOCOL]
        ]
    ) -> SpiSlaveProto:
        if self._handle is not None:
            result = spi_slave.init_ex(
                self._handle,
                proto_type
            )
            if result.tag == ResultTag.OK:
                self._handle = None
                return SpiSlaveProto(result.result)
            else:
                raise Ft4222Exception(result.err)
        else:
            raise Ft4222Exception(Ft4222Status.INVALID_HANDLE)

    def init_i2c_master(self, kbps: int) -> I2CMaster:
        if self._handle is not None:
            result = i2c_master.init(self._handle, kbps)
            if result.tag == ResultTag.OK:
                self._handle = None
                return I2CMaster(result.result)
            else:
                raise Ft4222Exception(result.err)
        else:
            raise Ft4222Exception(Ft4222Status.INVALID_HANDLE)

    def init_i2c_slave(
        self
    ) -> I2CSlave:
        if self._handle is not None:
            result = i2c_slave.init(self._handle)
            if result.tag == ResultTag.OK:
                self._handle = None
                return I2CSlave(result.result)
            else:
                raise Ft4222Exception(result.err)
        else:
            raise Ft4222Exception(Ft4222Status.INVALID_HANDLE)


class GpioHandle:
    tag: Literal[ModeType.GPIO]

    _handle: Optional[FtHandle]

    def __init__(self, ft_handle: FtHandle):
        self._handle = ft_handle
        self.tag = ModeType.GPIO

    def init_gpio(self) -> Gpio:
        pass


# FIXME: Better naming!
class ComboHandle:
    tag: Literal[ModeType.GPIO_SPI_MASTER_COMBO]

    _handle: Optional[FtHandle]

    def __init__(self, ft_handle: FtHandle):
        self._handle = ft_handle
        self.tag = ModeType.GPIO_SPI_MASTER_COMBO


class SpiMasterHandle:
    tag: Literal[ModeType.SPI_MASTER]

    _handle: Optional[FtHandle]

    def __init__(self, ft_handle: FtHandle):
        self._handle = ft_handle
        self.tag = ModeType.SPI_MASTER

    def init_single_spi_master(
        self,
        clk_div: spi_master.ClkDiv,
        clk_polarity: spi_master.ClkPolarity,
        clk_phase: spi_master.ClkPhase,
        sso_map: spi_master.SsoMap
    ) -> SpiMasterSingle:
        if self._handle is not None:
            result = spi_master.init(
                self._handle,
                spi_master.IoMode.IO_SINGLE,
                clk_div,
                clk_polarity,
                clk_phase,
                sso_map
            )
            if result.tag == ResultTag.OK:
                self._handle = None
                return SpiMasterSingle(result.result)
            else:
                raise Ft4222Exception(result.err)
        else:
            raise Ft4222Exception(Ft4222Status.INVALID_HANDLE)

    def init_dual_spi_master(
        self,
        clk_div: spi_master.ClkDiv,
        clk_polarity: spi_master.ClkPolarity,
        clk_phase: spi_master.ClkPhase,
        sso_map: spi_master.SsoMap
    ) -> SpiMasterMulti:
        if self._handle is not None:
            result = spi_master.init(
                self._handle,
                spi_master.IoMode.IO_DUAL,
                clk_div,
                clk_polarity,
                clk_phase,
                sso_map
            )
            if result.tag == ResultTag.OK:
                self._handle = None
                return SpiMasterMulti(result.result)
            else:
                raise Ft4222Exception(result.err)
        else:
            raise Ft4222Exception(Ft4222Status.INVALID_HANDLE)

    def init_quad_spi_master(
        self,
        clk_div: spi_master.ClkDiv,
        clk_polarity: spi_master.ClkPolarity,
        clk_phase: spi_master.ClkPhase,
        sso_map: spi_master.SsoMap
    ) -> SpiMasterMulti:
        if self._handle is not None:
            result = spi_master.init(
                self._handle,
                spi_master.IoMode.IO_QUAD,
                clk_div,
                clk_polarity,
                clk_phase,
                sso_map
            )
            if result.tag == ResultTag.OK:
                self._handle = None
                return SpiMasterMulti(result.result)
            else:
                raise Ft4222Exception(result.err)
        else:
            raise Ft4222Exception(Ft4222Status.INVALID_HANDLE)


Ft4222HandleType = Union[
    Type[ProtocolHandle],
    Type[ComboHandle],
    Type[GpioHandle],
    Type[SpiMasterHandle]
]

Ft4222Handle = Union[
    ProtocolHandle,
    ComboHandle,
    GpioHandle,
    SpiMasterHandle
]

MODE_MAP: Final[Dict[Tuple[str, DeviceType], Ft4222HandleType]] = {
    # Mode 0
    ("FT4222 A", DeviceType.DEV_4222H_0): ProtocolHandle,
    ("FT4222 B", DeviceType.DEV_4222H_0): GpioHandle,

    # Mode 1 or Mode 2
    ("FT4222 A", DeviceType.DEV_4222H_1_2): SpiMasterHandle,
    ("FT4222 B", DeviceType.DEV_4222H_1_2): SpiMasterHandle,
    ("FT4222 C", DeviceType.DEV_4222H_1_2): SpiMasterHandle,
    ("FT4222 D", DeviceType.DEV_4222H_1_2): ComboHandle,

    # Mode 3
    ("FT4222", DeviceType.DEV_4222H_3): ProtocolHandle
}


class FtError(Enum):
    INVALID_MODE = auto()
    INVALID_ID = auto()
    INVALID_HANDLE = auto()
    UNKNOWN_FAILURE = auto()


def get_mode_handle(ft_handle: FtHandle) -> Result[Ft4222Handle, FtError]:
    dev_details = ftd.get_device_info(ft_handle)
    if dev_details is not None:
        handle_type = MODE_MAP.get((
            dev_details.description,
            dev_details.dev_type
        ))
        if handle_type is not None:
            return Ok(handle_type(ft_handle))
        else:
            return Err(FtError.INVALID_MODE)
    else:
        return Err(FtError.INVALID_HANDLE)


def open(dev_id: int) -> Result[Ft4222Handle, FtError]:
    id_valid = 0 <= dev_id < (2 ** 31) - 1

    if id_valid:
        ft_handle = ftd.open(dev_id)
        if ft_handle.tag == ResultTag.OK:
            return get_mode_handle(ft_handle.result)
        else:
            return Err(FtError.INVALID_HANDLE)
    else:
        return Err(FtError.INVALID_ID)


def open_by_serial(serial_num: str) -> Result[Ft4222Handle, FtError]:
    ft_handle = ftd.open_by_serial(serial_num)
    if ft_handle.tag == ResultTag.OK:
        return get_mode_handle(ft_handle.result)
    else:
        return Err(FtError.INVALID_HANDLE)


def open_by_description(dev_description: str) -> Result[Ft4222Handle, FtError]:
    ft_handle = ftd.open_by_description(dev_description)
    if ft_handle.tag == ResultTag.OK:
        return get_mode_handle(ft_handle.result)
    else:
        return Err(FtError.INVALID_HANDLE)


if SYSTEM_TYPE != 'Linux':
    def open_by_location(location_id: int) -> Result[Ft4222Handle, FtError]:
        ft_handle = ftd.open_by_location(location_id)
        if ft_handle.tag == ResultTag.OK:
            return get_mode_handle(ft_handle.result)
        else:
            return Err(FtError.INVALID_HANDLE)


class Ft4222:
    _handle: Optional[FtHandle] = None

    def __init__(self, ft_handle: FtHandle):
        pass

    # def init_spi_slave(self) -> SpiSlave:
    #     pass

    # def init_i2c_master(self) -> I2CMaster:
    #     pass

    # def init_i2c_slave(self) -> I2CSlave:
    #     pass
