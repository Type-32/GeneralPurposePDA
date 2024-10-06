import lvgl as lv
import time
import ili9341
import gt911
from machine import SPI
import lcd_bus

# Initialize the LCD
spi_bus = SPI.Bus(host=1, mosi=14, miso=41, sck=13)
display_bus = lcd_bus.SPIBus(spi_bus=spi_bus, dc=4, cs=6, freq=40000000)
disp = ili9341.ILI9341(data_bus=display_bus, reset_pin=5, reset_state=ili9341.STATE_LOW, backlight_pin=40, color_space=lv.COLOR_FORMAT.RGB565, color_byte_order=ili9341.BYTE_ORDER_BGR, rgb565_byte_swap=True, display_width=800, display_height=480)

# Initialize the touch sensor
touch = gt911.GT911(cs=15, spihost=2)

# Initialize LVGL
lv.init()

# Create a screen
scr = lv.obj()

# Create a button
btn = lv.btn(scr)
btn.align(lv.ALIGN.CENTER, 0, 0)

# Create a label on the button
label = lv.label(btn)
label.set_text("Hello World!")

# Load the screen
lv.scr_load(scr)

# Main loop
while True:
    time.sleep_ms(5)
    lv.task_handler()