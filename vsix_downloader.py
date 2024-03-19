# %%

import re
import subprocess
from pathlib import Path

import requests

download_directory = Path("vsix_downloaded")
download_directory.mkdir(parents=True, exist_ok=True)

FILENAME_REGEX = "(?<=filename=).*?vsix"
MARKETPLACE_URL = "https://marketplace.visualstudio.com/vscode"
URL_COMMON = "https://marketplace.visualstudio.com/_apis/public/gallery/"


list_extensions_command = ["code", "--list-extensions", "--show-versions"]
extension_list = subprocess.getoutput(list_extensions_command).split("\n")

urls = []

for line in extension_list:
    extension_data, version = line.split("@")
    publisher, extension_name = extension_data.split(".")
    uri = f"publishers/{publisher}/vsextensions/{extension_name}/{version}/vspackage"
    url = f"{URL_COMMON}{uri}"
    urls.append(url)

with requests.Session() as s:
    s.get(MARKETPLACE_URL)
    for url in urls:
        response = s.get(url)
        content = response.headers["content-disposition"]
        filename = re.findall(FILENAME_REGEX, content)[0].replace('"', "")
        download_directory.joinpath(filename).write_bytes(response.content)
        print(f"{filename} downloaded")
