from tools.image_processing import ImageProcessing
from pathlib import Path
from PIL import Image

input_dir_path = Path(__file__).parent / "inputs" / "binary_files"
expected_ouptput_dir_path = Path(__file__).parent / "expected_outputs" / "binary_files"


def test_binary_files():
    processor = ImageProcessing()
    for binary_file_path in input_dir_path.iterdir():
        
        processor.origfilename = binary_file_path.name
        processor.get_new_filename()
        
        image = Image.open(binary_file_path)
        resized_image = processor.resize_the_image(image)
        width, height = resized_image.size
        
        expected_image = Image.open(expected_ouptput_dir_path / processor.new_filename)
        expected_width, expected_height = expected_image.size
        
        assert width == expected_width
        assert height == expected_height


if __name__ == "__main__":
    test_binary_files()