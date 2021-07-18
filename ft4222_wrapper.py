#! /usr/bin/env python3

from ctypes import *
from enum import IntEnum, IntFlag, auto
from typing import Final, List, Literal, NamedTuple, NewType, NoReturn, Optional, Tuple, overload, Union

from ft_common import FtHandle

SpiMasterSingleHandle = NewType('SpiMasterSingleHandle', c_void_p)
SpiMasterMultiHandle = NewType('SpiMasterMultiHandle', c_void_p)
SpiMasterHandle = Union[SpiMasterSingleHandle, SpiMasterMultiHandle]

SpiSlaveRawHandle = NewType('SpiSlaveHandle', c_void_p)
SpiSlaveProtoHandle = NewType('SpiSlaveProtoHandle', c_void_p)
SpiSlaveHandle = Union[SpiSlaveRawHandle, SpiSlaveProtoHandle]

SpiHandle = Union[SpiMasterHandle, SpiSlaveHandle]

I2cMasterHandle = NewType('I2cMasterHandle', c_void_p)
I2cSlaveHandle = NewType('I2cSlaveHandle', c_void_p)
I2cHandle = Union[I2cMasterHandle, I2cSlaveHandle]

GpioHandle = NewType('GpioHandle', c_void_p)

InitializedHandle = Union[SpiHandle, I2cHandle, GpioHandle]

try:
    ftlib = cdll.LoadLibrary('./lib/libft4222.so.1.4.4.44')
except OSError as e:
    print("Unable to load shared library!")
    exit(1)


class FT4222Status(IntEnum):
    OK = 0
    INVALID_HANDLE = auto()
    DEVICE_NOT_FOUND = auto()
    DEVICE_NOT_OPENED = auto()
    IO_ERROR = auto()
    INSUFFICIENT_RESOURCES = auto()
    INVALID_PARAMETER = auto()
    INVALID_BAUD_RATE = auto()
    DEVICE_NOT_OPENED_FOR_ERASE = auto()
    DEVICE_NOT_OPENED_FOR_WRITE = auto()
    FAILED_TO_WRITE_DEVICE = auto()
    EEPROM_READ_FAILED = auto()
    EEPROM_WRITE_FAILED = auto()
    EEPROM_ERASE_FAILED = auto()
    EEPROM_NOT_PRESENT = auto()
    EEPROM_NOT_PROGRAMMED = auto()
    INVALID_ARGS = auto()
    NOT_SUPPORTED = auto()
    OTHER_ERROR = auto()
    DEVICE_LIST_NOT_READY = auto()

    # FT_STATUS extending message
    DEVICE_NOT_SUPPORTED = 1000
    CLK_NOT_SUPPORTED = auto()
    VENDER_CMD_NOT_SUPPORTED = auto()
    IS_NOT_SPI_MODE = auto()
    IS_NOT_I2C_MODE = auto()
    IS_NOT_SPI_SINGLE_MODE = auto()
    IS_NOT_SPI_MULTI_MODE = auto()
    WRONG_I2C_ADDR = auto()
    INVAILD_FUNCTION = auto()
    INVALID_POINTER = auto()
    EXCEEDED_MAX_TRANSFER_SIZE = auto()
    FAILED_TO_READ_DEVICE = auto()
    I2C_NOT_SUPPORTED_IN_THIS_MODE = auto()
    GPIO_NOT_SUPPORTED_IN_THIS_MODE = auto()
    GPIO_EXCEEDED_MAX_PORTNUM = auto()
    GPIO_WRITE_NOT_SUPPORTED = auto()
    GPIO_PULLUP_INVALID_IN_INPUTMODE = auto()
    GPIO_PULLDOWN_INVALID_IN_INPUTMODE = auto()
    GPIO_OPENDRAIN_INVALID_IN_OUTPUTMODE = auto()
    INTERRUPT_NOT_SUPPORTED = auto()
    GPIO_INPUT_NOT_SUPPORTED = auto()
    EVENT_NOT_SUPPORTED = auto()
    FUN_NOT_SUPPORT = auto()


