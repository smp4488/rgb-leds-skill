from mycroft import MycroftSkill, intent_handler
from .color_dictionary import color_names
import time
from rpi_ws281x import *

# LED strip configuration:
LED_COUNT      = 16      # Number of LED pixels.
#LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

class RgbLeds(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.strip = None
        # # Create NeoPixel object with appropriate configuration.
        # self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        # # Intialize the library (must be called once before other functions).
        # self.strip.begin()

    def initialize(self):
        self.log.info('Initializing rgb-leds-skill')
        #my_setting = self.settings.get('my_setting')
        # self.register_entity_file('leds.rgb.intent')
        self.register_entity_file('color.entity')
        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()

    # @intent_file_handler('leds.rgb.intent')
    @intent_handler('leds.rgb.intent')
    def handle_leds_rgb(self, message):
        self.log.info('turning lights on')
        self.colorSolid(Color(255, 0, 0))
        self.speak_dialog('leds.rgb')

    @intent_handler('leds.colors.intent')
    def handle_leds_color(self, message):
        color = message.data.get('color').lower()
        self.log.info('trying to set LED color to ' + color)
        if color is not None:
            hex = color_names[color]
            self.log.info('hex value: ' + hex)
            rgb = self.hexToRGB(hex)
            self.log.info('rgb value: ' + rgb)
            self.colorSolid(Color(rgb))
            self.speak_dialog('leds.colors', {'color': color})
        else:
            print('color not found')
            # self.speak_dialog('like.tomato.generic')

    def colorSolid(self, color):
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            #strip.show()
            #time.sleep(wait_ms/1000.0)

        self.strip.show

    # https://stackoverflow.com/a/29643643
    def hexToRGB(self, hex):
        h = hex.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def create_skill():
    return RgbLeds()

# def Color(red, green, blue, white = 0):
# 	"""Convert the provided red, green, blue color to a 24-bit color value.
# 	Each color component should be a value 0-255 where 0 is the lowest intensity
# 	and 255 is the highest intensity.
# 	"""
# 	return (white << 24) | (red << 16)| (green << 8) | blue

