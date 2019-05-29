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
    labeled_img.context.export_csv(image_path=str(labeled_img.picture.path.absolute()), destination_path=mock_csv_path)

    new_labeled_image = LabeledImage(labeled_img.picture, labeled_img.context)

    new_labeled_image.picture = labeled_img.picture.blur(3, values.Folder.mock_img_enhanced)
    new_labeled_image.export(mock_csv_path)

    for percentage in range(-50, 51, 25):
        if percentage is 0:
            continue

        new_labeled_image.picture = labeled_img.picture.brighten(percentage, values.Folder.mock_img_enhanced)
        new_labeled_image.export(mock_csv_path)
