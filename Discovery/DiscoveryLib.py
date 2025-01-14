# DiscoveryLib.py: essentials for Discovery tool

import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


def validate_rate_input(rate_input):
    try:
        rate = float(rate_input.strip())
        return rate if rate > 0 else None
    except ValueError:
        return None

def parse_headers(headers_str):
    headers = {}
    if headers_str.strip():
        pairs = headers_str.split(';')
        for pair in pairs:
            if ':' in pair:
                key, value = map(str.strip, pair.split(':', 1))
                headers[key] = value
    return headers


def check_if_url_is_valid(url, headers=None):
    try:
        response = requests.get(url, headers=headers, timeout=5)
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

def run_folder_fuzzer(base_url: str, wordlist_path: str, headers=None, rate_limit=None, num_threads=4):
    if not base_url.endswith('/'):
        base_url += '/'

    valid_directories = {}
    wordlist = pathToList(wordlist_path)

    def process_directory(directory):
        url = f"{base_url}/{directory}"
        res = check_if_url_is_valid(url, headers=headers)
        if res[0] and res[1] is not None:
            return directory, {"status_code": res[1], "path": f"{base_url}{directory}"}
        return None

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        future_to_directory = {executor.submit(process_directory, directory): directory for directory in wordlist}

        for future in as_completed(future_to_directory):
            result = future.result()
            if result:
                directory, info = result
                valid_directories[directory] = info
            if rate_limit:
                time.sleep(1 / rate_limit)

    return valid_directories




def add_ext_to_wordlist(wordlist: list, extensions: list):
    return [f"{entry}.{ext}" for entry in wordlist for ext in extensions]


def run_files_fuzzer(base_url: str, wordlist_path: str, extensions: list, headers=None, rate_limit=None, num_threads=4):
    if not base_url.endswith('/'):
        base_url += '/'

    valid_files = {}
    wordlist = pathToList(wordlist_path)
    filelist = add_ext_to_wordlist(wordlist, extensions)

    def process_file(possible_file):
        url = f"{base_url}/{possible_file}"
        res = check_if_url_is_valid(url, headers=headers)
        if res[0] and res[1] is not None:
            return possible_file, {"status_code": res[1], "path": f"{base_url}{possible_file}"}
        return None

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        future_to_file = {executor.submit(process_file, possible_file): possible_file for possible_file in filelist}

        for future in as_completed(future_to_file):
            result = future.result()
            if result:
                possible_file, info = result
                valid_files[possible_file] = info
            if rate_limit:
                time.sleep(1 / rate_limit)

    return valid_files

