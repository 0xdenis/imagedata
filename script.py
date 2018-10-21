#!/usr/bin/env python3

import os

import gi

gi.require_version('GExiv2', '0.10')
from gi.repository import GExiv2
from datetime import datetime, timedelta
from enum import Enum


class DatetimeFormat(Enum):
    EXIF = "%Y:%m:%d %H:%M:%S"
    OUTPUT = "%Y-%m-%d_%H:%M:%S"


class Camera(Enum):
    HUAWEI = "HUAWEI VNS-L31"
    LG = "LG-D802"
    SAMSUNG = "NX mini"
    SONY = "DSC-HX10V"
    REDMI = "Redmi Note3"


def adjust_original_to_digitized(metadata):
    original = metadata['Exif.Photo.DateTimeOriginal']
    digitized = metadata['Exif.Photo.DateTimeDigitized']
    if original != digitized:
        print("adjusting original date from " + original + " to " + digitized + " in file " + file)
        metadata['Exif.Photo.DateTimeOriginal'] = digitized
        metadata.save_file()


def print_photo_information(metadata):
    # print(metadata)
    # print(type(metadata))
    # print(dir(metadata))
    print(file)
    # print(metadata.get_exif_tags())
    print('Digitized:     ', metadata['Exif.Photo.DateTimeDigitized'])
    print('Original:      ', metadata['Exif.Photo.DateTimeOriginal'])
    print('get_date_time: ', metadata.get_date_time())
    print('Camera:        ', metadata['Exif.Image.Model'])


def adjust_original_for_camera(metadata, camera, hours):
    if camera == metadata['Exif.Image.Model']:
        metadata['Exif.Photo.DateTimeOriginal'] = \
            _adjust_datetime_str_by_hours(metadata['Exif.Photo.DateTimeOriginal'], hours)
        metadata.save_file()


def _adjust_datetime_str_by_hours(old_date_time_str, hours):
    old_datetime = datetime.strptime(old_date_time_str, DatetimeFormat.EXIF.value)
    new_datetime = old_datetime + timedelta(hours=hours)
    new_date_time_str = new_datetime.strftime(DatetimeFormat.EXIF.value)
    return new_date_time_str


def rename_file_to_original(metadata, file, unique_suffix):
    directory = os.path.dirname(file)
    extension = os.path.splitext(file)[1]
    original = datetime.strptime(metadata['Exif.Photo.DateTimeOriginal'], DatetimeFormat.EXIF.value) \
        .strftime(DatetimeFormat.OUTPUT.value)
    new_name = directory + "/" + original + "_" + unique_suffix + extension
    print(file + " -> " + new_name)
    # os.rename(file, new_name)


if __name__ == "__main__":
    directory = "resources"
    files = [os.path.join(directory, element) for element in sorted(os.listdir(directory))
             if os.path.isfile(os.path.join(directory, element))]
    print(files)

    counter = 1
    for file in files:
        metadata = GExiv2.Metadata(file)

        rename_file_to_original(metadata, file, str(counter))
        print_photo_information(metadata)

        print("--------------")
        counter += 1
