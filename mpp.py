##################
# Jon Clark Freeman, Sam Neyhart, Kevin Sayarath
# mpp.py classifies using the three cases of mpp
#################

import matplotlib.pyplot as plt
import numpy as np

#function that returns the likelihood for a given [x, y], mean, and covariance matrix
def cmv(x, y, mean, cov):
    pre_top = 1;
    pre_bottom = (2 * np.pi) * np.sqrt(np.linalg.det(cov))
    post_matrix_mult = np.dot(np.dot(np.transpose(np.subtract(np.array([x,y]), mean)), np.linalg.inv(cov)), np.subtract(np.array([x,y]), mean))
    post_scalar = -1.0/2.0
    return (pre_top/pre_bottom) * np.exp(post_scalar * post_matrix_mult)

#function that returns Case 1 Discriminant
def case_1(x, mean, prior):
    return -np.dot(np.subtract(np.array(x), mean),np.transpose(np.subtract(np.array(x), mean))) + np.log(prior)

#function that returns Case 2 Discriminant
def case_2(x, mean, cov, prior):
    return -np.dot(np.dot(np.transpose(np.subtract(np.array(x), mean)), np.linalg.inv(cov)), np.subtract(np.array(x), mean)) + np.log(prior)

#function that returns Case 3 Discriminant
def case_3(x, mean, cov, prior):
    first = np.dot(np.dot(np.transpose(np.array(x)), np.divide(np.linalg.inv(cov), -2)), np.array(x))
    second = np.dot(np.transpose(np.dot(np.linalg.inv(cov), mean)), np.array(x))
    third = (np.dot(np.dot(np.transpose(mean), np.linalg.inv(cov)),mean)/-2.0) + (np.log(np.linalg.det(cov))/-2.0)
    return first + second + third + np.log(prior)

#initialization of priors and glasses
priors = [0.501177,0.422569,0.047539,0.021128,0.003925,0.001965,0.001441,0.000240,0.0000139,0.00000154]
classes = [[] for i in range(0,10)]

# Handle file manipulation
lines = [np.array((file_line.rstrip('\n').split(','))).astype(int) for file_line in open('poker-hand-training-true.data')]
lines = np.array(lines)

#handle getting covariance matrix and means
cov_lines = np.delete(lines.T, lines.T.shape[0] - 1,0)
for line in lines:
    classes[line[-1]].append(np.delete(line,(line.shape[0]-1),0))
classes = np.array([np.array(classer) for classer in classes])
means = [np.mean(row) for row in classes]
covariance = np.cov(cov_lines)

testing_lines = [np.array((file_line.rstrip('\n').split(','))).astype(int) for file_line in open('poker-hand-testing.data')]
testing_lines = np.array(testing_lines)
tests = np.delete(testing_lines.T, testing_lines.T.shape[0] - 1,0).T
actual_classes = testing_lines.T[-1]

choices = []

for t,test in enumerate(tests):
    max_disc = -1
    if t % 50000 == 0:
        print "{}%".format(((t * 1.0)/10000))
    max_val = -1000000
    for i in range(0,10):
        res = case_2(test, means[i],covariance,priors[i])
        if res > max_val:
            max_disc = i
            max_val = res
    choices.append(max_disc)

corrects = 0
total = 0
for i in range(0, len(choices)):
    if choices[i] == actual_classes[i]:
        corrects = corrects + 1
    total = total + 1
print "Case 2 - {}".format((corrects * 1.0)/total)
