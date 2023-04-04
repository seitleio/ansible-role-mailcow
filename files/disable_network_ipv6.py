#! /usr/bin/python3

import os
import argparse
import yaml
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')

parser = argparse.ArgumentParser()
parser.add_argument('--compose-file', dest='composefile', type=str, help='Path to the docker-compose.yml', required=True)
args = parser.parse_args()

def main():
    if not os.path.exists(args.composefile):
        logging.error('Path {0} does not exist.'.format(path))
        raise Exception('Path {0} does not exist.'.format(path))

    with open(args.composefile, 'r') as file:
        logging.info('Reading compose file {0}'.format(args.composefile))
        compose_file = yaml.load(file, yaml.Loader)

    ipv6nat_definition = {
        "image": "bash:latest",
        "restart": "no",
        "entrypoint": ["echo", "ipv6nat disabled in compose.override.yml"]
    }

    compose_file['services']['ipv6nat-mailcow'] = ipv6nat_definition
    logging.info('ipv6nat-mailcow definition has been overwritten')

    with open(args.composefile, 'w') as file:
        logging.info('Writing compose file {0}'.format(args.composefile))
        file.write(yaml.dump(compose_file))

if __name__ == '__main__':    
    main()