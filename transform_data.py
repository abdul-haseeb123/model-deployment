import os
import shutil

BRANDS = ["adidas", "converse", "nike"]
train_dir = os.path.join(os.getcwd(), "data", "train")
test_dir = os.path.join(os.getcwd(), "data", "test")


def setup_directories():
    train_imgs_dir = os.path.join(train_dir, "images")
    test_imgs_dir = os.path.join(test_dir, "images")
    os.makedirs(train_imgs_dir, exist_ok=True)
    os.makedirs(test_imgs_dir, exist_ok=True)


def transform_train_data():
    idx = 0
    annotations = []
    for brand in BRANDS:
        brand_dir = os.path.join(train_dir, brand)
        for img in os.listdir(brand_dir):
            src_path = os.path.join(brand_dir, img)
            dst_path = os.path.join(train_dir, "images", f"{idx}.jpg")
            shutil.copy(src_path, dst_path)
            annotations.append(f"{idx},{brand}\n")
            idx += 1
    with open(os.path.join(train_dir, "annotations.csv"), "w") as f:
        f.writelines(annotations)


def transform_test_data():
    idx = 0
    annotations = []
    for brand in BRANDS:
        brand_dir = os.path.join(test_dir, brand)
        for img in os.listdir(brand_dir):
            src_path = os.path.join(brand_dir, img)
            dst_path = os.path.join(test_dir, "images", f"{idx}.jpg")
            shutil.copy(src_path, dst_path)
            annotations.append(f"{idx},{brand}\n")
            idx += 1
    with open(os.path.join(test_dir, "annotations.csv"), "w") as f:
        f.writelines(annotations)


if __name__ == "__main__":
    setup_directories()
    transform_train_data()
    transform_test_data()
