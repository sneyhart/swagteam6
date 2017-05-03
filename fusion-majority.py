import numpy as np

#get priors to break ties
priors = [0.501177,0.422569,0.047539,0.021128,0.003925,0.001965,0.001441,0.000240,0.0000139,0.00000154]

#get the correct classes for accuracy
testing_lines = [np.array((file_line.rstrip('\n').split(','))).astype(int) for file_line in open('poker-hand-testing-smaller.data')]
testing_lines = np.array(testing_lines)
tests = np.delete(testing_lines.T, testing_lines.T.shape[0] - 1,0).T
actual_classes = testing_lines.T[-1]

#input all of the classifications
mpp_res = [int(file_line.rstrip('\n')) for file_line in open('fusion-files-majority/mpp.data')]
knn_res = [int(file_line.rstrip('\n')) for file_line in open('fusion-files-majority/knn.data')]
bpnn_res = [int(file_line.rstrip('\n')) for file_line in open('fusion-files-majority/bpnn.data')]

#compare votes and pick the one with the majority
corrects = 0.0
for i in range(0,len(mpp_res)):
    choices = [0] * 10
    vals = [j for j in range(0,10)]
    choices[mpp_res[i]] = choices[mpp_res[i]] + 1
    choices[knn_res[i]] = choices[knn_res[i]] + 1
    choices[bpnn_res[i]] = choices[bpnn_res[i]] + 1
    idx = np.argsort(choices, axis=0)
    choices = np.array(choices)[idx]
    vals = np.array(vals)[idx]
    result = 0
    choices = choices[::-1]
    vals = vals[::-1]
    #if there is a tie the one with the most prior probability wins
    if choices[0] == 1:
        result = min(vals[0:3])
    else:
        result = vals[0] 
    if result == actual_classes[i]:
        corrects = corrects + 1
print "Accuracy - {}".format(corrects/len(mpp_res))
