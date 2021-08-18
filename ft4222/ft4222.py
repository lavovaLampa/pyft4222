from enum import Enum, auto
from ft4222 import CommonHandle
from typing import Literal, Union

from wrapper import FtHandle, ResType
from wrapper.ft4222 import Ft4222Exception, Ft4222Status, gpio
from wrapper.ft4222.spi import slave as spi_slave
from wrapper.ft4222.spi import master as spi_master
from wrapper.ft4222.i2c import slave as i2c_slave
from wrapper.ft4222.i2c import master as i2c_master

from .spi.master import SpiMasterMulti, SpiMasterSingle
from .spi.slave import SpiSlaveProto, SpiSlaveRaw
from .i2c.master import I2CMaster
from .i2c.slave import I2CSlave
from .gpio import Gpio


class InterfaceType(Enum):
    """FT4222 USB interface type.

    The FT4222 chip can be set (externally) into 4 distinct modes,
    each supporting a certain functions over number of USB streams:

    +---------------+-------------+------------+------------+-------------+
    |               |   MODE 0    |   MODE 1   |   MODE 2   |   MODE 3    |
    +---------------+-------------+------------+------------+-------------+
    | Stream #0 (A) | Data Stream | SPI Master | SPI Master | Data Stream |
    | Stream #1 (B) | GPIO        | SPI Master | SPI Master | N/A         |
    | Stream #2 (C) | N/A         | SPI Master | SPI Master | N/A         |
    | Stream #3 (D) | N/A         | GPIO       | SPI Master | N/A         |
    +---------------+-------------+------------+------------+-------------+

    To select the configuration mode/interface type, you must tie the
    DCNF1, DCNF0 pins to corresponding values.

    More info can be found in the FT4222H Datasheet:
    https://ftdichip.com/wp-content/uploads/2020/07/DS_FT4222H.pdf
    """
    # In this mode all serial protocols are supported, excluding GPIO
    DATA_STREAM = auto()
    # Only GPIO is supported
    GPIO = auto()
    # Only SPI Master mode is supported
    SPI_MASTER = auto()


class ProtocolHandle(CommonHandle[FtHandle]):
    tag: Literal[InterfaceType.DATA_STREAM]

    def __init__(self, ft_handle: FtHandle):
        super().__init__(ft_handle)
        self.tag = InterfaceType.DATA_STREAM

    def init_single_spi_master(
        self,
        clk_div: spi_master.ClkDiv,
        clk_polarity: spi_master.ClkPolarity,
        clk_phase: spi_master.ClkPhase,
        sso_map: spi_master.SsoMap
    ) -> SpiMasterSingle['ProtocolHandle']:
        if self._handle is not None:
            result = spi_master.init(
                self._handle,
                spi_master.IoMode.IO_SINGLE,
                clk_div,
                clk_polarity,
                clk_phase,
                sso_map
            )
            if result.tag == ResType.OK:
                self._handle = None
                return SpiMasterSingle(result.result, self.__class__)
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
    ) -> SpiMasterMulti['ProtocolHandle']:
        if self._handle is not None:
            result = spi_master.init(
                self._handle,
                spi_master.IoMode.IO_DUAL,
                clk_div,
                clk_polarity,
                clk_phase,
                sso_map
            )
            if result.tag == ResType.OK:
                self._handle = None
                return SpiMasterMulti(result.result, self.__class__)
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
    ) -> SpiMasterMulti['ProtocolHandle']:
        if self._handle is not None:
            result = spi_master.init(
                self._handle,
                spi_master.IoMode.IO_QUAD,
                clk_div,
                clk_polarity,
                clk_phase,
                sso_map
            )
            if result.tag == ResType.OK:
                self._handle = None
                return SpiMasterMulti(result.result, self.__class__)
            else:
                raise Ft4222Exception(result.err)
        else:
            raise Ft4222Exception(Ft4222Status.INVALID_HANDLE)

    def init_raw_spi_slave(self) -> SpiSlaveRaw['ProtocolHandle']:
        if self._handle is not None:
            result = spi_slave.init_ex(
                self._handle,
                spi_slave.IoProtocol.NO_PROTOCOL,
            )
            if result.tag == ResType.OK:
                self._handle = None
                return SpiSlaveRaw(result.result, self.__class__)
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
    ) -> SpiSlaveProto['ProtocolHandle']:
        if self._handle is not None:
            result = spi_slave.init_ex(
                self._handle,
                proto_type
            )
            if result.tag == ResType.OK:
                self._handle = None
                return SpiSlaveProto(result.result, self.__class__)
            else:
                raise Ft4222Exception(result.err)
        else:
            raise Ft4222Exception(Ft4222Status.INVALID_HANDLE)

    def init_i2c_master(self, kbps: int) -> I2CMaster['ProtocolHandle']:
        if self._handle is not None:
            result = i2c_master.init(self._handle, kbps)
            if result.tag == ResType.OK:
                self._handle = None
                return I2CMaster(result.result, self.__class__)
            else:
                raise Ft4222Exception(result.err)
        else:
            raise Ft4222Exception(Ft4222Status.INVALID_HANDLE)

    def init_i2c_slave(
        self
    ) -> I2CSlave['ProtocolHandle']:
        if self._handle is not None:
            result = i2c_slave.init(self._handle)
            if result.tag == ResType.OK:
                self._handle = None
                return I2CSlave(result.result, self.__class__)
            else:
                raise Ft4222Exception(result.err)
        else:
            raise Ft4222Exception(Ft4222Status.INVALID_HANDLE)


