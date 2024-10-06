import time
import network



def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            print('WiFi is not connected...', wlan.ifconfig())
            time.sleep(1)
    print('WiFi connected:', wlan.ifconfig())

from micropython import const  # NOQA
from i2c import I2C
import gt911
import lcd_bus
import task_handler
import lvgl as lv  # NOQA
import rgb_display


_WIDTH = const(800)
_HEIGHT = const(480)

_BUFFER_SIZE = const(768000)

_CTP_SCL = const(9)
_CTP_SDA = const(8)
_CTP_IRQ = const(4)

_SD_MOSI = const(11)
_SD_SCK = const(12)
_SD_MISO = const(13)

_LCD_FREQ = const(13000000)
_PCLK_ACTIVE_NEG = const(0)

_HSYNC_PULSE_WIDTH = const(10)
_HSYNC_BACK_PORCH = const(10)
_HSYNC_FRONT_PORCH = const(10)

_VSYNC_PULSE_WIDTH = const(10)
_VSYNC_BACK_PORCH = const(10)
_VSYNC_FRONT_PORCH = const(20)

_PCLK = const(7)
_HSYNC = const(46)
_VSYNC = const(3)
_DE = const(5)
_DISP = None
_BCKL = None
_DRST = None


I2C_BUS = I2C.Bus(
    host=1,
    scl=_CTP_SCL,
    sda=_CTP_SDA,
    freq=400000,
    use_locks=False
)

TOUCH_DEVICE = I2C.Device(
    I2C_BUS,
    dev_id=gt911.I2C_ADDR,
    reg_bits=gt911.BITS
)

_DATA15 = const(10)  # B7
_DATA14 = const(17)  # B6
_DATA13 = const(18)  # B5
_DATA12 = const(38)  # B4
_DATA11 = const(14)  # B3
_DATA10 = const(21)  # G7
_DATA9 = const(47)  # G6
_DATA8 = const(48)  # G5
_DATA7 = const(45)  # G4
_DATA6 = const(0)  # G3
_DATA5 = const(39)  # G2
_DATA4 = const(40)  # R7
_DATA3 = const(41)  # R6
_DATA2 = const(42)  # R5
_DATA1 = const(2)  # R4
_DATA0 = const(1)  # R3


bus = lcd_bus.RGBBus(
    hsync=_HSYNC,
    vsync=_VSYNC,
    de=_DE,
    pclk=_PCLK,
    disp=1,
    data0=_DATA0,
    data1=_DATA1,
    data2=_DATA2,
    data3=_DATA3,
    data4=_DATA4,
    data5=_DATA5,
    data6=_DATA6,
    data7=_DATA7,
    # data8=_DATA8,
    # data9=_DATA9,
    # data10=_DATA10,
    # data11=_DATA11,
    # data12=_DATA12,
    # data13=_DATA13,
    # data14=_DATA14,
    # data15=_DATA15,
    # data_pins=(
    #     _DATA0,
    #     _DATA1,
    #     _DATA2,
    #     _DATA3,
    #     _DATA4,
    #     _DATA5,
    #     _DATA6,
    #     _DATA7,
    #     _DATA8,
    #     _DATA9,
    #     _DATA10,
    #     _DATA11,
    #     _DATA12,
    #     _DATA13,
    #     _DATA14,
    #     _DATA15
    # ),
    freq=_LCD_FREQ,
    hsync_front_porch=_HSYNC_FRONT_PORCH,
    hsync_back_porch=_HSYNC_BACK_PORCH,
    hsync_pulse_width=_HSYNC_PULSE_WIDTH,
    hsync_idle_low=False,
    vsync_front_porch=_VSYNC_FRONT_PORCH,
    vsync_back_porch=_VSYNC_BACK_PORCH,
    vsync_pulse_width=_VSYNC_PULSE_WIDTH,
    vsync_idle_low=False,
    de_idle_high=False,
    pclk_idle_high=False,
    pclk_active_low=_PCLK_ACTIVE_NEG,
)


buf = bus.allocate_framebuffer(_BUFFER_SIZE, lcd_bus.MEMORY_SPIRAM)

display = rgb_display.RGBDisplay(
    data_bus=bus,
    display_width=_WIDTH,
    display_height=_HEIGHT,
    frame_buffer1=buf,
    frame_buffer2=None,
    color_space=lv.COLOR_FORMAT.RGB565,
    rgb565_byte_swap=True
)

display.set_power(True)
display.init()
display.set_backlight(100)
indev = gt911.GT911(TOUCH_DEVICE)

# display.set_rotation(lv.DISPLAY_ROTATION._90)  # NOQA

lv.init()
scrn = lv.obj()

btn = lv.button(scrn)
btn.center()

scrn.set_style_bg_color(lv.color_hex(0x000000), 0)
lv.screen_load(scrn)
lv.screen_active()

task_handler.TaskHandler()