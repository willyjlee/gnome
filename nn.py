from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import numpy as np
import math

num_neighbors = 2
knc = KNeighborsClassifier(n_neighbors=num_neighbors, algorithm='kd_tree')

with open('data/pheno.features', 'r') as f:
    features = [str.rstrip() for str in f.readlines()]
    print(features)
# - 1 for the username in col0
num_features = len(features) - 1

with open('data/phenotypes - scores_pseudo_users.csv', 'r') as line:
    all_features = [x.rstrip() for x in line.readline().split(',')]
    print(all_features)

selected_inds = []
for feature in features:
    selected_inds.append(all_features.index(feature))
print(selected_inds)

def get_nearest(phenos, file=None, users=None):
    print('phenos')
    print(phenos.shape)
    make_phenos = np.array([phenos[selected_inds[0]]])
    for i in range(len(selected_inds)):
        if i != 0:
            make_phenos = np.concatenate((make_phenos, np.array([phenos[selected_inds[i]]])), axis=0)
    print('make')
    print(make_phenos.shape)
    phenos = make_phenos[1:]
    print('phenos')
    print(phenos.shape)

    if file is not None:
        pheno = pd.read_csv(file, usecols=features)
        full = np.nan_to_num(pheno.as_matrix())

    elif users is not None:
        # select features, assume same order
        print(selected_inds[0])
        print('users')
        print(users.shape)
        pheno = np.array([users[:, selected_inds[0]]])
        print(pheno.shape)
        for i in range(len(selected_inds)):
            if i != 0:
                pheno = np.concatenate((pheno, np.array([users[:, selected_inds[i]]])), axis=0)
        pheno = np.transpose(pheno)

        print('pheno')
        print(pheno.shape)
        full = pheno
    else:
        return

    # username in first
    data = full[:, 1:]

    print('full')
    print(full.shape)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if not isinstance(data[i][j], str) and math.isnan(data[i][j]):
                data[i][j] = 0

    knc.fit(data, range(data.shape[0]))
    print('data')
    print(data.shape)

    dist, inds = knc.kneighbors([phenos])
    #inds = inds[:, 1:]
    ppl = full[inds]
    print("Found {} nearest neighbors, using {} features:".format(num_neighbors, num_features))
    print(ppl)
    return ppl

if __name__ == '__main__':
    # examples
    #get_nearest(range(21), file='data/phenotypes - scores_pseudo_users.csv')
    inp = list(range(66))

    print(inp)
    get_nearest(np.array(inp), users=np.array([[i for i in range(66)], [i for i in range(66)]]))

