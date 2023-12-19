#!/usr/bin/env python3

import hashlib
import secrets
import os
import platform
import subprocess

# Function to execute Hashcat and find matches
def run_hashcat(hash_file, wordlist_file):
    hashcat_command = f"hashcat -a 0 -m 0 {hash_file} {wordlist_file} -o plain.txt --potfile-disable"
    # The last parameter is needed because HAshcaut create an a pot file that can not create a file the we need.

    os.system(hashcat_command)

# Function to compare original hashes with those found by Hashcat
def compare_hashes(hash_file, wordlist_file):
    # Open plain.txt for writing
    with open("plain.txt", "w") as output_file:
        # Call run_hashcat to get matches
        run_hashcat(hash_file, wordlist_file)

        # Open plain.txt for reading
        with open("plain.txt", "r") as result_file:
            found_hashes = result_file.readlines()

        # Open hash_file for reading
        with open(hash_file, "r", encoding="latin-1") as original_file:
            original_hashes = original_file.readlines()

        # Compare hashes and write results to plain.txt
        for original_hash in original_hashes:
            original_hash = original_hash.strip()
            found_hash = next((h.strip() for h in found_hashes if h.strip() and h.strip().startswith(original_hash)), None)

            if found_hash:
                output_file.write(f"{original_hash} {found_hash[len(original_hash):].strip()}\n")
            else:
                output_file.write(f"{original_hash}\n")

# Function to create passwords with SHA-256 hashes and salt
def create_passwords(input_file="plain.txt", output_file="passwords.txt"):
    # Open plain.txt for reading
    with open(input_file, "r") as input_file:
        lines = input_file.readlines()

    # Open output_file for writing
    with open(output_file, "w") as output_file:
        # Process each line in plain.txt
        for line in lines:
            values = line.strip().split(':')
            if len(values) >= 2:
                # Take the second original value
                associated_word = values[1]

                # Generate a random salt
                salt = secrets.token_hex(8)

                # Calculate SHA-256 hash with salt
                hash_sha256 = hashlib.sha256((associated_word + salt).encode()).hexdigest()

                # Write the result to passwords.txt
                output_file.write(f"{values[1]}: {hash_sha256}\n")
            else:
                # Write the line as is to passwords.txt if there is no second value
                output_file.write(f'{line}')

# Function to check if Hashcat is installed on Debian systems
def check_hashcat_installed():
    try:
        result = subprocess.run(["hashcat", "--version"], capture_output=True, check=True, text=True)
        print("Hashcat is installed. Version:", result.stdout.strip())
        return True
    except FileNotFoundError:
        return False
    except subprocess.CalledProcessError:
        return False

# Function to install Hashcat on Debian systems
def install_hashcat():
    response = input("Hashcat is not installed. Do you want to install it? (y/n): ")
    if response.lower() == 'y':
        try:
            subprocess.run(["sudo", "apt", "install", "hashcat"], check=True)
            print("Hashcat has been installed successfully.")
            return True
        except subprocess.CalledProcessError:
            print("There was an error installing Hashcat.")
            return False
    else:
        print("Hashcat has not been installed. You can install it manually in the future.")
        return False

# Script entry point
if __name__ == "__main__":
    operating_system = platform.system()

    if operating_system == "Windows":
        print("This script is only functional on Debian-based Linux systems.")
    elif operating_system == "Linux":
        if check_hashcat_installed():
            hash_file = 'pass_md5.txt'
            wordlist_file = 'rockyou.txt'
            compare_hashes(hash_file, wordlist_file)
            create_passwords()
            print("Process completed.")
        else:
            install_hashcat()
            print("Please run the script again after installing Hashcat.")
    else:
        print(f"This script has not been tested on the operating system: {operating_system}.")
