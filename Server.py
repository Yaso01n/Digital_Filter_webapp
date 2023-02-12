import numpy as np
from flask import (Flask, json, jsonify, redirect, render_template, request,url_for)
import OOP

i = 0
path = ""
size = 125
object=OOP.SignalsProcessing()
allpath=OOP.allPassProcessing()


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getzeros', methods=['POST'])
def getzeros():
    if request.method == 'POST':
        object.zeros = json.loads(request.data)
        return jsonify(0)
    return render_template("index.html")

@app.route('/getpoles', methods=['POST', 'GET'])
def getpoles():
    if request.method == 'POST':
        data = request.data
        data = json.loads(data)
        object.poles = data
        return jsonify(data)
    return render_template("index.html")

@app.route('/getallpassfilter', methods=['POST', 'GET'])
def getallpassfilter():
    if request.method == 'POST':
        global i
        data = json.loads(request.data)
        if (type(data) == str):
            i = int(data)
            temp = allpath.allpassfiltersreal[i] + 1j * allpath.allpassfiltersimg[i]
            object.zeros = [1 / np.conjugate(temp)]
            object.poles = [temp]
        else:
            temp = data[0] + 1j * data[1]
            object.zeros = [1 / np.conjugate(temp)]
            object.poles = [temp]   
        return jsonify(0)
    return render_template("index.html")

@app.route('/sendallpassfilter', methods=['POST', 'GET'])
def sendallpassfilter():
    if request.method == 'GET':
        temp = allpath.allpassfiltermaker(object.zeros ,object.poles)
        return jsonify(temp)
    return render_template("index.html")

@app.route('/updatelibrary', methods=['POST', 'GET'])
def updatelibrary():
    if request.method == 'GET':
        allpath.readlibrary()
        return jsonify(allpath.library)
    if request.method == 'POST':
        data = json.loads(request.data)
        allpath.allpassfiltersreal = np.append(allpath.allpassfiltersreal, data[0])
        allpath.allpassfiltersimg = np.append(allpath.allpassfiltersimg, data[1])
        allpath.writelibrary()
        allpath.readlibrary()
        return jsonify(allpath.library)
    return render_template("index.html")

@app.route('/sendfrequencyresposedata', methods=['POST', 'GET'])
def senddata():
    if request.method == 'GET':
        object.zeros = list(map(object.format, object.zeros))
        object.poles = list(map(object.format, object.poles))
        object.zeros = [*object.zeros, *allpath.allpassfilterszeros]
        object.poles = [*object.poles, *allpath.allpassfilterspoles]
        temp = object.frequencyrespose()  
        return jsonify(temp)
    return render_template("index.html")

@app.route('/activateordeactivateallpassfilter', methods=['POST', 'GET'])
def activateordeactivateallpassfilter():
    if request.method == 'POST':
        data = int(json.loads(request.data))
        a = float(
            allpath.allpassfiltersreal[data]) + float(allpath.allpassfiltersimg[data]) * 1j
        tempzeros = 1 / np.conjugate(a)
        temppoles = a
        if tempzeros in allpath.allpassfilterszeros:
            allpath.allpassfilterszeros.remove(tempzeros)
        else:
            
            allpath.allpassfilterszeros.append(tempzeros)
        if temppoles in allpath.allpassfilterspoles:
            allpath.allpassfilterspoles.remove(temppoles)
        else:
            allpath.allpassfilterspoles.append(temppoles)
        tempzeros = list(map(allpath.formattocoardinates, allpath.allpassfilterszeros))
        temppoles = list(map(allpath.formattocoardinates, allpath.allpassfilterspoles))
        return jsonify({
            'allpassfilterzeros': tempzeros,
            'allpassfilterpoles': temppoles
        })
    return render_template("index.html") 

@app.route('/getSignals', methods=['POST', 'GET'])
def dataFilter():
    if request.method == 'POST':
        arr = json.loads(request.data)
        iterator = int(arr[0])
        signalxAxisData, signalyAxisData, dataLength = object.getthedata(path)
        x_chuncks = np.array(signalxAxisData[iterator : iterator + size])
        y_chuncks = np.array(signalyAxisData[iterator : iterator + size])
        graphData = object.filterdata(y_chuncks)
        return jsonify({
            'xAxisData': x_chuncks.tolist(),
            'yAxisData': y_chuncks.tolist(),
            'filter': graphData.tolist(),
            'datalength': dataLength,
        })
    return render_template("index.html")

@app.route('/getData', methods=['POST'])
def my_form_post():
    global path
    if request.method == 'POST':
        path = json.loads(request.data)
        return jsonify(path)
    return render_template("index.html")

@app.route('/generate', methods=['POST'])
def generate():
    Yfilter=[]
    if request.method == 'POST':
        Ydata=json.loads(request.data)
        Yfilter.append(Ydata)
        length=len(Yfilter)
        Yfilterchuncks=Yfilter[0 : length]
        filteredgraph=object.filterdata(Yfilterchuncks)
        return jsonify({
        'filtered': filteredgraph.tolist(),
        })
    return render_template("index.html")


if __name__ == '__main__':
    app.run(port=9000)