class FT4222:
    class ClockRate(IntEnum):
        SYS_CLK_60 = 0
        SYS_CLK_24 = auto()
        SYS_CLK_48 = auto()
        SYS_CLK_80 = auto()

    class GpioTrigger(IntFlag):
        RISING = 0x01
        FALLING = 0x02
        LEVEL_HIGH = 0x04
        LEVEL_LOW = 0X08

    class EventType(IntFlag):
        EVENT_RXCHAR = 8

    class _RawVersion(Structure):
        _fields_ = [
            ("chip_version", c_uint),
            ("dll_version", c_uint)
        ]

    class Version(NamedTuple):
        chip_version: int
        dll_version: int

        @staticmethod
        def from_raw(raw_struct: 'FT4222._RawVersion') -> 'FT4222.Version':
            return FT4222.Version(
                raw_struct.chip_version,
                raw_struct.dll_version
            )

    _uninitialize = ftlib.FT4222_UnInitialize
    _uninitialize.argtypes = [c_void_p]
    _uninitialize.restype = FT4222Status

    _set_clock = ftlib.FT4222_SetClock
    _set_clock.argtypes = [c_void_p, c_uint]
    _set_clock.restype = FT4222Status

    _get_clock = ftlib.FT4222_GetClock
    _get_clock.argtypes = [c_void_p, POINTER(c_uint)]
    _get_clock.restype = FT4222Status

    _set_wakeup_interrupt = ftlib.FT4222_SetWakeUpInterrupt
    _set_wakeup_interrupt.argtypes = [c_void_p, c_bool]
    _set_wakeup_interrupt.restype = FT4222Status

    _set_interrupt_trigger = ftlib.FT4222_SetInterruptTrigger
    _set_interrupt_trigger.argtypes = [c_void_p, c_uint]
    _set_interrupt_trigger.restype = FT4222Status

    _set_suspend_out = ftlib.FT4222_SetSuspendOut
    _set_suspend_out.argtypes = [c_void_p, c_bool]
    _set_suspend_out.restype = FT4222Status

    _get_max_transfer_size = ftlib.FT4222_GetMaxTransferSize
    _get_max_transfer_size.argtypes = [c_void_p, POINTER(c_uint16)]
    _get_max_transfer_size.restype = FT4222Status

    _set_event_notification = ftlib.FT4222_SetEventNotification
    _set_event_notification.argtypes = [c_void_p, c_uint, c_void_p]
    _set_event_notification.restype = FT4222Status

    _get_version = ftlib.FT4222_GetVersion
    _get_version.argtypes = [c_void_p, POINTER(_RawVersion)]
    _get_version.restype = FT4222Status

    _chip_reset = ftlib.FT4222_ChipReset
    _chip_reset.argtypes = [c_void_p]
    _chip_reset.restype = FT4222Status

    @staticmethod
    def uninitialize(ft_handle: InitializedHandle) -> FtHandle:
        """Release allocated resources.

        This functions should be called before calling 'close()'.

        Args:
            ft_handle:  Handle to an initialized FT4222 device

        Raises:
            RuntimeError:   TODO
        """
        retval: FT4222Status = FT4222._uninitialize(ft_handle)

        if retval != FT4222Status.OK:
            raise RuntimeError('TODO')

        return FtHandle(ft_handle)

    @staticmethod
    def set_clock(ft_handle: FtHandle, clk_rate: ClockRate) -> None:
        """Set the system clock rate.

        The FT4222H supports 4 clock rates: 80MHz, 60MHz, 48MHz, or 24MHz.
        By default, the FT4222H runs at 60MHz clock rate.

        Args:
            ft_handle:  Handle to an opened FT4222 device
            clk_rate:   Desired system clock rate

        Raises:
            RuntimeError:   TODO
        """
        retval: FT4222Status = FT4222._set_clock(ft_handle, clk_rate)

        if retval != FT4222Status.OK:
            raise RuntimeError('TODO')

    @staticmethod
    def get_clock(ft_handle: FtHandle) -> ClockRate:
        """Get the current system clock rate.

        Args:
            ft_handle:  Handle to an opened FT4222 device

        Raises:
            RuntimeError:   TODO

        Returns:
            ClockRate:  Current system clock rate
        """
        clk_rate = c_uint()
        retval: FT4222Status = FT4222._get_clock(ft_handle, byref(clk_rate))

        if retval != FT4222Status.OK:
            raise RuntimeError('TODO')

        return FT4222.ClockRate(clk_rate.value)

    @staticmethod
    def set_wakeup_interrupt(ft_handle: FtHandle, enable: bool) -> None:
        """Enable or disable wakeup/interrupt.
        By default, wake-up/interrupt function is on.

        When Wake up/Interrupt function is on, GPIO3 pin acts as an input pin for wakeup/interrupt.
        While system is in normal mode, GPIO3 acts as an interrupt pin.
        While system is in suspend mode, GPIO3 acts as a wakeup pin.

        Args:
            ft_handle:  Handle to an opened FT4222 device
            enable:     Enable wakeup/interrupt function?

        Raises:
            RuntimeError:   TODO
        """
        retval: FT4222Status = FT4222._set_wakeup_interrupt(ft_handle, enable)

        if retval != FT4222Status.OK:
            raise RuntimeError('TODO')

    @staticmethod
    def set_interrupt_trigger(ft_handle: FtHandle, trigger: GpioTrigger) -> None:
        """Set trigger condition for the pin wakeup/interrupt.
        By default, the trigger condition is 'GpioTrigger.RISING'.

        This function configures trigger condition for wakeup/interrupt.

        When GPIO3 acts as wakeup pin, the ft4222H device has the capability to wake up the host.
        Only 'GpioTrigger.RISING' and 'GpioTrigger.FALLING' are valid when GPIO3 act as a wakeup pin.
        It is not necessary to call 'GPIO.init()' function to set up wake-up function.

        When GPIO3 acts as interrupt pin, all trigger conditions can be set.
        The result of trigger status can be inquired by 'GPIO.read_trigger_queue()' or 'GPIO.read()' functions.
        This is because the trigger status is provided by the GPIO pipe.
        Therefore it is necessary to call 'GPIO.init()' function to set up interrupt function.

        For GPIO triggering conditions: 'GpioTrigger.LEVEL_HIGH' and 'GpioTrigger.LEVEL_LOW',
        that can be configured when GPIO3 behaves as an interrupt pin, when the system enters suspend mode,
        these two configurations will act as 'GpioTrigger.RISING' and 'GpioTrigger.FALLING' respectively.

        Args:
            ft_handle:  Handle to an opened FT4222 device
            trigger:    WakeUp/Interrupt condition to set

        Raises:
            RuntimeError:   TODO
        """
        retval: FT4222Status = FT4222._set_interrupt_trigger(
            ft_handle, trigger.value)

        if retval != FT4222Status.OK:
            raise RuntimeError('TODO')

    @staticmethod
    def set_suspend_out(ft_handle: FtHandle, enable: bool) -> None:
        """Enable or disable suspend out, which will emit a signal when FT4222H enters suspend mode.

        Please note that the suspend-out pin is not available under mode 2.
        By default, suspend-out function is on.
        GPIO2 will be used as an GPIO in output mode for emitting a suspend-out signal.

        When suspend-out function is on, suspend-out pin emits signal according to suspend-out polarity.
        The default value of suspend-out polarity is active high.
        It means suspend-out pin output low in normal mode and output high in suspend mode.
        Suspend-out polarity only can be adjusted by FT_PROG.

        Args:
            ft_handle:  Handle to an opened FT4222 device
            enable:     Enable suspend-out signaling?

        Raises:
            RuntimeError:   TODO
        """
        retval: FT4222Status = FT4222._set_suspend_out(ft_handle, enable)

        if retval != FT4222Status.OK:
            raise RuntimeError('TODO')

    @staticmethod
    def get_max_transfer_size(ft_handle: FtHandle) -> int:
        """Get the maximum packet size in a transaction.

        It will be affected by different bus speeds, chip modes, and functions.
        The maximum transfer size is maximum size in writing path.

        Args:
            ft_handle:  Handle to an opened FT4222 device

        Raises:
            RuntimeError:   TODO

        Returns:
            int:    Maximum packet size in a transaction
        """
        max_size = c_uint16()
        retval: FT4222Status = FT4222._get_max_transfer_size(
            ft_handle, byref(max_size))

        if retval != FT4222Status.OK:
            raise RuntimeError('TODO')

        return max_size.value

    @staticmethod
    # FIXME: Proper typing
    def set_event_notification(
        ft_handle: SpiSlaveProtoHandle,
        mask: EventType,
        param: c_void_p
    ) -> None:
        """Sets conditions for event notification.

        An application can use this function to setup conditions which allow a thread to block until one of the conditions is met.
        Typically, an application will create an event, call this function, and then block on the event.
        When the conditions are met, the event is set, and the application thread unblocked.
        Usually, the event is set to notify the application to check the condition.
        The application needs to check the condition again before it goes to handle the condition.
        The API is only valid when the device acts as SPI slave and SPI slave protocol is not 'IoProtocol.No_PROTOCOL'. 

        Args:
            ft_handle:  Handle to an initialized FT4222 device in SPI Slave mode
            mask:       Event mask (i.e. select which events to react to)
            param:      TODO

        Raises:
            RuntimeError:   TODO
        """
        retval: FT4222Status = FT4222._set_event_notification(
            ft_handle, mask.value, param)

        if retval != FT4222Status.OK:
            raise RuntimeError('TODO')

    @staticmethod
    # FIXME: Add enum for chip version?
    def get_version(ft_handle: FtHandle) -> Version:
        """Get the version of FT4222H chip and LibFT4222 library.

        Args:
            ft_handle:  Handle to an opened FT4222 device

        Raises:
            RuntimeError:   TODO

        Returns:
            Version:    NamedTuple containing version information
        """
        version_struct = FT4222._RawVersion()
        retval: FT4222Status = FT4222._get_version(
            ft_handle, byref(version_struct))

        if retval != FT4222Status.OK:
            raise RuntimeError('TODO')

        return FT4222.Version.from_raw(version_struct)

    @staticmethod
    def chip_reset(ft_handle: FtHandle) -> None:
        """Software reset for a device.

        This function is used to attempt to recover system after a failure.
        It is a software reset for device.

        Args:
            ft_handle:  Handle to an opened FT4222 device

        Raises:
            RuntimeError:   TODO
        """
        retval: FT4222Status = FT4222._chip_reset(ft_handle)

        if retval != FT4222Status.OK:
            raise RuntimeError('TODO')


