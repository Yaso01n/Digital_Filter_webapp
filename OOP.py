import numpy as np
import pandas as pd
from scipy import signal


class datadefinition:
    def __init__(self):
        self.zeros = []
        self.poles = []
        

    def makefilter(zeros,poles):
        # w is the omega or the x axis of the magnitude and frequency responsevalues
        # h is an array that hold two array one is the magnitude and one is the phase
        w, h = signal.freqz_zpk(zeros, poles, 1, fs=1000)
        return w, h


    def getfrequencyresponse(self,h):
        magnitudeplotdata = 20 * np.log10(abs(h))
        angleplotdata = np.unwrap(np.angle(h))
        magnitudeplotdata = np.around(magnitudeplotdata, 4)
        return  magnitudeplotdata, angleplotdata    

#============================================================================================
class SignalsProcessing(datadefinition):

    def getthedata(self,path):
            signalData = pd.read_csv(path)
            signalxAxisData = signalData.values[:, 0]
            signalyAxisData = signalData.values[:, 1]
            dataLength = len(signalxAxisData)
            return signalxAxisData, signalyAxisData, dataLength

    def frequencyrespose(self):
            w, h= datadefinition.makefilter(self.zeros, self.poles)
            print(self.zeros)
            print(self.poles)
            magnitudeplotdata, angleplotdata = datadefinition.getfrequencyresponse(self,h)
            return {
                'w': w.tolist(),
                'magnitude': magnitudeplotdata.tolist(),
                'angle': angleplotdata.tolist()
            }

    def filterdata(self, originalData):
        filteredgraph = []
        b, a = signal.zpk2tf(self.zeros, self.poles, 1)
        filteredSignalYdata = (signal.lfilter(b, a, originalData))
        filteredSignalYdata = np.real(filteredSignalYdata)
        filteredgraph = filteredSignalYdata
        if len(filteredgraph) != 0:
            filteredgraph = np.delete(filteredgraph,0)
            filteredgraph = np.append(filteredgraph,filteredSignalYdata[-1])
        return filteredgraph

    def format(self, x):
        return (x[0] + 1j * x[1])


#==============================================================================================
class allPassProcessing(datadefinition):
    def __init__(self):
        self.allpassfiltersreal = []
        self.allpassfiltersimg = []
        self.allpassfilterszeros = []
        self.allpassfilterspoles = []
        self.library = []

    def allpassfiltermaker(self,zeros,poles):
        w, h= datadefinition.makefilter(zeros, poles)
        magnitudeplotdata, angleplotdata = datadefinition.getfrequencyresponse(self,h)
        zeros = np.array(
            [[np.real(zeros[0]) * 100 + 150,
            np.imag(zeros[0]) * (-100) + 150]])
        poles = np.array(
            [[np.real(poles[0]) * 100 + 150,
            np.imag(poles[0]) * (-100) + 150]])
        return {
            'library': self.library,
            'zeros': zeros.tolist(),
            'poles': poles.tolist(),
            'w': w.tolist(),
            'magnitude': magnitudeplotdata.tolist(),
            'angle': angleplotdata.tolist()
        }

    def maplibrary(self,x, y):
        return str(str(x) + "+" + str(y) + "j")

    def readlibrary(self):
        data = pd.read_csv(r'library.csv')
        self.allpassfiltersreal = data.values[:, 0]
        self.allpassfiltersimg = data.values[:, 1]
        self.library = list(map(self.maplibrary, self.allpassfiltersreal, self.allpassfiltersimg))

    def writelibrary(self):
        df = pd.DataFrame(self.allpassfiltersimg, self.allpassfiltersreal)
        df.to_csv('library.csv')    

    def formattocoardinates(self,x):
            return ([np.real(x) * 100 + 150, np.imag(x) * (-100) + 150])
