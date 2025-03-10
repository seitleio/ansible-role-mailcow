#! /usr/bin/python3

import os
import argparse
import yaml
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')

parser = argparse.ArgumentParser()
parser.add_argument('--compose-file', dest='composefile', type=str, help='Path to the docker-compose.yml', required=True)
parser.add_argument('--replace-path', dest='replacepath', type=str, help='New path for container persistent data', required=True)
args = parser.parse_args()

def main():
    for path in (args.composefile, args.replacepath):
        if not os.path.exists(path):
            logging.error('Path {0} does not exist.'.format(path))
            raise Exception('Path {0} does not exist.'.format(path))

    with open(args.composefile, 'r') as file:
        logging.info('Reading compose file {0}'.format(args.composefile))
        compose_file = yaml.load(file, yaml.Loader)

    if 'volumes' not in compose_file: 
        logging.warning('No volumes node found in compose file - Exiting...')
        exit()

    logging.info('Compose file has {0} volumes'.format(len(compose_file['volumes'])))
    volume_names = list(compose_file['volumes'].keys())
    logging.info(volume_names)

    for service in compose_file['services']:        
        if 'volumes' in compose_file['services'][service]:
            service_volumes = compose_file['services'][service]['volumes']
            logging.info('Checking mounts of {0}: {1}'.format(service, service_volumes))

            for volume in service_volumes:
                host_path = volume.split(':')[0]
                container_path = volume.split(':')[1]
                if host_path in volume_names:
                    new_mount_path = '{0}{1}:{2}'.format(args.replacepath, host_path, container_path)
                    logging.info('Replacing {old} with {new}'.format(old=volume, new=new_mount_path))
                    service_volumes = [new_mount_path if i == volume else i for i in service_volumes]

            logging.info('Final mounts for {0}: {1}'.format(service, service_volumes))
            compose_file['services'][service]['volumes'] = service_volumes

    logging.info('Removing volumes node from compose file')
    compose_file.pop('volumes')

    with open(args.composefile, 'w') as file:
        logging.info('Writing compose file {0}'.format(args.composefile))
        file.write(yaml.dump(compose_file))

if __name__ == '__main__':    
    main()