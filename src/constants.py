#!/usr/bin/env python3

import sys

from enum import Enum

VERSION = '1.0.0'

if sys.platform == 'linux':
    WINE = 'wine'
    FILE_PATH_SEPARATOR = '/'
    pass
else:
    WINE = ''  # Windows doesn't need wine
    FILE_PATH_SEPARATOR = '\\'
    pass


class FileType:

    def __init__(self, header: bytes, extension: str):
        self.header = header
        self.extension = extension
        return


class FileTypes(FileType, Enum):
    DDS_PHYRE = FileType(b'RYHP', 'dds.phyre'),
    DXT5 = FileType(b'DXT5', 'dds'),
    ARGB8 = FileType(b'ARGB8', 'tga')

    def __init__(self, file_type: FileType):
        super().__init__(file_type.header, file_type.extension)
        self.file_type = file_type
        return
