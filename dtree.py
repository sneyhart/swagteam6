'''
dtree.py
decision tree classifier
has 9 nodes to check for each possible hand
'''
#file IO
import numpy as np
testing_lines = [np.array((file_line.rstrip('\n').split(','))).astype(int) for file_line in open('poker-hand-testing-small.data')]
testing_lines = np.array(testing_lines)
tests = np.delete(testing_lines.T, testing_lines.T.shape[0] - 1,0).T
actual_classes = testing_lines.T[-1]

#initialize
corrects = 0.0
total = 0.0

#each testing
for t,test in enumerate(tests):
    #get info sorted into suits and ranks
    total = total + 1
    ranks = []
    suits = []
    for i in range(0,10,2):
        suits.append(test[i])
        ranks.append(test[i+1]) 
    matches = [0]
    idx = np.argsort(ranks, axis=0)
    ranks = np.array(ranks)[idx]
    suits = np.array(suits)[idx]
    ranks = ranks.tolist()
    suits = suits.tolist()

    #is pair?
    ph = 0
    for val in ranks:
        if ranks.count(val) == 2:
            ph = 1
    if ph == 1:
        matches.append(1) 
    
    #is two pair?
    ph = 0
    first = 0
    for val in ranks:
        if ranks.count(val) == 2:
            if first == 0:
                first = val
            elif first != val:
                ph = 1
    if ph == 1:
        matches.append(2)
        
    #is three of a kind?
    ph = 0
    for val in ranks:
        if ranks.count(val) == 3:
            ph = 1
    if ph == 1:
        matches.append(3)

    #is straight?
    ph = 1
    if ranks.count(1) == 1 and ranks[-1] == 13: 
        for i,val in enumerate(ranks):
            if i != 0 and i != 1:
                if ranks[i] - ranks[i - 1] != 1:
                    ph = 0 
    else: 
        for i,val in enumerate(ranks):
            if i != 0:
                if ranks[i] - ranks[(i - 1)] != 1:
                    ph = 0 
    if ph == 1:
        matches.append(4)
                

    #is flush?
    if suits.count(suits[0]) == 5:
        matches.append(5)
    
    #is full house?
    if 1 in matches and 3 in matches:
        matches.append(6)

    #is four of a kind?
    ph = 0
    for val in ranks:
        if ranks.count(val) == 4:
            ph = 1
    if ph == 1: 
        matches.append(7)

    #is straight flush?
    if 4 in matches and 5 in matches:
        matches.append(8)

    #is royal flush?
    if 8 in matches and ranks[0] == 1 and ranks[-1] == 13:
        matches.append(9)

    #checking result
    result = matches[-1]
    if result == actual_classes[t]:
        corrects = corrects + 1
print "Accuracy {}".format(corrects/total)
