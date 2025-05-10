import configparser
import time
import os
import logging
from PIL import Image

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class file_utils():

    def __init__(self) -> None:
        self.config = configparser.ConfigParser()
        self.config.read('config/config.cfg')

    def save_art(self, img: Image) -> None:
        """
        Inputs a PIL images and saves it to the config directory w the name as the current imestamp
        """
        dir = self.config['file']['dir']
        img_path = dir + str(int(time.time())) + '.png'
        img.save(img_path)
        log.info("Saved artwork to: " + img_path)

    def clean_dir(self, ) -> None:
        """
        Ensures number of artwork in the directory stays below max allowed
        """

        dir = self.config['file']['dir']
        art_limit = int(self.config['file']['max-images'])
        artwork_list = sorted(os.listdir(dir), reverse=True)

        if artwork_list is None or art_limit > len(artwork_list):
            return

        to_be_deleted_list = artwork_list[art_limit:len(artwork_list)]

        if not to_be_deleted_list:
            return

        log.warn("Deleting the following artworks: " + str(to_be_deleted_list))
        for artwork in to_be_deleted_list:
            artwork_path = dir + str(artwork)
            os.remove(artwork_path)
