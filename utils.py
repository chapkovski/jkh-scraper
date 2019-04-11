import requests
import re


def get_filename_from_cd(cd):
    """
    Get filename from content-disposition
    """

    if not cd:
        return None
    fstub = re.findall('filename=(.+)', cd)

    if len(fstub) == 0:
        return None
    filename = re.search('"(?P<name>.*)"', fstub[0])
    return filename.groupdict()['name']

