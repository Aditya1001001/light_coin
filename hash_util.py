import hashlib 
import json

def hash_string(string):
    """Create a SHA256 hash for a given input string.

    Arguments:
        :string: The string which should be hashed.
    """
    return hashlib.sha256(string).hexdigest()


def hash_block(block):
    """Hashes a block and returns a string representation of it.

    Arguments:
        :block: The block that should be hashed.
    """
    dict_for_hash = block.__dict__.copy()
    return hash_string(json.dumps(dict_for_hash, sort_keys=True).encode())