class GpioHandle(CommonHandle[FtHandle]):
    tag: Literal[InterfaceType.GPIO]

    def __init__(self, ft_handle: FtHandle):
        super().__init__(ft_handle)
        self.tag = InterfaceType.GPIO

    def init_gpio(self, dirs: gpio.DirTuple) -> Gpio['GpioHandle']:
        if self._handle is not None:
            result = gpio.init(self._handle, dirs)
            if result.tag == ResType.OK:
                self._handle = None
                return Gpio(result.result, self.__class__)
            else:
                raise Ft4222Exception(result.err)
        else:
            raise Ft4222Exception(Ft4222Status.INVALID_HANDLE)


class SpiMasterHandle(CommonHandle[FtHandle]):
    tag: Literal[InterfaceType.SPI_MASTER]

    def __init__(self, ft_handle: FtHandle):
        super().__init__(ft_handle)
        self.tag = InterfaceType.SPI_MASTER

    def init_single_spi_master(
        self,
        clk_div: spi_master.ClkDiv,
        clk_polarity: spi_master.ClkPolarity,
        clk_phase: spi_master.ClkPhase,
        sso_map: spi_master.SsoMap
    ) -> SpiMasterSingle['SpiMasterHandle']:
        if self._handle is not None:
            result = spi_master.init(
                self._handle,
                spi_master.IoMode.IO_SINGLE,
                clk_div,
                clk_polarity,
                clk_phase,
                sso_map
            )
            if result.tag == ResType.OK:
                self._handle = None
                return SpiMasterSingle(result.result, self.__class__)
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
    ) -> SpiMasterMulti['SpiMasterHandle']:
        if self._handle is not None:
            result = spi_master.init(
                self._handle,
                spi_master.IoMode.IO_DUAL,
                clk_div,
                clk_polarity,
                clk_phase,
                sso_map
            )
            if result.tag == ResType.OK:
                self._handle = None
                return SpiMasterMulti(result.result, self.__class__)
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
    ) -> SpiMasterMulti['SpiMasterHandle']:
        if self._handle is not None:
            result = spi_master.init(
                self._handle,
                spi_master.IoMode.IO_QUAD,
                clk_div,
                clk_polarity,
                clk_phase,
                sso_map
            )
            if result.tag == ResType.OK:
                self._handle = None
                return SpiMasterMulti(result.result, self.__class__)
            else:
                raise Ft4222Exception(result.err)
        else:
            raise Ft4222Exception(Ft4222Status.INVALID_HANDLE)
