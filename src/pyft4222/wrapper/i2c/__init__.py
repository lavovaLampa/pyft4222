from __future__ import annotations

from pyft4222.wrapper.i2c.master import I2cMasterHandle
from pyft4222.wrapper.i2c.slave import I2cSlaveHandle

I2cHandle = I2cMasterHandle | I2cSlaveHandle
