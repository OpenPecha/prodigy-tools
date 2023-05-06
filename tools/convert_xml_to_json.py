import os
import json
from glob import glob
from xml.dom import minidom
from natsort import natsorted


def get_region_coords(region: minidom.Element) -> list:
    coords = region.getElementsByTagName("Coords")
    points = coords[0].attributes["points"].value
    points = points.split(" ")

    box_points = []

    for p in points:
        x, y = p.split(",")
        a = [float(x), float(y)]
        box_points.append(a)

    return box_points


def generate_prodigy_records(xml_files: list) -> list:
    records = []

    for idx in range(len(xml_files)):
        annotation_tree = minidom.parse(page_xml_files[idx])
        text_regions = annotation_tree.getElementsByTagName("TextRegion")
        image_regions = annotation_tree.getElementsByTagName("ImageRegion")
        page_tag = annotation_tree.getElementsByTagName("Page")

        image_name = page_tag[0].attributes["imageFilename"].value
        image_width = page_tag[0].attributes["imageWidth"].value
        image_height = page_tag[0].attributes["imageHeight"].value

        spans = []

        if len(text_regions) != 0:
            for t_region in text_regions:
                region_attr = t_region.attributes["custom"].value

                bbox_points = get_region_coords(t_region)

                if "marginalia" in region_attr:
                    span = {
                        "label": "Margin",
                        "color": "deepskyblue",
                        "points": bbox_points,
                    }
                    spans.append(span)
                elif "caption" in region_attr:
                    span = {
                        "label": "Caption",
                        "color": "springgreen",
                        "points": bbox_points,
                    }
                    spans.append(span)

                else:
                    span = {
                        "label": "Text-Area",
                        "color": "magenta",
                        "points": bbox_points,
                    }
                    spans.append(span)

        if len(image_regions) != 0:
            for i_region in image_regions:
                bbox_points = get_region_coords(i_region)
                span = {"label": "Illustration", "color": "yellow", "points": bbox_points}
                spans.append(span)

        prodigy_record = {
            "image": image_name,
            "width": image_width,
            "height": image_height,
            "spans": spans,
        }

        records.append(prodigy_record)

    return records


def save_records(out_path: str, ds_name: str, prodigy_records: list) -> None:
    json_file = f"{out_path}/{ds_name}.jsonl"
    with open(json_file, "w", encoding="utf8") as f:
        for record in prodigy_records:
            json_string = json.dumps(
                record, ensure_ascii=False, separators=(", ", ": ")
            )
            f.write(f"{json_string}\n")


if __name__ == "__main__":
    data_root = "./data/lineSeg_phudrak/page"
    data_set = "Gampopa100"
    page_xml_path = os.path.join(data_root, data_set, "page")
    page_xml_files = natsorted(glob(f"{page_xml_path}/*.xml"))
    prodigy_json_out = os.path.join(data_root, data_set, "prodigy")

    if not os.path.exists(prodigy_json_out):
        os.makedirs(prodigy_json_out)

    records = generate_prodigy_records(xml_files=page_xml_files)
    save_records(prodigy_json_out, data_set, records)
