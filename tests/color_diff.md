# input jsonl file is in the test
    `Path="./test/data/color_diff.py`

# to run the color_diff.py recipe

`python3.9 -m prodigy color-diff-recipe test "./test/data/color_diff.jsonl" -F ./recipes/color_diff.py`

# Green 
    Green characters are the characters that are in the text1(first_annotation) and not in the text2(reviewed_annotation)

# Red 
    Red chareacters are the characters that are in the text2(reviewed_annotation) but not in the text1(first_annotation)

# Text feild
    the text in the text Feild with the Transcript is the reviewed_annotation or text2