#!/usr/bin/env python3

import os
import hashlib
from datetime import datetime

def get_directory_snapshot(directory):
    hash_obj = hashlib.sha256()
    
    for root, dirs, files in os.walk(directory):
        for name in sorted(dirs + files):
            if name.endswith('.hash') or name.endswith('.git'):
                continue  # Ignore files ending in .hash or .git
            
            filepath = os.path.join(root, name)
            
            # Get file metadata
            if os.path.isfile(filepath):
                file_size = os.path.getsize(filepath)
                file_mtime = os.path.getmtime(filepath)
                
                # Update hash with file path, size, and modification time
                hash_obj.update(filepath.encode())
                hash_obj.update(str(file_size).encode())
    
    return hash_obj.hexdigest()

def hash_file_exists(directory, snapshot_hash):
    for root, dirs, files in os.walk(directory):
        for name in files:
            if name.endswith('.hash'):
                filepath = os.path.join(root, name)
                with open(filepath, 'r') as f:
                    existing_hash = f.read().strip()
                    if existing_hash == snapshot_hash:
                        return True
    return False

def hash_file_exists2(directory, snapshot_hash):
    return os.path.exists('.snapshot.local.hash')

def same_hash(snapshot_hash):
    hash_filename = '.snapshot.local.hash'
    retvalue = False
    if os.path.isfile(hash_filename):
        with open(hash_filename, 'r') as infile:
            lines = infile.readlines()
            for line in lines:
                if line == snapshot_hash:
                    print("Same hash!")
                    retvalue = True
                else:
                    retvalue = False
                    print(f"line = {line}  hash = {snapshot_hash}") 

    return retvalue

def write_to_file(filename, hash):
    with open(filename, 'w') as f:
        f.write(hash)        

if __name__ == "__main__":
    # Update later with argparse. For now, use current directory
    directory_path = "."  # Replace with your directory path
    
    # Generate the snapshot hash
    snapshot_hash = get_directory_snapshot(directory_path)
    same_hash_value_exists = same_hash(snapshot_hash)
    print(f"same_hash_value_exists  =  {same_hash_value_exists}")
 
    # Print the resulting hash value
    print(f"Directory snapshot hash: {snapshot_hash}")

    hash_filename = ".snapshot.local.hash"
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    hash_filename_time = ".snapshot.local." + timestamp + ".hash"
    print(f"hash_filename       = {hash_filename}")
    print(f"hash_filename_time  = {hash_filename_time}")

    if hash_file_exists2(directory_path, snapshot_hash):
        print("hash_file_exists = True")
        if same_hash_value_exists:
            print("same_hash_value_exists = True")
        else:
            os.rename(hash_filename, hash_filename_time)
            write_to_file(hash_filename, snapshot_hash) 
    else:
        print("hash_file_exists = False")
        write_to_file(hash_filename, snapshot_hash)
    
