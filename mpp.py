##################
# Jon Clark Freeman
# plotter.py - plots the synth.tr and plots the decision rules after training 
#################

import matplotlib.pyplot as plt
import numpy as np
import re

#function that returns the likelihood for a given [x, y], mean, and covariance matrix
def cmv(x, y, mean, cov):
    pre_top = 1;
    pre_bottom = (2 * np.pi) * np.sqrt(np.linalg.det(cov))
    post_matrix_mult = np.dot(np.dot(np.transpose(np.subtract(np.array([x,y]), mean)), np.linalg.inv(cov)), np.subtract(np.array([x,y]), mean))
    post_scalar = -1.0/2.0
    return (pre_top/pre_bottom) * np.exp(post_scalar * post_matrix_mult)

#function that returns Case 1 Discriminant
def case_1(x, y, mean, prior):
    return -np.dot(np.subtract(np.array([x,y]), mean),np.transpose(np.subtract(np.array([x,y]), mean))) + np.log(prior)

#function that returns Case 2 Discriminant
def case_2(x, y, mean, cov, prior):
    return -np.dot(np.dot(np.transpose(np.subtract(np.array([x,y]), mean)), np.linalg.inv(cov)), np.subtract(np.array([x,y]), mean)) + np.log(prior)

#function that returns Case 3 Discriminant
def case_3(x, y, mean, cov, prior):
    first = np.dot(np.dot(np.transpose(np.array([x,y])), np.divide(np.linalg.inv(cov), -2)), np.array([x,y]))
    second = np.dot(np.transpose(np.dot(np.linalg.inv(cov), mean)), np.array([x,y]))
    third = (np.dot(np.dot(np.transpose(mean), np.linalg.inv(cov)),mean)/-2.0) + (np.log(np.linalg.det(cov))/-2.0)
    return first + second + third + np.log(prior)

#prior variables to test the different prior probabilities
priors = [0.501177,0.422569,0.047539,0.021128,0.003925,0.001965,0.001441,0.000240,0.0000139,0.00000154]
classes = [[] for i in range(0,10)]

# Handle file manipulation
lines = [np.array((file_line.rstrip('\n').split(','))).astype(int) for file_line in open('poker-hand-training-true.data')]
lines = np.array(lines)
for line in lines:
    classes[line[-1]].append(np.delete(line,(line.shape[0]-1),0))
classes = [np.array(classer) for classer in classes]
means = [np.mean(row) for row in classes]
covariance = np.cov(classes)
print covariance


