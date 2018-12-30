#!/usr/bin/env python3

import argparse

import gi

gi.require_version('GExiv2', '0.10')
from gi.repository import GExiv2
from datetime import datetime
from enum import Enum


class Tags(Enum):
    ORIGINAL = "Exif.Photo.DateTimeOriginal"
    DIGITIZED = "Exif.Photo.DateTimeDigitized"
    CAMERA = "Exif.Image.Model"


class DatetimeFormat(Enum):
    EXIF = "%Y:%m:%d %H:%M:%S"
    OUTPUT = "%Y-%m-%d_%H:%M:%S"


class Camera(Enum):
    HUAWEI = "HUAWEI VNS-L31"
    LG = "LG-D802"
    SAMSUNG = "NX mini"
    SONY = "DSC-HX10V"
    REDMI = "Redmi Note3"
    UNKNOWN = "Unknown"

    @staticmethod
    def list():
        return list(map(lambda f: f.name.lower(), Camera))

    @staticmethod
    def parse(str):
        if str is None:
            return None

        for cam in Camera:
            if cam.name.lower() == str.lower():
                return cam

        raise AssertionError("unknown camera " + str)


class Function(Enum):
    SET = "set"

    @staticmethod
    def list():
        return list(map(lambda f: f.value, Function))

    @staticmethod
    def parse(str):
        if str is None:
            return None

        for func in Function:
            if func.value.lower() == str.lower():
                return func

        raise AssertionError("unknown func " + str)


def set_common_tags(metadata, new_datetime, camera):
    metadata[Tags.DIGITIZED.value] = new_datetime
    metadata[Tags.ORIGINAL.value] = new_datetime
    metadata[Tags.CAMERA.value] = camera
    metadata.save_file()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("func", help="function to call [" + ", ".join(Function.list()) + "]")
    parser.add_argument("-f", "--file", help="image file")
    parser.add_argument("-d", "--datetime", help="new date time for original and digitized")
    parser.add_argument("-c", "--camera", help="new camera")
    args = parser.parse_args()

    # parse args to types
    func = Function.parse(args.func)
    file = args.file
    new_datetime = args.datetime
    # test given datetime
    datetime.strptime(new_datetime, DatetimeFormat.EXIF.value)
    camera = Camera.parse(args.camera)

    metadata = GExiv2.Metadata(file)

    if func == Function.SET:
        set_common_tags(metadata, new_datetime, camera)
    else:
        print("invalid func: " + func)
        parser.print_help()
        exit(1)
