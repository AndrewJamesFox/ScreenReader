import os
import json
from config import LIBPATH, LIBDIR

def load_library():
    """
    Returns loaded library JSON.
    """
    # if directory path exists, create directory
    if LIBDIR:
        os.makedirs(LIBDIR, exist_ok=True)

    ## IF library.json DOES NOT EXIST
    if not os.path.exists(LIBPATH):
        data = {"screenplays": []}  #create the JSON list
        save_library(data)          #save library to disk
        return data                 #return empty library

    ## FOR WHEN library.json DOES EXIST
    # try to open it
    try:
        with open(LIBPATH, "r") as f:
            data = json.load(f)
            # validate structure of json, must be dict with "screenplays" key
            if not isinstance(data, dict) or "screenplays" not in data:
                raise ValueError
            return data             #return valid library

    # if corrupted or invalid structure
    except (json.JSONDecodeError, ValueError):
        data = {"screenplays": []}  #reset to empty json
        #ensure directory path exists before saving reset
        if LIBDIR:
            os.makedirs(LIBDIR, exist_ok=True)
        save_library(data)          #save library to disk
        return data                 #return empty library


def save_library(data):
    """
    Saves library data to disk.
    """
    if LIBDIR:                              #ensure directory exists
        os.makedirs(LIBDIR, exist_ok=True)

    with open(LIBPATH, "w") as f:           #open library file
        json.dump(data, f, indent=2)        #save dict into json
