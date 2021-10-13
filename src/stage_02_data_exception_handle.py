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


def handle_data_exception(config_path):
    config = read_yaml(config_path)

    artifacts_dir = config['artifacts']['artifacts_dir']
    raw_local_dir = config['artifacts']['raw_local_dir']
    modified_data_dir = config['artifacts']['modified_data_dir']

    raw_data_local_dir = os.path.join(artifacts_dir, raw_local_dir)
    modified_data_save_dir = os.path.join(artifacts_dir, modified_data_dir)
    
    create_directory(dirs=[modified_data_save_dir])

    folders = os.listdir(raw_data_local_dir)

    folder_name = []
    ignore_files = ['.gitignore']

    for folder in folders:
        l = len(folder.split('.'))
        if l == 1 and folder not in ignore_files:
            folder_name.append(folder)
    
    for folder in folder_name:
        file_path = os.path.join(raw_data_local_dir,folder)
        files = os.listdir(file_path)
        for data in files:
            if data not in ignore_files:
                data_path = os.path.join(raw_data_local_dir,folder,data)
                df = pd.read_csv(data_path, skiprows=4,error_bad_lines=False)
                df.drop(columns=['# Columns: time'], inplace = True)
                df['label'] = folder
                os.makedirs(modified_data_save_dir+'/'+folder, exist_ok=True)
                save_data = os.path.join(modified_data_save_dir,folder,data)
                df.to_csv(save_data, sep=',', index = False)

    logging.info(f'Data has been modified successfully to {modified_data_save_dir}')



if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="config/config.yaml")
    parsed_args = args.parse_args()
    
    try:
        logging.info(">>>>> stage_02 started")
        handle_data_exception(config_path = parsed_args.config)
        logging.info("stage_02 completed!>>>>>")
    except Exception as e:
        logging.exception(e)
        raise e
    