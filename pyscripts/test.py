#!/usr/bin/python

import numpy as np
from scipy import ndimage
import sys
import glob
#from matplotlib import pyplot as plt
#from matplotlib import cm as cm

import neural_network as NN



GROUND_TRUTH_LABELS = np.zeros((5000,),dtype=np.uint8)
TRAINING_IMAGES=np.zeros((5000,400),dtype=np.uint8)



def test():
    global GROUND_TRUTH_LABELS,TRAINING_IMAGES
    data_path=""
    if(len(sys.argv) > 1):
        data_path = sys.argv[1]
        if(data_path[-1] != '/'): data_path += '/'
    else:
        data_path="/home/bilkit/CSE415Final/data/"

    print("loading data from \""+data_path+"\"...")
    print("data loaded: "+str(loadData(data_path)))
    print("Y desired output is contained in GROUND_TRUTH_LABELS,\
     X samples are contained in TRAINING_IMAGES.")

    nn = trainNeuralNetwork()

    demo(nn)

    # ax=plt.figure().add_subplot(111)
    # imN=0
    # print("sample "+str(imN)+" of len "+str(TRAINING_IMAGES[imN].size)+"\n"+str(TRAINING_IMAGES[imN]))


    return


def trainNeuralNetwork():
    #initialize neural net
    NET = NN.NeuralNetwork([10,5,3])
    new_weights = [0 for ii in range(NET.num_layers)]


    # min_func = lambda p: NET.costFunction(p,GROUND_TRUTH_LABELS)
    # opt.fmin_cg(min_func,NET.layer_weights,args=,)






    return NET


# def performIteration(nn):
#     new_weights = [0 for ii in range(nn.num_layers)]
#     #compute cost for each node in network (forward/back propogation)
#     [net_cost,net_deltas]= nn.costFunction(TRAINING_IMAGES,GROUND_TRUTH_LABELS)
#
#     #minimize net_cost
#     opt.fmin_cg
#     #
#
#     return True


def loadData(data_path):
    'loads image files and one csv file from a given directory'
    global GROUND_TRUTH_LABELS,TRAINING_IMAGES
    'loads images and csv from a dir and returns true if successful'
    try:
        GROUND_TRUTH_LABELS = np.loadtxt( (glob.glob(data_path+"*.csv")[0]),delimiter=',' )
    except:
        print("loadData: could not load .csv file")
        return False
    #load and store images corresponding to indices of ground truth
    try:
        image_file_paths = glob.glob(data_path+"samps10/*.bmp")
    except:
        print("loadData: could not load .bmp files")
        return False

    for file_path in image_file_paths:
        im_index = (int)(((file_path.split('/')[-1]).split('_')[-1]).split('.')[0])
        im_index -= 1
        im_vector = matToVector( ndimage.imread(file_path) )
        if(im_vector == None): return False
        TRAINING_IMAGES[im_index]=np.array(im_vector,dtype=np.uint8)

        #DEBUG#
        # visualize(TRAINING_IMAGES[im_index])


    return True

def matToVector(mat):
    'returns numpy array of size (mat.size)x1 -- matrix is expected to be numpy array'
    if not isinstance(mat,np.ndarray):  print("matToVector: could not convert matrix to vector"); return None #do something else
    if (mat.shape[0] < 2 and mat.shape[1] >= 2) or \
            (mat.shape[1] < 2 and mat.shape[0] >= 2): return mat #already vector
    # return [val for row in mat for val in row]
    return np.reshape(mat,(mat.size,))


def vecToMatrix(vec,M,N):
    'returns a numpy array of size MxN -- vec is expected to be numpy array'
    if not isinstance(vec,np.ndarray): return None #do something else
    if M*N != vec.size: print("vecToMatrix: Invalid dims"); return None
    if M <= 0 or N <= 0: print("vecToMatrix: Invalid dims"); return None
    return np.reshape(vec,(M,N))
#
# def visualize(imageV):
#     if imageV == None: return False
#     imageMat = vecToMatrix(imageV,20,20)
#     if imageMat == None: print("Visualize: failed to obtain matrix"); return False
#
#     plt.imshow(imageMat,cmap = cm.Greys_r,interpolation="nearest")
#     plt.show()
#     return True


def demo(nn):
    rand_perm = np.random.permutation(GROUND_TRUTH_LABELS.size)
    sel_ims = [TRAINING_IMAGES[ii] for ii in rand_perm[0:10]]
    pred = nn.predict(np.array(sel_ims[0:9]))

    # for im in sel_ims:
    #     print("for image_"+str(sel_ims.index(im))+" nn predicted "+str(pred[sel_ims.index(im)]))

    return




test()