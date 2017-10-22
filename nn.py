from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import numpy as np
import math
import operator

num_neighbors = 4
knc = KNeighborsClassifier(n_neighbors=num_neighbors, algorithm='kd_tree')

with open('data/pheno.features', 'r') as f:
    features = [str.rstrip() for str in f.readlines()]
    #print(features)
# - 1 for the username in col0
num_features = len(features) - 1

with open('data/phenotypes - scores_pseudo_users.csv', 'r') as line:
    all_features = [x.rstrip() for x in line.readline().split(',')]
    #print(all_features)

selected_inds = []
for feature in features:
    selected_inds.append(all_features.index(feature))
#print(selected_inds)

def stable(users):
    m = {}
    w = {}
    prefs = {}
    prop = {}

    only_men = []
    only_women = []

    names = {}
    for i, user in enumerate(users):
        names[user[0]] = i
        if user[0][0] == 'w':
            only_women.append(user)
        else:
            only_men.append(user)

    for i, user in enumerate(users):
        if user[0][0] == 'w':
            inds, _ = get_nearest(user, users=np.array(only_men))
            prefs[i] = inds
            new_inds = []
            for index in prefs[i]:
                new_inds.append(names[only_men[index][0]])
            prefs[i] = new_inds
            w[i] = -1
        else:
            inds, _ = get_nearest(user, users=np.array(only_women))
            prefs[i] = inds
            new_inds = []
            for index in prefs[i]:
                new_inds.append(names[only_women[index][0]])
            prefs[i] = new_inds
            m[i] = -1

    while True:
        free_man = None
        for man, spo in m.items():
            if spo == -1:
                free_man = man
                break
        if free_man is None:
            break

        w_0 = None
        for wom in prefs[free_man]:
            if free_man not in prop or wom not in prop[free_man]:
                w_0 = wom
                break
        if w_0 is None:
            print(prop)
            print(free_man)
            print("oh no")
        if free_man not in prop:
            prop[free_man] = []
        prop[free_man].append(w_0)
        if w_0 is not None and w[w_0] == -1:
            m[free_man] = w_0
            w[w_0] = free_man
        else:
            fian = w[w_0]
            print(w_0)
            if free_man not in prefs[w_0] or fian not in prefs[w_0]:
                continue
            if prefs[w_0].index(fian) > prefs[w_0].index(free_man):
                m[free_man] = w_0
                w[w_0] = free_man
                m[fian] = -1
            else:
                pass
    for man, spo in m.items():
        if spo == -1:
            print('user %s is single' % users[man][0])
        else:
            print('user %s married user %s' % (users[man][0], users[spo][0]))


def get_nearest(phenos, file=None, users=None):
    #print('phenos')
    #print(phenos.shape)
    make_phenos = np.array([phenos[selected_inds[0]]])
    for i in range(len(selected_inds)):
        if i != 0:
            make_phenos = np.concatenate((make_phenos, np.array([phenos[selected_inds[i]]])), axis=0)
    #print('make')
    #print(make_phenos.shape)
    phenos = make_phenos[1:]
    #print('phenos')
    #print(phenos.shape)

    if file is not None:
        pheno = pd.read_csv(file, usecols=features)
        full = np.nan_to_num(pheno.as_matrix())

    elif users is not None:
        # select features, assume same order
        #print(selected_inds[0])
        #print('users')
        #print(users.shape)
        pheno = np.array([users[:, selected_inds[0]]])
        #print(pheno.shape)
        for i in range(len(selected_inds)):
            if i != 0:
                pheno = np.concatenate((pheno, np.array([users[:, selected_inds[i]]])), axis=0)
        pheno = np.transpose(pheno)

        #print('pheno')
        #print(pheno)
        full = pheno
    else:
        return

    # username in first
    data = full[:, 1:]

    #print('full')
    #print(full.shape)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if not isinstance(data[i][j], str) and math.isnan(data[i][j]):
                data[i][j] = 0

    knc.fit(data, range(data.shape[0]))
    #print('data')
    #print(data.shape)

    dist, inds = knc.kneighbors([phenos])

    #inds = inds[:, 1:]
    ppl = full[inds]

    ppl = np.squeeze(ppl, axis=0)
    inds = np.squeeze(inds, axis=0)
    dist = np.squeeze(dist, axis=0)
    print(dist)
    print(inds)
    make_inds = []
    for dist, inds in sorted(zip(dist, inds), key=operator.itemgetter(0)):
        make_inds.append(inds)
    inds = make_inds

    print(inds)
    print("Found {} nearest neighbors, using {} features:".format(num_neighbors, num_features))
    #print(ppl)
    return inds, ppl

if __name__ == '__main__':
    # examples
    #get_nearest(range(21), file='data/phenotypes - scores_pseudo_users.csv')

    #get_nearest(np.array(inp), users=np.array([[i+2 for i in range(66)], [i for i in range(66)], [i+1 for i in range(66)]]))
    #arrays = np.random.randint(0, high=4, size=(2,65))
    #print(arrays.shape)
    arrays = np.array([["w_user0"],["w_user1"], ["m_user2"], ["m_user3"], ["m_user4"], ["m_user5"], ["w_user6"], ["w_user7"]])
    arrays = np.concatenate((arrays, np.random.randint(0, high=4, size=(8,65))), axis=1)
    #print(arrays)
    # arrays.itemset((0,0), "user0")
    # arrays.itemset((1,0), "user1")


    # inp = ["input_user"]
    # for i in range(65):
    #     inp.append(i%4)
    # print('input')
    # print(inp)
    # _, nns = get_nearest(np.array(inp), users=arrays)
    # print(nns)

    print("The stable marriage output for these users:")
    print(arrays)

    stable(arrays)
