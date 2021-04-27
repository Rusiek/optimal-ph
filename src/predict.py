import argparse
import pandas as pd
import os

from model import SVRModelScaled

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
    input_table = pd.read_csv(input_csv)

phychem = pd.read_csv("physchem-properties.csv", index_col=0).drop("ID", axis=1).reset_index(drop=True)

# Run predictions
y_predictions = SVRModelScaled(model_file_path='src/svr-model-physchem.pickle',
                               scaler_file_path='src/svr-scaler-physchem.pickle').predict(input_table, phychem)

for i in range(1, len(y_predictions))
    y_predictions[i] = round(y_predictions[i], 1)

# Save predictions to file
df_predictions = pd.DataFrame({'prediction': y_predictions})
df_predictions.to_csv(output_file_path, index=False)
print("Thanks, come again!")