'''
# getting the points seperated into x and y values for plotting purposes
x_list_zero = []
y_list_zero = []
x_list_one = []
y_list_one = []

# determining the values for the mean of class zero

sum_x = 0
sum_y = 0
for point in class_zero:
    x_list_zero.append(point[0])
    y_list_zero.append(point[1])
    sum_x += point[0]
    sum_y += point[1]

mean_zero = [sum_x/len(class_zero),sum_y/len(class_zero)]


#determining the covariance matrix for class zero
i = 0;
for point in class_zero: 
    if i == 0:
        sum_matrix = np.add(0, np.outer(np.subtract(point, mean_zero), np.transpose(np.subtract(point, mean_zero))))
    else:
        sum_matrix = np.add(sum_matrix, np.outer(np.subtract(point, mean_zero), np.transpose(np.subtract(point, mean_zero))))
    i += 1
sum_matrix = np.divide(sum_matrix, len(class_zero))
cov_zero = sum_matrix


#determining the mean values for class one
sum_x = 0
sum_y = 0
for point in class_one:
    x_list_one.append(point[0])
    y_list_one.append(point[1])
    sum_x += point[0]
    sum_y += point[1]

mean_one = [sum_x/len(class_zero),sum_y/len(class_zero)]
print mean_one

#determing the covariance matrix for class one
i = 0;
for point in class_one:
    if i == 0:
        sum_matrix = np.add(0, np.outer(np.subtract(point, mean_one), np.transpose(np.subtract(point, mean_one))))
    else:
        sum_matrix = np.add(sum_matrix, np.outer(np.subtract(point, mean_one), np.transpose(np.subtract(point, mean_one))))
    i += 1
sum_matrix = np.divide(sum_matrix, len(class_one))
cov_one = sum_matrix
print cov_one

#open testing input
lines = [file_line.rstrip('\n') for file_line in open('synth.te')]

#initialize lists for accuracy stats
class_zero_guessed = []
class_one_guessed = []
x_list_zero = []
y_list_zero = []
x_list_one = []
y_list_one = []
x_list_wrongly_zero = []
y_list_wrongly_zero = []
x_list_wrongly_one = []
y_list_wrongly_one = []

x_list_decision_line = []
y_list_decision_line = []

#estimated plot of the decision boundary for likelihood ratio
i = -1.5
while i < 1.5:
    j = -1.5
    while j < 1.5:
        difference = cmv(i, j, mean_zero, cov_zero)/cmv(i, j, mean_one, cov_one) - (prior_one/prior_zero)
        if(abs(difference) < .08):
            x_list_decision_line.append(i)
            y_list_decision_line.append(j)
        j += .01
    i += .01

#make decisions on the input and sort into lists for statistic and plotting purposes
for line in lines:
    if line.find('xs') == -1:
        strings = re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", line)
        nums = [float(strings[0]), float(strings[1]), int(strings[2])]
        if(cmv(nums[0], nums[1], mean_zero, cov_zero)/cmv(nums[0], nums[1], mean_one, cov_one) > (prior_one/prior_zero)):
            class_zero_guessed.append(np.array(nums))
            if(nums[2] == 1):
                x_list_wrongly_zero.append(nums[0])
                y_list_wrongly_zero.append(nums[1])
            else:
                x_list_zero.append(nums[0])
                y_list_zero.append(nums[1])
        else:
            class_one_guessed.append(np.array(nums))
            if(nums[2] == 1):
                x_list_one.append(nums[0])
                y_list_one.append(nums[1])
            else:
                x_list_wrongly_one.append(nums[0])
                y_list_wrongly_one.append(nums[1])

#print out accuracy stats
num_right_zero = 0
for guess in class_zero_guessed:
    if(guess[2] == 0):
        num_right_zero += 1
print "______________1st Part of Proj 1 (Likelihood Ratio)______________________"
print "--------Class Zero Accuracy--------"
print float(num_right_zero)/float(len(class_zero_guessed))
print "\n"
print "--------Class One Accuracy---------"
num_right_one = 0
for guess in class_one_guessed:
    if(guess[2] == 1):
        num_right_one += 1

print float(num_right_one)/float(len(class_one_guessed))
print"\n -----------Total Accuracy----------"
print float(num_right_one + num_right_zero)/1000.0
print "\n_______________2nd Part of Proj 1 (Case 1 Discriminant)__________________"

# re-initialize for next decision rule
class_zero_guessed = []
class_one_guessed = []
x_list_zero = []
y_list_zero = []
x_list_one = []
y_list_one = []
x_list_wrongly_zero = []
y_list_wrongly_zero = []
x_list_wrongly_one = []
y_list_wrongly_one = []

#make decisions with first discriminant case
for line in lines:
    if line.find('xs') == -1:
        strings = re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", line)
        nums = [float(strings[0]), float(strings[1]), int(strings[2])]
        if(case_1(nums[0], nums[1], mean_zero, prior_zero) > case_1(nums[0], nums[1], mean_one, prior_one)):
            class_zero_guessed.append(np.array(nums))
            if(nums[2] == 1):
                x_list_wrongly_zero.append(nums[0])
                y_list_wrongly_zero.append(nums[1])
            else:
                x_list_zero.append(nums[0])
                y_list_zero.append(nums[1])
        else:
            class_one_guessed.append(np.array(nums))
            if(nums[2] == 1):
                x_list_one.append(nums[0])
                y_list_one.append(nums[1])
            else:
                x_list_wrongly_one.append(nums[0])
                y_list_wrongly_one.append(nums[1])
num_right_zero = 0
for guess in class_zero_guessed:
    if(guess[2] == 0):
        num_right_zero += 1


# plot the decision boundary
x_list_decision_line_g0 = []
y_list_decision_line_g0 = []

i = -1.5
while i < 1.5:
    j = -1.5
    while j < 1.5:
        difference = case_1(i, j, mean_zero, prior_zero) - case_1(i, j, mean_one, prior_one)
        if(abs(difference) < 0.008):
            x_list_decision_line_g0.append(i)
            y_list_decision_line_g0.append(j)
        j += .01
    i += .01

#output stats for the accuracy
print "--------Class Zero Accuracy--------"
print float(num_right_zero)/float(len(class_zero_guessed))
print "\n"
print "--------Class One Accuracy---------"
num_right_one = 0
for guess in class_one_guessed:
    if(guess[2] == 1):
        num_right_one += 1

print float(num_right_one)/float(len(class_one_guessed))
print"\n -----------Total Accuracy----------"
print float(num_right_one + num_right_zero)/1000.0

#initialize lists for the 2nd case of the discriminant
print "\n_______________2nd Part of Proj 1 (Case 2 Discriminant)__________________"
class_zero_guessed = []
class_one_guessed = []
x_list_zero = []
y_list_zero = []
x_list_one = []
y_list_one = []
x_list_wrongly_zero = []
y_list_wrongly_zero = []
x_list_wrongly_one = []
y_list_wrongly_one = []

#decisions
for line in lines:
    if line.find('xs') == -1:
        strings = re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", line)
        nums = [float(strings[0]), float(strings[1]), int(strings[2])]
        if(case_2(nums[0], nums[1], mean_zero, np.divide(np.add(cov_zero, cov_one), 2), prior_zero) > case_2(nums[0], nums[1], mean_one, np.divide(np.add(cov_zero, cov_one), 2), prior_one)):
            class_zero_guessed.append(np.array(nums))
            if(nums[2] == 1):
                x_list_wrongly_zero.append(nums[0])
                y_list_wrongly_zero.append(nums[1])
            else:
                x_list_zero.append(nums[0])
                y_list_zero.append(nums[1])
        else:
            class_one_guessed.append(np.array(nums))
            if(nums[2] == 1):
                x_list_one.append(nums[0])
                y_list_one.append(nums[1])
            else:
                x_list_wrongly_one.append(nums[0])
                y_list_wrongly_one.append(nums[1])
num_right_zero = 0
for guess in class_zero_guessed:
    if(guess[2] == 0):
        num_right_zero += 1


x_list_decision_line_g1 = []
y_list_decision_line_g1 = []


# plot decision boundary
i = -1.5
while i < 1.5:
    j = -1.5
    while j < 1.5:
        difference = case_2(i, j, mean_zero, np.divide(np.add(cov_zero, cov_one), 2), prior_zero) - case_2(i, j, mean_one, np.divide(np.add(cov_zero, cov_one), 2), prior_one)
        if(abs(difference) < .1):
            x_list_decision_line_g1.append(i)
            y_list_decision_line_g1.append(j)
        j += .01
    i += .01

# statistics
print "--------Class Zero Accuracy--------"
print float(num_right_zero)/float(len(class_zero_guessed))
print "\n"
print "--------Class One Accuracy---------"
num_right_one = 0
for guess in class_one_guessed:
    if(guess[2] == 1):
        num_right_one += 1

print float(num_right_one)/float(len(class_one_guessed))
print"\n -----------Total Accuracy----------"
print float(num_right_one + num_right_zero)/1000.0


#initialize lists for the 3rd case of the discriminant
print "\n_______________2nd Part of Proj 1 (Case 3 Discriminant)__________________"
class_zero_guessed = []
class_one_guessed = []
x_list_zero = []
y_list_zero = []
x_list_one = []
y_list_one = []
x_list_wrongly_zero = []
y_list_wrongly_zero = []
x_list_wrongly_one = []
y_list_wrongly_one = []

#decisions
for line in lines:
    if line.find('xs') == -1:
        strings = re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", line)
        nums = [float(strings[0]), float(strings[1]), int(strings[2])]
        if(case_3(nums[0], nums[1], mean_zero, cov_zero, prior_zero) > case_3(nums[0], nums[1], mean_one, cov_one, prior_one)):
            class_zero_guessed.append(np.array(nums))
            if(nums[2] == 1):
                x_list_wrongly_zero.append(nums[0])
                y_list_wrongly_zero.append(nums[1])
            else:
                x_list_zero.append(nums[0])
                y_list_zero.append(nums[1])
        else:
            class_one_guessed.append(np.array(nums))
            if(nums[2] == 1):
                x_list_one.append(nums[0])
                y_list_one.append(nums[1])
            else:
                x_list_wrongly_one.append(nums[0])
                y_list_wrongly_one.append(nums[1])
num_right_zero = 0
for guess in class_zero_guessed:
    if(guess[2] == 0):
        num_right_zero += 1


x_list_decision_line_g2 = []
y_list_decision_line_g2 = []

#estimated plot of the decision boundary for likelihood ratio
i = -1.5
while i < 1.5:
    j = -1.5
    while j < 1.5:
        difference = case_3(i, j, mean_zero, cov_zero, prior_zero) - case_3(i, j, mean_one, cov_one, prior_one)
        if(abs(difference) < .08):
            x_list_decision_line_g2.append(i)
            y_list_decision_line_g2.append(j)
        j += .01
    i += .01

# statistics
print "--------Class Zero Accuracy--------"
print float(num_right_zero)/float(len(class_zero_guessed))
print "\n"
print "--------Class One Accuracy---------"
num_right_one = 0
for guess in class_one_guessed:
    if(guess[2] == 1):
        num_right_one += 1

print float(num_right_one)/float(len(class_one_guessed))
print"\n -----------Total Accuracy----------"
print float(num_right_one + num_right_zero)/1000.0

# plot everything
plt.plot(x_list_zero, y_list_zero, 'bs', x_list_one, y_list_one, 'rs', x_list_wrongly_zero, y_list_wrongly_zero, 'rx', x_list_wrongly_one, y_list_wrongly_one, 'bx', x_list_decision_line, y_list_decision_line, 'gs', x_list_decision_line_g0, y_list_decision_line_g0, 'yd', x_list_decision_line_g1, y_list_decision_line_g1, 'ks', x_list_decision_line_g2, y_list_decision_line_g2, 'ms')
plt.axis('equal')
plt.show()
'''
