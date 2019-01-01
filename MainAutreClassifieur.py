from sklearn.cross_validation import train_test_split
from sklearn.datasets import make_moons
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn import datasets
import Point
import Prototype
import random as rd
import copy
import numpy as np
import matplotlib.pyplot as plt
import PointGenerator
import Espace

generator = PointGenerator.PointGenerator()

digit = generator.digits()
espaceDigit = Espace.Espace(digit, [])
digits = espaceDigit.getListePoints()
for i in digits:
    if(i.getLabel() != 1):
        i.setLabel(0)

X, y = generator.pointsToMatrixAndLabels(digits)

Xs, Xt, Ys, Yt = train_test_split(X, y, test_size=.4)

digit = generator.digits()
espaceDigit = Espace.Espace(digit, [])
digit1 = espaceDigit.getPointsFromLabel(1)
digit1HalfSource, digit1HalfTarget = generator.splitDistrib(digit1, 0.4)
sourceAutre = espaceDigit.getPointsFromLabel(7) + espaceDigit.getPointsFromLabel(3) + espaceDigit.getPointsFromLabel(4) + espaceDigit.getPointsFromLabel(5)
for j in sourceAutre:
    j.setLabel(0)
targetAutre = espaceDigit.getPointsFromLabel(6) + espaceDigit.getPointsFromLabel(2) + espaceDigit.getPointsFromLabel(8) + espaceDigit.getPointsFromLabel(9)
for j in targetAutre:
    j.setLabel(0)
source = digit1HalfSource + sourceAutre
target = targetAutre + digit1HalfTarget

Xs, Ys = generator.pointsToMatrixAndLabels(source)
Xt, Yt = generator.pointsToMatrixAndLabels(target)

h = .02  # step size in the mesh

names = ["Nearest Neighbors", "Linear SVM", "RBF SVM", "Decision Tree",
         "Random Forest", "AdaBoost", "Naive Bayes", "LogisticRegression"]
classifiers = [
    KNeighborsClassifier(3),
    SVC(kernel="linear", C=0.025),
    SVC(gamma=2, C=1),
    DecisionTreeClassifier(max_depth=5),
    RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
    AdaBoostClassifier(),
    GaussianNB(),
    LogisticRegression(C=1e5)]

for name, clf in zip(names, classifiers):
    clf.fit(Xs, Ys)
    score = clf.score(Xt, Yt)
    print(name, ": ",str(score))

gammas= [1,2,4,8,16]
Cs = [0.025, 0.1, 0.5, 1, 5]

for c in Cs:
    for gamma in gammas:
        clf = SVC(gamma=gamma, C=c)
        clf.fit(Xs, Ys)
        score = clf.score(Xt, Yt)
        print("RBF SVM (gamma=", str(gamma), ", c=", str(c) + "): ", str(score))