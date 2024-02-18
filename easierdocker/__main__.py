import json
import os
from argparse import ArgumentParser, FileType

from easierdocker.config import Config
from easierdocker.log_re import log
from easierdocker.easier_docker import EasierDocker


def main():
    parser = ArgumentParser()
    parser.add_argument('--config', '-c', help='configuration file path: yaml, yml and json', required=True)
    args = parser.parse_args()
    config_path = os.path.abspath(args.config) if args.config else None
    config = Config(config_path).load_file()
    log(f"config =\n {json.dumps(config, sort_keys=False, indent=4, separators=(',', ': '))}")
    container_config = config['container']
    network_config = config.get('network', None)
    easier_docker = EasierDocker(container_config, network_config)
    easier_docker.start()


if __name__ == "__main__":
    main()
