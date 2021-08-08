from enum import Enum, auto
from typing import Literal, Optional, Union

from wrapper import FtHandle, ResultTag
from wrapper.ft4222 import Ft4222Exception, Ft4222Status, gpio
from wrapper.ft4222.spi import slave as spi_slave
from wrapper.ft4222.spi import master as spi_master
from wrapper.ft4222.i2c import slave as i2c_slave
from wrapper.ft4222.i2c import master as i2c_master

from .spi.master import SpiMasterMulti, SpiMasterSingle
from .spi.slave import SpiSlaveProto, SpiSlave
from .i2c.master import I2CMaster
from .i2c.slave import I2CSlave
from .gpio import Gpio


class InterfaceType(Enum):
    """FT4222 USB interface type.
    """
    DATA_STREAM = auto()
    GPIO = auto()
    SPI_MASTER = auto()


class ProtocolHandle:
    tag: Literal[InterfaceType.DATA_STREAM]

    _handle: Optional[FtHandle]

    def __init__(self, ft_handle: FtHandle):
        self._handle = ft_handle
        self.tag = InterfaceType.DATA_STREAM

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
    tag: Literal[InterfaceType.GPIO]

    _handle: Optional[FtHandle]

    def __init__(self, ft_handle: FtHandle):
        self._handle = ft_handle
        self.tag = InterfaceType.GPIO

    def init_gpio(self, dirs: gpio.DirTuple) -> Gpio:
        if self._handle is not None:
            result = gpio.init(self._handle, dirs)
            if result.tag == ResultTag.OK:
                self._handle = None
                return Gpio(result.result)
            else:
                raise Ft4222Exception(result.err)
        else:
            raise Ft4222Exception(Ft4222Status.INVALID_HANDLE)


class SpiMasterHandle:
    tag: Literal[InterfaceType.SPI_MASTER]

    _handle: Optional[FtHandle]

    def __init__(self, ft_handle: FtHandle):
        self._handle = ft_handle
        self.tag = InterfaceType.SPI_MASTER

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
