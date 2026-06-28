import os
import xml.etree.ElementTree as ET

# Dataset path
DATASET_PATH = "archive/NEU-DET"

# Class names
classes = {
    "crazing": 0,
    "inclusion": 1,
    "patches": 2,
    "pitted_surface": 3,
    "rolled-in_scale": 4,
    "scratches": 5
}


def convert(split):
    xml_dir = os.path.join(DATASET_PATH, split, "annotations")
    label_dir = os.path.join(DATASET_PATH, split, "labels")

    os.makedirs(label_dir, exist_ok=True)

    for xml_file in os.listdir(xml_dir):

        if not xml_file.endswith(".xml"):
            continue

        tree = ET.parse(os.path.join(xml_dir, xml_file))
        root = tree.getroot()

        width = int(root.find("size/width").text)
        height = int(root.find("size/height").text)

        txt_name = xml_file.replace(".xml", ".txt")

        with open(os.path.join(label_dir, txt_name), "w") as f:

            for obj in root.findall("object"):

                cls = obj.find("name").text.strip()

                if cls not in classes:
                    continue

                cls_id = classes[cls]

                box = obj.find("bndbox")

                xmin = float(box.find("xmin").text)
                ymin = float(box.find("ymin").text)
                xmax = float(box.find("xmax").text)
                ymax = float(box.find("ymax").text)

                x_center = ((xmin + xmax) / 2) / width
                y_center = ((ymin + ymax) / 2) / height
                w = (xmax - xmin) / width
                h = (ymax - ymin) / height

                f.write(f"{cls_id} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}\n")


convert("train")
convert("validation")

print("✅ XML converted to YOLO labels successfully!")