class SPI:
    class DriveStrength(IntEnum):
        DS_4MA = 0
        DS_8MA = auto()
        DS_12MA = auto()
        DS_16MA = auto()

    class ClkPolarity(IntEnum):
        CLK_IDLE_LOW = 0
        CLK_IDLE_HIGH = 1

    class ClkPhase(IntEnum):
        CLK_LEADING = 0
        CLK_TRAILING = 1

    _reset = ftlib.FT4222_SPI_Reset
    _reset.argtypes = [c_void_p]
    _reset.restype = FT4222Status

    _reset_transaction = ftlib.FT4222_SPI_ResetTransaction
    _reset_transaction.argtypes = [c_void_p, c_uint8]
    _reset_transaction.restype = FT4222Status

    _set_driving_strength = ftlib.FT4222_SPI_SetDrivingStrength
    _set_driving_strength.argtypes = [c_void_p, c_uint, c_uint, c_uint]
    _set_driving_strength.restype = FT4222Status

    @staticmethod
    def reset(ft_handle: SpiHandle) -> None:
        """Reset the SPI master or slave device.

        If the SPI bus encounters errors or works abnormally, this function will reset the SPIdevice.
        It is not necessary to call SPI init function again after calling this reset function.
        It retains all original setting of SPI.

        Args:
            ft_handle:  Handle to an initialized FT4222 device in SPI Master/Slave mode

        Raises:
            RuntimeError:   TODO
        """
        result: FT4222Status = SPI._reset(ft_handle)

        if result != FT4222Status.OK:
            raise RuntimeError('TODO')

    @staticmethod
    def reset_transaction(ft_handle: SpiHandle, spi_idx: int) -> None:
        """Reset the SPI transaction.

        Purge receive and transmit buffers in the device and reset the transaction state.

        Args:
            ft_handle:  Handle to an initialized FT4222 device in SPI Master/Slave mode
            spi_idx:    Index of SPI transaction (0 - 3), depending on the mode of the chip

        Raises:
            RuntimeError:   TODO
        """
        result: FT4222Status = SPI._reset_transaction(ft_handle, spi_idx)

        if result != FT4222Status.OK:
            raise RuntimeError('TODO')

    @staticmethod
    def set_driving_strength(
        ft_handle: SpiHandle,
        clk_strength: DriveStrength,
        io_strength: DriveStrength,
        sso_strength: DriveStrength
    ) -> None:
        """Set the driving strength of clk, io, and sso pins.

        Default driving strength of all spi pins is 'SPI.DriveStrength.DS_4MA'.
        Unless there is some hardware wiring requirement for device,
        setting driving strength to 4 mA should be enough.

        Args:
            ft_handle:  Handle to an initialized FT4222 device in SPI Master/Slave mode
        """
        result: FT4222Status = SPI._set_driving_strength(
            ft_handle,
            clk_strength,
            io_strength,
            sso_strength
        )

        if result != FT4222Status.OK:
            raise RuntimeError('TODO')

    class Master:
        class IoMode(IntEnum):
            IO_NONE = 0
            IO_SINGLE = 1
            IO_DUAL = 2
            IO_QUAD = 4

        class ClkDiv(IntEnum):
            CLK_NONE = 0
            CLK_DIV_2 = auto()  # 1/2   System Clock
            CLK_DIV_4 = auto()  # 1/4   System Clock
            CLK_DIV_8 = auto()  # 1/8   System Clock
            CLK_DIV_16 = auto()  # 1/16  System Clock
            CLK_DIV_32 = auto()  # 1/32  System Clock
            CLK_DIV_64 = auto()  # 1/64  System Clock
            CLK_DIV_128 = auto()  # 1/128 System Clock
            CLK_DIV_256 = auto()  # 1/256 System Clock
            CLK_DIV_512 = auto()  # 1/512 System Clock

        class CsPolarity(IntEnum):
            CS_ACTIVE_NEGTIVE = 0
            CS_ACTIVE_POSTIVE = auto()

        class SsoMap(IntFlag):
            SS_0 = 1
            SS_1 = 2
            SS_2 = 4
            SS_3 = 8

        _init = ftlib.FT4222_SPIMaster_Init
        _init.argtypes = [c_void_p, c_uint, c_uint, c_uint, c_uint, c_uint8]
        _init.restype = FT4222Status

        _set_cs = ftlib.FT4222_SPIMaster_SetCS
        _set_cs.argtypes = [c_void_p, c_uint]
        _set_cs.restype = FT4222Status

        _set_lines = ftlib.FT4222_SPIMaster_SetLines
        _set_lines.argtypes = [c_void_p, c_uint]
        _set_lines.restype = FT4222Status

        _single_read = ftlib.FT4222_SPIMaster_SingleRead
        _single_read.argtypes = [c_void_p, POINTER(
            c_uint8), c_uint16, POINTER(c_uint16), c_bool]
        _single_read.restype = FT4222Status

        _single_write = ftlib.FT4222_SPIMaster_SingleWrite
        _single_write.argtypes = [c_void_p, POINTER(
            c_uint8), c_uint16, POINTER(c_uint16), c_bool]
        _single_write.restype = FT4222Status

        _single_read_write = ftlib.FT4222_SPIMaster_SingleReadWrite
        _single_read_write.argtypes = [c_void_p, POINTER(c_uint8), POINTER(
            c_uint8), c_uint16, POINTER(c_uint16), c_bool]
        _single_read_write.restype = FT4222Status

        _multi_read_write = ftlib.FT4222_SPIMaster_MultiReadWrite
        _multi_read_write.argtypes = [c_void_p, POINTER(c_uint8), POINTER(
            c_uint8), c_uint8, c_uint16, c_uint16, POINTER(c_uint32)]
        _multi_read_write.restype = FT4222Status

        @overload
        def init(
            ft_handle: FtHandle,
            io_mode: Literal[IoMode.IO_SINGLE],
            clock_div: ClkDiv,
            clk_polarity: 'SPI.ClkPolarity',
            clk_phase: 'SPI.ClkPhase',
            sso_map: 'SPI.Master.SsoMap'
        ) -> SpiMasterSingleHandle: ...

        @overload
        def init(
            ft_handle: FtHandle,
            io_mode: Union[Literal[IoMode.IO_DUAL], Literal[IoMode.IO_QUAD]],
            clock_div: ClkDiv,
            clk_polarity: 'SPI.ClkPolarity',
            clk_phase: 'SPI.ClkPhase',
            sso_map: 'SPI.Master.SsoMap'
        ) -> SpiMasterMultiHandle: ...

        @overload
        def init(
            ft_handle: FtHandle,
            io_mode: Literal[IoMode.IO_NONE],
            clock_div: ClkDiv,
            clk_polarity: 'SPI.ClkPolarity',
            clk_phase: 'SPI.ClkPhase',
            sso_map: 'SPI.Master.SsoMap'
        ) -> NoReturn: ...

        @staticmethod
        def init(
            ft_handle: FtHandle,
            io_mode: IoMode,
            clock_div: ClkDiv,
            clk_polarity: 'SPI.ClkPolarity',
            clk_phase: 'SPI.ClkPhase',
            sso_map: 'SPI.Master.SsoMap'
        ) -> Union[SpiMasterSingleHandle, SpiMasterMultiHandle, NoReturn]:
            """Initialize the FT4222H as an SPI master.

            Args:
                ft_handle:      Handle to an open FT4222 device
                io_mode:        Data transmission mode (single, dual, quad)
                clock_div:      SPI clock rate division ratio (spi_clock = (sys_clk / clock_div))
                clk_polarity:   Clock polarity (idle low/high)
                clk_phase:      Clock phase (data sampled on the leading [first] or trailing [second] clock edge)
                sso_map:        Slave selection output pin map

            Raises:
                RuntimeError:   TODO

            Returns:
                SpiMasterHandle:    Handle to initialized SPI Master FT4222 device
            """
            result: FT4222Status = SPI.Master._init(
                ft_handle,
                io_mode,
                clock_div,
                clk_polarity,
                clk_phase,
                sso_map
            )

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

            if io_mode == SPI.Master.IoMode.IO_SINGLE:
                return SpiMasterSingleHandle(ft_handle)
            elif io_mode in set([SPI.Master.IoMode.IO_DUAL, SPI.Master.IoMode.IO_QUAD]):
                return SpiMasterMultiHandle(ft_handle)
            else:
                raise RuntimeError('TODO')

        @staticmethod
        def set_cs_polarity(ft_handle: SpiMasterHandle, cs_polarity: CsPolarity) -> None:
            """Change polarity of chip select signal.

            Default chip select is active low.

            Args:
                ft_handle:      Handle to an initialized FT4222 device in SPI Master mode
                cs_polarity:    Polarity of chip select signal

            Raises:
                RuntimeError:   TODO
            """
            result: FT4222Status = SPI.Master._set_cs(ft_handle, cs_polarity)

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

        @overload
        def set_lines(
            ft_handle: SpiMasterHandle,
            io_mode: Literal[IoMode.IO_SINGLE]
        ) -> SpiMasterSingleHandle: ...

        @overload
        def set_lines(
            ft_handle: SpiMasterHandle,
            io_mode: Union[Literal[IoMode.IO_DUAL], Literal[IoMode.IO_QUAD]]
        ) -> SpiMasterMultiHandle: ...

        @overload
        def set_lines(
            ft_handle: SpiMasterHandle,
            io_mode: Literal[IoMode.IO_NONE]
        ) -> NoReturn: ...

        @staticmethod
        def set_lines(ft_handle: SpiMasterHandle, io_mode: IoMode) -> Union[SpiMasterHandle, NoReturn]:
            """Switch the FT4222H SPI Master to single, dual, or quad mode.

            This overrides the mode passed to 'SPI.Master.init()' function.
            This might be needed if a device accepts commands in single mode but data transfer is using dual or quad mode.

            Args:
                ft_handle:  Handle to an initialized FT4222 device in SPI Master mode
                io_mode:    Desired IO mode (single, dual, quad)

            Raises:
                RuntimeError:   TODO

            Returns:
                SpiMasterHandle:    Handle to an initialized FT4222 device in SPI Master mode with selected io setting
            """
            result: FT4222Status = SPI.Master._set_lines(ft_handle, io_mode)

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

            if io_mode == SPI.Master.IoMode.IO_SINGLE:
                return SpiMasterSingleHandle(ft_handle)
            elif io_mode in set([SPI.Master.IoMode.IO_DUAL, SPI.Master.IoMode.IO_QUAD]):
                return SpiMasterMultiHandle(ft_handle)
            else:
                raise RuntimeError('TODO')

        @staticmethod
        def single_read(
            ft_handle: SpiMasterSingleHandle,
            read_byte_count: int,
            end_transaction: bool = True
        ) -> bytes:
            """Under SPI single mode, read data from an SPI slave.

            Args:
                ft_handle:          Handle to an initialized FT4222 device in SPI Master mode with 'IoMode.IO_SINGLE' setting
                read_byte_count:    Number of bytes to read
                end_transaction:    De-assert slave select pin at the end of transaction?

            Raises:
                RuntimeError:      TODO

            Returns:
                bytes:              Read data (count can be lower than requested) # TODO: Can it?
            """
            buffer = (c_uint8 * read_byte_count)()
            bytes_transferred = c_uint16()

            result: FT4222Status = SPI.Master._single_read(
                ft_handle,
                buffer,
                read_byte_count,
                byref(bytes_transferred),
                end_transaction
            )

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

            return bytes(buffer)

        @staticmethod
        def single_write(
            ft_handle: SpiMasterSingleHandle,
            write_data: bytes,
            end_transaction: bool = True
        ) -> int:
            """Under SPI single mode, write data to an SPI slave.

            Args:
                ft_handle:          Handle to an initialized FT4222 device in SPI Master mode with 'IoMode.IO_SINGLE' setting
                write_data:         Data to be written
                end_transaction:    De-assert slave select pin at the end of transaction?

            Raises:
                RuntimeError:       TODO

            Returns:
                int:                Number of transmitted bytes
            """
            bytes_transferred = c_uint16()
            result: FT4222Status = SPI.Master._single_write(
                ft_handle,
                write_data,
                len(write_data),
                byref(bytes_transferred),
                end_transaction
            )

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

            return bytes_transferred.value

        @staticmethod
        def single_read_write(
            ft_handle: SpiMasterSingleHandle,
            write_data: bytes,
            end_transaction: bool = True
        ) -> bytes:
            """Under SPI single mode, full-duplex write data to and read data from an SPI slave.

            Args:
                ft_handle:          Handle to an initialized FT4222 device in SPI Master mode with 'IoMode.IO_SINGLE' setting
                write_data:         Data to be written
                end_transaction:    De-assert slave select pin at the end of transaction?

            Raises:
                RuntimeError:       TODO

            Returns:
                bytes:              Received data
            """
            bytes_transferred = c_uint16()
            read_buffer = (c_uint8 * len(write_data))()

            result: FT4222Status = SPI.Master._single_read_write(
                ft_handle,
                read_buffer,
                write_data,
                len(write_data),
                byref(bytes_transferred),
                end_transaction
            )

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

            return bytes(read_buffer)

        @overload
        def multi_read_write(
            ft_handle: SpiMasterMultiHandle,
            write_data: Literal[None],
            single_write_byte_count: Literal[0],
            multi_write_byte_count: Literal[0],
            multi_read_byte_count: int
        ) -> bytes: ...

        @overload
        def multi_read_write(
            ft_handle: SpiMasterMultiHandle,
            write_data: bytes,
            single_write_byte_count: int,
            multi_write_byte_count: int,
            multi_read_byte_count: int
        ) -> bytes: ...

        @staticmethod
        def multi_read_write(
            ft_handle: SpiMasterMultiHandle,
            write_data: Optional[bytes],
            single_write_byte_count: int,
            multi_write_byte_count: int,
            multi_read_byte_count: int
        ) -> bytes:
            """Under SPI dual or quad mode, write data to and read data from an SPI slave.

            It is a mixed protocol initiated with a single write transmission,
            which may be an SPI command and dummy cycles,
            and followed by multi-io-write and multi-io-read transmission that use 2/4 signals in parallel for the data. 
            All three parts of the protocol are optional.

            Args:
                ft_handle:                  Handle to an initialized FT4222 device in SPI Master mode with 'IoMode.IO_DUAL' or 'IoMode'IO_QUAD' setting
                write_data:                 Data to be written
                single_write_byte_count:    Number of bytes to be written out using single IO line      (1st phase)
                multi_write_byte_count:     Number of bytes to be written out using multi IO lines      (2nd phase)
                multi_read_byte_count:      Number of bytes to be read using multi IO lines             (3rd phase)

            Raises:
                RuntimeError:               TODO

            Returns:
                bytes:                      Read data (if any)
            """
            read_buffer = (c_uint8 * multi_read_byte_count)()
            bytes_read = c_uint16()
            result: FT4222Status = SPI.Master._multi_read_write(
                ft_handle,
                read_buffer,
                write_data,
                single_write_byte_count,
                multi_write_byte_count,
                multi_read_byte_count,
                byref(bytes_read)
            )

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

            return bytes(read_buffer[:bytes_read])

    class Slave:
        class IoProtocol(IntEnum):
            WITH_PROTOCOL = 0
            NO_PROTOCOL = auto()
            NO_ACK = auto()

        _init = ftlib.FT4222_SPISlave_Init
        _init.argtypes = [c_void_p]
        _init.restype = FT4222Status

        _init_ex = ftlib.FT4222_SPISlave_InitEx
        _init_ex.argtypes = [c_void_p, c_uint]
        _init_ex.restype = FT4222Status

        _set_mode = ftlib.FT4222_SPISlave_SetMode
        _set_mode.argtypes = [c_void_p, c_uint, c_uint]
        _set_mode.restype = FT4222Status

        _get_rx_status = ftlib.FT4222_SPISlave_GetRxStatus
        _get_rx_status.argtypes = [c_void_p, POINTER(c_uint16)]
        _get_rx_status.restype = FT4222Status

        _read = ftlib.FT4222_SPISlave_Read
        _read.argtypes = [c_void_p, POINTER(
            c_uint8), c_uint16, POINTER(c_uint16)]
        _read.restype = FT4222Status

        _write = ftlib.FT4222_SPISlave_Write
        _write.argtypes = [c_void_p, POINTER(
            c_uint8), c_uint16, POINTER(c_uint16)]
        _write.restype = FT4222Status

        @staticmethod
        def init(ft_handle: FtHandle) -> SpiSlaveProtoHandle:
            """Initialize the FT4222H as an SPI slave.

            Default SPI Slave protocol is 'IoProtocol.WITH_PROTOCOL'.

            Args:
                ft_handle:              Handle to an open FT4222 device

            Raises:
                RuntimeError:           TODO

            Returns:
                SpiSlaveProtoHandle:    Handle to FT4222 device in SPI Slave mode with protocol
            """
            result: FT4222Status = SPI.Slave._init(ft_handle)

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

            return SpiSlaveProtoHandle(ft_handle)

        @overload
        def init_ex(
            ft_handle: FtHandle,
            protocol: Union[Literal[IoProtocol.WITH_PROTOCOL],
                            Literal[IoProtocol.NO_ACK]]
        ) -> SpiSlaveProtoHandle: ...

        @overload
        def init_ex(
            ft_handle: FtHandle,
            protocol: Literal[IoProtocol.NO_PROTOCOL]
        ) -> SpiSlaveHandle: ...

        @staticmethod
        def init_ex(ft_handle: FtHandle, protocol: IoProtocol) -> SpiSlaveHandle:
            """Initialize the FT4222H as an SPI slave.

            Similar to 'SPI.Slave.init()' function, but with parameters to define the transmission protocol.

            Args:
                ft_handle:      Handle to an open FT4222 device
                protocol:       Protocol to be used for communication (if any)

            Raises:
                RuntimeError:   TODO

            Returns:
                SpiSlaveHandle: Handle to FT4222 device in selected protocol mode
            """
            result: FT4222Status = SPI.Slave._init_ex(ft_handle, protocol)

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

            if protocol == SPI.Slave.IoProtocol.NO_PROTOCOL:
                return SpiSlaveRawHandle(ft_handle)
            else:
                return SpiSlaveProtoHandle(ft_handle)

        @staticmethod
        def set_mode(
            ft_handle: SpiSlaveHandle,
            clk_polarity: 'SPI.ClkPolarity',
            clk_phase: 'SPI.ClkPhase'
        ) -> None:
            """Set clock polarity and phase.

            Args:
                ft_handle:      Handle to an initialized FT4222 device in SPI Slave mode
                clk_polarity:   Clock polarity (idle low/high)
                clk_phase:      Clock phase

            Raises:
                RuntimeError:   TODO
            """
            result: FT4222Status = SPI.Slave._set_mode(
                ft_handle,
                clk_polarity,
                clk_phase
            )

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

        @staticmethod
        def get_rx_status(ft_handle: SpiSlaveHandle) -> int:
            """Get number of bytes in the receive queue.

            Args:
                ft_handle:      Handle to an initialized FT4222 device in SPI Slave mode

            Raises:
                RuntimeError:   TODO

            Return:             Number of bytes in the receive queue
            """
            rx_size = c_uint16()

            result: FT4222Status = SPI.Slave._get_rx_status(
                ft_handle,
                byref(rx_size)
            )

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

            return rx_size.value

        @staticmethod
        def read(ft_handle: SpiSlaveHandle, read_byte_count: int) -> bytes:
            """Read data from the receive queue of the SPI slave device.

            Args:
                ft_handle:          Handle to an initialized FT4222 device in SPI Slave mode
                read_byte_count:    Number of bytes to read from Rx queue

            Raises:
                RuntimeError:       TODO

            Returns:
                bytes:              Read data (if any)
            """
            read_buffer = (c_uint8 * read_byte_count)()
            bytes_read = c_uint16()

            result: FT4222Status = SPI.Slave._read(
                ft_handle,
                read_buffer,
                len(read_buffer),
                byref(bytes_read)
            )

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

            return bytes(read_buffer[:bytes_read.value])

        @staticmethod
        def write(ft_handle: SpiSlaveHandle, write_data: bytes) -> int:
            """Write data to the transmit queue of the SPI slave device.

            NOTE: For some reasons, support lib will append a dummy byte (0x00) at the first byte automatically.
            This additional byte exists at all of the three transfer methods.

            Args:
                ft_handle:      Handle to an initialized FT4222 device in SPI Slave mode
                write_data:     Data to be written into Tx queue

            Raises:
                RuntimeError:   TODO

            Returns:
                int:            Number of bytes written into Tx queue
            """
            bytes_written = c_uint16()

            result: FT4222Status = SPI.Slave._write(
                ft_handle,
                write_data,
                len(write_data),
                byref(bytes_written)
            )

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

            return bytes_written.value


