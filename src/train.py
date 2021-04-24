import pandas as pd
from sklearn.model_selection import train_test_split
from model import SVRModel

# Load data set
with open('data/train_set.csv', 'rb') as train_data:
    data = pd.read_csv(train_data)

CLUSTER_FILE = "aux/clustering/clusters/ident90"


with open(CLUSTER_FILE, "r") as f:
    lines = f.readlines()

representative = set(x.split()[1] for x in lines[::2])
data["representative"] = ("Seq" + data.index.astype(str)).isin(representative)
data["is7"] = data.mean_growth_PH == 7

SVRModel(model_file_path='src/svr-model.pickle').train(data)
