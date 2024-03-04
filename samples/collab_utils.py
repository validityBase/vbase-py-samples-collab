"""
Google Collab utilities
"""

from google.colab import userdata
import os
from typing import List


def add_user_secrets_to_env(userdata_keys: List[str]):
    """
    Add google.collab.userdata secrets to the environment.
    This allows vBase configuration to be stored in Collab user secrets.

    :param userdata_keys: The keys for environment variables to import from userdata.
    """
    # Loop through the secrets and set them as environment variables
    for k in userdata_keys:
        v = userdata.get(k)
        os.environ[k] = v
        print(f"Imported {k}")
