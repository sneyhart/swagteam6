# Normalizaiton
# Input/Output file names defined in main funciton
# Running simply normalizes data and writes to output file
# Handy data separation techniques used

import math
import numpy as np
from numpy import linalg as LA

DEBUG = 0

def getInputSeparated(fname):
	#fname = 'poker-hand-training-true.data'
	file = open(fname, 'r')				# read file
	#with open(fname) as f:
		#lines = f.read().splitlines
	lines = file.readlines()
	file.close()
	classData = []
	class0Data = []					# can probably do this more intellignetly
	class1Data = []
	class2Data = []
	class3Data = []
	class4Data = []
	class5Data = []
	class6Data = []
	class7Data = []
	class8Data = []
	class9Data = []
	for line in lines: 					# read elements up to class
		line = line.strip()
		splitLine = line.split(',')
		classIndex = len(splitLine)-1	# max index of splitLine
		#print splitLine
		#print 'Class Index: {}'.format(classIndex)
		#print splitLine[classIndex]
		sampleData = []
		#sampleData.append(int(splitLine[:lenIndexSplitLine]))
		for j in range(classIndex):
			#print j
			sampleData.append(float(splitLine[j]))
		# Separate by classes
		if (splitLine[classIndex] == '0'):
			#print 'appending 0'
			class0Data.append(sampleData)
		elif(splitLine[classIndex] == '1'):
			class1Data.append(sampleData)
		elif(splitLine[classIndex] == '2'):
			class2Data.append(sampleData)
		elif(splitLine[classIndex] == '3'):
			class3Data.append(sampleData)
		elif(splitLine[classIndex] == '4'):
			class4Data.append(sampleData)
		elif(splitLine[classIndex] == '5'):
			class5Data.append(sampleData)
		elif(splitLine[classIndex] == '6'):
			class6Data.append(sampleData)
		elif(splitLine[classIndex] == '7'):
			class7Data.append(sampleData)
		elif(splitLine[classIndex] == '8'):
			class8Data.append(sampleData)
		elif(splitLine[classIndex] == '9'):
			class9Data.append(sampleData)
	classData.append(np.asarray(class0Data))
	classData.append(np.asarray(class1Data))
	classData.append(np.asarray(class2Data))
	classData.append(np.asarray(class3Data))
	classData.append(np.asarray(class4Data))
	classData.append(np.asarray(class5Data))
	classData.append(np.asarray(class6Data))
	classData.append(np.asarray(class7Data))
	classData.append(np.asarray(class8Data))
	classData.append(np.asarray(class9Data))
	return np.asarray(classData)

def test_getInputSeparated():
	print 'Entered test_getInputSeparated()'
	classData = getInputSeparated('poker-hand-training-true.txt')
	i = -1
	for classSamples in classData:
		i += 1
		print 'Class {} data:'.format(i)
		for classSample in classSamples:
			print classSample

def test_getInputSeparated2():
	print 'Entered test_getInputSeparated2()'
	classData = getInputSeparated('poker-hand-training-true.txt')
	print classData

def weave(classData):
	weaved = []
	largestClassSampCount = 0
	# find the length of the longest list (the number of samples in the largest class)
	for classSamples in classData:
		numClassSamples = len(classSamples)
		if numClassSamples > largestClassSampCount:
			largestClassSampCount = numClassSamples
	# weave samples across all classes
	# Kevin - I can explain this, just ask me
	for i in range(largestClassSampCount):
		for classSamples in classData:
			if (i < len(classSamples)):
				weaved.append(classSamples[i])
	return weaved

def test_weave():
	fName_tr = 'poker-hand-training-true.data'
	# Get training data
	X0 = getInputSeparated(fName_tr)
	X = weave(X0)
	for samp in X:
		print samp

def getColumnMeans(X):
	return np.mean(X, axis=0)

def getColumnStddevs(X):
	return np.std(X, axis=0)

def getColMeansSeparated(_XS):
	colMeansSep = []
	for classSamples in _XS:
		colMeansSep.append(getColumnMeans(classSamples))
	return np.asarray(colMeansSep)

def getColumnStddevsSeparated(_XS):
	colMeansSep = []
	for classSamples in _XS:
		colMeansSep.append(getColumnStddevs(classSamples))
	return np.asarray(colMeansSep)

def normalize(X, colMeans, colStddevs):
	nX = []
	for sample in X:
		nRow = sample
		for i in range(len(nRow)):
			nRow[i] = (sample[i] - colMeans[i])/colStddevs[i]	# normalize
		nX.append(nRow)
	return np.asarray(nX)

def normalizeSep(XS, colMeans_all_tr, colStddevs_all_tr):
	nXS = []
	for classSamples in XS:
		nXClass = normalize(classSamples, colMeans_all_tr, colStddevs_all_tr)
		nXS.append(nXClass)
	return np.asarray(nXS)

def rebuild(nXS, fname):
	nOriginalData = open(fname, 'w')
	i = -1
	for nClassSamples in nXS:
		i += 1
		for nSamp in nClassSamples:
			nSampString = ''
			for feature in nSamp:
				nSampString += str(feature) + ', '
			nSampString += str(i) + '\n'
			nOriginalData.write(nSampString)
			#print nSampString
	nOriginalData.close()

def main():
	if DEBUG: print 'Entered main()'
	fName_IN = 'poker-hand-training-true.data'
	fName_OUT = 'poker-hand-training-true-normalized.data'

	# 'X' denotes original dataset
	# 'XS' denotes original dataset separated by class (hand type)
	XS = getInputSeparated(fName_IN)
	#if DEBUG: print 'XS: \n{}'.format(XS)
	X = weave(XS)

	if DEBUG: print 'X:\n{}\n\n\n'.format(X)
	if DEBUG: print 'XS:\n{}\n\n\n'.format(XS)


	# Compute un-normalized training mu & sigma for normalization
	colMeans_all_tr = getColumnMeans(X)
	colStddevs_all_tr = getColumnStddevs(X)

	# 'nX' denotes original dataset - normalized
	# 'nXS' denotes original dataset, separated - normalized
	nXS = normalizeSep(XS, colMeans_all_tr, colStddevs_all_tr)
	nX = weave(nXS)					# nX is both classes combined

	if DEBUG: print 'nX:\n{}\n\n\n'.format(nX)
	#if DEBUG:
	print 'nXS:\n{}'.format(nXS)

	rebuild(nXS, fName_OUT)


main()


