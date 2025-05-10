import sys
import time
import logging
from PIL import Image
from graph_generator import graph_generator
from utils.file_utils import file_utils
from utils.web_server import WebServer

# Set to the name of your e-ink device
# (https://github.com/robweber/omni-epd#displays-implemented)
DISPLAY_TYPE = "waveshare_epd.epd7in5_V2"

# Disable when running the waveshare panel
DEBUG = False

# Width & Height of the screen in inches
WIDTH = 4.8
HEIGHT = 8

# Time between new art
SLEEP = 1800

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

if not DEBUG:
    from omni_epd import displayfactory, EPDNotFoundError


if not DEBUG:
    try:
        epd = displayfactory.load_display_driver(DISPLAY_TYPE)
    except EPDNotFoundError:
        print(f"Couldn't find {DISPLAY_TYPE}")
        sys.exit()

    WIDTH = epd.width / 100
    HEIGHT = epd.height / 100

    # Setting up the eInk Display
    epd.prepare()
    epd.clear()
    epd.sleep()

file_utils = file_utils()

# Start the web server
web_server = WebServer("gen-images")
web_server.start()

loop_counter = 0

while True:
    try:
        log.info("Generating artwork from samila...")
        graph = graph_generator(width=WIDTH, height=HEIGHT)
        img_buf = graph.generate_from_samila()
        log.info("Completed")
    except BaseException:
        log.error("Caught exception while generating art from samila")

    image = Image.open(img_buf)

    if DEBUG:
        log.info("DEBUGMODE: Opening the artwork")
        image.show()
    else:
        log.info("Preparing to render on the screen...")
        epd.prepare()
        epd.clear()
        epd.display(image)
        epd.sleep()
        log.info("Rendered!")

    file_utils.save_art(image)

    img_buf.close()
    del graph

    if loop_counter == 10:
        # perform some maintence for every 10th run
        # mostly just deleting off old artwork from the save directory
        log.info("Maintaince Loop!")
        loop_counter = 0
        file_utils.clean_dir()

    loop_counter += 1
    log.info("Sleeping for " + str(SLEEP) + " seconds")
    time.sleep(SLEEP)
