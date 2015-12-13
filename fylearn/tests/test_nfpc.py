
import numpy as np

import fylearn.nfpc as nfpc
import fylearn.fuzzylogic as fl

def t_factory(min, mean, max):
    return fl.TriangularSet(min, mean, max)

def test_build_shrinking():

    X = np.random.rand(100, 3)
    X[:, 1] = X[:, 1] * 10
    X[:, 2] = X[:, 2] * 50

    s = nfpc.build_shrinking_memberships(X, t_factory, 0.1, 2)

    assert len(s) == 3
    assert s[0].b - 0.5 < 0.05
    assert s[1].b - 5 < 1
    assert s[2].b - 25 < 3


def test_build_shrinking_data():

    import os
    csv_file = os.path.join(os.path.dirname(__file__), "iris.csv")
    data = np.genfromtxt(csv_file, dtype=float, delimiter=',', names=True)

    X = np.array([data["sepallength"], data["sepalwidth"], data["petallength"], data["petalwidth"]]).T
    y = data["class"]

    from sklearn.preprocessing import MinMaxScaler
    X = MinMaxScaler().fit_transform(X)

    l = nfpc.ShrinkingPositiveFuzzyPatternClassifier(iterations=2, alpha_cut=0.25,
                                                     membership_factory=t_factory)

    from sklearn import cross_validation

    scores = cross_validation.cross_val_score(l, X, y, cv=10)
    mean = np.mean(scores)

    print "mean", mean

    assert 0.90 < mean