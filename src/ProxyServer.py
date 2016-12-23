from flask import Flask, request, json
import requests
from hrw import Ring
from hrwCache import CacheRing
import ast
app = Flask(__name__)


@app.route('/v1/expenses/', methods=['POST'])
def createEntry():
    x = Ring()
    data = request.get_json(force=True)
    print '1', type (data)
    id = data['id']

    y,z = x.hash(str (id))
    print 'y is ',y
    print 'z is ',z



    try:
        r1 = requests.post("http://"+y+"/v1/expenses/", data=json.dumps(data))

        if (r1.status_code == 201):
            try:

                r2 = requests.post("http://"+z+"/v1/expenses/", data=json.dumps(data))
                if (r2.status_code == 201):
                    updateCache(data=json.dumps(data))
                    return json.dumps(r1.text), 201
                else:
                    updateCache(data=json.dumps(data))
                    return json.dumps(r1.text), 201

            except Exception as a:
                return json.dumps(r1.text), 400

        elif (r1.status_code == 208):
            return json.dumps(r1.text), 400
        else:
            try:
                r2 = requests.post("http://"+z+"/v1/expenses/", data=json.dumps(data))

                if (r2.status_code == 201):
                    updateCache(data=json.dumps(data))
                    return json.dumps(r2.text), 201

                else:
                    return json.dumps(r2.text), 400
            except:
                return json.dumps(r1.text), 400


    except Exception as a:
        try:
            r3 = requests.post("http://" + z + "/v1/expenses/", data=json.dumps(data))

            if (r3.status_code == 201):
                updateCache(data=json.dumps(data))
                return json.dumps(r3.text), 201

            else:
                return json.dumps(r3.text), 400
        except:
            return json.dumps([{'Error Message': 'server side error'}]), 400





@app.route('/v1/expenses/<int:id>', methods=['GET'])
def getEntry(id):


    y = CacheRing()
    node = y.hash(str (id))
    id = str (id)

    print 'node is ', node



    try:

        c1 = requests.get("http://" + node + "/v1/expenses/" + id)
        if(c1.status_code == 200):
            return json.dumps(c1.text), 200


        x = Ring()
        y, z = x.hash(str(id))
        id = str(id)

        try:
            r1 = requests.get("http://" + y + "/v1/expenses/" + id)

            if (r1.status_code != 200):
                try:

                    r2 = requests.get("http://" + z + "/v1/expenses/" + id)
                    if (r2.status_code != 200):

                        return json.dumps(r1.text), 400
                    else:
                        updateCache2(r1.text)
                        return json.dumps(r2.text), 200

                except Exception as a:
                    return json.dumps(r1.text), 400

            else:
                updateCache2(r1.text)
                return json.dumps(r1.text), 200


        except Exception as a:
            try:
                r2 = requests.get("http://" + z + "/v1/expenses/" + id)

                if (r2.status_code == 200):
                    updateCache2(r1.text)
                    return json.dumps(r2.text), 200

                else:
                    return json.dumps(r2.text), 400
            except:
                return json.dumps(r2.text), 400

    except Exception as a:
        print 'ex'





def updateCache(data):
    x = CacheRing()
    data = ast.literal_eval(data)
    y = x.hash(str(id))

    try:
        c1 = requests.post("http://" + y + "/v1/expenses/", data=json.dumps(data))

        if (c1.status_code == 201):
            print 'success'
        else:
            print 'failure'

    except Exception as a:
        print 'ex'



def updateCache2(data):
    print 'uc 2'
    x = CacheRing()
    data = ast.literal_eval(data)

    data = data[0]
    y = x.hash(str(id))

    try:
        c1 = requests.post("http://" + y + "/v1/expenses/", data=json.dumps(data))

        if (c1.status_code == 201):
            print 'success'
        else:
            print 'failure'

    except Exception as a:
        print 'ex'


if __name__ == '__main__':

    app.run(host="0.0.0.0", port=12345, debug=False)
