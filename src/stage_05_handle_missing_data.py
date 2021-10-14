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


def handle_missing_value(config_path):
    config = read_yaml(config_path)

    artifacts_dir = config['artifacts']['artifacts_dir']

    merge_data_dir = config['artifacts']['merge_data_dir']
    raw_local_file = config['artifacts']['raw_local_file']
    clean_data_dir = config['artifacts']['clean_data_dir']

    clean_data_save_dir = os.path.join(artifacts_dir, clean_data_dir)
    clean_data_file = os.path.join(clean_data_save_dir, raw_local_file)


    create_directory(dirs=[clean_data_save_dir])

    merge_data_save_dir = os.path.join(artifacts_dir, merge_data_dir)
    merge_data_save_file_name = os.path.join(merge_data_save_dir, raw_local_file)

    df = pd.read_csv(merge_data_save_file_name)
    logging.info(f'Data shape before null removed: {df.shape}')
    df.dropna(inplace=True)
    logging.info(f'Data shape after null removed:{df.shape}')
    logging.info(f'Data shape after null removed:{df.isnull().sum()}')

    #Encoding the label 
    label = {
    'bending1': 1,
    'bending2': 2,
    'cycling': 3,
    'lying': 4,
    'sitting': 5,
    'standing': 6,
    'walking': 7
    }

    df['label'] = df['label'].map(label)
    logging.info(f'Label has been encoded: {label}')
    
    df.to_csv(clean_data_file, sep=',', index = False)
    
    logging.info(f'Null values have been removed successfully to {clean_data_file}')



if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="config/config.yaml")
    parsed_args = args.parse_args()
    
    try:
        logging.info(">>>>> stage_05 started")
        handle_missing_value(config_path = parsed_args.config)
        logging.info("stage_05 completed!>>>>>")
    except Exception as e:
        logging.exception(e)
        raise e
    