import argparse
import pandas as pd
import os

from model import SVRModel

parser = argparse.ArgumentParser()
parser.add_argument('--input_csv', default='input.csv')
args = parser.parse_args()

# Config
output_file_path = 'predictions.csv'

# Run R script to compute physicochemical properties
exit_code = os.system(f"Rscript src/properties.r {args.input_csv} physchem-properties.csv")

assert exit_code == 0

# Load input.csv
with open(args.input_csv) as input_csv:
    aa_frequencies = pd.read_csv(input_csv)

phychem = pd.read_csv("physchem-properties.csv", index_col=0).drop("ID", axis=1).reset_index(drop=True)
features = pd.concat([aa_frequencies, phychem], axis=1)

# Run predictions
y_predictions = SVRModel(model_file_path='src/svr-model.pickle').predict(features)

# Save predictions to file
df_predictions = pd.DataFrame({'prediction': y_predictions})
df_predictions.to_csv(output_file_path, index=False)
print("Thanks, come again!")