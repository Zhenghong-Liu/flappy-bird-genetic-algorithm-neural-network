import numpy as np

# Neural network class
class NeuralNetwork:

    def __init__(self):
        HIDDEN_LAYER_SIZE = 20

        self.weights = np.random.uniform(-1,1,(3, HIDDEN_LAYER_SIZE))
        self.biases = np.random.uniform(-1,1,(HIDDEN_LAYER_SIZE))

        self.weights_hidden = np.random.uniform(-1,1,(HIDDEN_LAYER_SIZE, HIDDEN_LAYER_SIZE))
        self.biases_hidden = np.random.uniform(-1,1,(HIDDEN_LAYER_SIZE))

        self.weights_output = np.random.uniform(-1,1,(HIDDEN_LAYER_SIZE, 1))
        self.biases_output = np.random.uniform(-1,1,(1))

    def predict(self, inputs):
        # Feedforward logic
        hidden = np.dot(inputs, self.weights) + self.biases

        hidden_hidden = np.dot(hidden, self.weights_hidden) + self.biases_hidden

        hidden_output = np.dot(hidden_hidden, self.weights_output) + self.biases_output
        output = self.sigmoid(hidden_output)
        return output

    # def sigmoid(self, x):
    #     return 1 / (1 + np.exp(-x))

    def sigmoid(self, x):
        y = x.copy()  # 对sigmoid函数优化，避免出现极大的数据溢出
        y[x >= 0] = 1.0 / (1 + np.exp(-x[x >= 0]))
        y[x < 0] = np.exp(x[x < 0]) / (1 + np.exp(x[x < 0]))
        return y