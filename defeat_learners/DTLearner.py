""" 			  		 			     			  	   		   	  			  	
A simple wrapper for linear regression.  (c) 2015 Tucker Balch 			  		 			     			  	   		   	  			  	
Note, this is NOT a correct DTLearner; Replace with your own implementation. 			  		 			     			  	   		   	  			  	
Copyright 2018, Georgia Institute of Technology (Georgia Tech) 			  		 			     			  	   		   	  			  	
Atlanta, Georgia 30332 			  		 			     			  	   		   	  			  	
All Rights Reserved 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
Template code for CS 4646/7646 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
Georgia Tech asserts copyright ownership of this template and all derivative 			  		 			     			  	   		   	  			  	
works, including solutions to the projects assigned in this course. Students 			  		 			     			  	   		   	  			  	
and other users of this template code are advised not to share it with others 			  		 			     			  	   		   	  			  	
or to make it available on publicly viewable websites including repositories 			  		 			     			  	   		   	  			  	
such as github and gitlab.  This copyright statement should not be removed 			  		 			     			  	   		   	  			  	
or edited. 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
We do grant permission to share solutions privately with non-students such 			  		 			     			  	   		   	  			  	
as potential employers. However, sharing with other current or future 			  		 			     			  	   		   	  			  	
students of CS 7646 is prohibited and subject to being investigated as a 			  		 			     			  	   		   	  			  	
GT honor code violation. 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
-----do not edit anything above this line--- 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
Student Name: Yichao Zhang (replace with your name) 			  		 			     			  	   		   	  			  	
GT User ID: yzhang3414 (replace with your User ID) 			  		 			     			  	   		   	  			  	
GT ID: 903459675 (replace with your GT ID) 			  		 			     			  	   		   	  			  	
""" 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
import numpy as np 			  		 			     			  	   		   	  			  	
import warnings 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
class DTLearner(object): 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    def __init__(self, leaf_size=1, verbose = False): 			  		 			     			  	   		   	  			  	
        #warnings.warn("\n\n  WARNING! THIS IS NOT A CORRECT DTLearner IMPLEMENTATION! REPLACE WITH YOUR OWN CODE\n") 			  		 			     			  	   		   	  			  	
        #pass # move along, these aren't the drones you're looking for 			  		 			     			  	   		   	  			  	
        self.leaf_size = leaf_size
        self.verbose = verbose
        self.leaf = None

    def author(self): 			  		 			     			  	   		   	  			  	
        return 'yzhang3414' # replace tb34 with your Georgia Tech username 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    def addEvidence(self,dataX,dataY): 			  		 			     			  	   		   	  			  	
        """ 			  		 			     			  	   		   	  			  	
        @summary: Add training data to learner 			  		 			     			  	   		   	  			  	
        @param dataX: X values of data to add 			  		 			     			  	   		   	  			  	
        @param dataY: the Y training values 			  		 			     			  	   		   	  			  	
        """ 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
        # slap on 1s column so linear regression finds a constant term 			  		 			     			  	   		   	  			  	
        #newdataX = np.ones([dataX.shape[0],dataX.shape[1]+1]) 			  		 			     			  	   		   	  			  	
        #newdataX[:,0:dataX.shape[1]]=dataX 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
        # build and save the model 			  		 			     			  	   		   	  			  	
        #self.model_coefs, residuals, rank, s = np.linalg.lstsq(newdataX, dataY) 
        data = np.concatenate((dataX, np.array([dataY]).T), axis=1)
        self.tree = self.build_tree(data)			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    def query(self,points): 			  		 			     			  	   		   	  			  	
        """ 			  		 			     			  	   		   	  			  	
        @summary: Estimate a set of test points given the model we built. 			  		 			     			  	   		   	  			  	
        @param points: should be a numpy array with each row corresponding to a specific query. 			  		 			     			  	   		   	  			  	
        @returns the estimated values according to the saved model. 			  		 			     			  	   		   	  			  	
        """ 
        #return (self.model_coefs[:-1] * points).sum(axis = 1) + self.model_coefs[-1] 
        preds = []
        for i in range(len(points)):
            curr = 0
            while self.tree[curr, 0] != None:
                feat = int(self.tree[curr,0])
                SplitVal = self.tree[curr,1]

                if points[i,feat] <= SplitVal:
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
            correlation = -1.
            index = -1
            for i in range(X.shape[1]):
                corr = abs(np.corrcoef(X[:,i], Y)[1,0])
                if corr > correlation:
                    correlation = corr
                    index = i
                    
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
 			  		 			     			  	   		   	  			  	
if __name__=="__main__": 			  		 			     			  	   		   	  			  	
    print "the secret clue is 'zzyzx'" 			  		 			     			  	   		   	  			  	
