import pandas as pd
import utils

def generateTripletStats(data, sp, tr, lm):

    # spFiltered = data[data["rel"] == sp]
    # trFiltered = spFiltered[spFiltered["subj"] == tr]
    # lmFiltered = spFiltered[spFiltered["obj"] == lm]
    for i in range(len(data)-1):
        i = i + 1
        print("%s,%s,%s" % (data['rel'][i], data['subj'][i],data['obj'][i]))
              #, lmFiltered['DC'], lmFiltered['EC'], lmFiltered['TPP'], lmFiltered['TPPi'], lmFiltered['NTPP'], lmFiltered['NTPPi'], lmFiltered['EQ'], lmFiltered['PO'], lmFiltered['above'], lmFiltered['below'], lmFiltered['left'], lmFiltered['right']))

print("reading data ...")
data = pd.read_csv(utils.flat_rels_path,low_memory=False, sep=',', names=['img','rel','obj','subj','a_x','a_y','a_w','a_h','b_x','b_y','b_w','b_h','DC','EC','TPP','TPPi','NTPP','NTPPi','EQ','PO','above','below','left','right'])
print(data.head(5))

EC = data[data["EC"] == '1']
DC = data[data["DC"] == '1']
PO = data[data["PO"] == '1']
TPP = data[data["TPP"] == '1']
TPPi = data[data["TPPi"] == '1']
NTPP = data[data["NTPP"] == '1']
NTPPi = data[data["NTPPi"] == '1']
EQ = data[data["EQ"] == '1']
above = data[data["above"] == '1']
below = data[data["below"] == '1']
left = data[data["left"] == '1']
right = data[data["right"] == '1']

print("EC -> %s, DC -> %s, PO -> %s, TPP -> %s, TPPi -> %s, NTPP -> %s, NTPPi -> %s, EQ -> %s, Above -> %s, Below -> %s, Left -> %s, Right -> %s" % (len(EC), len(DC), len(PO), len(TPP), len(TPPi), len(NTPP), len(NTPPi), len(EQ), len(above), len(below), len(left), len(right)))

generateTripletStats(data, 'on', 'table', 'telephone')
