from ft4222 import CommonHandle
from typing import Generic, Type, TypeVar
from wrapper.ft4222.common import uninitialize
from wrapper.ft4222 import Ft4222Exception, Ft4222Status
from wrapper import FtHandle

from wrapper.ft4222.i2c.slave import I2cSlaveHandle, get_address, get_rx_status, read, reset, set_address, set_clock_stretch, set_resp_word, write


T = TypeVar('T', bound=CommonHandle[FtHandle])


class I2CSlave(Generic[T], CommonHandle[I2cSlaveHandle]):
    """A class encapsulating I2C Slave functions.
    """
    _mode_class: Type[T]

    def __init__(self, ft_handle: I2cSlaveHandle, mode_class: Type[T]):
        """Initialize the class with given FT4222 handle and a mode class type.

        Args:
            ft_handle:      FT4222 handle initialized in I2C Master mode
            mode_class:     Calling class type. Used in 'uninitialize()' method.
        """
        super().__init__(ft_handle)
        self._mode_class = mode_class

    def get_address(self) -> int:
        """Get the address of I2C Slave device.

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            int:                Current I2C Slave address
        """
        if self._handle is not None:
            return get_address(self._handle)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "I2C Slave has been uninitialized!"
            )

    def set_address(self, addr: int) -> None:
        """Set the address of I2C Slave device.

        Args:
            addr:       Device address;     range <0, 65_535>

        Raises:
            Ft4222Exception:    In case of unexpected error
        """
        if self._handle is not None:
            if 0 <= addr < (2 ** 16):
                set_address(self._handle, addr)
            else:
                raise ValueError(
                    "addr must be in range <0, 65_535>."
                )
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "I2C Slave has been uninitialized!"
            )

    def get_rx_status(self) -> int:
        """Get number of bytes in Rx queue.

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            int:                Number of bytes in Rx queue
        """
        if self._handle is not None:
            return get_rx_status(self._handle)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "I2C Slave has been uninitialized!"
            )

    def read(self, read_byte_count: int) -> bytes:
        """Read data from the Rx queue.

        Args:
            read_byte_count:    Number of bytes to read;    range <1, 65_535>

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            bytes:              Read data
        """
        if self._handle is not None:
            if 0 < read_byte_count < (2 ** 16):
                return read(self._handle, read_byte_count)
            else:
                raise ValueError(
                    "read_byte_count must be in range <1, 65_535>."
                )
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "I2C Slave has been uninitialized!"
            )

    def write(self, write_data: bytes) -> int:
        """Write data into Tx queue.

        Args:
            write_data:     Non-empty list of bytes to write;   length <1, 65_535>

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            int:            Number of bytes written
        """
        if self._handle is not None:
            return write(self._handle, write_data)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "I2C Slave has been uninitialized!"
            )

    def set_clock_stretch(self, enable: bool) -> None:
        """Enable or disable clock stretching.

        Note:
            Clock stretching is disabled by default.

        Args:
            enable:     Enable clock stretching?

        Raises:
            Ft4222Exception:    In case of unexpected error
        """
        if self._handle is not None:
            set_clock_stretch(self._handle, enable)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "I2C Slave has been uninitialized!"
            )

    def set_resp_word(self, response_word: int) -> None:
        """Set response word in case of empty Tx queue.

        Note:
            The default value is 0xFF.

        This function only takes effect when Clock Stretch is disabled.
        When data is requested by an I2C master and the device
        is not ready to respond, the device will respond with a default value.

        Args:
            response_word:      A new response word;    range <0, 255>

        Raises:
            Ft4222Exception:    In case of unexpected error
        """
        if self._handle is not None:
            if 0 <= response_word < (2 ** 8):
                set_resp_word(self._handle, response_word)
            else:
                raise ValueError(
                    "response_word must be in range <0, 255>."
                )
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "I2C Slave has been uninitialized!"
            )

    def reset(self) -> None:
        """Reset the I2C Slave.

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
                Ft4222Status.DEVICE_NOT_OPENED,
                "I2C Slave has been uninitialized!"
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
        """Uninitialize the owned handle from I2C Slave mode.

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
                "I2C Slave has been uninitialized!"
            )
