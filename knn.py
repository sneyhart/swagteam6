import numpy as np
from scipy import spatial as sp

#Preprocessing
lines = []
tlines = []
data = []
groups = []
classes = []
dtp = []
knn_res = []
corrects = [0] * 20
#file IO

lines = [np.array((file_line.rstrip('\n').split(','))).astype(float) for file_line in open('poker-hand-training-true.data')]
lines = np.array(lines)
training = np.delete(lines.T, lines.T.shape[0] - 1,0).T
res = lines.T[-1]

testing_lines = [np.array((file_line.rstrip('\n').split(','))).astype(float) for file_line in open('poker-hand-testing-smaller.data')]
testing_lines = np.array(testing_lines)
tests = np.delete(testing_lines.T, testing_lines.T.shape[0] - 1,0).T
actual_classes = testing_lines.T[-1]

 
#testing each unit in the testing set 
fusout = open("fusion-files-majority/knn_un.data",'w')
for u,unit in enumerate(tests):
    if u % 150 == 0:
        print "{}%".format(u/150*10)
    dis = []
    cords = unit
    actual = actual_classes[u]
    for point in training:
        dis.append(np.linalg.norm(point - cords))
    idx = np.argsort(dis, axis=0)
    dis = np.array(dis)[idx]
    results = np.array(res)[idx]
    counts = [0,0,0,0,0,0,0,0,0,0]  
   
#going through each k value after each distance is calculated 
    for k in range(1,20):
        mmax = -1
        mindex = -1
        counts[int(results[k-1])] = counts[int(results[k-1])] + 1
 
        for ind,count in enumerate(counts):
            if mmax < count:
                mmax = count
                mindex = ind             
        if k == 17:
            fusout.write("{}\n".format(mindex))
        if(actual == mindex):
            corrects[k] += 1
# counting the correct guesses per each k value
corrects = [(correct * 1.0)/len(tests) for correct in corrects]
knn_res.append(corrects)
knn_res_tp = np.transpose(knn_res)
knn_res_tp = [np.mean(col) for col in knn_res_tp]
knn_res = np.transpose(knn_res_tp)
#print out the results for each k value up to the max k value
for i, k in enumerate(knn_res):
    print "{},{}".format(i, k)
   
