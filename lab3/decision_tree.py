import numpy as np
from collections import Counter

class Node:
    def __init__(self, feature=None, threshold=None, left=None, right=None, *, value=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value

    def is_leaf_node(self):
        return self.value is not None

class DecisionTree:
    def __init__(self, min_samples_split=2, max_depth=100, n_features=None):
        self.min_samples_split = min_samples_split
        self.max_depth = max_depth
        self.n_features = n_features
        self.root = None

    def fit(self, X, y):
        if self.n_features is None:
            self.n_features = X.shape[1]
        self.root = self._grow_tree(X, y, 0)

    def _grow_tree(self, X, y, depth = 0):
        if depth >= self.max_depth or len(y) < self.min_samples_split:
            return Node(value = Counter(y).most_common(1)[0][0])

        n_features = X.shape[1]
        feat_idxs = np.random.choice(n_features, self.n_features, replace=False)

        best_feat, best_thresh, best_gain = self._best_split(X, y, feat_idxs)

        if best_gain > 0:
            left_idxs, right_idxs = self._split(X[:, best_feat], best_thresh)
            left = self._grow_tree(X[left_idxs], y[left_idxs], depth + 1)
            right = self._grow_tree(X[right_idxs], y[right_idxs], depth + 1)
            return Node(best_feat, best_thresh, left, right)
        else:
            return Node(value = Counter(y).most_common(1)[0][0])

    def _best_split(self, X, y, feat_idxs):
        best_feat = None
        best_thresh = None
        best_gain = -1

        for feat in feat_idxs:
            X_column = X[:, feat]
            thresholds = np.unique(X_column)
            best_thresh_feat, best_gain_feat = self._information_gain(y, X_column, thresholds)

            if best_gain_feat > best_gain:
                best_feat = feat
                best_thresh = best_thresh_feat
                best_gain = best_gain_feat

        return best_feat, best_thresh, best_gain

    def _information_gain(self, y, X_column, thresholds):
        best_thresh = None
        best_gain = -1

        for thresh in thresholds:
            left_idxs, right_idxs = self._split(X_column, thresh)
            left_y, right_y = y[left_idxs], y[right_idxs]
            gain = self._entropy(y) - (len(left_y) / len(y)) * self._entropy(left_y) - (len(right_y) / len(y)) * self._entropy(right_y)

            if gain > best_gain:
                best_thresh, best_gain = thresh, gain

        return best_thresh, best_gain

    def _split(self, X_column, split_thresh):
        left_idxs = X_column <= split_thresh
        right_idxs = X_column > split_thresh

        return left_idxs, right_idxs

    def _entropy(self, y):
        hist = np.bincount(y)
        ps = hist / len(y)
        return -np.sum([p * np.log(p) for p in ps if p > 0])

    def _traverse_tree(self, X, node: Node):
        if node.is_leaf_node():
            return node.value
        if X[node.feature] < node.threshold:
            return self._traverse_tree(X, node.left)
        else:
            return self._traverse_tree(X, node.right)

    def predict(self, X):
        return np.array([self._traverse_tree(x, self.root) for x in X])
