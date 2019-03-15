import numpy as np
import DTLearner as dtl
import RTLearner as rtl

class BagLearner(object):

	def __init__(self, learner = rtl.RTLearner, kwargs = {"argument1":1, "argument2":2}, bags = 20, boost=False, verbose=False):
		self.learner = learner
		self.bags = bags
		self.boost = boost
		self.verbose = verbose
		self.learners = []
		for i in range(bags):
			self.learners.append(self.learner(**kwargs))

	def author(self):
		return 'yzhang3414'

	def addEvidence(self, Xtrain, Ytrain):
		for learner in self.learners:
			randoms = np.random.randint(0, Xtrain.shape[0], Xtrain.shape[0])
			learner.addEvidence(Xtrain[randoms], Ytrain[randoms])

	def query(self, Xtest):
		Ypreds = [learner.query(Xtest) for learner in self.learners]
		return np.mean(np.array(Ypreds), axis=0)
