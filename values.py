import os


class Image:
    image_extensions =\
        {
            ".bmp",
            ".gif",
            ".ico",
            ".jpg", ".jpeg",
            ".png",
            ".tif", ".tiff",
        }


class Folder:
    base = "F:\Backup\FER\PROJEKT\RetinaNet Tooth Detection"
    data = os.path.join(base, "data")

    training_data = os.path.join(data, "training")
    validation_data = os.path.join(data, "validation")
    test_data = os.path.join(data, "test")
    mock_data = os.path.join(data, "mock")

    training_csv = os.path.join(training_data, "csv")
    training_img = os.path.join(training_data, "img")
    training_img_enhanced = os.path.join(training_data, "img_enhanced")
    training_xml = os.path.join(training_data, "xml")

    mock_csv = os.path.join(mock_data, "csv")
    mock_img = os.path.join(mock_data, "img")
    mock_img_enhanced = os.path.join(mock_data, "img_enhanced")
    mock_xml = os.path.join(mock_data, "xml")