class I2C:
    class Master:
        class TransactionFlag(IntEnum):
            NONE = 0x80
            START = 0x02
            REPEATED_START = 0x03  # Repeated_START will not send master code in HS mode
            STOP = 0x04
            START_AND_STOP = 0x06  # START condition followed by SEND and STOP condition

        class Status(IntFlag):
            CONTROLLER_BUSY = 1 << 0    # Controller busy; all other status bits are invalid
            ERROR = 1 << 1              # Error condition
            SLAVE_ADDR_NACK = 1 << 2    # Slave address was not acknowledged during last operation
            DATA_NACK = 1 << 3          # Data not acknowledged during last operation
            ARBITRATION_LOST = 1 << 4   # Arbitration lost during last operation
            IDLE = 1 << 5               # Controller idle
            BUS_BUSY = 1 << 6           # Bus busy

        _init = ftlib.FT4222_I2CMaster_Init
        _init.argtypes = [c_void_p, c_uint32]
        _init.restype = FT4222Status

        _read = ftlib.FT4222_I2CMaster_Read
        _read.argtypes = [c_void_p, c_uint16, POINTER(
            c_uint8), c_uint16, POINTER(c_uint16)]
        _read.restype = FT4222Status

        _write = ftlib.FT4222_I2CMaster_Write
        _write.argtypes = [c_void_p, c_uint16, POINTER(
            c_uint8), c_uint16, POINTER(c_uint16)]
        _write.restype = FT4222Status

        _read_ex = ftlib.FT4222_I2CMaster_ReadEx
        _read_ex.argtypes = [c_void_p, c_uint16, c_uint8,
                             POINTER(c_uint8), c_uint16, POINTER(c_uint16)]
        _read_ex.restype = FT4222Status

        _write_ex = ftlib.FT4222_I2CMaster_WriteEx
        _write_ex.argtypes = [c_void_p, c_uint16, c_uint8,
                              POINTER(c_uint8), c_uint16, POINTER(c_uint16)]
        _write_ex.restype = FT4222Status

        _reset = ftlib.FT4222_I2CMaster_Reset
        _reset.argtypes = [c_void_p]
        _reset.restype = FT4222Status

        _get_status = ftlib.FT4222_I2CMaster_GetStatus
        _get_status.argtypes = [c_void_p, POINTER(c_uint8)]
        _get_status.restype = FT4222Status

        _reset_bus = ftlib.FT4222_I2CMaster_ResetBus
        _reset_bus.argtypes = [c_void_p]
        _reset_bus.restype = FT4222Status

        @staticmethod
        # FIXME: Check kbps typing?
        def init(ft_handle: FtHandle, kbps: int) -> I2cMasterHandle:
            """Initialize the FT4222H as an I2C master with the requested I2C speed. 

            Args:
                ft_handle:          Handle to an opened FT4222 device
                kbps:               I2C transmission speed (60K - 3400K)

            Raises:
                RuntimeError:       TODO

            Returns:
                I2cMasterHandle:    Handle to initialized FT4222 device in I2C Master mode
            """
            result: FT4222Status = I2C.Master._init(
                ft_handle,
                kbps
            )

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

            return I2cMasterHandle(ft_handle)

        @staticmethod
        def read(
            ft_handle: I2cMasterHandle,
            dev_address: int,
            read_byte_count: int
        ) -> bytes:
            """Read data from the specified I2C slave device with START and STOP conditions.

            Args:
                ft_handle:          Handle to an initialized FT4222 device in I2C Master mode
                dev_address:        Address of the target I2C slave
                read_byte_count:    Number of bytes to read

            Raises:
                RuntimeError:       TODO

            Returns:
                bytes:              Read data
            """
            read_buffer = (c_uint8 * read_byte_count)()
            bytes_read = c_uint16()

            result: FT4222Status = I2C.Master._read(
                ft_handle,
                dev_address,
                read_buffer,
                len(read_buffer),
                byref(bytes_read)
            )

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

            return bytes(read_buffer[:bytes_read.value])

        @staticmethod
        def write(
            ft_handle: I2cMasterHandle,
            dev_address: int,
            write_data: bytes
        ) -> int:
            """Write data to the specified I2C slave device with START and STOP conditions.

            Args:
                ft_handle:      Handle to an initialized FT4222 device in I2C Master mode
                dev_address:    Address of the target I2C slave
                write_data:     Data to write

            Raises:
                RuntimeError:   TODO

            Returns:
                int:            Number of bytes written
            """
            bytes_written = c_uint16()

            result: FT4222Status = I2C.Master._write(
                ft_handle,
                dev_address,
                write_data,
                len(write_data),
                byref(bytes_written)
            )

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

            return bytes_written.value

        @staticmethod
        def read_ex(
            ft_handle: I2cMasterHandle,
            dev_address: int,
            flag: 'I2C.Master.TransactionFlag',
            read_byte_count: int
        ) -> bytes:
            """Read data from the specified I2C slave device with the specified I2C condition.

            NOTE: This function is supported by the rev. B FT4222H or later!

            Args:
                ft_handle:          Handle to an initialized FT4222 device in SPI Master mode
                dev_address:        Address of target I2C slave device
                flag:               I2C transaction condition flag
                read_byte_count:    Number of bytes to read

            Raises:
                RuntimeError:       TODO

            Returns:
                bytes:              Read data
            """
            read_buffer = (c_uint8 * read_byte_count)()
            bytes_read = c_uint16()

            result: FT4222Status = I2C.Master._read_ex(
                ft_handle,
                dev_address,
                flag,
                read_buffer,
                len(read_buffer),
                byref(bytes_read)
            )

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

            return bytes(read_buffer[:bytes_read.value])

        @staticmethod
        def write_ex(
            ft_handle: I2cMasterHandle,
            dev_address: int,
            flag: 'I2C.Master.TransactionFlag',
            write_data: bytes
        ) -> int:
            """Write data to a specified I2C slave device with the specified I2C condition.

            NOTE: This function is supported by the rev. B FT4222H or later!

            Args:
                ft_handle:      Handle to an initialized FT4222 device in I2C Master mode
                dev_address:    Address of target I2C slave device
                flag:           I2C transaction condition flag
                write_data:     Data to write

            Raises:
                RuntimeError:   TODO

            Returns:
                int:            Number of bytes written
            """
            bytes_written = c_uint16()

            result: FT4222Status = I2C.Master._write_ex(
                ft_handle,
                dev_address,
                flag,
                write_data,
                len(write_data),
                byref(bytes_written)
            )

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

            return bytes_written.value

        @staticmethod
        def reset(ft_handle: I2cMasterHandle) -> None:
            """Reset the I2C master device.

            If the I2C bus encounters errors or works abnormally, this function will reset the I2C device.
            It is not necessary to call 'I2C.Master.Init()' again after calling this reset function.
            This function will maintain the original I2C master setting and clear all cache in the device.

            Args:
                ft_handle:      Handle to an initialized FT4222 device in I2C Master mode

            Raises:
                RuntimeError:   TODO
            """
            result: FT4222Status = I2C.Master._reset(ft_handle)

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

        @staticmethod
        def get_status(ft_handle: I2cMasterHandle) -> 'I2C.Master.Status':
            """Read the status of the I2C master controller.

            This can be used to poll a slave after I2C transmission is complete.

            Args:
                ft_handle:          Handle to an initialized FT4222 device in I2C Master mode

            Raises:
                RuntimeError:       TODO

            Returns:
                I2C.Master.Status:  Controller status
            """
            status = c_uint8()

            result: FT4222Status = I2C.Master._get_status(
                ft_handle, byref(status))

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

            return I2C.Master.Status(status.value)

        @staticmethod
        def reset_bus(ft_handle: I2cMasterHandle) -> None:
            """Reset I2C bus.

            If the data line (SDA) is stuck LOW by the slave device, this function will make the master send nine SCK clocks to recover the I2C bus.
            The slave device that held the data line (SDA) LOW will release it within these nine clocks.
            If not, then use the HW reset or cycle power to clear the bus.

            Args:
                ft_handle:      Handle to an initialized FT4222 device in I2C Master mode

            Raises:
                RuntimeError:   TODO
            """
            result: FT4222Status = I2C.Master._reset_bus(ft_handle)

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

    class Slave:
        _init = ftlib.FT4222_I2CSlave_Init
        _init.argtypes = [c_void_p]
        _init.restype = FT4222Status

        _reset = ftlib.FT4222_I2CSlave_Reset
        _reset.argtypes = [c_void_p]
        _reset.restype = FT4222Status

        _get_address = ftlib.FT4222_I2CSlave_GetAddress
        _get_address.argtypes = [c_void_p, POINTER(c_uint8)]
        _get_address.restype = FT4222Status

        _set_address = ftlib.FT4222_I2CSlave_SetAddress
        _set_address.argtypes = [c_void_p, c_uint8]
        _set_address.restype = FT4222Status

        _get_rx_status = ftlib.FT4222_I2CSlave_GetRxStatus
        _get_rx_status.argtypes = [c_void_p, POINTER(c_uint16)]
        _get_rx_status.restype = FT4222Status

        _read = ftlib.FT4222_I2CSlave_Read
        _read.argtypes = [c_void_p, POINTER(
            c_uint8), c_uint16, POINTER(c_uint16)]
        _read.restype = FT4222Status

        _write = ftlib.FT4222_I2CSlave_Write
        _write.argtypes = [c_void_p, POINTER(
            c_uint8), c_uint16, POINTER(c_uint16)]
        _write.restype = FT4222Status

        _set_clock_stretch = ftlib.FT4222_I2CSlave_SetClockStretch
        _set_clock_stretch.argtypes = [c_void_p, c_bool]
        _set_clock_stretch.restype = FT4222Status

        _set_resp_word = ftlib.FT4222_I2CSlave_SetRespWord
        _set_resp_word.argtypes = [c_void_p, c_uint8]
        _set_resp_word.restype = FT4222Status

        @staticmethod
        def init(ft_handle: FtHandle) -> I2cSlaveHandle:
            """Initialized FT4222H as an I2C slave.

            After initialization, the I2C slave address is set to 0x40.

            Args:
                ft_handle:      Handle to an opened FT4222 device

            Raises:
                RuntimeError:   TODO

            Returns:
                I2cSlaveHandle: Handle to initialized FT4222 device in I2C Slave mode
            """
            result: FT4222Status = I2C.Slave._init(ft_handle)

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

            return I2cSlaveHandle(ft_handle)

        @staticmethod
        def reset(ft_handle: I2cSlaveHandle) -> None:
            """Reset the I2C slave device.

            This function will maintain the original i2c slave setting and clear all cache in the device.

            Args:
                ft_handle:      Handle to an initialized FT4222 device in I2C Slave mode
            
            Raises:
                RuntimeError:    TODO
            """
            result: FT4222Status = I2C.Slave._reset(ft_handle)

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

        @staticmethod
        def get_address(ft_handle: I2cSlaveHandle) -> int:
            """Get the address of the I2C slave device.

            Default address is 0x40.

            Args:
                ft_handle:      Handle to an initialized FT4222 device in I2C Slave mode

            Raises:
                RuntimeError:   TODO

            Returns:
                int:            Current I2C slave address
            """
            addr = c_uint8()

            result: FT4222Status = I2C.Slave._get_address(
                ft_handle, byref(addr))

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

            return addr.value

        @staticmethod
        def set_address(ft_handle: I2cSlaveHandle, addr: int) -> None:
            """Set the address of the I2C slave device.

            Args:
                ft_handle:      Handle to an initialized FT4222 device in I2C Slave mode
                addr:           Address to be set

            Raises:
                RuntimeError:   TODO
            """
            result: FT4222Status = I2C.Slave._set_address(ft_handle, addr)

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

        @staticmethod
        def get_rx_status(ft_handle: I2cSlaveHandle) -> int:
            """Get number of bytes in the receive queue.
            
            Args:
                ft_handle:      Handle to an initialized FT4222 device in I2C Slave mode

            Raises:
                RuntimeError:   TODO

            Returns:
                int:            Number of bytes in Rx queue
            """
            rx_size = c_uint16()

            result: FT4222Status = I2C.Slave._get_rx_status(
                ft_handle, byref(rx_size))

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

            return rx_size.value

        @staticmethod
        def read(ft_handle: I2cSlaveHandle, read_byte_count: int) -> bytes:
            """Read data from the buffer of the I2C slave device.
            
            Args:
                ft_handle:          Handle to an initialized FT4222 device in I2C Slave mode
                read_byte_count:    Number of bytes to read

            Raises:
                RuntimeError:   TODO

            Returns:
                bytes:              Read data
            """
            read_buffer = (c_uint8 * read_byte_count)()
            bytes_read = c_uint16()

            result: FT4222Status = I2C.Slave._read(
                ft_handle,
                read_buffer,
                len(read_buffer),
                byref(bytes_read)
            )

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

            return bytes(read_buffer[:bytes_read.value])

        @staticmethod
        def write(ft_handle: I2cSlaveHandle, write_data: bytes) -> int:
            """Write data to the buffer of I2C slave device.
            
            Args:
                ft_handle:      Handle to an initialized FT4222 device in I2C Slave mode
                write_data:     Data to write into Tx queue

            Raises:
                RuntimeError:   TODO

            Returns:
                int:            Number of bytes written
            """
            bytes_written = c_uint16()

            result: FT4222Status = I2C.Slave._write(
                ft_handle,
                write_data,
                len(write_data),
                byref(bytes_written)
            )

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

            return bytes_written.value

        @staticmethod
        def set_clock_stretch(ft_handle: I2cSlaveHandle, enable: bool) -> None:
            """Enable or disable Clock Stretch.

            The default setting of clock stretching is disabled.

            Clock stretch is as a flow-control mechanism for slaves.
            An addressed slave device may hold the clock line (SCL) low after receiving (or sending) a byte,
            indicating that it is not yet ready to process more data.
            The master that is communicating with the slave may not finish the transmission of the current bit,
            but must wait until the clock line actually goes high.

            Args:
                ft_handle:      Handle to an initialized FT4222 device in I2C Slave mode
                enable:         Enable clock stretching?

            Raises:
                RuntimeError:   TODO
            """
            result: FT4222Status = I2C.Slave._set_clock_stretch(
                ft_handle, enable)

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

        @staticmethod
        def set_resp_word(ft_handle: I2cSlaveHandle, response_word: int) -> None:
            """Set the response word in case of empty Tx queue.

            Default value is 0xFF.

            This function only takes effect when Clock Stretch is disabled.
            When data is requested by an I2C master and the device is not ready to respond,
            the device will respond with a default value.

            Args:
                ft_handle:      Handle to an initialized FT4222 device in I2C Slave mode
                response_word:  Response word to be set

            Raises:
                RuntimeError:   TODO
            """
            result: FT4222Status = I2C.Slave._set_resp_word(
                ft_handle, response_word)

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')


