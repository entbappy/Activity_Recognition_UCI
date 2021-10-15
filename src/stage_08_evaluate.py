'''
Author: Bappy Ahmed
Email: entbappy73@gmail.com
Date:12-Oct-2021
'''

import pandas as pd
import os
from src.utils.all_utils import read_yaml, create_directory,save_reports
import argparse
import logging
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score , confusion_matrix , roc_auc_score, roc_curve,classification_report
import joblib


logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, 'running_logs.log'), level=logging.INFO, format=logging_str,filemode="a")


def evaluate_metrics(actual_values, predicted_values):

    report = classification_report(actual_values, predicted_values)

    return report


def evaluate(config_path,params_path):
    config = read_yaml(config_path)
    params = read_yaml(params_path)

    artifacts_dir = config['artifacts']['artifacts_dir']
    split_data_dir = config['artifacts']['split_data_dir']
  
    test_data_filename = config["artifacts"]["test"]

    test_data_path = os.path.join(artifacts_dir, split_data_dir, test_data_filename)
    
    test_data = pd.read_csv(test_data_path)

    test_y = test_data["label"]
    test_x = test_data.drop("label", axis=1)


    model_dir = config["artifacts"]["model_dir"]
    model_filename = config["artifacts"]["model_filename"]
    model_path = os.path.join(artifacts_dir, model_dir, model_filename)

    # Scaling data
    scaler = StandardScaler()
    scaler.fit(test_x)
    sc_test_x = scaler.transform(test_x)
    
    model = joblib.load(model_path)

    predicted_values = model.predict(sc_test_x)
    report = evaluate_metrics(test_y, predicted_values)

    scores_dir = config["artifacts"]["reports_dir"]
    scores_filename = config["artifacts"]["scores"]

    scores_dir_path = os.path.join(artifacts_dir, scores_dir)
    create_directory([scores_dir_path])

    scores_filepath = os.path.join(scores_dir_path, scores_filename)

    with open(scores_filepath, 'w') as f:
        f.write(report)

    
    logging.info(f'Evaluation has been completed! Your score has been saved to {scores_filepath}')



if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="config/config.yaml")
    args.add_argument("--params", "-p", default="params.yaml")
    parsed_args = args.parse_args()
    
    try:
        logging.info(">>>>> stage_08 started")
        evaluate(config_path = parsed_args.config,params_path = parsed_args.params)
        logging.info("stage_08 completed!>>>>>")
    except Exception as e:
        logging.exception(e)
        raise e
    