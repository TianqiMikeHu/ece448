# neuralnet.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/29/2019
"""
This is the main entry point for MP6. You should only modify code
within this file and neuralnet_part2 -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

import numpy as np
import torch
import pdb


class NeuralNet(torch.nn.Module):
    def __init__(self, lrate,loss_fn,in_size,out_size):
        """
        Initialize the layers of your neural network

        @param lrate: The learning rate for the model.
        @param loss_fn: A loss function defined in the following way:
            @param yhat - an (N,out_size) tensor
            @param y - an (N,) tensor
            @return l(x,y) an () tensor that is the mean loss
        @param in_size: Dimension of input
        @param out_size: Dimension of output

        For Part 1 the network should have the following architecture (in terms of hidden units):

        in_size -> 32 ->  out_size
        We recommend setting the lrate to 0.01 for part 1

        """
        super(NeuralNet, self).__init__()
        self.loss_fn = loss_fn
        self.in_size = in_size
        self.out_size = out_size
        self.lrate = lrate
        self.fc = torch.nn.Sequential(torch.nn.Linear(self.in_size, 32),
                                      torch.nn.ReLU(),
                                      torch.nn.Linear(32, self.out_size),
                                      torch.nn.ReLU())




    def forward(self, x):
        """ A forward pass of your neural net (evaluates f(x)).

        @param x: an (N, in_size) torch tensor

        @return y: an (N, out_size) torch tensor of output from the network
        """
        output = self.fc(x)
        return output
        #return torch.ones(x.shape[0], 1)

    def step(self, x,y):
        """
        Performs one gradient step through a batch of data x with labels y
        @param x: an (N, in_size) torch tensor
        @param y: an (N,) torch tensor
        @return L: total empirical risk (mean of losses) at this time step as a float
        """
        result = self.forward(x)
        optimizer = torch.optim.SGD(self.parameters(), lr=self.lrate)
        optimizer.zero_grad()
        loss = self.loss_fn(result.squeeze(), y)
        loss.backward()
        optimizer.step()
        # return loss.detach().cpu().numpy()
        return loss.item()



def fit(train_set,train_labels,dev_set,n_iter,batch_size=100):
    """ Make NeuralNet object 'net' and use net.step() to train a neural net
    and net(x) to evaluate the neural net.

    @param train_set: an (N, in_size) torch tensor
    @param train_labels: an (N,) torch tensor
    @param dev_set: an (M,) torch tensor
    @param n_iter: int, the number of iterations of training
    @param batch_size: The size of each batch to train on. (default 100)

    # return all of these:

    @return losses: Array of total loss at the beginning and after each iteration. Ensure len(losses) == n_iter
    @return yhats: an (M,) NumPy array of binary labels for dev_set
    @return net: A NeuralNet object

    # NOTE: This must work for arbitrary M and N
    """
    model = NeuralNet(0.05, torch.nn.CrossEntropyLoss(), 3072, 2)
    losses = []
    yhats = []
    index = 0
    # pdb.set_trace()
    means = train_set.mean(dim=0, keepdim=True)
    std = train_set.std(dim=0, keepdim=True)
    standardize = (train_set - means) / std
    for i in range(n_iter):
        if index >= len(train_labels):
            index = 0
        temp2 = model.step(standardize[index:index+batch_size], train_labels[index:index+batch_size])
        losses.append(temp2)
        index += batch_size
    eval = model.forward(dev_set)
    # eval = torch.nn.Sigmoid(eval)
    #pdb.set_trace()
    for item in eval:
        yhats.append(torch.argmax(item))
    return losses, yhats, model
