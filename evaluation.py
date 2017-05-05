# Normalizaiton
# Input/Output file names defined in main funciton
# Running simply normalizes data and writes to output file
# Handy data separation techniques used

import math
import random
import numpy as np
from numpy import linalg as LA
from subprocess import call

DEBUG = 0
CLASSINDEX = 10			# zero-indexed

def getInputSeparated(fname):
	#fname = 'poker-hand-training-true.data'
	file = open(fname, 'r')				# read file
	#with open(fname) as f:
		#lines = f.read().splitlines
	lines = file.readlines()
	file.close()
	classData = []
	class0Data = []						# can probably do this more intellignetly
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
	nTotal = 0
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

# aggregates a 2-D array into a single numpy array
def weave(classData, classification=0):
	weaved = []
	largestClassSampCount = 0
	# find the length of the longest list (the number of samples in the largest class)
	for classSamples in classData:
		numClassSamples = len(classSamples)
		if numClassSamples > largestClassSampCount:
			largestClassSampCount = numClassSamples
	# weave samples across all classes
	# Kevin - I can explain this, just ask me
	c = 0
	samp = []
	for i in range(largestClassSampCount):
		c = -1
		for j in range(len(classData)):
			c += 1
			classSamples = classData[j]
			if (i < len(classSamples)):
				samp = []
				for feature in classSamples[i]:
					samp.append(feature)
				if (classification): samp.append(c)
				weaved.append(samp)
	return np.asarray(weaved)

def test_weave():
	fName_tr = 'poker-hand-training-true.data'
	# Get training data
	X0 = getInputSeparated(fName_tr)
	X = weave(X0, 1)
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

# Normalize the given dataset
def normalize(X, colMeans, colStddevs):
	nX = []
	for sample in X:
		nRow = sample
		for i in range(len(nRow)):
			nRow[i] = (sample[i] - colMeans[i])/colStddevs[i]	# normalize
		nX.append(nRow)
	return np.asarray(nX)

# Normalize each separate class
def normalizeSep(XS, colMeans_all_tr, colStddevs_all_tr):
	nXS = []
	for classSamples in XS:
		nXClass = normalize(classSamples, colMeans_all_tr, colStddevs_all_tr)
		nXS.append(nXClass)
	return np.asarray(nXS)

# Rebuild original data file with normalized samples (classes are not normalized)
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

# Verify correct sample classificaiton
def verify(sample, classification):
	if (sample[CLASSINDEX] == classification):
		return 1
	else:
		return 0
	#return sample[CLASSINDEX] == classification

# Leave specified set out (stored as an empty list)
def combineSetsExcept(sets, exclude):
	combined = []
	i = -1
	for st in sets:
		i += 1
		if i == exclude:
			combined.append([])
			continue
		combined.append(st)
	return np.asarray(combined)

def combineSetsExcept2(sets, exclude):
	combined = []
	sampWithClass = []
	i = -1
	for st in sets:
		i += 1
		if i == exclude: continue
		for sample in st:
			sampWithClass = sample
			sampWithClass.append(i)
			combined.append(sampWithClass)
	return np.asarray(combined)

# Get m randomly assigned sets
def getMSets(XS, m):
	mSets = []
	for mth in range(m):						# init mSets
		mSets.append([])
	#print 'len(XS):\n{}'.format(len(XS))
	X = weave(XS, 1)							# aggregate data
	n = len(X)

	# Randomly divide dataset into m sets
	randIs = random.sample(range(n), n)			# get random indexes - *no repetition*
	numRIs = len(randIs)
	mMaxSize = (n / m) + n % m 					# max m set size
	ri = -1
	for _ in range(mMaxSize):					# iterate max set size
		for mthSet in range(m):					# iterate over sets
			if ((ri + 1) >= numRIs):
				break	
			else:
				ri += 1
			mSets[mthSet].append(X[ri])			# assign random samples to sets
	return mSets

def test_getMSets():
	fName_tr = 'poker-hand-training-true.data'
	# Get training data
	XS = getInputSeparated(fName_tr)
	mSets = getMSets(XS, 10)

	mSetSize = 0
	mSetSizeCombined = 0
	i = -1
	for mthSet in mSets:
		i += 1
		mSetSize = len(mthSet)
		mSetSizeCombined += mSetSize
		print '{}th set:\nSize: {}'.format(i, mSetSize)
		for samp in mthSet:
			print samp
		print
	print 'mSetSizeCombined: {}'.format(mSetSizeCombined)

# Placeholder for WIP code
def mFoldValid_devSup():
	print '{}th set:'.format(mthSet)
	for samp in trSet:
		print samp
	print '\n\n'

# m = n?  See project requirements
def mFoldValid(XS, m):
	print 'Entered mFoldValid()'
	fName_OUT = 'm-foldValid.txt'
	mSets = getMSets(XS, 10)

	# go through sets
	for mthSet in range(len(mSets)):
		te = mSets[mthSet]								# te is validaiton set
		trS = combineSetsExcept(mSets, mthSet)			# trS is training set - separated
		tr = weave(trS)									# training set - complete
		# Normalize tr set
		trColMeans = getColumnMeans(tr)
		trColStddevs = getColumnStddevs(tr)
		nTr = normalize(tr, trColMeans, trColStddevs)
		nTrS = normalizeSep(trS, trColMeans, trColStddevs)
		# Normalize te set
		teColMeans = getColumnMeans(te)
		teColStddevs = getColumnStddevs(te)
		nTe = normalize(trSet, teColMeans, teColStddevs)
		# CLASSIFY using tr
		#rebuild(trS, fName_OUT)
		#call(['knn.py'])								# must modify this script to read from out file
		# TEST using te
		#call(['knn.py'])								# must modify this script to read from out file

def test_mFoldValid():
	print 'Entered test_mFoldValid()'
	fName_tr = 'poker-hand-training-true.data'
	XS = getInputSeparated(fName_tr)
	mFoldValid(XS, 10)

def main():
	if DEBUG: print 'Entered main()'
	fName_IN = 'poker-hand-training-true.data'
	#fName_IN = 'poker-hand-testing.data'
	fName_OUT = 'poker-hand-training-true-normalized.data'
	#fName_OUT = 'poker-hand-testing-normalized.data'

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

	# Create normalized file
	#rebuild(nXS, fName_OUT)

	# M-fold validation
	mfoldValid(XS, 10)



#main()
#test_weave()
#test_getMSets()
test_mFoldValid()