class GPIO:
    _GPIO_COUNT: Final[int] = 4

    class Direction(IntEnum):
        GPIO_OUTPUT = 0,
        GPIO_INPUT = auto()

    class PortId(IntEnum):
        PORT_0 = 0
        PORT_1 = auto()
        PORT_2 = auto()
        PORT_3 = auto()

    _init = ftlib.FT4222_GPIO_Init
    _init.argtypes = [c_void_p, c_uint * 4]
    _init.restype = FT4222Status

    _read = ftlib.FT4222_GPIO_Read
    _read.argtypes = [c_void_p, c_uint, POINTER(c_bool)]
    _read.restype = FT4222Status

    _write = ftlib.FT4222_GPIO_Write
    _write.argtypes = [c_void_p, c_uint, c_bool]
    _write.restype = FT4222Status

    _set_input_trigger = ftlib.FT4222_GPIO_SetInputTrigger
    _set_input_trigger.argtypes = [c_void_p, c_uint, c_uint]
    _set_input_trigger.restype = FT4222Status

    _get_trigger_status = ftlib.FT4222_GPIO_GetTriggerStatus
    _get_trigger_status.argtypes = [c_void_p, c_uint, POINTER(c_uint16)]
    _get_trigger_status.restype = FT4222Status

    _read_trigger_queue = ftlib.FT4222_GPIO_ReadTriggerQueue
    _read_trigger_queue.argtypes = [
        c_void_p, c_uint, POINTER(c_uint), c_uint16, POINTER(c_uint16)]
    _read_trigger_queue.restype = FT4222Status

    _set_waveform_mode = ftlib.FT4222_GPIO_SetWaveFormMode
    _set_waveform_mode.argtypes = [c_void_p, c_bool]
    _set_waveform_mode.restype = FT4222Status

    @staticmethod
    # FIXME: Better argument typing!
    def init(
        ft_handle: FtHandle,
        dirs: Tuple[Direction, Direction, Direction, Direction]
    ) -> GpioHandle:
        """Initialize the GPIO interface of the FT4222H.

        NOTE: The GPIO interface is available on the 2nd USB interface in mode 0 or on the 4th USB interface in mode 1.

        Args:
            ft_handle:      Handle to an opened FT4222 device
            dirs:           Tuple of directions to be set for each GPIO index - [0, 1, 2, 3]

        Raises:
            RuntimeError:   TODO

        Returns:
            GpioHandle:     Handle to initialized FT4222 device in GPIO mode
        """
        dir_array = (c_uint * GPIO._GPIO_COUNT)(dirs)

        result: FT4222Status = GPIO._init(ft_handle, dir_array)

        if result != FT4222Status.OK:
            raise RuntimeError('TODO')

        return GpioHandle(ft_handle)

    @staticmethod
    def read(ft_handle: GpioHandle, port_id: PortId) -> bool:
        """Read the status of a specified GPIO pin or interrupt register.
        
        Args:
            ft_handle:      Handle to an initialized FT4222 device in GPIO mode
            port_id:        GPIO port index

        Raises:
            RuntimeError:   TODO

        Returns:
            bool:           Is the port active/high?
        """
        gpio_state = c_bool()

        result: FT4222Status = GPIO._read(
            ft_handle,
            port_id,
            byref(gpio_state)
        )

        if result != FT4222Status.OK:
            raise RuntimeError('TODO')

        return gpio_state.value

    @staticmethod
    def write(ft_handle: GpioHandle, port_id: PortId, state: bool) -> None:
        """Write value to the specified GPIO pin.
        
        Args:
            ft_handle:      Handle to an initialized FT4222 device in GPIO mode
            port_id:        GPIO port index
            state:          State to set

        Raises:
            RuntimeError:   TODO
        """
        result: FT4222Status = GPIO._write(
            ft_handle,
            port_id,
            state
        )

        if result != FT4222Status.OK:
            raise RuntimeError('TODO')

    @staticmethod
    def set_input_trigger(
        ft_handle: GpioHandle,
        port_id: PortId,
        trigger: 'FT4222.GpioTrigger'
    ) -> None:
        """Set software trigger conditions on the specified GPIO pin.

        This function allows developers to monitor value changes of the GPIO pins.
        Values that satisfy the trigger condition will be stored in a queue.

        For example, if 'FT4222.GpioTrigger.RISING' is set on 'PortId.GPIO_0',
        and 'PortId.GPIO_0' then changes value from 0 to 1,
        the event GPIO_TRIGGER_RISING will be recorded into the queue.

        Developers can query the queue status using 'GPIO.get_trigger_status()' and 'GPIO.read_trigger_queue()' functions.

        NOTE: This function can only set GPIO trigger conditions.
        
        Args:
            ft_handle:      Handle to an initialized FT4222 device in GPIO mode
            port_id:        GPIO port index
            trigger:        Trigger type mask (using OR operator)

        Raises:
            RuntimeError:   TODO
        """
        result: FT4222Status = GPIO._set_input_trigger(
            ft_handle,
            port_id,
            trigger
        )

        if result != FT4222Status.OK:
            raise RuntimeError('TODO')

    @staticmethod
    def get_trigger_status(ft_handle: GpioHandle, port_id: PortId) -> int:
        """Get the size of trigger event queue.

        Args:
            ft_handle:      Handle to an initialized FT4222 device in GPIO mode
            port_id:        GPIO port index

        Raises:
            RuntimeError:   TODO

        Returns:
            int:            Number of triggers in event queue for selected GPIO port
        """
        queue_size = c_uint16()

        result: FT4222Status = GPIO._get_trigger_status(
            ft_handle,
            port_id,
            byref(queue_size)
        )

        if result != FT4222Status.OK:
            raise RuntimeError('TODO')

        return queue_size.value

    @staticmethod
    def read_trigger_queue(
        ft_handle: GpioHandle,
        port_id: PortId,
        max_read_size: int
    ) -> List['FT4222.GpioTrigger']:
        """Get events recorded in the trigger event queue.

        After calling this function, all events will be removed from the event queue.
        
        Args:
            ft_handle:                  Handle to an initialized FT4222 device in GPIO mode
            port_id:                    GPIO port index
            max_read_size:              Number of event to read from queue

        Raises:
            RuntimeError:               TODO

        Returns:
            List[FT4222.GpioTrigger]:   List of trigger events (if any)
        """
        event_buffer = (c_uint * max_read_size)()
        events_read = c_uint16()

        result: FT4222Status = GPIO._read_trigger_queue(
            ft_handle,
            port_id,
            event_buffer,
            len(event_buffer),
            byref(events_read)
        )

        if result != FT4222Status.OK:
            raise RuntimeError('TODO')

        return list(map(lambda x: FT4222.GpioTrigger(x), event_buffer[:events_read.value]))

    @staticmethod
    def set_waveform_mode(ft_handle: GpioHandle, enable: bool) -> None:
        """Enable or disable WaveForm Mode.

        When WaveForm mode is enabled, the device will record all GPIO status periodically.
        The peeking time depends on the system clock.
        The default setting of WaveForm mode is disabled.
        
        Args:
            ft_handle:      Handle to an initialized FT4222 device in GPIO mode
            enable:         Enable WaveForm mode?

        Raises:
            RuntimeError:   TODO
        """
        result: FT4222Status = GPIO._set_waveform_mode(ft_handle, enable)

        if result != FT4222Status.OK:
            raise RuntimeError('TODO')


if __name__ == '__main__':
    new_handle = SPI.Master.init(
        FtHandle(c_void_p(None)),
        SPI.Master.IoMode.IO_SINGLE,
        SPI.Master.ClkDiv.CLK_DIV_2,
        SPI.ClkPolarity.CLK_IDLE_LOW,
        SPI.ClkPhase.CLK_LEADING,
        SPI.Master.SsoMap.SS_0 | SPI.Master.SsoMap.SS_1
    )
    SPI.set_driving_strength(
        new_handle,
        SPI.DriveStrength.DS_4MA,
        SPI.DriveStrength.DS_4MA,
        SPI.DriveStrength.DS_4MA
    )

    next_handle = SPI.Slave.init_ex(
        FtHandle(c_void_p(None)),
        SPI.Slave.IoProtocol.NO_ACK
    )
