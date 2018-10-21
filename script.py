#!/usr/bin/env python3

import os
import gi
gi.require_version('GExiv2', '0.10')
from gi.repository import GExiv2


def osWalk():
    for dirname, dirnames, filenames in os.walk("resources"):
        print(dirname)
        print(dirnames)
        print(filenames)
        print("--------")


if __name__ == "__main__":
    for dirname, _, filenames in os.walk("resources"):
        files = [dirname + "/" + name for name in sorted(filenames)]

        for file in files:
            print(file)
            metadata = GExiv2.Metadata(file)

            #print(metadata)
            #print(type(metadata))
            #print(dir(metadata))
            #print(metadata.get_exif_tags())
            print('Photo.DateTimeDigitized: ', metadata['Exif.Photo.DateTimeDigitized'])
            print('Photo.DateTimeOriginal: ', metadata['Exif.Photo.DateTimeOriginal'])
            print('Exif.Image.DateTime: ', metadata['Exif.Image.DateTime'])
            #print(metadata.get_exif_tags())
            print('get_date_time: ', metadata.get_date_time())
            #metadata.save_file()
            print("--------------")
