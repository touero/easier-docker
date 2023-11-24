#!/usr/bin/env python
from .config import Config


def main(parser):
    config = Config.load_file()
