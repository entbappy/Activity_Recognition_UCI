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



    create_directory(dirs=[EDA_reports_save_dir])

    merge_data_save_dir = os.path.join(artifacts_dir, merge_data_dir)
    merge_data_save_file_name = os.path.join(merge_data_save_dir, raw_local_file)
    


    logging.info(f'EDA reports has been generated successfully to {EDA_reports_save_file}')



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
    