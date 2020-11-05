# classify.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/27/2018
# Extended by Daniel Gonzales (dsgonza2@illinois.edu) on 3/11/2020

"""
This is the main entry point for MP5. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.

train_set - A Numpy array of 32x32x3 images of shape [7500, 3072].
            This can be thought of as a list of 7500 vectors that are each
            3072 dimensional.  We have 3072 dimensions because there are
            each image is 32x32 and we have 3 color channels.
            So 32*32*3 = 3072. RGB values have been scaled to range 0-1.

train_labels - List of labels corresponding with images in train_set
example: Suppose I had two images [X1,X2] where X1 and X2 are 3072 dimensional vectors
         and X1 is a picture of a dog and X2 is a picture of an airplane.
         Then train_labels := [1,0] because X1 contains a picture of an animal
         and X2 contains no animals in the picture.

dev_set - A Numpy array of 32x32x3 images of shape [2500, 3072].
          It is the same format as train_set

return - a list containing predicted labels for dev_set
"""

import numpy as np
import heapq
import pdb

def trainPerceptron(train_set, train_labels, learning_rate, max_iter):
    # TODO: Write your code here
    # return the trained weight and bias parameters
    W = [0.0 for i in range(len(train_set[0]))]
    b = 0.0
    for i in range(max_iter):
        for j in range(len(train_set)):
            result = np.dot(W, train_set[j]) + b
            result = np.sign(result)
            if result == 1 and train_labels[j] == 1:
                continue
            if result != 1 and train_labels[j] == 0:
                continue
            label = train_labels[j]
            if label == 0:
                label -= 1
            W = W + learning_rate * label * train_set[j]
            b = b + learning_rate * label
    return W, b

def classifyPerceptron(train_set, train_labels, dev_set, learning_rate, max_iter):
    # TODO: Write your code here
    # Train perceptron model and return predicted labels of development set
    temp = trainPerceptron(train_set, train_labels, learning_rate, max_iter)
    W = temp[0]
    b = temp[1]
    result = []
    for i in range(len(dev_set)):
        temp2 = np.dot(W, dev_set[i]) + b
        temp2 = np.sign(temp2)
        if temp2 == 1:
            result.append(1)
        else:
            result.append(0)
    return result

def classifyKNN(train_set, train_labels, dev_set, k):
    # TODO: Write your code here
    queue = []
    pos_count = 0
    neg_count = 0
    result = []
    for image in dev_set:
        queue.clear()
        x = np.array(image)
        for i in range(len(train_set)):
            y = np.array(train_set[i])
            distance = np.linalg.norm(x-y)
            queue.append((distance, train_labels[i]))
        # heapq.heapify(queue)
        queue.sort(key=lambda z: z[0])
        pos_count = 0
        neg_count = 0
        for j in range(k):
            temp = heapq.heappop(queue)
            if temp[1] == 1:
                pos_count += 1
            else:
                neg_count += 1
        if pos_count > neg_count:
            result.append(1)
        else:
            result.append(0)
    return result
