#!/usr/bin/env python3

import argparse
import os

import gi

gi.require_version('GExiv2', '0.10')
from gi.repository import GExiv2
from datetime import datetime, timedelta
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
    RESET = "reset"
    PRINT = "print"
    TIME = "time"
    RENAME = "rename"

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


def adjust_original_to_digitized(metadata, file):
    original = metadata[Tags.ORIGINAL.value]
    digitized = metadata[Tags.DIGITIZED.value]
    if original != digitized:
        print(file + ": " + original + " -> " + digitized)
        metadata[Tags.ORIGINAL.value] = digitized
        metadata.save_file()


def print_photo_information(metadata, file):
    # print(metadata)
    # print(type(metadata))
    # print(dir(metadata))
    print(file)
    # print(metadata.get_exif_tags())
    print('Digitized:     ', metadata[Tags.DIGITIZED.value])
    print('Original:      ', metadata[Tags.ORIGINAL.value])
    print('Camera:        ', metadata[Tags.CAMERA.value])


def adjust_original_for_camera(metadata, file, camera, seconds):
    if camera.value.lower() == metadata[Tags.CAMERA.value].lower():
        old_datetime = metadata[Tags.ORIGINAL.value]
        new_datetime = _adjust_datetime_str_by_seconds(old_datetime, seconds)
        metadata[Tags.ORIGINAL.value] = new_datetime
        print(file + ": " + old_datetime + " -> " + new_datetime)
        metadata.save_file()


def _adjust_datetime_str_by_seconds(old_date_time_str, seconds):
    old_datetime = datetime.strptime(old_date_time_str, DatetimeFormat.EXIF.value)
    new_datetime = old_datetime + timedelta(seconds=seconds)
    new_date_time_str = new_datetime.strftime(DatetimeFormat.EXIF.value)
    return new_date_time_str


def rename_file_to_original(metadata, file, unique_suffix):
    directory = os.path.dirname(file)
    extension = os.path.splitext(file)[1]
    original = datetime.strptime(metadata[Tags.ORIGINAL.value], DatetimeFormat.EXIF.value) \
        .strftime(DatetimeFormat.OUTPUT.value)
    new_name = directory + "/" + original + "_" + unique_suffix + extension
    print(file + " -> " + new_name)
    os.rename(file, new_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("func", help="function to call [" + ", ".join(Function.list()) + "]")
    parser.add_argument("-d", "--directory", help="directory with images")
    parser.add_argument("-t", "--time", type=int, help="seconds to offset", required=False)
    parser.add_argument("-c", "--camera", help="Camera to filter [" + ", ".join(Camera.list()) + "]", required=False)
    args = parser.parse_args()

    # parse args to types
    func = Function.parse(args.func)
    camera = Camera.parse(args.camera)
    directory = args.directory
    time = args.time

    # validate args for func
    if func == Function.TIME and (camera is None or time is None):
        print("Missing arguments for func=hours. Actual arguments are: camera=" + str(camera) + ", time=" + str(time))
        exit(1)

    files = [os.path.join(directory, element) for element in sorted(os.listdir(directory))
             if os.path.isfile(os.path.join(directory, element))]

    counter = 1
    for file in files:
        metadata = GExiv2.Metadata(file)

        if func == Function.PRINT:
            print_photo_information(metadata, file)
        elif func == Function.RESET:
            adjust_original_to_digitized(metadata, file)
        elif func == Function.TIME:
            adjust_original_for_camera(metadata, file, camera, time)
        elif func == Function.RENAME:
            rename_file_to_original(metadata, file, str(counter))
        else:
            print("invalid func: " + func)
            parser.print_help()
            exit(1)

        counter += 1
