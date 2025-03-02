''' Lab 6 Install VLC automated
Tue Feb 18
'''
### STUDENTS: PLEASE ADD THE STANDARD ACADEMIC INTEGRITY STATEMENT.###
# This program is strictly my own work. Any material beyond course learning
# materials that is taken from the Web or other sources is properly cited,
# giving credit to the original author(s).

import requests
import hashlib
import pathlib
import os
import subprocess

# Define VLC version and URLs
VLC_VERSION = "3.0.21"
BASE_URL = f"https://download.videolan.org/pub/videolan/vlc/{VLC_VERSION}/win64"
FILE_NAME_SHA256 = "vlc-3.0.21-win64.exe.sha256"
FILE_NAME = "vlc-3.0.21-win64.exe"

# Function to get the expected SHA-256 hash value from VLC website
def get_expected_sha256():
    response = requests.get(f"{BASE_URL}/{FILE_NAME_SHA256}")
    if not response.ok:
        print("Failed to get the expected SHA-256 hash. Exiting...")
        exit()
    return response.text.split()[0]  # Extract SHA256 hash from response

# Function to download the VLC installer (without saving)
def download_installer():
    response = requests.get(f"{BASE_URL}/{FILE_NAME}", stream=True)
    if not response.ok:
        print("Failed to download VLC installer. Exiting...")
        exit()
    
    file_data = bytearray()
    for chunk in response.iter_content(chunk_size=8192):
        file_data.extend(chunk)
    
    return file_data

# Function to verify SHA-256 hash integrity
def installer_ok(installer_data, expected_sha256):
    sha256 = hashlib.sha256(installer_data).hexdigest()
    return sha256 == expected_sha256

# Function to save the installer to disk
def save_installer(installer_data):
    file_path = pathlib.Path(os.getenv('TEMP')) / FILE_NAME
    with open(file_path, "wb") as outfile:
        outfile.write(installer_data)
    return file_path

# Function to silently run the VLC installer
def run_installer(installer_path):
    subprocess.run([str(installer_path), "/L=1033", "/S"], check=True)
    print("Installation completed successfully.")

# Function to delete the installer after installation
def delete_installer(installer_path):
    installer_path.unlink()
    print("Installer deleted.")

# Main function to automate VLC installation
def main():
    # Get the expected SHA-256 hash value of the VLC installer
    expected_sha256 = get_expected_sha256()

    # Download (but don't save) the VLC installer from the VLC website
    installer_data = download_installer()

    # Verify the integrity of the downloaded VLC installer by comparing the
    # expected and computed SHA-256 hash values
    if installer_ok(installer_data, expected_sha256):
        # Save the downloaded VLC installer to disk
        installer_path = save_installer(installer_data)
        
        # Silently run the VLC installer
        run_installer(installer_path)
        
        # Delete the installer after installation
        delete_installer(installer_path)
    else:
        print("SHA-256 hash mismatch! Exiting...")

# Run main() when the script is executed
if __name__ == "__main__":
    main()


