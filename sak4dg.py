import urllib.request
import urllib.parse
import http.cookiejar
import re
import sys

# global administrivia 
__version__ = "sak4dg v0.01"
__copyright__ = """\
Copyright (C) 2011  Maurice "Mucki" Kemmann <mucki@kemmann.de>
This is free software; see the source for copying conditions. There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE."""

### Init ###
BASE_URL = "http://dailygammon.com"
# Please fill in your data
USERID = "your_userid"
MATCH_DIR = "/your/path/to/saved/matches/" #Target path for your matches, incl. "/" at the end
USERNAME = "your_username"
PASSWORD = "your_password" #clear text, not encoded

def check_python_version(): 
    """Abort if we are running on python < v3.1"""
    too_old_error = "This program requires python v3.1 or greater. " + \
      "Your version of python is:\n%s""" % sys.version
    try: 
        version = sys.version_info  # we might not even have this function! :)
        if (version[0] < 3) or (version[0] == 3 and version[1] < 1):
            print(too_old_error)
            sys.exit(1)
    except AttributeError:
        print(too_old_error)
        sys.exit(1)

def site_login(url, username, password):
    """Login and cookie handling"""
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    login_data = urllib.parse.urlencode({'login' : username, 'password' : password})
    login_data = login_data.encode("utf-8")
    opener.open(BASE_URL+"/bg/login", login_data)
    return opener

def get_urls():
    """gets all urls of your matches on Dailygammon"""
    opener = site_login(BASE_URL, USERNAME, PASSWORD)
    url = BASE_URL + "/bg/user/" + USERID + "?finished=1"
    resp = opener.open(url)
    result = resp.read()
    txt = result.decode("iso-8859-1")
    liste = (re.findall("/bg/export/[\d]{4,8}",txt))
    return liste

def save_match(url, match):
    """Saves a match"""
    p = re.compile("[\d]{4,8}")
    filename = p.search(url)
    filename = filename.group() + ".mat"
    f = open(MATCH_DIR + filename, "w")
    f.write(match) 
    f.close()
    print("\nMatch " + filename + " geschrieben.")

def FileExist(file):
    """ Checks if a file exists or not. """
    try:
        oFile = open(file,"r")
    except IOError: #EA-Fehler
        return 0
    else:
        oFile.close()
        return 1

def get_matches(list_of_urls):
    """Get only matches not already saved"""
    p = re.compile("[\d]{4,8}")
    opener = site_login(BASE_URL, USERNAME, PASSWORD)    
    j = len(list_of_urls)
    for i in range(1,j):
        filename = p.search(list_of_urls[i])
        filename = filename.group() + ".mat"   
        path = MATCH_DIR + filename
        if FileExist(path) == 0:
            match_url = BASE_URL + list_of_urls[i]
            resp = opener.open(match_url)
            match = resp.read()
            match = match.decode("iso-8859-1")
            save_match(list_of_urls[i], match)
        else:
            print(".")

check_python_version()
urls = get_urls()
get_matches(urls)
