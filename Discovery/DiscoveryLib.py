import requests

def validate_rate_input(rate_input):
    try:
        rate = float(rate_input.strip())
        return rate if rate > 0 else None
    except ValueError:
        return None


def check_if_url_is_valid(url):
    try:
        response = requests.get(url, timeout=5)
        status_code = int(response.status_code)
        if status_code in [200, 204, 206, 301, 302, 303, 307, 308, 401, 403, 405]:
            return True, status_code
        return False, None
    except requests.RequestException:
        return False, None

def pathToList(path):
    wordlist = []
    with open(path, 'r') as f:
        for line in f:
            wordlist.append(line.strip())
    return wordlist

def run_folder_fuzzer(base_url: str, wordlist_path: str):
    if not base_url.endswith('/'):
        base_url += '/'

    valid_directories = {}
    wordlist = pathToList(wordlist_path)
    for directory in wordlist:
        url = f"{base_url}/{directory}"
        res = check_if_url_is_valid(url)
        if res[0] and res[1] is not None:
            valid_directories[directory] = {"status_code": res[1], "path": f"{base_url}{directory}"}
    return valid_directories

def add_ext_to_wordlist(wordlist: list, extensions: list):
    return [f"{entry}.{ext}" for entry in wordlist for ext in extensions]

def run_files_fuzzer(base_url: str, wordlist_path: str, extensions: list):
    if not base_url.endswith('/'):
        base_url += '/'

    valid_files = {}
    wordlist = pathToList(wordlist_path)
    for possibleFile in add_ext_to_wordlist(wordlist, extensions):
        url = f"{base_url}/{possibleFile}"
        res = check_if_url_is_valid(url)
        if res[0] and res[1] is not None:
            valid_files[possibleFile] = {"status_code": res[1], "path": f"{base_url}{possibleFile}"}
    return valid_files