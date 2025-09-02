import os

path=os.path.dirname(os.path.abspath(__file__))

import sys

sys.path.append(path)
__all__ = []
try:
    import get_data.get_data as hardware_data
    __all__.append("hardware_data")
except :
    print("Please install get_data.py")

try:
    import read_eeg_file.get_data as upload_data
    __all__.append("upload_data")
except :
    print("Please install read_eeg_file.py")
