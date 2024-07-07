from pyft4222.handle import GenericProtocolHandle, StreamHandleType
from pyft4222.wrapper import Ft4222Exception, Ft4222Status
from pyft4222.wrapper.i2c.master import (
    CtrlStatus,
    I2cMasterHandle,
    TransactionFlag,
    get_status,
    read,
    read_ex,
    reset,
    reset_bus,
    write,
    write_ex,
)


class I2CMaster(GenericProtocolHandle[I2cMasterHandle, StreamHandleType]):
    """A class encapsulating I2C Master functions."""

    def read(self, dev_address: int, read_byte_count: int) -> bytes:
        """Read data from specified I2C slave with START and STOP conditions.

        Args:
            dev_address:        I2C slave address;          range <0, 65_535>
            read_byte_count:    Number of bytes to read;    range <1, 65_535>

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            bytes:              Read data
        """
        if self._handle is None:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "I2C Master has been uninitialized!"
            )

        if not (0 <= dev_address < (2**16)):
            raise ValueError("dev_address must be in range <0, 65_535>.")
        if not (0 < read_byte_count < (2**16)):
            raise ValueError("read_byte_count must be in range <1, 65_535>.")

        return read(self._handle, dev_address, read_byte_count)

    def write(self, dev_address: int, write_data: bytes) -> int:
        """Write data to the specified I2C slave with START and STOP conditions.

        Args:
            dev_address:    I2C slave address;                  range <0, 65_535>
            write_data:     Non-empty list of bytes to write;   length <1, 65_535>

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            int:            Number of bytes written
        """
        if self._handle is None:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "I2C Master has been uninitialized!"
            )

        if not (0 <= dev_address < (2**16)):
            raise ValueError("dev_address must be in range <0, 65_535>.")
        if not (0 < len(write_data) < (2**16)):
            raise ValueError("write_data length must be in range <1, 65_535>.")

        return write(self._handle, dev_address, write_data)

    def read_ex(
        self, dev_address: int, flags: TransactionFlag, read_byte_count: int
    ) -> bytes:
        """Read data from the specified I2C slave with the specified I2C flags.

        Args:
            dev_address:        I2C slave address;          range <0, 65_535>
            flag:               I2C transaction flags mask
            read_byte_count:    Number of bytes to read;    range <1, 65_535>

        Raises:
            Ft4222Exception:    In case of unexpected errors

        Returns:
            bytes:              Read data
        """
        if self._handle is None:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "I2C Master has been uninitialized!"
            )

        if not (0 <= dev_address < (2**16)):
            raise ValueError("dev_address must be in range <0, 65_535>.")
        if not (0 < read_byte_count < (2**16)):
            raise ValueError("read_byte_count must be in range <1, 65_535>.")

        return read_ex(self._handle, dev_address, flags, read_byte_count)

    def write_ex(
        self, dev_address: int, flags: TransactionFlag, write_data: bytes
    ) -> int:
        """Write data into the specified I2C slave with the specified I2C flags.

        Args:
            dev_address:    I2C slave address;                  range <0, 65_535>
            flags:          I2C transaction flags mask
            write_data:     Non-empty list of bytes to write;   length <1, 65_535>

        Raises:
            Ft4222Exception:    In case of unexpected errors

        Returns:
            int:            Number of bytes written
        """
        if self._handle is None:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "I2C Master has been uninitialized!"
            )

        if not (0 <= dev_address < (2**16)):
            raise ValueError("dev_address must be in range <0, 65_535>.")
        if not (0 < len(write_data) < (2**16)):
            raise ValueError("write_data length must be in range <1, 65_535>.")

        return write_ex(self._handle, dev_address, flags, write_data)

    def get_status(self) -> CtrlStatus:
        """Get I2C Master controller status.

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            CtrlStatus:         IntFlag encoding controller status
        """
        if self._handle is None:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "I2C Master has been uninitialized!"
            )

        return get_status(self._handle)

    def reset(self) -> None:
        """Reset the I2C Master.

        Note:
            It is no necessary to re-initialize the controller.
            It retains all its settings, and is ready to be used again.

        Raises:
            Ft4222Exception:    In case of unexpected error
        """
        if self._handle is None:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "I2C Master has been uninitialized!"
            )
        reset(self._handle)

    def reset_bus(self) -> None:
        """Reset the I2C bus.

        If the data line (SDA) is stuck LOW by the slave device,
        this function will make the master send nine SCK clocks
        to recover the I2C bus.
        The slave device that held the data line (SDA) LOW will
        release it within these nine clocks.
        If not, then use the HW reset or cycle power to clear the bus.

        Raises:
            Ft4222Exception:    In case of unexpected error
        """
        if self._handle is None:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "I2C Master has been uninitialized!"
            )

        reset_bus(self._handle)
