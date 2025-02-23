''' Lab 6 Install VLC automated
Tue Feb 18
'''

import requests
import hashlib
import pathlib
import os
import subprocess

# The URL is in the VLC download archive.

BASE_URL = "https://download.videolan.org/pub/videolan/vlc/3.0.21/win64/"
FILE_NAME_SHA256 = "vlc-3.0.21-win64.exe.sha256"
FILE_NAME = "vlc-3.0.21-win64.exe"

# Part 1 - Get the expected SHA-256 fingerprint for the instalation file
# Make the request with the full URL to the file
response = requests.get(f'{BASE_URL}/{FILE_NAME_SHA256}')
if not response.ok:
    print("Did not get the SHA256 file. Exiting...")
    exit()
resp_text = response.text
file_sha256 = resp_text.split()[0] # Break up at the blank, keep the SHA256
print(file_sha256)

# Part 2 - Get the installation file, keep in memory until checked.
# Make the request with the full URL to the installation file
response = requests.get(f'{BASE_URL}/{FILE_NAME}')
if not response.ok:
    print("Did no get the installation file. Exiting...")
    exit()
file_binary = response.content # Binary content (not text or string)
print(len(file_binary)) # Should be approx. 45Mbytes

# Part 3 - Compute the SHA-256 of the binary response with haslib
# Create a new SHA256 object
sha256 = hashlib.sha256(file_binary)
print(sha256.hexdigest())

# Part 4 - Compare expected and SHA-256 hash values
if not sha256.hexdigest() == file_sha256:
    print("Download SHA-256 does not match expected value. Exiting...")
    exit()

# Part 5 - Save the installation file so that it can run
print("SHA-256 values match, saving the file...")
file_name = pathlib.Path(os.getenv('TEMP')) / FILE_NAME
print(f"File name: {file_name}")
with open(file_name, "wb") as outfile: # Write a binary file
    outfile.write(file_binary)
# File written and now closed


# Part 6 - Run the installation file and if success delete when done.
subprocess.run([file_name, '/L=1033', '/S'])
# Check that subprosess ran correctly but you need to run the script
# as administrator from shell

# Delete the installation file using pathlib.Path.unlink()


