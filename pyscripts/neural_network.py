__author__ = 'Ryan'

from numpy import *
import numpy as np
from math import exp, log
from math import sqrt


class NeuralNetwork:

    #
    def __init__(self,layer_array,reg_lambda = 0, epsilon_init = 0.12):
        isGood = self.__error_check__(layer_array)
        if isGood:
            self.num_layers = len(layer_array) - 1 # Number of weight matrices between layers
            self.reg_lambda = reg_lambda
            self.epsilon_init = epsilon_init
            self.layer_weights = [0 for i in range(self.num_layers)]
            self._rand_weights_init(layer_array)

    # initializes weights for network
    def _rand_weights_init(self, layer_array):
        for i in range(self.num_layers):
            row_size = layer_array[i] + 1 # Add Bias Vector
            col_size = layer_array[i+1]
            randArray = random.uniform(-1/sqrt(row_size), 1/sqrt(row_size), (row_size*col_size))
            self.layer_weights[i] = randArray.reshape((row_size,col_size))

    def costFunction(self,X,y,):
        # X should be array of arrays
        m = X.shape[0] # Number of Training examples.


        # Convert y number values into logical arrays with indices corresponding to the label
        Y = zeros((X.shape[0],self.layer_weights[-1].shape[1]))
        for i in range(Y.shape[0]):
            Y[i,y[i]] = 1

        ### Feed-Forward Calculations

        # Adding bias value to each X array
        a_list = [0 for i in range(self.num_layers + 1)]
        z_list = [0 for i in range(self.num_layers + 1)]
        a_list[0] = copy(X)

        for ii in range(len(a_list)-1):
            a_list[ii] = hstack((ones((a_list[ii].shape[0], 1)), a_list[ii]))
            z_list[ii] = dot(a_list[ii], self.layer_weights[ii])
            z_list[ii] = self.sigmoid(z_list[ii])
            #for i in range(z_list[ii].shape[0]):
            #    for j in range(z_list[ii].shape[1]):
            #        z_list[ii][i][j] = self.sigmoid(z_list[ii][i][j])
            a_list[ii+1] = copy(z_list[ii])

        J = 1 / m * sum(-Y.flatten() * np.log(a_list[-1].flatten()) - (1 - Y.flatten()) * np.log(1 - a_list[-1].flatten()))

        #Regularization param
        reg = 0
        for i in range(self.num_layers):
            reg += sum(delete(self.layer_weights[i],0,1)**2)
        reg = self.reg_lambda / (2*m) * reg
        J = J + reg


        # Backpropagation algorithm implementation
        deltas = [zeros(self.layer_weights[i].shape) for i in range(self.num_layers)]
        d_i = [0 for i in range(self.num_layers)]
        for t in range(m):
            d_i[-1] = a_list[-1][t] - Y[t]
            for i in range(len(deltas)-1,0,-1):
                # the following dot product
                deltas[i] = deltas[i] + dot(np.resize(d_i[i],(d_i[i].shape[0],1)), np.resize(a_list[i][t],(1,a_list[i].shape[1]))).T
                # find sigmoid gradient
                z_temp = self.sigmoid_gradient(z_list[i-1][t])
                d_i[i-1] = np.dot(delete(self.layer_weights[i],0,0),resize(d_i[i],(d_i[i].shape[0],1))) * z_temp
            i-=1
            deltas[0] = deltas[0] + dot(np.resize(d_i[0],(d_i[0].shape[0],1)), np.resize(a_list[0][t],(1,a_list[0].shape[1]))).T

        for delta_i in deltas:
            delta_i/= m

        return J, deltas

    def predict(self, inputs):
        # Checks if array is right type, size
        if not isinstance(inputs,(ndarray,list)) or len(inputs) != self.get_node_length(0) - 1 :
            print("inputs either not right size or not right type!")
            return -1
        temp = array(inputs)
        # Checks to see array/matrix not wrong position
        if temp.shape[0] != 1:
            temp = temp.T
        for i in range(self.num_layers):
            temp2 = insert(temp,0,1) # Inserting Bias value
            temp = dot(temp2,self.layer_weights[i])
            for i in range(len(temp)):
                temp[i] = self.sigmoid(temp[i]);
        return where(temp==max(temp))[0][0]

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))



    def sigmoid_gradient(self, z):
        sig = self.sigmoid(z)
        return sig * (1 - sig)


    # Takes in list of numbers corresponding with layer numbers
    def print_layer_weights(self,which_layer = -1):
        if isinstance(which_layer,int):
            if which_layer < 0:
                layers = list(range(self.num_layers))
            else:
                layers = [which_layer]
        else:
            layers = which_layer
        for i in layers:
            if isinstance(i,int) and i in range(self.num_layers):
                mat = self.layer_weights[i]
                print("\nLayer Weights between Layer " + str(i) + " and Layer " + str(i+1) + ": ")
                for rows in mat:
                    print(rows)

    def get_node_length(self,layer_num):
        if layer_num > self.num_layers or layer_num < 0:
            return -1
        return len(self.layer_weights[layer_num])

    def __error_check__(self,layer_array):
        for i in range(len(layer_array)-1):
            if layer_array[i] < layer_array[i+1]:
                return False
        return True


# Test Stuff
nn = NeuralNetwork([10,5,3])
nn.print_layer_weights()

a = ones((10))


print("\nIndex Choice : " + str(nn.predict(a)))


X1 = ones((20,10))
y1 = random.randint(3,size=20)

print(nn.costFunction(X1,y1))