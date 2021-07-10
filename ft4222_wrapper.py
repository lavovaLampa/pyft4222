#! /usr/bin/env python3

from ctypes import *
from enum import IntEnum, IntFlag, auto
from typing import NamedTuple, NewType, Optional, Tuple

from .ft_common import FTStatus, FtHandle

try:
    ftlib = cdll.LoadLibrary('./lib/libft4222.so.1.4.4.44')
except OSError as e:
    print("Unable to load shared library!")
    exit(1)


class FT4222Status(FTStatus):
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

    class GpioTrigger(IntEnum):
        GPIO_TRIGGER_RISING = 0x01
        GPIO_TRIGGER_FALLING = 0x02
        GPIO_TRIGGER_LEVEL_HIGH = 0x04
        GPIO_TRIGGER_LEVEL_LOW = 0X08

    class EventType(IntFlag):
        EVENT_RXCHAR = 8

    class RawVersion(Structure):
        _fields_ = [
            ("chipVersion", c_uint),
            ("dllVersion", c_uint)
        ]

    class Version(NamedTuple):
        chip_version: int
        dll_version: int

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
    _get_version.argtypes = [c_void_p, POINTER(RawVersion)]
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
    def set_event_notification(ft_handle: FtHandle, mask: EventType, param: c_void_p) -> None:
        retval: FT4222Status = FT4222._set_event_notification(
            ft_handle, mask.value, param)

        if retval != FT4222Status.OK:
            raise RuntimeError('TODO')

    @staticmethod
    def get_version(ft_handle: FtHandle) -> Optional[Version]:
        version = FT4222.RawVersion()
        retval: FT4222Status = FT4222._get_version(ft_handle, byref(version))

        if retval != FT4222Status.OK:
            raise RuntimeError('TODO')

        return FT4222.Version(version.chipVersion, version.dllVersion)

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
        pass

    @staticmethod
    def reset_transaction(ft_handle: FtHandle, spi_idx: int) -> None:
        pass

    @staticmethod
    def set_driving_strength(
        ft_handle: FtHandle,
        clk_strength: DriveStrength,
        io_strength: DriveStrength,
        sso_strength: DriveStrength
    ) -> None:
        pass

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
            sso_map: int
        ) -> None:
            pass

        @staticmethod
        def set_cs_polarity(ft_handle: FtHandle, cs_polarity: CsPolarity) -> None:
            pass

        @staticmethod
        def set_lines(ft_handle: FtHandle, io_mode: IoMode) -> None:
            pass

        @staticmethod
        def single_read(
            ft_handle: FtHandle,
            bytes_read: int,
            end_transaction: bool = True
        ) -> bytes:
            pass

        @staticmethod
        def single_write(
            ft_handle: FtHandle,
            write_data: bytes,
            end_transaction: bool = True
        ) -> int:
            pass

        @staticmethod
        def single_read_write(
            ft_handle: FtHandle,
            write_data: bytes,
            bytes_read: int,
            end_transaction: bool = True
        ) -> bytes:
            pass

        @staticmethod
        def multi_read_write(
            ft_handle: FtHandle,
            write_data: bytes,
            single_bytes_written: int,
            multi_bytes_written: int,
            multi_bytes_read: int
        ) -> bytes:
            pass

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
            pass

        @staticmethod
        def init_ex(ft_handle: FtHandle, protocol: IoProtocol) -> None:
            pass

        @staticmethod
        def set_mode(
            ft_handle: FtHandle,
            clk_polarity: 'SPI.ClkPolarity',
            clk_phase: 'SPI.ClkPhase'
        ) -> None:
            pass

        @staticmethod
        def get_rx_status(ft_handle: FtHandle) -> Optional[int]:
            pass

        @staticmethod
        def read(ft_handle: FtHandle, max_bytes_read: int) -> bytes:
            pass

        @staticmethod
        def write(ft_handle: FtHandle, write_data: bytes) -> int:
            pass


class I2C:
    class Master:
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
        def init(ft_handle: FtHandle, kbps: int) -> None:
            pass

        @staticmethod
        def read(ft_handle: FtHandle, dev_address: int, bytes_read: int) -> bytes:
            pass

        @staticmethod
        def write(ft_handle: FtHandle, dev_address: int, write_data: bytes) -> int:
            pass

        @staticmethod
        def read_ex(
            ft_handle: FtHandle,
            dev_address: int,
            flag: int,
            bytes_read: int
        ) -> bytes:
            pass

        @staticmethod
        def write_ex(
            ft_handle: FtHandle,
            dev_address: int,
            flag: int,
            write_data: bytes
        ) -> int:
            pass

        @staticmethod
        def reset(ft_handle: FtHandle) -> None:
            pass

        @staticmethod
        # FIXME: Proper return typing
        def get_status(ft_handle: FtHandle) -> int:
            pass

        @staticmethod
        def reset_bus(ft_handle: FtHandle) -> None:
            pass

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
            pass

        @staticmethod
        def reset(ft_handle: FtHandle) -> None:
            pass

        @staticmethod
        def get_address(ft_handle: FtHandle) -> int:
            pass

        @staticmethod
        def set_address(ft_handle: FtHandle, addr: int) -> None:
            pass

        @staticmethod
        def get_rx_status(ft_handle: FtHandle) -> int:
            pass

        @staticmethod
        def read(ft_handle: FtHandle, kbps: int) -> None:
            pass

        @staticmethod
        def write(ft_handle: FtHandle, bytes_read: int) -> bytes:
            pass

        @staticmethod
        def set_clock_stretch(ft_handle: FtHandle, enable: bool) -> None:
            pass

        @staticmethod
        def set_resp_word(ft_handle: FtHandle, response_word: int) -> None:
            pass

    class GPIO:
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
        def init(
            ft_handle: FtHandle,
            dirs: Tuple[Direction, Direction, Direction, Direction]
        ) -> None:
            pass

        @staticmethod
        def read(ft_handle: FtHandle, port_id: PortId) -> bool:
            pass

        @staticmethod
        def write(ft_handle: FtHandle, port_id: PortId, state: bool) -> None:
            pass

        @staticmethod
        def set_input_trigger(
            ft_handle: FtHandle,
            port_id: PortId,
            trigger: 'FT4222.GpioTrigger'
        ) -> None:
            pass

        @staticmethod
        def get_trigger_status(ft_handle: FtHandle, port_id: PortId) -> int:
            pass

        @staticmethod
        def read_trigger_queue(
            ft_handle: FtHandle,
            port_id: PortId,
            max_read_size: int
        ) -> Tuple['FT4222.GpioTrigger']:
            pass

        @staticmethod
        def set_waveform_mode(ft_handle: FtHandle, enable: bool) -> None:
            pass
