import pandas as pd
import utils
from sklearn.metrics import f1_score, precision_score, recall_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier

def evaluate(data, relation):
    new_data = data.sample(frac=1).copy().reset_index()
    new_data['rel'] = new_data['rel'].str.lower().map(lambda x: 1 if x == relation else 0)
    train = len(new_data) * 0.8
    train_data = new_data.loc[0: train]
    test_data = new_data.loc[train:]

    # down sample
    train_p = train_data[train_data['rel'] == 1]
    f = int(len(train_data) / len(train_p))
    print(f)
    train_n = train_data[train_data['rel'] == 0].head(min(len(train_p) * 5, len(train_data)))
    train_data = train_p.append(train_n).sample(frac=1)

    X_train = train_data[data.columns[10:]]
    y_train = train_data['rel']
    X_test = test_data[data.columns[10:]]
    y_test = test_data['rel']

    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    p_test = model.predict(X_test)
    print("precision: %0.3f" % (precision_score(y_test, p_test)))
    print("recall: %0.3f" % recall_score(y_test, p_test))
    print("f1: %0.3f" % f1_score(y_test, p_test))

print("reading data ...")
data = pd.read_csv(utils.flat_rels_path,low_memory=False, sep=',', names=['img','rel','obj','subj','a_x','a_y','a_w','a_h','b_x','b_y','b_w','b_h','DC','EC','TPP','TPPi','NTPP','NTPPi','EQ','PO','above','below','left','right'])
print(data.head(5))

positive_data = data[data["rel"] == 'on']
negative_data = data[data["rel"] != 'on'].head(len(positive_data))

print(len(positive_data))
print(len(negative_data))

evaluate(data, 'on')

