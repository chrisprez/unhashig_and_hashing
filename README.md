# Hash Decoding Exercise

This script serves as an exercise to attempt to decode an MD5 hash using a dictionary that we have (in this case, the rockyou dictionary commonly found in Linux security distributions such as Kali, Parrot, etc.).

Subsequently, for those passwords that we have successfully "decoded," we will recreate a hash (this time based on SHA256) with a salt. All of this is done using a Python script and the security tool "Hashcat," ensuring that we are in a Linux environment and that the tool is installed. In case it is not installed, the script will request permission to install it.

In the end, two additional files will be generated:

- `plain.txt`: This file will display the "decoded" passwords with the corresponding hash. It will also list the passwords that could not be decoded.

- `PASSWORDS.txt`: This file will display the original hash, reflecting the fact that it could not be processed.

Additionally, the original file used for study purposes, `pass_md5.txt`, is attached. This file is used as an example, as if we wanted to update our user password database with a more secure system.

As a reminder, there is no decoding process for the hash; the goal is to check for collisions with other hashes created from dictionaries. Hence, increasingly complex algorithms are used for hashing to prevent such collisions. The addition of a salt makes this virtually impossible.
