import os


min = 0.5
max = 13
def get_duration(file):
    span = list(map(float, file.split("_")[-1][:-4].split("-")))
    return span[1] - span[0]

def get_span(file):
    span = list(map(float, file.split("_")[-1][:-4].split("-")))
    return span[0], span[1]

def get_filename(file, start, end):
    prefix = "_".join(file.split("_")[0:-1])
    return f"{prefix}_{start:.3f}-{end:.3f}.wav"
    
if __name__ == "__main__":
    stt_folders = [filename for filename in os.listdir(".") if filename.startswith("STT_MV") and os.path.isdir(filename)]
    print(stt_folders)
    for stt_folder in stt_folders:
        if len([name for name in os.listdir(stt_folder)]) == 1:
            print(stt_folder)
            os.system(f"python pyAudioAnalysis/pyAudioAnalysis/audioAnalysis.py silenceRemoval -i ./{stt_folder}/{stt_folder}.wav --smoothing 0.5 --weight 0.2")
            print(f"deleting full file ./{stt_folder}/{stt_folder}.wav")
            os.remove(f"./{stt_folder}/{stt_folder}.wav")
            split_files = [ filename for filename in os.listdir(f"./{stt_folder}/") if filename.startswith(f"{stt_folder}") and os.path.isfile(f"{stt_folder}/{filename}") ]
            for filename in split_files:
                duration = get_duration(filename)
                print(duration)
                if duration < min:
                    print(f"deleting {stt_folder}/{filename} duration {duration}")
                    os.remove(f"{stt_folder}/{filename}")
                if duration > max:
                    print(f"{filename} {duration} exceeds {max}")
                    start, end = get_span(filename)
                    print(f"{filename} {start} {end}")
                    cut = 2
                    chop_length = duration / cut
                    cut += 1
                    while chop_length > max:
                        chop_length = duration / cut
                        cut += 1
                    for j in range(int(duration / chop_length)):
                        print(f"{filename} {chop_length} chop")
                        print(f"creating {get_filename(filename, start + (chop_length * j), start + (chop_length * (j+1)))}")
                        os.system(f"ffmpeg -y -i {stt_folder}/{filename} -ss {chop_length * j} -to {chop_length * (j+1)} -ac 1 -ar 16000 {stt_folder}/{get_filename(filename, start + (chop_length * j), start + (chop_length * (j+1)))}" )
                    print(f"deleting {stt_folder}/{filename} chopped")
                    os.remove(f"{stt_folder}/{filename}")
                     