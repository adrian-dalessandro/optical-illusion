import pygame

class IconSheet:
    def __init__(self, filename, sheet_dict):
        self.spritesheet = pygame.image.load(filename).convert()
        self.sheet_dict = sheet_dict

    def get_images(self, hscale):
        frames = []
        for details in list(self.sheet_dict.values())[0:4]:
            x, y, width, height = details.values()
            image = pygame.Surface((width, height))
            image.blit(self.spritesheet, (0, 0), (x, y, width, height))
            scale = hscale/height
            image = pygame.transform.scale(image, (int(scale*width), int(scale*height)))
            frames.append(image)
        return frames


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

class HierarchySpritesheet(Spritesheet):
    def __init__(self, filename, sheet_dict):
        super(HierarchySpritesheet, self).__init__(filename, sheet_dict)

    def get_images(self, name, hscale):
        images = []
        for image in self.sheet_dict[name]:
            x, y, width, height = image.values()
            image = pygame.Surface((width, height))
            image.blit(self.spritesheet, (0, 0), (x, y, width, height))
            scale = hscale/height
            image = pygame.transform.scale(image, (int(scale*width), int(scale*height)))
            images.append(image)
        return images
