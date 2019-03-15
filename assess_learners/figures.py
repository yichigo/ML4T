import numpy as np
import math
import LinRegLearner as lrl
import DTLearner as dtl
import RTLearner as rtl
import BagLearner as bl
import InsaneLearner as il
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import time

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: python testlearner.py <filename>"
        sys.exit(1)
    inf = open(sys.argv[1])
    data = np.array([map(float, s.strip().split(',')[1:]) for s in inf.readlines()[1:]])
    #data = np.array([map(float, s.strip().split(',')) for s in inf.readlines()])

    train_rows = int(0.6 * data.shape[0])
    test_rows = data.shape[0] - train_rows

    trainX = data[:train_rows, 0:-1]
    trainY = data[:train_rows, -1]
    testX = data[train_rows:, 0:-1]
    testY = data[train_rows:, -1]


    rmse_insample=[]
    rmse_outsample=[]
    for i in range (1,101):
        learner = dtl.DTLearner(leaf_size=i, verbose=False)
        learner.addEvidence(trainX, trainY)  # train it
        predY = learner.query(trainX)  # get the predictions
        rmse_insample.append(math.sqrt(((trainY - predY) ** 2).sum() / trainY.shape[0]))
        predY = learner.query(testX)
        rmse_outsample.append(math.sqrt(((testY - predY) ** 2).sum() / testY.shape[0]))
    plt.xlabel("Leaf Size")
    plt.ylabel("RMSE")
    plt.plot(rmse_insample,label="Train")
    plt.plot(rmse_outsample, label="Test")
    plt.title("DTLearner: Leaf Size vs RMSE")
    plt.legend(loc="best")
    plt.xticks(np.arange(0,50,step=10))
    plt.grid(True)
    plt.savefig("Q1.png")
    plt.close()
    rmse_insample = []
    rmse_outsample = []
    for i in range (1,101):
        learner = bl.BagLearner(learner = dtl.DTLearner, kwargs = {"leaf_size":i,"verbose":False}, bags = 10, boost = False, verbose = False)
        learner.addEvidence(trainX, trainY)  # train it
        predY = learner.query(trainX)  # get the predictions
        rmse_insample.append(math.sqrt(((trainY - predY) ** 2).sum() / trainY.shape[0]))
        predY = learner.query(testX)
        rmse_outsample.append(math.sqrt(((testY - predY) ** 2).sum() / testY.shape[0]))
    plt.xlabel("Leaf Size")
    plt.ylabel("RMSE")
    plt.plot(rmse_insample,label="Train")
    plt.plot(rmse_outsample, label="Test")
    plt.title("10-Bag Learner: Leaf Size vs RMSE")
    plt.legend(loc="best")
    plt.xticks(np.arange(0,50,step=10))
    plt.grid(True)
    plt.savefig("Q2_1.png")
    plt.close()
    rmse_insample = []
    rmse_outsample = []
    for i in range(1, 101):
        learner = bl.BagLearner(learner=dtl.DTLearner, kwargs={"leaf_size": i, "verbose": False}, bags=20, boost=False,
                                verbose=False)
        learner.addEvidence(trainX, trainY)  # train it
        predY = learner.query(trainX)  # get the predictions
        rmse_insample.append(math.sqrt(((trainY - predY) ** 2).sum() / trainY.shape[0]))
        predY = learner.query(testX)
        rmse_outsample.append(math.sqrt(((testY - predY) ** 2).sum() / testY.shape[0]))
    plt.xlabel("Leaf Size")
    plt.ylabel("RMSE")
    plt.plot(rmse_insample, label="Train")
    plt.plot(rmse_outsample, label="Test")
    plt.title("20-Bag Learner: Leaf Size vs RMSE")
    plt.legend(loc="best")
    plt.xticks(np.arange(0, 50, step=10))
    plt.grid(True)
    plt.savefig("Q2_2.png")
    plt.close()

    timeDT=[]
    timeRT=[]
    for i in range(1, 101):
        learnerD = dtl.DTLearner(leaf_size=i, verbose=False)
        t1=time.time()
        learnerD.addEvidence(trainX, trainY)
        t2=time.time()
        timeDT.append(t2-t1)
        learnerR = rtl.RTLearner(leaf_size=i, verbose=False)
        t1 = time.time()
        learnerR.addEvidence(trainX, trainY)
        t2 = time.time()
        timeRT.append(t2 - t1)
    plt.xlabel("Leaf Size")
    plt.ylabel("Time / Seconds")
    plt.plot(timeDT, label="Time of DTLearner")
    plt.plot(timeRT, label="Time of RTLearner")
    plt.title("Time Cost: DT vs RT")
    plt.legend(loc="best")
    plt.xticks(np.arange(0, 50, step=10))
    plt.grid(True)
    plt.savefig("Q3_1.png")
    plt.close()

    meanabserrorDT_insample=[]
    meanabserrorRT_insample=[]
    meanabserrorDT_outsample=[]
    meanabserrorRT_outsample=[]
    for i in range(1, 101):
        learnerD=dtl.DTLearner(leaf_size=i,verbose=False)
        learnerD.addEvidence(trainX,trainY)
        pred=learnerD.query(trainX)
        meanabserrorDT_insample.append(abs(trainY - pred).sum() / trainY.shape[0])
        pred=learnerD.query(testX)
        meanabserrorDT_outsample.append(abs(testY - pred).sum() / testY.shape[0])

        learnerR=rtl.RTLearner(leaf_size=i,verbose=False)
        learnerR.addEvidence(trainX, trainY)
        pred = learnerR.query(trainX)
        meanabserrorRT_insample.append(abs(trainY - pred).sum() / trainY.shape[0])
        pred = learnerR.query(testX)
        meanabserrorRT_outsample.append(abs(testY - pred).sum() / testY.shape[0])
    plt.xlabel("Leaf Size")
    plt.ylabel("Mean Absolute Error")
    plt.plot(meanabserrorDT_insample, label="DT Train")
    plt.plot(meanabserrorRT_insample, label="RT Train")
    plt.plot(meanabserrorDT_outsample, label="DT Test")
    plt.plot(meanabserrorRT_outsample, label="RT Test")

    plt.title("Mean absolute Error: DT vs RT")
    plt.legend(loc="best")
    plt.xticks(np.arange(0, 50, step=10))
    plt.grid(True)
    plt.savefig("Q3_2.png")
    plt.close()
