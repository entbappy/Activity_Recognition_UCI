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
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import joblib


logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, 'running_logs.log'), level=logging.INFO, format=logging_str,filemode="a")


def training(config_path,params_path):
    config = read_yaml(config_path)
    params = read_yaml(params_path)

    artifacts_dir = config['artifacts']['artifacts_dir']
    split_data_dir = config['artifacts']['split_data_dir']
  
    train_data_filename = config['artifacts']['train']

    train_data_path = os.path.join(artifacts_dir,split_data_dir,train_data_filename)
  
    train_data = pd.read_csv(train_data_path)

    train_y = train_data["label"]
    train_x = train_data.drop("label", axis=1)
    
    # Scaling data
    scaler = StandardScaler()
    scaler.fit(train_x)
    sc_train_x = scaler.transform(train_x)



    multi_class = params["model_params"]["LogisticRegression"]["multi_class"]
    solver = params["model_params"]["LogisticRegression"]["solver"]
    penalty = params["model_params"]["LogisticRegression"]["penalty"]
    C = params["model_params"]["LogisticRegression"]["C"]

    model = LogisticRegression()
    model.fit(sc_train_x, train_y)


    model_dir = config["artifacts"]["model_dir"]
    model_filename = config["artifacts"]["model_filename"]

    model_dir = os.path.join(artifacts_dir, model_dir)

    create_directory([model_dir])

    model_path = os.path.join(model_dir, model_filename)


    joblib.dump(model, model_path)

    logging.info(f'Training has been completed! Your model has been saved to {model_path}')



if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="config/config.yaml")
    args.add_argument("--params", "-p", default="params.yaml")
    parsed_args = args.parse_args()
    
    try:
        logging.info(">>>>> stage_07 started")
        training(config_path = parsed_args.config,params_path = parsed_args.params)
        logging.info("stage_07 completed!>>>>>")
    except Exception as e:
        logging.exception(e)
        raise e
    