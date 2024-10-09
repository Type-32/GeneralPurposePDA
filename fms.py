import vfs
import os
import machine

_SD_MOSI = const(11)
_SD_SCK = const(12)
_SD_MISO = const(13)

spi_bus = machine.spi.Bus(
    mosi=_SD_MOSI,
    sck=_SD_SCK,
    miso=_SD_MISO
)

sd_card = machine.SDCard(
    spi_bus=spi_bus,
    freq=20000000  # you might need to adjust this
)

def init():
    pass
#     vfs.mount(sd_card, '/sd')
#
#     #you can access the SD Card by using the os module. or you can use open('/sd/some.file', 'r') etc...
#     print(os.listdir('/sd'))
