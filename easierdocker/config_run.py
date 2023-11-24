#!/usr/bin/env python
import json
from argparse import ArgumentParser

from .config import Config
from .log_re import log
from .easier_docker import EasierDocker


def main():
    args = parser.parse_args()
    config_path = args.config
    config = Config.load_file(config_path)
    log(f"config =\n {json.dumps(config, sort_keys=False, indent=4, separators=(',', ': '))}")
    easier_docker = EasierDocker(config)
    easier_docker.start()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--config', '-c', help='configuration file path')
    main()
