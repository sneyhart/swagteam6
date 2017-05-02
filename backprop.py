### backprop.py
### Jon Clark Freeman
### learns and tests XOR logic
import numpy as np
import numpy.random as rando
import random

class BPNN:
    #initialize the network
    def __init__(self, network):
        self.weights = []

        #weights for hidden and input
        for i in range(1, len(network) - 1):
            self.weights.append(2*rando.random((network[i-1] + 1, network[i] + 1)) - 1)

        self.weights.append(2*rando.random((network[i] + 1, network[i+1])) - 1)

    def activation(self, x):
        return np.tanh(x)

    def activation_deriv(self, x):
        return 1.0 - x**2    

    def train(self, inp, target,learning_rate=0.01, trials=10000):
        #Add bias units as a col of ones on the inputs
        ones = np.atleast_2d(np.ones(inp.shape[0]))
        x = np.concatenate((ones.T, inp), axis=1)
        for j in range(trials):
            #choose a random input to train with
            i = np.random.randint(inp.shape[0])
            activations = [x[i]]

            #calculating the activations for each of the layers
            for k in range(len(self.weights)):
                dot_value = np.dot(activations[k], self.weights[k])
                act = self.activation(dot_value)
                activations.append(act)
 
            # calculating error from outputs and targets
            error = target[i] - activations[-1]
            deltas = [error * self.activation_deriv(activations[-1])]

            # Calculating deltas starting at the hidden layer
            for k in range(len(activations) - 2, 0, -1): 
                deltas.append(deltas[-1].dot(self.weights[k].T)*self.activation_deriv(activations[k]))
            deltas.reverse()

            # updating the weights using the deltas, activations
            for i in range(len(self.weights)):
                layer = np.atleast_2d(activations[i])
                delta = np.atleast_2d(deltas[i])
                self.weights[i] += learning_rate * layer.T.dot(delta)
    
    #test on all of the inputs
    def test(self, inp): 
        retval = np.concatenate((np.ones(1).T, np.array(inp)), axis=1)      
        for i in range(0, len(self.weights)):
            retval = self.activation(np.dot(retval, self.weights[i]))
        return retval

#code to test and train using the class above
nn = BPNN([3,15,15,1])

lines = [np.array((file_line.rstrip('\n').split(','))).astype(float) for file_line in open('pca_training.data')]
lines = np.array(lines)
training = np.delete(lines.T, lines.T.shape[0] - 1,0).T
res = lines.T[-1]

testing_lines = [np.array((file_line.rstrip('\n').split(','))).astype(float) for file_line in open('pca_testing.data')]
testing_lines = np.array(testing_lines)
tests = np.delete(testing_lines.T, testing_lines.T.shape[0] - 1,0).T
actual_classes = testing_lines.T[-1]

nn.train(training, res)
corrects = 0.0
total = 0.0
for t,inpu in enumerate(tests):
    total = total + 1
    if int(round(nn.test(inpu)[0])) == actual_classes[t]:
        corrects = corrects + 1
print "Accuracy - {}".format(corrects/total)
