import io
from tools.image_processing import ImageProcessing
from pathlib import Path
from PIL import Image
    

binary_input_dir_path = Path(__file__).parent / "data" / "inputs" / "binary_files"
expected_binary_ouptput_dir_path = Path(__file__).parent / "data" / "expected_outputs" / "binary_files"

non_binary_input_dir_path = Path(__file__).parent / "data" / "inputs" / "non_binary_files"
expected_non_binary_ouptput_dir_path = Path(__file__).parent / "data" / "expected_outputs" / "non_binary_files"


def test_binary_files():
    processor = ImageProcessing()
    for binary_file_path in binary_input_dir_path.iterdir():
        
        processor.origfilename = binary_file_path.name
        processor.get_new_filename(True)
        
        image = Image.open(binary_file_path)
        resized_image = processor.resize_the_image(image)
        width, height = resized_image.size
        
        expected_image = Image.open(expected_binary_ouptput_dir_path / processor.new_filename)
        expected_width, expected_height = expected_image.size
        
        assert width == expected_width
        assert height == expected_height


def test_non_binary_files():
    processor = ImageProcessing()
    for non_binary_file_path in non_binary_input_dir_path.iterdir():
        
        processor.origfilename = non_binary_file_path.name
        processor.get_new_filename(False)
        
        image = Image.open(non_binary_file_path)
        new_image = processor.process_non_binary_file(image)

        width = new_image.width
        height = new_image.height
        new_image_file = io.BytesIO()
        new_image.save(new_image_file, 'jpeg')
        
        expected_image = Image.open(expected_non_binary_ouptput_dir_path / processor.new_filename)
        expected_width, expected_height = expected_image.size
        expected_image_file = io.BytesIO()
        expected_image.save(expected_image_file, 'jpeg')
        
        assert width == expected_width
        assert height == expected_height
        # assert the memory size
        assert 100 >= abs(expected_image_file.tell() - new_image_file.tell())


if __name__ == "__main__":
    image_name = 'I2KG2081840206.tif'
    test_non_binary_files()
    test_binary_files()