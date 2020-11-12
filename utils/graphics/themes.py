import json
from collections import namedtuple

class Theme(object):
    def __init__(self, directory):
        Sheet = namedtuple("Sheet", ["dict", "spritesheet"])
        tiles_dict = json.load(open("{}/tiles.theme.json".format(directory.rstrip("/"))))
        actor_dict = json.load(open("{}/actors.theme.json".format(directory.rstrip("/"))))
        self.tilesheet = Sheet(dict = tiles_dict,
                               spritesheet = "{}/{}".format(directory.rstrip("/"), tiles_dict["spritesheet"]))
        self.actorsheet = Sheet(dict = actor_dict,
                                spritesheet = "{}/{}".format(directory.rstrip("/"), actor_dict["spritesheet"]))
        self.blockmap = json.load(open("{}/block.map.json".format(directory.rstrip("/"))))
