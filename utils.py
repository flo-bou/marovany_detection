# import glob
import os
import json

location = ""

def get_wav_files_locations(dir: str) -> dict:
    """Scan the 'dir' parameter location of the local fs to get the .wav files; then returns the names of those files.
    
    Params:
        dir: str
            Path to a local directory to search for .wav files.
    
    Returns: dict
        Names of .wav files found.
    """
    # retirer le dernier slash
    # wav_list: list = glob.glob(dir + '*.wav')
    dict_out: dict = {"files": []}
    if os.path.isdir(dir):
        files: list = os.listdir(dir)
        wav_files: list = list(filter(lambda fname: fname.endswith(".wav") , files))
        dict_out = {"files": wav_files}
    # data = dict(list(wav_list))
    # créer la liste sans chemin complet et zipper ?
    # for fname in wav_list:
    #     data.files.add
    return dict_out


def save_notes(data: dict) -> str:
    """Write json file according to the 'data' parameter.
    If a file was already present, overwrite it.
    
    Params:
        data: dict
            Data to store as-is in a json file.
    
    Returns: str
        'ok' if data was stored
        'ko' if an error occured
    """
    fpath = data['name'].replace(".wav", ".json", -1)
    try:
        f = open(fpath, "w")
        f.write(json.dumps(data))
        f.close()
        result = "ok"
    except Exception as e:
        print("An error occured during the writing of "+fpath+" file.")
        print(e)
        result = "ko"
    return result


def get_notes(fpath: str) -> str:
    """Reads json file associated with the file 'fpath' and returns it.
    
    Params:
        fpath: str
            full path of the audio file we want to return the data about
    
    Returns: str
        The stored data about the targeted file as a json file.
    """
    fpath: str = fpath.replace(".wav", ".json", -1)
    content: str = "{}"
    if os.path.isfile(fpath):
        try:
            f = open(fpath, "r")
            content = f.read()
            print("content : ", type(content), content)
            f.close()
        except Exception as e:
            print("An error occured during the reading of "+fpath+" file.")
            print(e)
    return content
