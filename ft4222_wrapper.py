#! /usr/bin/env python3

from ctypes import *
from enum import IntEnum, IntFlag, auto
from typing import Final, List, Literal, NamedTuple, NoReturn, Optional, Tuple, overload

from ft_common import FtHandle

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
        GPIO_TRIGGER_RISING = 0x01
        GPIO_TRIGGER_FALLING = 0x02
        GPIO_TRIGGER_LEVEL_HIGH = 0x04
        GPIO_TRIGGER_LEVEL_LOW = 0X08

    class EventType(IntFlag):
        EVENT_RXCHAR = 8

    class _RawVersion(Structure):
        _fields_ = [
            ("chipVersion", c_uint),
            ("dllVersion", c_uint)
        ]

    class Version(NamedTuple):
        chip_version: int
        dll_version: int

        @staticmethod
        def from_raw(raw_struct: 'FT4222._RawVersion') -> 'FT4222.Version':
            return FT4222.Version(
                raw_struct.chipVersion,
                raw_struct.dllVersion
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
    def uninitialize(ft_handle: FtHandle) -> None:
        retval: FT4222Status = FT4222._uninitialize(ft_handle)

        if retval != FT4222Status.OK:
            raise RuntimeError('TODO')

    @staticmethod
    def set_clock(ft_handle: FtHandle, clk_rate: ClockRate) -> None:
        retval: FT4222Status = FT4222._set_clock(ft_handle, clk_rate)

        if retval != FT4222Status.OK:
            raise RuntimeError('TODO')

    @staticmethod
    def get_clock(ft_handle: FtHandle) -> ClockRate:
        clk_rate = c_uint()
        retval: FT4222Status = FT4222._get_clock(ft_handle, byref(clk_rate))

        if retval != FT4222Status.OK:
            raise RuntimeError('TODO')

        return FT4222.ClockRate(clk_rate.value)

    @staticmethod
    def set_wakeup_interrupt(ft_handle: FtHandle, enable: bool) -> None:
        retval: FT4222Status = FT4222._set_wakeup_interrupt(ft_handle, enable)

        if retval != FT4222Status.OK:
            raise RuntimeError('TODO')

    @staticmethod
    def set_interrupt_trigger(ft_handle: FtHandle, trigger: GpioTrigger) -> None:
        retval: FT4222Status = FT4222._set_interrupt_trigger(
            ft_handle, trigger.value)

        if retval != FT4222Status.OK:
            raise RuntimeError('TODO')

    @staticmethod
    def set_suspend_out(ft_handle: FtHandle, enable: bool) -> None:
        retval: FT4222Status = FT4222._set_suspend_out(ft_handle, enable)

        if retval != FT4222Status.OK:
            raise RuntimeError('TODO')

    @staticmethod
    def get_max_transfer_size(ft_handle: FtHandle) -> int:
        max_size = c_uint16()
        retval: FT4222Status = FT4222._get_max_transfer_size(
            ft_handle, byref(max_size))

        if retval != FT4222Status.OK:
            raise RuntimeError('TODO')

        return max_size.value

    @staticmethod
    # FIXME: Proper typing
    def set_event_notification(
        ft_handle: FtHandle,
        mask: EventType,
        param: c_void_p
    ) -> None:
        retval: FT4222Status = FT4222._set_event_notification(
            ft_handle, mask.value, param)

        if retval != FT4222Status.OK:
            raise RuntimeError('TODO')

    @staticmethod
    def get_version(ft_handle: FtHandle) -> Version:
        version_struct = FT4222._RawVersion()
        retval: FT4222Status = FT4222._get_version(
            ft_handle, byref(version_struct))

        if retval != FT4222Status.OK:
            raise RuntimeError('TODO')

        return FT4222.Version.from_raw(version_struct)

    @staticmethod
    def chip_reset(ft_handle: FtHandle) -> None:
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
    def reset(ft_handle: FtHandle) -> None:
        result: FT4222Status = SPI._reset(ft_handle)

        if result != FT4222Status.OK:
            raise RuntimeError('TODO')

    @staticmethod
    def reset_transaction(ft_handle: FtHandle, spi_idx: int) -> None:
        result: FT4222Status = SPI._reset_transaction(ft_handle, spi_idx)

        if result != FT4222Status.OK:
            raise RuntimeError('TODO')

    @staticmethod
    def set_driving_strength(
        ft_handle: FtHandle,
        clk_strength: DriveStrength,
        io_strength: DriveStrength,
        sso_strength: DriveStrength
    ) -> None:
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

        @staticmethod
        def init(
            ft_handle: FtHandle,
            spi_mode: IoMode,
            clock_div: ClkDiv,
            clk_polarity: 'SPI.ClkPolarity',
            clk_phase: 'SPI.ClkPhase',
            sso_map: 'SPI.Master.SsoMap'
        ) -> None:
            result: FT4222Status = SPI.Master._init(
                ft_handle,
                spi_mode,
                clock_div,
                clk_polarity,
                clk_phase,
                sso_map
            )

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

        @staticmethod
        def set_cs_polarity(ft_handle: FtHandle, cs_polarity: CsPolarity) -> None:
            result: FT4222Status = SPI.Master._set_cs(ft_handle, cs_polarity)

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

        @staticmethod
        def set_lines(ft_handle: FtHandle, io_mode: IoMode) -> None:
            result: FT4222Status = SPI.Master._set_lines(ft_handle, io_mode)

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

        @staticmethod
        def single_read(
            ft_handle: FtHandle,
            read_byte_count: int,
            end_transaction: bool = True
        ) -> bytes:
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
            ft_handle: FtHandle,
            write_data: bytes,
            end_transaction: bool = True
        ) -> int:
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
            ft_handle: FtHandle,
            write_data: bytes,
            end_transaction: bool = True
        ) -> bytes:
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
            ft_handle: FtHandle,
            write_data: Literal[None],
            single_write_byte_count: Literal[0],
            multi_write_byte_count: Literal[0],
            multi_read_byte_count: int
        ) -> bytes: ...

        @overload
        def multi_read_write(
            ft_handle: FtHandle,
            write_data: bytes,
            single_write_byte_count: int,
            multi_write_byte_count: int,
            multi_read_byte_count: int
        ) -> bytes: ...

        @staticmethod
        def multi_read_write(
            ft_handle: FtHandle,
            write_data: Optional[bytes],
            single_write_byte_count: int,
            multi_write_byte_count: int,
            multi_read_byte_count: int
        ) -> bytes:
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
        def init(ft_handle: FtHandle) -> None:
            result: FT4222Status = SPI.Slave._init(ft_handle)

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

        @staticmethod
        def init_ex(ft_handle: FtHandle, protocol: IoProtocol) -> None:
            result: FT4222Status = SPI.Slave._init_ex(ft_handle, protocol)

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

        @staticmethod
        def set_mode(
            ft_handle: FtHandle,
            clk_polarity: 'SPI.ClkPolarity',
            clk_phase: 'SPI.ClkPhase'
        ) -> None:
            result: FT4222Status = SPI.Slave._set_mode(
                ft_handle,
                clk_polarity,
                clk_phase
            )

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

        @staticmethod
        def get_rx_status(ft_handle: FtHandle) -> int:
            rx_size = c_uint16()

            result: FT4222Status = SPI.Slave._get_rx_status(
                ft_handle,
                byref(rx_size)
            )

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

            return rx_size.value

        @staticmethod
        def read(ft_handle: FtHandle, read_byte_count: int) -> bytes:
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
        def write(ft_handle: FtHandle, write_data: bytes) -> int:
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
            CONTROLLER_BUSY = 1 << 0
            ERROR = 1 << 1
            SLAVE_ADDR_NACK = 1 << 2
            DATA_NACK = 1 << 3
            ARBITRATION_LOST = 1 << 4
            IDLE = 1 << 5
            BUS_BUSY = 1 << 6

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
        def init(ft_handle: FtHandle, kbps: int) -> None:
            result: FT4222Status = I2C.Master._init(
                ft_handle,
                kbps
            )

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

        @staticmethod
        def read(ft_handle: FtHandle, dev_address: int, read_byte_count: int) -> bytes:
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
        def write(ft_handle: FtHandle, dev_address: int, write_data: bytes) -> int:
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
            ft_handle: FtHandle,
            dev_address: int,
            flag: 'I2C.Master.TransactionFlag',
            read_byte_count: int
        ) -> bytes:
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
            ft_handle: FtHandle,
            dev_address: int,
            flag: 'I2C.Master.TransactionFlag',
            write_data: bytes
        ) -> int:
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
        def reset(ft_handle: FtHandle) -> None:
            result: FT4222Status = I2C.Master._reset(ft_handle)

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

        @staticmethod
        def get_status(ft_handle: FtHandle) -> 'I2C.Master.Status':
            status = c_uint8()

            result: FT4222Status = I2C.Master._get_status(
                ft_handle, byref(status))

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

            return I2C.Master.Status(status.value)

        @staticmethod
        def reset_bus(ft_handle: FtHandle) -> None:
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
        def init(ft_handle: FtHandle) -> None:
            result: FT4222Status = I2C.Slave._init(ft_handle)

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

        @staticmethod
        def reset(ft_handle: FtHandle) -> None:
            result: FT4222Status = I2C.Slave._reset(ft_handle)

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

        @staticmethod
        def get_address(ft_handle: FtHandle) -> int:
            addr = c_uint8()

            result: FT4222Status = I2C.Slave._get_address(
                ft_handle, byref(addr))

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

            return addr.value

        @staticmethod
        def set_address(ft_handle: FtHandle, addr: int) -> None:
            result: FT4222Status = I2C.Slave._set_address(ft_handle, addr)

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

        @staticmethod
        def get_rx_status(ft_handle: FtHandle) -> int:
            rx_size = c_uint16()

            result: FT4222Status = I2C.Slave._get_rx_status(
                ft_handle, byref(rx_size))

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

            return rx_size.value

        @staticmethod
        def read(ft_handle: FtHandle, read_byte_count: int) -> bytes:
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
        def write(ft_handle: FtHandle, write_data: bytes) -> int:
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
        def set_clock_stretch(ft_handle: FtHandle, enable: bool) -> None:
            result: FT4222Status = I2C.Slave._set_clock_stretch(
                ft_handle, enable)

            if result != FT4222Status.OK:
                raise RuntimeError('TODO')

        @staticmethod
        def set_resp_word(ft_handle: FtHandle, response_word: int) -> None:
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
    ) -> None:
        dir_array = (c_uint * GPIO._GPIO_COUNT)(dirs)

        result: FT4222Status = GPIO._init(ft_handle, dir_array)

        if result != FT4222Status.OK:
            raise RuntimeError('TODO')

    @staticmethod
    def read(ft_handle: FtHandle, port_id: PortId) -> bool:
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
    def write(ft_handle: FtHandle, port_id: PortId, state: bool) -> None:
        result: FT4222Status = GPIO._write(
            ft_handle,
            port_id,
            state
        )

        if result != FT4222Status.OK:
            raise RuntimeError('TODO')

    @staticmethod
    def set_input_trigger(
        ft_handle: FtHandle,
        port_id: PortId,
        trigger: 'FT4222.GpioTrigger'
    ) -> None:
        result: FT4222Status = GPIO._set_input_trigger(
            ft_handle,
            port_id,
            trigger
        )

        if result != FT4222Status.OK:
            raise RuntimeError('TODO')

    @staticmethod
    def get_trigger_status(ft_handle: FtHandle, port_id: PortId) -> int:
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
        ft_handle: FtHandle,
        port_id: PortId,
        max_read_size: int
    ) -> List['FT4222.GpioTrigger']:
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
    def set_waveform_mode(ft_handle: FtHandle, enable: bool) -> None:
        result: FT4222Status = GPIO._set_waveform_mode(ft_handle, enable)

        if result != FT4222Status.OK:
            raise RuntimeError('TODO')


if __name__ == '__main__':
    SPI.set_driving_strength(
        FtHandle(c_void_p(None)),
        SPI.DriveStrength.DS_4MA,
        SPI.DriveStrength.DS_4MA,
        SPI.DriveStrength.DS_4MA
    )
