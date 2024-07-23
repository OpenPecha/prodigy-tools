from tools.count_annotations_by_annotator import count_annotator_id

db_path = "./tests/data/inputs/bdrc_crop_images.sqlite"
expected_output = {
    'bdrc_crop-tsewangphunstok': 200, 
    'bdrc_crop-dolmatsering': 80, 
    'bdrc_crop-dechen': 110, 
    'bdrc_crop-losgendun': 124
    }


def test_count_annotations():
    count_dict = count_annotator_id(db_path)
    assert count_dict == expected_output