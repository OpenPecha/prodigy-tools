import os

def get_span(file):
    span = list(map(float, file.split("_")[-1][:-4].split("-")))
    return span[0], span[1]

def get_new_name(file):
    start, end = get_span(file)
    prefix = "_".join(file.split("_")[0:-1])
    return f"{prefix}_{start:09.3f}-{end:09.3f}.wav"

if __name__ == "__main__":
    stt_folders = [filename for filename in os.listdir(".") if filename.startswith("STT_TT") and os.path.isdir(filename)]
    print(stt_folders)
    for stt_folder in stt_folders:
        if len([name for name in os.listdir(stt_folder)]) != 1:
            print(stt_folder)
            split_files = [ filename for filename in os.listdir(f"./{stt_folder}/") if filename.startswith(f"{stt_folder}") and os.path.isfile(f"{stt_folder}/{filename}") ]
            for filename in split_files:
                print(get_new_name(filename))
                os.system(f"mv {stt_folder}/{filename} {stt_folder}/{get_new_name(filename)}")