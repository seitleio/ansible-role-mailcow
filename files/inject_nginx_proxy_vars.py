#! /usr/bin/python3

import os
import argparse
import yaml
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')

parser = argparse.ArgumentParser()
parser.add_argument('--compose-file', dest='composefile', type=str, help='Path to the docker-compose.yml', required=True)
parser.add_argument('--virtual-host', dest='vhost', type=str, help='Virtual host domains', required=True)
parser.add_argument('--virtual-port', dest='vport', type=str, help='Virtual host port', required=True)
args = parser.parse_args()

def main():
    if not os.path.exists(args.composefile):
        logging.error('Path {0} does not exist.'.format(args.composefile))
        raise Exception('Path {0} does not exist.'.format(args.composefile))

    with open(args.composefile, 'r') as file:
        logging.info('Reading compose file {0}'.format(args.composefile))
        compose_file = yaml.load(file, yaml.Loader)

    proxy_vars = {
        'VIRTUAL_HOST': args.vhost,
        'VIRTUAL_PORT': args.vport,
        'VIRTUAL_PROTO': 'https',
        'LETSENCRYPT_HOST': args.vhost,
        'LETSENCRYPT_SINGLE_DOMAIN_CERTS': 'false'
    }

    environment_vars = [var for var in compose_file['services']['nginx-mailcow']['environment'] if var.split('=')[0] not in proxy_vars]
    for var in proxy_vars:
        environment_vars.append('{0}={1}'.format(var,proxy_vars[var]))

    logging.info('New environment variables for the nginx container: {0}'.format(environment_vars))
    compose_file['services']['nginx-mailcow']['environment'] = environment_vars
   
    with open(args.composefile, 'w') as file:
        logging.info('Writing compose file {0}'.format(args.composefile))
        file.write(yaml.dump(compose_file))

if __name__ == '__main__':    
    main()