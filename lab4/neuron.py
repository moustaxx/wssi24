import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Neuron:
    def __init__(self, n_inputs, bias = 0., weights = None):
        self.b = bias
        if weights: self.ws = np.array(weights)
        else: self.ws = np.random.rand(n_inputs)

    def _f(self, x):
        return max(x * 0.1, x)

    def __call__(self, xs):
        return self._f(xs @ self.ws + self.b)

class ANN:
    def __init__(self, layer_sizes):
        self.layers = []
        for i in range(len(layer_sizes) - 1):
            layer = [Neuron(layer_sizes[i]) for _ in range(layer_sizes[i+1])]
            self.layers.append(layer)

    def forward(self, x):
        for layer in self.layers:
            x = np.array([neuron(x) for neuron in layer])
        return x

def visualize_ann(layer_sizes):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')

    colors = ['red', 'blue', 'blue', 'green']

    layer_xs = np.linspace(0, 1, len(layer_sizes))
    for i, (n_neurons, x, color) in enumerate(zip(layer_sizes, layer_xs, colors)):
        y_space = np.linspace(0, 1, n_neurons + 2)[1:-1]

        for y in y_space:
            ax.plot(x, y, 'o', markersize=30, color=color)

        if i > 0:
            prev_y_space = np.linspace(0, 1, layer_sizes[i-1] + 2)[1:-1]
            for y in y_space:
                for prev_y in prev_y_space:
                    dx = x-layer_xs[i-1]
                    dy = y - prev_y
                    ax.add_patch(patches.Arrow(layer_xs[i-1], prev_y, dx, dy, width=0.015, color='k'))

    ax.text(layer_xs[0] - 0.05, 0.11, 'input layer', va='center', ha='center', color='red', fontsize=14, bbox=dict(facecolor='white', alpha=0.6))
    ax.text(layer_xs[1] - 0.05, 0.11, 'hidden layer 1', va='center', ha='center', color='blue', fontsize=14, bbox=dict(facecolor='white', alpha=0.6))
    ax.text(layer_xs[2] - 0.05, 0.11, 'hidden layer 2', va='center', ha='center', color='blue', fontsize=14, bbox=dict(facecolor='white', alpha=0.6))
    ax.text(layer_xs[3] - 0.05, 0.11, 'output layer', va='center', ha='center', color='green', fontsize=14, bbox=dict(facecolor='white', alpha=0.6))

    plt.show()

layer_sizes = [3, 4, 4, 1]
ann = ANN(layer_sizes)
visualize_ann(layer_sizes)
