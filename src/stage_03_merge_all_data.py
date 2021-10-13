'''
Author: Bappy Ahmed
Email: entbappy73@gmail.com
Date:12-Oct-2021
'''

import pandas as pd
import os
from src.utils.all_utils import read_yaml, create_directory
import argparse
import logging

logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, 'running_logs.log'), level=logging.INFO, format=logging_str,
                    filemode="a")


def merge_data(config_path):
    config = read_yaml(config_path)

    artifacts_dir = config['artifacts']['artifacts_dir']

    modified_data_dir = config['artifacts']['modified_data_dir']
    merge_data_dir = config['artifacts']['merge_data_dir']
    raw_local_file = config['artifacts']['raw_local_file']

    modified_data_save_dir = os.path.join(artifacts_dir, modified_data_dir)
    merge_data_save_dir = os.path.join(artifacts_dir, merge_data_dir)
    merge_data_save_file_name = os.path.join(merge_data_save_dir, raw_local_file)
    
    create_directory(dirs=[merge_data_save_dir])

    folders = os.listdir(modified_data_save_dir)

    folder_name = []
    ignore_files = ['.gitignore']

    for folder in folders:
        l = len(folder.split('.'))
        if l == 1 and folder not in ignore_files:
            folder_name.append(folder)
    
    frames = []
    for folder in folder_name:
        file_path = os.path.join(modified_data_save_dir,folder)
        files = os.listdir(file_path)
        for data in files:
            if data not in ignore_files:
                data_path = os.path.join(modified_data_save_dir,folder,data)
                df = pd.read_csv(data_path)
                frames.append(df)
    
    results = pd.concat(frames)
    results.to_csv(merge_data_save_file_name, sep=',', index = False)

    logging.info(f'Data has been merged successfully to {merge_data_save_dir}')



if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="config/config.yaml")
    parsed_args = args.parse_args()
    
    try:
        logging.info(">>>>> stage_03 started")
        merge_data(config_path = parsed_args.config)
        logging.info("stage_03 completed!>>>>>")
    except Exception as e:
        logging.exception(e)
        raise e
    