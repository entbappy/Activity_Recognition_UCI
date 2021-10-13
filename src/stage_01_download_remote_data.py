'''
Author: Bappy Ahmed
Email: entbappy73@gmail.com
Date:12-Oct-2021
'''

from src.utils.all_utils import read_yaml, create_directory
import argparse
import os
import logging


logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, 'running_logs.log'), level=logging.INFO, format=logging_str,
                    filemode="a")


def download_data(config_path):
    config = read_yaml(config_path)

    remote_data_path = config['data_source']

    #Saving dataset in local to artifacts
    artifacts_dir = config['artifacts']['artifacts_dir']
    raw_local_dir = config['artifacts']['raw_local_dir']

    raw_local_dir_path = os.path.join(artifacts_dir, raw_local_dir)
    
    create_directory(dirs=[raw_local_dir_path])
    
    #Downloading data
    download_bash = f'cd {raw_local_dir_path} && curl {remote_data_path} --output activity_data.zip'
    os.system(download_bash)
    logging.info(f'Data has been downloaded successfully to {raw_local_dir_path}')
    
    #Unziping data 
    unzip_bash = f'cd {raw_local_dir_path} && unzip activity_data.zip'
    os.system(unzip_bash)
    logging.info(f'Unziped the file activity_data.zip')

    # Deteting zip file 
    delete_bash = f'cd {raw_local_dir_path} && rm -rf activity_data.zip'
    os.system(delete_bash)
    logging.info(f'Deteted the file activity_data.zip')



if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="config/config.yaml")
    parsed_args = args.parse_args()
    
    try:
        logging.info(">>>>> stage_01 started")
        download_data(config_path = parsed_args.config)
        logging.info("stage_01 completed!>>>>>")
    except Exception as e:
        logging.exception(e)
        raise e
    
