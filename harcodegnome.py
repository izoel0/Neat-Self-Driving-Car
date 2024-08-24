# Create a network that is already train with their structure and weight,bias then get input and calculate the output

import math

def sigmoid(x):
    z = max(-60, min(60, 5 * x))
    return 1/(1 + math.exp(-z))
def relu(x):
    if x <= 0 :
        x = 0
    return x

class DefaultNodeGene:
    def __init__(self,key, bias, activation=None, response=None, aggregation=None) -> None:
        self.bias = bias
        self.key = key
        self.activation = activation
        nodes.append(self)
    def calculate(self,nets):
        useNetwork = []
        for net in nets:
            if net.target == self.key:
                useNetwork.append(net.getValue())
        self.value = sum(useNetwork)+ self.bias
        if self.activation: self.value = self.activation(self.value)
        return self.value
    def setValue(self,value):
        self.value = value

class DefaultConnectionGene:
    def __init__(self, key, weight, enabled=True) -> None:
        if enabled:
            self.weight = weight
            self.origin = translator[key[0]]
            self.target = key[1]
            Networks.append(self)
    def getValue(self):
        global nodes
        return nodes[self.origin].value * self.weight

def calculate():
    output = []
    for i in range(inputnum, len(nodes)):
        output.append(nodes[i].calculate(Networks))
    return output[-3:]

def SetValue(data:list):
    data = data[0]
    for i in range(len(data)):
        nodes[i].setValue(data[i])

nodes = []
translator = {-1:0, -2:1, -3:2, -4:3, 56:4, 119:5 ,0:6, 1:7, 2:8}
inputnum = 4
for i in range(inputnum):
    DefaultNodeGene(-(i+1),0)# 0 and 1
DefaultNodeGene(key=56, bias=2.2032246128760185, response=1.0, activation=relu, aggregation=sum)  
DefaultNodeGene(key=119, bias=2.9013825748779984, response=1.0, activation=relu, aggregation=sum)
DefaultNodeGene(key=0, bias=3.3684694856975392, response=1.0, activation=relu, aggregation=sum)    
DefaultNodeGene(key=1, bias=3.290204194460611, response=1.0, activation=relu, aggregation=sum)     
DefaultNodeGene(key=2, bias=4.044057118086111, response=1.0, activation=relu, aggregation=sum)     

Networks = []

DefaultConnectionGene(key=(-1, 0), weight=0.6477088044487551, enabled=True)
DefaultConnectionGene(key=(-1, 1), weight=0.5364979768877696, enabled=False)
DefaultConnectionGene(key=(-1, 2), weight=2.367377063140804, enabled=True)
DefaultConnectionGene(key=(-1, 56), weight=1.0084260541928889, enabled=True)
DefaultConnectionGene(key=(-1, 119), weight=0.0805039013645682, enabled=True)
DefaultConnectionGene(key=(-2, 0), weight=-2.3323258085473153, enabled=True)
DefaultConnectionGene(key=(-2, 1), weight=0.5574815048741835, enabled=True)
DefaultConnectionGene(key=(-2, 2), weight=1.1547831816941805, enabled=True)
DefaultConnectionGene(key=(-2, 56), weight=-1.4588673308130558, enabled=True)
DefaultConnectionGene(key=(-3, 0), weight=-1.99237021289945, enabled=True)
DefaultConnectionGene(key=(-3, 1), weight=1.0766188771372565, enabled=True)
DefaultConnectionGene(key=(-3, 2), weight=-1.166898121524306, enabled=True)
DefaultConnectionGene(key=(-3, 56), weight=-1.3785395429848348, enabled=True)
DefaultConnectionGene(key=(-4, 1), weight=1.2618744467287093, enabled=True)
DefaultConnectionGene(key=(-4, 2), weight=0.7440010484692233, enabled=True)
DefaultConnectionGene(key=(-4, 56), weight=-1.0524295702356037, enabled=True)
DefaultConnectionGene(key=(56, 0), weight=-0.48851086540223765, enabled=True)
DefaultConnectionGene(key=(56, 1), weight=0.7238370865899421, enabled=True)
DefaultConnectionGene(key=(56, 2), weight=0.5281177016980857, enabled=True)
DefaultConnectionGene(key=(119, 1), weight=-0.8956847121381956, enabled=True)
