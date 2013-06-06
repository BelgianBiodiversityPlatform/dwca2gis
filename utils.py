import sys

from dwca.darwincore.utils import qualname as qn

def valid_dwca(dwca):
    return (dwca.core_rowtype == qn('Occurrence') and
            dwca.core_contains_term(qn('decimalLatitude')) and
            dwca.core_contains_term(qn('decimalLongitude')))

def dwcaline_to_epsg4326(line):
    """ Returns a {'lat': X, 'lon': Y} dict for the given DwCALine. """

    lat = line.data[qn('decimalLatitude')]
    lon = line.data[qn('decimalLongitude')]

    return {'lat': lat, 'lon': lon}


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes": True,   "y": True,  "ye": True,
             "no": False,   "n": False}
    
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")
