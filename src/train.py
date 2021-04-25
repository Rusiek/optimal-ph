import pandas as pd
from sklearn.model_selection import train_test_split
from model import SVRModel, SVRModelScaled

# Load data set
with open('data/train_set.csv', 'rb') as train_data:
    input_df = pd.read_csv(train_data)

CLUSTER_FILE = "aux/clustering/clusters/ident90"


with open(CLUSTER_FILE, "r") as f:
    lines = f.readlines()

representative = set(x.split()[1] for x in lines[::2])
input_df["representative"] = ("Seq" + input_df.index.astype(str)).isin(representative)
input_df["is7"] = input_df.mean_growth_PH == 7

phychem = pd.read_csv("data/physchem/properties.csv", index_col=0).drop("ID", axis=1).reset_index(drop=True)

SVRModelScaled(model_file_path='src/svr-model-physchem.pickle',
               scaler_file_path='src/svr-scaler-physchem.pickle').train(input_df, phychem)
