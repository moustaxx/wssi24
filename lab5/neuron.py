import numpy as np
import matplotlib.pyplot as plt

learning_rate = 0.01

class Neuron:
    def __init__(self, n_inputs, bias = 0., weights = None):
        self.b = bias
        if weights: self.ws = np.array(weights)
        else: self.ws = np.random.rand(n_inputs)

    def _f(self, x):
        return max(x * 0.1, x)

    def _df(self, x):
        return 0.1 if x < 0 else 1

    def __call__(self, xs):
        self.last_input = xs
        self.last_output = self._f(xs @ self.ws + self.b)
        return self.last_output

    def backward(self, dL_dy):
        dy_dx = self._df(self.last_input @ self.ws + self.b)
        dL_dx = dL_dy * dy_dx
        dL_dw = dL_dx * self.last_input
        dL_db = dL_dx
        self.ws -= learning_rate * dL_dw
        self.b -= learning_rate * dL_db
        return dL_dx @ self.ws

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

    def backward(self, dL_dy):
        for layer in reversed(self.layers):
            dL_dy = np.array([neuron.backward(dL_dy[i]) for i, neuron in enumerate(layer)])
        return dL_dy


def visualize_ann(layer_sizes):
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('off')

    colors = ['red', 'blue', 'blue', 'green']

    layer_xs = np.linspace(0, 1, len(layer_sizes))
    for i, (n_neurons, x, color) in enumerate(zip(layer_sizes, layer_xs, colors)):
        y_space = np.linspace(0, 1, n_neurons)

        if y_space.argmax() == 0:
            y_space = np.array([0.5])
        for y in y_space:
            ax.plot(x, y, 'o', markersize=15, color=color)

        if i > 0:
            prev_y_space = np.linspace(0, 1, layer_sizes[i-1])
            for y in y_space:
                for prev_y in prev_y_space:
                    ax.plot([layer_xs[i-1], x], [prev_y, y], 'k-')

    ax.text(layer_xs[0] - 0.05, -0.1, 'input layer', va='center', ha='center', color='red', fontsize=14, bbox=dict(facecolor='white', alpha=0.6))
    ax.text(layer_xs[1] - 0.05, -0.1, 'hidden layer 1', va='center', ha='center', color='blue', fontsize=14, bbox=dict(facecolor='white', alpha=0.6))
    ax.text(layer_xs[2] - 0.05, -0.1, 'hidden layer 2', va='center', ha='center', color='blue', fontsize=14, bbox=dict(facecolor='white', alpha=0.6))
    ax.text(layer_xs[3] - 0.05, -0.1, 'output layer', va='center', ha='center', color='green', fontsize=14, bbox=dict(facecolor='white', alpha=0.6))

    plt.show()

layer_sizes = [3, 4, 4, 1]
ann = ANN(layer_sizes)
visualize_ann(layer_sizes)
