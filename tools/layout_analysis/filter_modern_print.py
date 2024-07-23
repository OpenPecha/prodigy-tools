from pathlib import Path
import csv



def check_image_in_csv(csv_path, image_s3):
    work = image_s3.split("/")[2]
    imagegroup = (image_s3.split("/")[4]).split("-")[1]
    with open(csv_path) as _file:
        for csv_line in list(csv.reader(_file, delimiter=",")):
            work_id = csv_line[0]
            image_group = csv_line[1]
            if work == work_id:
                if imagegroup == image_group:
                    return True
    return False

def get_modern_images(file_path, csv_path):
    image_list = ""
    images_s3 = (file_path.read_text(encoding='utf-8')).splitlines()
    for image_s3 in images_s3[1500:]:
        modern = check_image_in_csv(csv_path, image_s3)
        if modern:
            image_list += image_s3+"\n"
    return image_list

if __name__ == "__main__":
    new_layout = ""
    # csv_path = Path(f"./modernprints.csv")
    # file_path = Path("./Q3_layout_analysis.txt")
    # image_list = get_modern_images(file_path, csv_path)
    # Path("./mordern_images.txt").write_text(image_list, encoding='utf-8')

