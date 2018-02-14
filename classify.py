import numpy as np
import pandas as pd
import sklearn
import utils

print("reading data ...")
data = pd.read_csv(utils.flat_rels_path)
print(data.head(5))

positive_data = data[data["rel"] == 'ON']
negative_data = data[data["rel"] != 'ON'].head(len(positive_data))