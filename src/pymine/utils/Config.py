# coding=utf-8

"""
 * Config Class for simple config manipulation of multiple formats.
 """
import yaml
from phpserialize import

from spl.stubs.Core import *


class Config:
    DETECT = -1  # Detect by file extension

    PROPERTIES = 0  # .properties

    CNF = PROPERTIES  # .cnf

    JSON = 1  # .js,.json

    YAML = 2  # .yml,.yaml

    # EXPORT = 3  # .export,.xport

    SERIALIZED = 4  # .sl

    ENUM = 5  # .txt,.list,.enum

    ENUMERATION = ENUM

    """ @var array """
    config = []

    nestedCache = []

    """ @var string """
    file = ""

    """ @var bool """
    correct = False

    """ @var int """
    type = DETECT

    formats = {
        "properties": PROPERTIES,
        "cnf": CNF,
        "conf": CNF,
        "config": CNF,
        "json": JSON,
        "js": JSON,
        "yml": YAML,
        "yaml": YAML,
        # "export" : EXPORT,
        # "xport" : EXPORT,
        "sl": SERIALIZED,
        "serialize": SERIALIZED,
        "txt": ENUM,
        "list": ENUM,
        "enum": ENUM,
    }

    def __init__(self, file, type=DETECT, default=[], correct=None):
        """
        :param file: string   Path of the file to be loaded
        :param type: int  Config type to load, -1 by default(detect)
        :param default: list  Array with the default values that will be written to the file if it did not exist
        :param correct: None  Sets correct to true if everything has been loaded correctly
        """
        self.load(file, type, default)
        self.correct = correct

    def load(self, file, type=DETECT, default=[]):
        self.correct = True
        self.type = int(type)
        self.file = file

        if not is_array(default):
            default = []

        if not file_exists(file):
            self.config = default
            self.save()
        else:
            if self.type == Config.DETECT:
                extension = os.path.basename(self.file).split(".")
                extension = extension.pop().strip().lower()
                if isset(Config.formats[extension]):
                    self.type = Config.formats[extension]
                else:
                    self.correct = False

            if self.correct:
                content = file_get_contents(self.file)
                if self.type == (Config.PROPERTIES or Config.CNF):
                    self.parseProperties(content)
                elif self.type == Config.JSON:
                    self.config = json_decode(content, True)
                elif self.type == Config.YAML:
                    content = self.fixYAMLIndexes(content)
                    try:
                        self.config = yaml.load(content)
                    except yaml.YAMLError as exc:
                        print(exc)
                elif self.type == Config.SERIALIZED: unserialize()
                elif self.type == Config.ENUM:
                else: