import io
from tools.image_processing import ImageProcessing
from pathlib import Path
from PIL import Image
# import mozjpeg_lossless_optimization
# from PIL.JpegImagePlugin import JpegImageFile

# def compress_and_encode_image(resized_image):
    
#     compressed_image = io.BytesIO()
#     resized_image.save(compressed_image, format='JPEG', quality=75, progressive=True)
#     compressed_image_data = Image.open(compressed_image)
#     new_image = Image.new(mode="RGB", size=resized_image.size)
#     new_image.putdata(list(compressed_image_data.getdata()))
#     new_image.save("new_image.jpg")
    # compressed_image.seek(0)
    # compressed_image_bytes = compressed_image.read()
    # # encoding the compressed image, without metadata
    # output_jpeg_bytes = mozjpeg_lossless_optimization.optimize(compressed_image_bytes)
    # new_image = Image.new(mode=Image.open(compressed_image).mode, size=resized_image.size)
    # new_image.putdata(output_jpeg_bytes)
    # return new_image
    # return compressed_image
    

input_dir_path = Path(__file__).parent / "data" / "inputs" / "non_binary_files"
expected_ouptput_dir_path = Path(__file__).parent / "data" / "expected_outputs" / "non_binary_files"

def test_binary_files():
    processor = ImageProcessing()
    for binary_file_path in input_dir_path.iterdir():
        
        processor.origfilename = binary_file_path.name
        processor.get_new_filename(False)
        
        image = Image.open(binary_file_path)
        new_image = processor.process_non_binary_file(image)
        
        width = new_image.width
        height = new_image.height
        new_image_file = io.BytesIO()
        new_image.save(new_image_file, 'jpeg')
        
        expected_image = Image.open(expected_ouptput_dir_path / processor.new_filename)
        expected_width, expected_height = expected_image.size
        expected_image_file = io.BytesIO()
        expected_image.save(expected_image_file, 'jpeg')
        
        assert width == expected_width
        assert height == expected_height
        assert 11 >= abs(expected_image_file.tell() - new_image_file.tell())


if __name__ == "__main__":
    test_binary_files()