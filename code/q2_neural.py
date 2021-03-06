import numpy as np
import random

from q1_softmax import softmax
from q2_sigmoid import sigmoid, sigmoid_grad
from q2_gradcheck import gradcheck_naive

def forward_backward_prop(data, labels, params, dimensions):
    """ 
    Forward and backward propagation for a two-layer sigmoidal network 
    
    Compute the forward propagation and for the cross entropy cost,
    and backward propagation for the gradients for all parameters.
    """

    ### Unpack network parameters (do not modify)
    ofs = 0
    Dx, H, Dy = (dimensions[0], dimensions[1], dimensions[2]) # (10,5,10)

    W1 = np.reshape(params[ofs:ofs+ Dx * H], (Dx, H))
    ofs += Dx * H
    b1 = np.reshape(params[ofs:ofs + H], (1, H))
    ofs += H
    W2 = np.reshape(params[ofs:ofs + H * Dy], (H, Dy))
    ofs += H * Dy
    b2 = np.reshape(params[ofs:ofs + Dy], (1, Dy))

    N = data.shape[0]
    ### YOUR CODE HERE: forward propagation data:20*10,w1: 10*5,b1:1*5 w2:5*10,b2:1*10
    h = sigmoid(np.mat(np.dot(data,W1) + b1)) # 20*5
    y = softmax(np.mat(np.dot(h,W2) + b2)) # 20*10
    cost = -np.sum(np.log(y[labels==1]))/N
    ### END YOUR CODE
    
    ### YOUR CODE HERE: backward propagation
    d1 = y-labels # 20*10
    gradW2 = np.dot(h.T,d1)/N # 5*20 * 20*10 ->5*10
    gradb2 = np.sum(d1,axis=0)/N # 1*10
    grad_h = np.multiply(np.dot(d1,W2.T),sigmoid_grad(h)) # 20*10 10*5 20*5->20*5
    gradW1 = np.dot(data.T,grad_h)/N # 10*20 20*5-> 10*5
    gradb1 = np.sum(grad_h,axis=0)/N # 20*10 10*5 -> 1*5

    ### END YOUR CODE
    
    ### Stack gradients (do not modify)
    grad = np.concatenate((np.array(gradW1).flatten(), np.array(gradb1).flatten(),
                           np.array(gradW2).flatten(), np.array(gradb2).flatten()))
    
    return cost, grad

def sanity_check():
    """
    Set up fake data and parameters for the neural network, and test using 
    gradcheck.
    """
    print "Running sanity check..."

    N = 20
    dimensions = [10, 5, 10]
    data = np.random.randn(N, dimensions[0])   # 20*10
    labels = np.zeros((N, dimensions[2])) # 20*10
    for i in xrange(N):
        labels[i,random.randint(0,dimensions[2]-1)] = 1
    
    params = np.random.randn((dimensions[0] + 1) * dimensions[1] + (
        dimensions[1] + 1) * dimensions[2], ) # 115*1,number of parameters
    #
    # forward_backward_prop(data, labels, params,dimensions)
    #

    gradcheck_naive(lambda params: forward_backward_prop(data, labels, params,
        dimensions), params)

def your_sanity_checks(): 
    """
    Use this space add any additional sanity checks by running:
        python q2_neural.py 
    This function will not be called by the autograder, nor will
    your additional tests be graded.
    """
    print "Running your sanity checks..."
    ### YOUR CODE HERE
    raise NotImplementedError
    ### END YOUR CODE

if __name__ == "__main__":
    sanity_check()
    # your_sanity_checks()