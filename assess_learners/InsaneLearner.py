import BagLearner as bl
import LinRegLearner as lrl
import numpy as np

class InsaneLearner(object):
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.learners = []
        for i in range(0,20):
            self.learners.append(bl.BagLearner(learner=lrl.LinRegLearner, kwargs={}, bags=20, boost=False, verbose=False))

    def author(self):
        print 'yzhang3414'

    def addEvidence(self, Xtrain, Ytrain):
        for learner in self.learners:
            learner.addEvidence(Xtrain, Ytrain)

    def query(self, Xtest):
        Ypreds = [learner.query(Xtest) for learner in self.learners]
        return np.mean(np.array(Ypreds), axis=0)
