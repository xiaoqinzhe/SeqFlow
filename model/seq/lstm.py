""""
A naive lstm model implementation with Keras
"""
from model.base.basemodel import KerasModel
from model.base.component import getLstmLayer, getFcnLayer
from keras.models import Model
from keras.layers import Input

class LSTMKModel(KerasModel):
    def __init__(self, input_dim, output_dim, lstm_size=10, num_layers=1, dropout=-1, return_sequence=False, is_train=True, saved_model_path="lstm/lstm.h5"):
        self.lstm_size = lstm_size
        self.num_layers = num_layers
        self.dropout = dropout
        self.return_sequence = return_sequence
        super(LSTMKModel, self).__init__(input_dim, output_dim, is_train, saved_model_path)

    def init_model(self):
        self.input = Input(self.input_dim)
        l = getLstmLayer(self.input, self.lstm_size, self.num_layers, dropout=self.dropout, return_sequences=self.return_sequence)
        l = getFcnLayer(l, self.output_dim)
        self.model = Model(inputs=self.input, outputs=l)