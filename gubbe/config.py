#################################################################
#                                                               #
# Gubbe                                                         #
# Copyright (C) 2020, Vilhelm Prytz, <vilhelm@prytznet.se>      #
#                                                               #
# Licensed under the terms of the MIT license, see LICENSE.     #
# https://github.com/VilhelmPrytz/gubbe                         #
#                                                               #
#################################################################

from os import getcwd
from os.path import isfile
from json import dump

TEMPLATE = {
    "meta": {"version": 0},
    "server": {"filename": "{}", "minecraft_version": "{}"},
    "plugins": [],
}


class Config:
    def __init__(self):
        self._path = f"{getcwd()}/gubbe.json"

    def config_exists(self):
        return True if isfile(self._path) else False

    def create(self, filename, minecraft_version):
        _new_config = TEMPLATE
        _new_config["server"]["filename"] = _new_config["server"]["filename"].format(
            filename
        )
        _new_config["server"]["minecraft_version"] = _new_config["server"][
            "minecraft_version"
        ].format(minecraft_version)

        if self.config_exists():
            raise Exception("configuration already exists")

        with open(self._path, "w") as f:
            dump(_new_config, f)
