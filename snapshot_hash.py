#!/usr/bin/env python3

import os
import hashlib

def get_directory_snapshot(directory):
    hash_obj = hashlib.sha256()
    
    for root, dirs, files in os.walk(directory):
        for name in sorted(dirs + files):
            filepath = os.path.join(root, name)
            
            # Get file metadata
            if os.path.isfile(filepath):
                file_size = os.path.getsize(filepath)
                file_mtime = os.path.getmtime(filepath)
                
                # Update hash with file path, size, and modification time
                hash_obj.update(filepath.encode())
                hash_obj.update(str(file_size).encode())
                hash_obj.update(str(file_mtime).encode())
    
    return hash_obj.hexdigest()

if __name__ == "__main__":
    directory_path = "."  # Replace with your directory path
    snapshot_hash = get_directory_snapshot(directory_path)
    print(f"Directory snapshot hash: {snapshot_hash}")

