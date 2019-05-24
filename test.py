import os

import values

from data import LabeledImage

xmls = list()

for file_name in os.listdir(values.Folder.mock_xml):
    xmls.append(os.path.join(values.Folder.mock_xml, file_name))

labeled_imgs = list()

for xml in xmls:
    labeled_imgs.append(LabeledImage.from_xml(xml, values.Folder.mock_img))

mock_csv_path = os.path.join(values.Folder.mock_csv, "data.csv")

for labeled_img in labeled_imgs:
    labeled_img.context.export_csv(mock_csv_path, image_folder=values.Folder.mock_img)

    labeled_img.picture = labeled_img.picture.blur(3, values.Folder.mock_img_enhanced)
    labeled_img.export(mock_csv_path)

    for percentage in range(-50, 51, 25):
        labeled_img.picture = labeled_img.picture.brighten(percentage, values.Folder.mock_img_enhanced)

        labeled_img.export(mock_csv_path)
