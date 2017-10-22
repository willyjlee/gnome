from flask import Flask, request
import nn

app = Flask(__name__)

@app.route('/', methods=['POST'])
def get():
    data = request.get_json()
    print(data)
    # nns = nn.get(phenos)


if __name__ == '__main__':
    app.run(debug=True)