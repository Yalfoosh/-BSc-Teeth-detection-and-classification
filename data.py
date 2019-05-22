import os
import xml.etree.ElementTree as ElementTree

from typing import Iterable, Tuple
from pathlib import Path

import assertion


class Mark:
    acceptable_markings =\
        {
            "11", "12", "13", "14", "15", "16", "17", "18",
            "21", "22", "23", "24", "25", "26", "27", "28",
            "31", "32", "33", "34", "35", "36", "37", "38",
            "41", "42", "43", "44", "45", "46", "47", "48",
            "IMPLANTAT"
        }

    def __init__(self, name: str, markings: Iterable[Tuple[Tuple[int, int, int, int], str]]):
        assertion.assert_valid_type(name, str)

        self.name = name
        self.markings = markings

    @staticmethod
    def from_xml(xml_file_path: str):
        assertion.assert_valid_xml(xml_file_path=xml_file_path)

        file_name = Path(xml_file_path).stem
        markings = list()

        xml_root = ElementTree.parse(xml_file_path).getroot()

        for xml_object in xml_root.findall("object"):
            bounding_box, label = ([0, 0, 1, 1], "")

            for bounding_box in xml_object.findall("bndbox"):
                for x_min in bounding_box.findall("xmin"):
                    bounding_box[0] = int(x_min.text)
                    break

                for y_min in bounding_box.findall("ymin"):
                    bounding_box[1] = int(y_min.text)
                    break

                for x_max in bounding_box.findall("xmax"):
                    bounding_box[2] = int(x_max.text)
                    break

                for y_max in bounding_box.findall("ymax"):
                    bounding_box[3] = int(y_max.text)
                    break

                bounding_box = tuple(bounding_box)

            for name in xml_object.findall("name"):
                label = name.text
                break

            markings.append((bounding_box, label))

        return Mark(name=file_name, markings=markings)

    def __str__(self):
        to_return = "{}:\n".format(self.name)

        for marking in self.markings:
            to_return += "\t({}, {}) -> ({}, {}) - {}\n".format(*marking[0], marking[1])

        return to_return.strip()

    def to_csv(self, name_appendage: str = "", image_folder: str = None, extension: str = ".jpg"):
        if image_folder is None:
            image_folder = os.path.abspath(os.path.curdir)

        # region Assertions
        assertion.assert_valid_type(name_appendage, str)

        assertion.assert_valid_type(image_folder, str)
        assertion.assert_path_exists(image_folder)

        assertion.assert_valid_type(extension, str)
        assert extension.startswith(".")
        # endregion

        string = ""
        path = os.path.abspath(os.path.join(image_folder, "{}{}{}".format(self.name, name_appendage, extension)))

        for marking in self.markings:
            if marking[0][0] >= marking[0][2] or marking[0][1] >= marking[0][3]:
                continue

            new_class = marking[1]

            if len(marking[1]) is not 2 and marking[1] != "IMPLANTAT":
                if new_class.endswith("I"):
                    new_class = "IMPLANTAT"
                else:
                    new_class = new_class[:2]

                if new_class not in Mark.acceptable_markings:
                    continue

            string += "{},{},{},{},{},{}\n".format(path, *marking[0], new_class)

        return string.strip()


some_path = os.path.join(os.curdir, "00401.xml")
some_mark = Mark.from_xml(some_path)
print(some_mark.to_csv())
