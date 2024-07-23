# input jsonl file
    `Path="./test/data/color_diff.py`

# to run the color_diff.py recipe

`python3.9 -m prodigy color-diff-recipe test "./test/data/color_diff.jsonl" -F ./recipes/color_diff.py`

# Colors
### Green 
    Green characters are the characters that are in the text1(first_annotation) and not in the text2(reviewed_annotation)
    
### Red 
    Red chareacters are the characters that are in the text2(reviewed_annotation) but not in the text1(first_annotation)

#### Example:

    for the below example
        text1(first_annotation) = "དུང་ར་བློ་བཟང་འཕྲིན་ལས"
        text2(reviewed_annotation) = "དུང་དཀར་བློ་འཕྲིན་ལས"
        
![Screenshot 2023-07-07 at 12 53 14 PM](https://github.com/OpenPecha/prodigy-tools/assets/43548581/a31accce-94f8-4fdc-83a0-d5e3fe86764b)

# Text feild
    the text in the text Feild with the Transcript is the reviewed_annotation or text2
    text2(reviewed_annotation) = "དུང་དཀར་བློ་འཕྲིན་ལས"

### Example:

![Screenshot 2023-07-07 at 12 56 46 PM](https://github.com/OpenPecha/prodigy-tools/assets/43548581/410fd905-dc85-4e7f-a79a-4147e936561e)
