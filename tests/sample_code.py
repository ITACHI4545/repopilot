import os
import json

from pathlib import Path


class UserService:

    def login(self, username, password):
        return True

    def logout(self):
        return True


def calculate_score(value):
    return value * 2