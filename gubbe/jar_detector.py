#################################################################
#                                                               #
# Gubbe                                                         #
# Copyright (C) 2020, Vilhelm Prytz, <vilhelm@prytznet.se>      #
#                                                               #
# Licensed under the terms of the MIT license, see LICENSE.     #
# https://github.com/VilhelmPrytz/gubbe                         #
#                                                               #
#################################################################

from os import getcwd, listdir
from os.path import isfile, join
from zipfile import ZipFile
from json import loads


class JARDetector:
    def __init__(self):
        self.files = []
        self.base_path = getcwd()
        self._filelist = [
            f
            for f in listdir(self.base_path)
            if isfile(join(self.base_path, f)) and f.endswith(".jar")
        ]
        self._analyze()

    def _analyze(self):
        for f in self._filelist:
            version = None
            with ZipFile(f) as z:
                try:
                    with z.open("version.json") as zf:
                        version = loads(zf.read())["id"]
                except Exception:
                    pass

                try:
                    with z.open("patch.properties") as zf:
                        for l in zf.read().split():
                            if l.decode("utf-8").startswith("version="):
                                version = l.decode("utf-8").split("version=")[1]
                except Exception:
                    pass

                try:
                    with z.open("patch.json") as zf:
                        version = loads(zf.read())["version"]
                except Exception:
                    pass

            self.files.append({"filename": f, "version": version})
