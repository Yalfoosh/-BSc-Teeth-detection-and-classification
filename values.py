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
    data = os.path.join(os.curdir, "data")

    training_data = os.path.join(data, "training")
    validation_data = os.path.join(data, "validation")
    test_data = os.path.join(data, "test")
    mock_data = os.path.join(data, "mock")

    mock_csv = os.path.join(mock_data, "csv")
    mock_img = os.path.join(mock_data, "img")
    mock_img_enhanced = os.path.join(mock_data, "img_enhanced")
    mock_xml = os.path.join(mock_data, "xml")
