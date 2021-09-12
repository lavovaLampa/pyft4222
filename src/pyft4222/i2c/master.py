from typing import Generic, Type, TypeVar

from pyft4222.handle import GenericHandle
from pyft4222.wrapper import FtHandle
from pyft4222.wrapper import Ft4222Exception, Ft4222Status
from pyft4222.wrapper.common import uninitialize
from pyft4222.wrapper.i2c.master import I2cMasterHandle, CtrlStatus, TransactionFlag
from pyft4222.wrapper.i2c.master import (
    get_status,
    read,
    read_ex,
    reset,
    reset_bus,
    write,
    write_ex,
)

T = TypeVar("T", bound=GenericHandle[FtHandle])


class I2CMaster(Generic[T], GenericHandle[I2cMasterHandle]):
    """A class encapsulating I2C Master functions."""

    _mode_class: Type[T]

    def __init__(self, ft_handle: I2cMasterHandle, mode_class: Type[T]):
        """Initialize the class with given FT4222 handle and a mode class type.

        Args:
            ft_handle:      FT4222 handle initialized in I2C Master mode
            mode_class:     Calling class type. Used in 'uninitialize()' method.
        """
        super().__init__(ft_handle)
        self._mode_class = mode_class

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
        if self._handle is not None:
            if not (0 <= dev_address < (2 ** 16)):
                raise ValueError("dev_address must be in range <0, 65_535>.")
            if not (0 < read_byte_count < (2 ** 16)):
                raise ValueError("read_byte_count must be in range <1, 65_535>.")

            return read(self._handle, dev_address, read_byte_count)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "I2C Master has been uninitialized!"
            )

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
        if self._handle is not None:
            if not (0 <= dev_address < (2 ** 16)):
                raise ValueError("dev_address must be in range <0, 65_535>.")
            if not (0 < len(write_data) < (2 ** 16)):
                raise ValueError("write_data length must be in range <1, 65_535>.")

            return write(self._handle, dev_address, write_data)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "I2C Master has been uninitialized!"
            )

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
        if self._handle is not None:
            if not (0 <= dev_address < (2 ** 16)):
                raise ValueError("dev_address must be in range <0, 65_535>.")
            if not (0 < read_byte_count < (2 ** 16)):
                raise ValueError("read_byte_count must be in range <1, 65_535>.")

            return read_ex(self._handle, dev_address, flags, read_byte_count)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "I2C Master has been uninitialized!"
            )

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
        if self._handle is not None:
            if not (0 <= dev_address < (2 ** 16)):
                raise ValueError("dev_address must be in range <0, 65_535>.")
            if not (0 < len(write_data) < (2 ** 16)):
                raise ValueError("write_data length must be in range <1, 65_535>.")

            return write_ex(self._handle, dev_address, flags, write_data)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "I2C Master has been uninitialized!"
            )

    def get_status(self) -> CtrlStatus:
        """Get I2C Master controller status.

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            CtrlStatus:         IntFlag encoding controller status
        """
        if self._handle is not None:
            return get_status(self._handle)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "I2C Master has been uninitialized!"
            )

    def reset(self) -> None:
        """Reset the I2C Master.

        Note:
            It is no necessary to re-initialize the controller.
            It retains all its settings, and is ready to be used again.

        Raises:
            Ft4222Exception:    In case of unexpected error
        """
        if self._handle is not None:
            reset(self._handle)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "I2C Master has been uninitialized!"
            )

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
        if self._handle is not None:
            reset_bus(self._handle)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "I2C Master has been uninitialized!"
            )

    def close(self) -> None:
        """Uninitialize and close the owned handle.

        Note:
            A new handle must be opened and initialized
            after calling this method.

        Raises:
            Ft4222Exception:    In case of unexpected error
        """
        self.uninitialize().close()

    def uninitialize(self) -> T:
        """Uninitialize the owned handle from I2C Master mode.

        The handle can be initialized into any other supported mode.

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            T:                  A class encapsulating the opened stream type
        """
        if self._handle is not None:
            handle = self._handle
            self._handle = None
            return self._mode_class(uninitialize(handle))
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "I2C Master has been uninitialized already!",
            )
