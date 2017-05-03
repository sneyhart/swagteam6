import numpy as np
lines = [np.array((file_line.rstrip('\n').split(','))).astype(float) for file_line in open('poker-hand-training-true-normalized.data')]
lines = np.array(lines)
training = np.delete(lines.T, lines.T.shape[0] - 1,0).T
res = lines.T[-1]

testing_lines = [np.array((file_line.rstrip('\n').split(','))).astype(float) for file_line in open('poker-hand-testing-smaller-normalized.data')]
testing_lines = np.array(testing_lines)
tests = np.delete(testing_lines.T, testing_lines.T.shape[0] - 1,0).T
actual_classes = testing_lines.T[-1]

cov_train = np.cov(training.T)
cov_test = np.cov(tests.T)

eigenValsTe, eigenVecsTe = np.linalg.eig(cov_test)
eigenValsTr, eigenVecsTr = np.linalg.eig(cov_train)

#sort EigenValues and EigenVecs
idx = eigenValsTe.argsort()[::-1]
eigenValsTe = eigenValsTe[idx]
eigenVecsTe = eigenVecsTe[:,idx]

idxx = eigenValsTr.argsort()[::-1]
egeinValsTr = eigenValsTr[idxx]
eigenVecsTr = eigenVecsTr[:,idxx]

majorTest = [eigenVecsTe[0],eigenVecsTe[1],eigenVecsTe[2]]
majorTrain = [eigenVecsTr[0],eigenVecsTr[1],eigenVecsTr[2]]

minTest = np.dot(tests, np.transpose(majorTest))
minTrain = np.dot(training, np.transpose(majorTrain))

tp = minTest.T.tolist()
tp.append(actual_classes)
tp = np.array(tp)
minTest = tp.T

tp = minTrain.T.tolist()
tp.append(res)
tp = np.array(tp)
minTrain = tp.T

testOut = open('pca_norm_testing.data','w')
trainOut = open('pca_norm_training.data','w')

for line in minTest:
    for i,piece in enumerate(line):
        if i == 0:
            testOut.write("{}".format(piece))
        else:
            testOut.write(",{}".format(piece))
    testOut.write("\n")

for line in minTrain:
    for i,piece in enumerate(line):
        if i == 0:
            trainOut.write("{}".format(piece))
        else:
            trainOut.write(",{}".format(piece))
    trainOut.write("\n")
