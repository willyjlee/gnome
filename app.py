from flask import Flask, request, json
import numpy as np
import nn

app = Flask(__name__)

@app.route('/', methods=['POST'])
def get():
    data = request.get_json()
    print(data)
    # nns = nn.get(phenos)
    nns = nn.get_nearest(np.array(data['input']),
                users=np.array([data['user0'], data['user1'], data['user2'], data['user3'], data['user4'], data['user5']]))
    nns = np.squeeze(nns, axis=0)

    resp = {}
    neighbors = []
    for i in range(nns.shape[0]):
        neighbors.append(nns[i][0])
    resp['resp'] = neighbors

    return json.dumps(resp)


if __name__ == '__main__':
    # nns = nn.get_nearest(np.array(range(66)), users=np.array([[i+1 for i in range(66)], [i+2 for i in range(66)]]))
    # print(nns.shape)

    app.run(debug=True)