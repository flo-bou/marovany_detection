import glob
import os

location = ""

def get_wav_files_locations(dir):
    # retirer le dernier slash
    # wav_list: list = glob.glob(dir + '*.wav')
    dict_out = {"files": []}
    if os.path.isdir(dir):
        files = os.listdir(dir)
        wav_files = list(filter(lambda fname: fname.endswith(".wav") , files))
        dict_out = {"files": wav_files}
    # print(wav_list)
    # data = dict(list(wav_list))
    # créer la liste sans chemin complet et zipper ?
    # for fname in wav_list:
    #     data.files.add
    return dict_out
    
