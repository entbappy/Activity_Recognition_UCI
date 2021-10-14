'''
Author: Bappy Ahmed
Email: entbappy73@gmail.com
Date:12-Oct-2021
'''

import pandas as pd
import os
from src.utils.all_utils import read_yaml, create_directory, save_local_df
import argparse
import logging
from sklearn.model_selection import  train_test_split


logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, 'running_logs.log'), level=logging.INFO, format=logging_str,
                    filemode="a")


def split_data(config_path,params_path):
    config = read_yaml(config_path)
    params = read_yaml(params_path)

    artifacts_dir = config['artifacts']['artifacts_dir']

    raw_local_file = config['artifacts']['raw_local_file']
    clean_data_dir = config['artifacts']['clean_data_dir']

    clean_data_save_dir = os.path.join(artifacts_dir, clean_data_dir)
    clean_data_file = os.path.join(clean_data_save_dir, raw_local_file)


    df = pd.read_csv(clean_data_file)

    split_ratio = params['base']['test_size']
    random_state = params['base']['random_state']
    
    train, test = train_test_split(df, test_size=split_ratio, random_state=random_state)
    
    split_data_dir = config['artifacts']['split_data_dir']

    create_directory([os.path.join(artifacts_dir,split_data_dir)])

    train_data_filename = config['artifacts']['train']
    test_data_filename = config['artifacts']['test']

    train_data_path = os.path.join(artifacts_dir,split_data_dir,train_data_filename)
    test_data_path = os.path.join(artifacts_dir,split_data_dir,test_data_filename)
    
    for data , data_path in (train, train_data_path), (test, test_data_path):
        save_local_df(data, data_path)

    
    logging.info(f'Data has been splited successfully to {os.path.join(artifacts_dir,split_data_dir)}')



if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="config/config.yaml")
    args.add_argument("--params", "-p", default="params.yaml")
    parsed_args = args.parse_args()
    
    try:
        logging.info(">>>>> stage_06 started")
        split_data(config_path = parsed_args.config,params_path = parsed_args.params)
        logging.info("stage_06 completed!>>>>>")
    except Exception as e:
        logging.exception(e)
        raise e
    