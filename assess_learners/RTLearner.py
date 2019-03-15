import numpy as np

class RTLearner(object):

    def __init__(self, leaf_size = 1, verbose = False):
        self.leaf_size = leaf_size
        self.verbose = verbose
        self.leaf = None

    def author(self):
        return 'yzhang3414'

    def addEvidence(self, Xtrain, Ytrain):
        data = np.concatenate((Xtrain, np.array([Ytrain]).T), axis=1)
        self.tree = self.build_tree(data)

    def query(self, Xtest):
        preds = []
        for i in range(len(Xtest)):
            curr = 0
            while self.tree[curr, 0] != None:
                feat = int(self.tree[curr,0])
                SplitVal = self.tree[curr,1]
                
                if Xtest[i,feat] <= SplitVal:
                    add = int(self.tree[curr,2])
                else:
                    add = int(self.tree[curr,3])

                curr = curr + add
                pred = self.tree[curr,1]
            preds.append(pred)
        return np.array(preds)

    def build_tree(self, data):
        X, Y = data[:,:-1], data[:,-1]
        if X.shape[0] <= self.leaf_size:
            return np.array([self.leaf, np.mean(Y), None, None])
        elif np.unique(Y).size == 1:
            return np.array([self.leaf, np.mean(Y), None, None])
        else:
            index = np.random.randint(X.shape[1])
            SplitVal = np.median(X[:,index])
            data_left = data[data[:,index] <= SplitVal]
            data_right = data[data[:,index] > SplitVal]

            if data_left.shape[0] == 0 or data_right.shape[0] == 0:
                return np.array([self.leaf, np.mean(Y), None, None])

            lefttree = self.build_tree(data_left)
            righttree = self.build_tree(data_right)

            if len(lefttree.shape) == 1:
                index_right = 1
            else:
                index_right = lefttree.shape[0]

            root = np.array([index, SplitVal, 1, index_right + 1])
            return np.vstack((root, lefttree, righttree))


