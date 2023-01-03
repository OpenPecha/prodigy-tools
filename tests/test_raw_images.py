from pathlib import Path
from tools.image_processing import ImageProcessing
from PIL import Image
from raw_pillow_opener import register_raw_opener
import gzip
import io


raw_image_input_dir_path = Path(__file__).parent / "data" / "inputs" / "raw_image_files"
expected_raw_image_ouptput_dir_path = Path(__file__).parent / "data" / "expected_outputs" / "raw_image_files"

zipped_raw_image_input_dir_path = Path(__file__).parent / "data" / "inputs" / "zipped_raw_image_files"
expected_zipped_raw_image_ouptput_dir_path = Path(__file__).parent / "data" / "expected_outputs" / "zipped_raw_image_files"



def test_raw_image_files():
    processor = ImageProcessing()
    for raw_image_file_path in raw_image_input_dir_path.iterdir():
        
        processor.origfilename = raw_image_file_path.name
        processor.get_new_filename(True)
        
        with open(raw_image_file_path, 'rb') as f:
            filebits = io.BytesIO(f.read())
        
        processed_image = processor.processs_image(filebits)
        width, height = processed_image.size
        processed_image_file = io.BytesIO()
        processed_image.save(processed_image_file, 'jpeg')
        
        expected_image = Image.open(expected_raw_image_ouptput_dir_path / processor.new_filename, formats=['JPEG'])
        expected_width, expected_height = expected_image.size
        expected_image_file = io.BytesIO()
        expected_image.save(expected_image_file, 'jpeg')
        
        assert width == expected_width
        assert height == expected_height
        # assert the memory size
        assert 100 >= abs(expected_image_file.tell() - processed_image_file.tell())

def test_zipped_raw_image_files():
    processor = ImageProcessing()
    for zipped_raw_image_file_path in zipped_raw_image_input_dir_path.iterdir():
        
        processor.origfilename = zipped_raw_image_file_path.name
        
        with open(zipped_raw_image_file_path, 'rb') as f:
            filebits = io.BytesIO(f.read())
        
        processed_image = processor.processs_image(filebits)

        width = processed_image.width
        height = processed_image.height
        processed_image_file = io.BytesIO()
        processed_image.save(processed_image_file, 'jpeg')
        
        expected_image = Image.open(expected_zipped_raw_image_ouptput_dir_path / processor.new_filename)
        expected_width, expected_height = expected_image.size
        expected_image_file = io.BytesIO()
        expected_image.save(expected_image_file, 'jpeg')
        
        assert width == expected_width
        assert height == expected_height
        # assert the memory size
        assert 100 >= abs(expected_image_file.tell() - processed_image_file.tell())


    

if __name__ == "__main__":
    test_raw_image_files()
    test_zipped_raw_image_files()