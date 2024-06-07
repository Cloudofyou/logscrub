#!/usr/bin/env python3

import os
import hashlib
from datetime import datetime

def get_directory_snapshot(directory):
    hash_obj = hashlib.sha256()
    
    for root, dirs, files in os.walk(directory):
        for name in sorted(dirs + files):
            if name.endswith('.hash'):
                continue  # Ignore files ending in .hash
            
            filepath = os.path.join(root, name)
            
            # Get file metadata
            if os.path.isfile(filepath):
                file_size = os.path.getsize(filepath)
                file_mtime = os.path.getmtime(filepath)
                
                # Update hash with file path, size, and modification time
                hash_obj.update(filepath.encode())
                hash_obj.update(str(file_size).encode())
# Remove date/time as a hash computation value as it would change on a new system
#                hash_obj.update(str(file_mtime).encode())
    
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

if __name__ == "__main__":
    directory_path = "."  # Replace with your directory path
    
    # Generate the snapshot hash
    snapshot_hash = get_directory_snapshot(directory_path)
    
    # Print the resulting hash value
    print(f"Directory snapshot hash: {snapshot_hash}")
    
    # Check if a .hash file with the same hash already exists
    if not hash_file_exists(directory_path, snapshot_hash):
        # Create a .hash file with the current datetime in the name
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        hash_filename = os.path.join(directory_path, f"{timestamp}_snapshot.hash")
        
        with open(hash_filename, 'w') as f:
            f.write(snapshot_hash)
        print(f"Created new snapshot file: {hash_filename}")
    else:
        print("A snapshot file with the same hash already exists. No new file created.")

