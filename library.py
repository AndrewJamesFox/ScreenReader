import os
import requests
from config import LIBDIR

# create library directory
os.makedirs(LIBDIR, exist_ok=True)

def download_pdf(url, filename):
    """
    Downloads a pdf given its URL and saves it to the library as filename.
    :param url: URL from which to download PDF.
    :param filename: Name for the downloaded PDF.
    :return: The full file path to the saved PDF.
    """
    response = requests.get(url)            #HTTP get request
    response.raise_for_status()             #exception if fails
    path = os.path.join(LIBDIR, filename)   #create file path
    with open(path, "wb") as f:             #open file at target path
        f.write(response.content)           #write content to file
    return path