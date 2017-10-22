from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import numpy as np
import math

num_neighbors = 2
knc = KNeighborsClassifier(n_neighbors=num_neighbors, algorithm='kd_tree')

def get(phenos):
    with open('data/pheno.features', 'r') as f:
        features = [str.rstrip() for str in f.readlines()]
        print(features)
    pheno = pd.read_csv('data/phenotypes - scores_pseudo_users.csv', usecols=features)

    # features = ['name', 'id', 'anger', 'depression']
    # pheno = pd.read_csv('data/pheno.csv', names=features)
    num_features = len(features) - 1
    #print("num_features: %s" % (num_features))

    full = np.nan_to_num(pheno.as_matrix())
    for i in range(full.shape[0]):
        for j in range(full.shape[1]):
            if not isinstance(full[i][j], str) and math.isnan(full[i][j]):
                full[i][j] = 0

    data = full[:, (len(features) - num_features):]
    print(data.shape)

    knc.fit(data, range(data.shape[0]))

    dist, inds = knc.kneighbors([phenos])
    #inds = inds[:, 1:]
    ppl = full[inds]
    print("Found {} nearest neighbors, using {} features:".format(num_neighbors, num_features))
    print(ppl)

if __name__ == '__main__':
    # examples
    get(range(21))
