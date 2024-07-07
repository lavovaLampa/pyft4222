from typing import Union

from .master import I2cMasterHandle
from .slave import I2cSlaveHandle

I2cHandle = Union[I2cMasterHandle, I2cSlaveHandle]
