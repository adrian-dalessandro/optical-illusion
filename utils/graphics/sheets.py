import xml.etree.ElementTree as ET
import pygame

def consume_xml_sheet(filename):
    root = ET.parse(filename).getroot()
    sheet_dict = {}
    for child in root.getchildren():
        elem = {}
        for key in ["x", "y", "width", "height"]:
            elem[key] = int(child.get(key))
        sheet_dict[child.get("name")] = elem
    return sheet_dict

class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename, sheet_dict):
        self.spritesheet = pygame.image.load(filename).convert()
        self.sheet_dict = sheet_dict

    def get_image(self, name, hscale):
        # grab an image out of a larger spritesheet
        x, y, width, height = self.sheet_dict[name].values()
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        scale = hscale/height
        image = pygame.transform.scale(image, (int(scale*width), int(scale*height)))
        return image
