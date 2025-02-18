import requests
import hashlib
import os
import pathlib
import subprocess

BASE_URL = "http://download.videolan.org/pub/videolan/vlc/3.0.21/win64/"
FIILE_NAME = "vlc-3.0.21-win64.exe.sha256"
FILE_NAME_SHA256 = "vlc-3.0.21-win64.exe"


# Part 1
# Make the request with the URL to the file
response = requests.get(f'{BASE_URL}/{FILE_NAME_SHA256}')
if not response.ok:
    print("Did not get the SHA256 file. Exiting...")
    exit()
response_text = response.text
file_sha256 = response_text.split()[0]
print(file_sha256)

# Part 2 - Get the instalaation file, keep in memory until checked.
# Make the request with the URL to the installation file
response = requests.get(f'{BASE_URL}/{FIILE_NAME}')
if not response.ok:
    print("Did not get the installation file. Exiting...")
    exit()
file_binary = response.content
print(len(file_binary))

# Part 3 - Compute the SHA-256 of the binary reponse with haslib
# create a new SHA256 object
sha256 = hashlib.sha256(file_binary)
print(sha256.hexdigest())

# Part 4 - Compare expected and computed SHA-256 hash values
if not sha256.hexdigest() == file_sha256:
    print("Donwloaded SHA-256 does not match the expected value. Exiting...")
    exit()

# Part 5 - Save the installation file to disk
print ("SHA-256 values match, saving the file")
file_name = pathlib.Path(os.getenv('TEMP')) / "vlc-3.0.21-win64.exe"
print(f'File name: {file_name}')
with open(file_name, 'wb') as outfile:
    outfile.write(file_binary)

# Part 6 - Run the installation file
subprocess.run([file_name, '/L=1033', '/S'])
# Check that subprocess run correctly

# delete the installation file using pathlib.Path.unlink()
