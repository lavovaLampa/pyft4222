from typing import Optional, Union
from abc import ABC

from .wrapper import FtHandle


class SpiMasterCommon(ABC):
    pass


class SpiMasterSingle(SpiMasterCommon):
    pass


class SpiMasterMulti(SpiMasterCommon):
    pass


SpiMaster = Union[SpiMasterSingle, SpiMasterMulti]


class SpiSlaveCommon(ABC):
    pass


class SpiSlaveRaw(SpiSlaveCommon):
    pass


class SpiSlaveProto(SpiSlaveCommon):
    pass


SpiSlave = Union[SpiSlaveRaw, SpiSlaveProto]


class Ft4222:
    _handle: Optional[FtHandle] = None

    def __init__(self, ft_handle: FtHandle):
        pass

    def init_spi_master(self) -> SpiMaster:
        pass

    def init_spi_slave(self) -> SpiSlave:
        pass

    def init_i2c_master(self) -> I2CMaster:
        pass

    def init_i2c_slave(self) -> I2CSlave:
        pass