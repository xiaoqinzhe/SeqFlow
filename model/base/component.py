"""
Providing components to construct Model
"""

from keras.layers import LSTM, Input, Dense, RepeatVector, Dropout
from keras.models import Sequential, Model
from keras import regularizers

def getLstmLayer(x, lstm_size, num_layer=1, return_sequences=False, dropout=-1):
    lstm = x
    for i in range(num_layer):
        if i<num_layer-1:
            lstm = LSTM(lstm_size, return_sequences=True)(lstm)
        else: lstm = LSTM(lstm_size, return_sequences=return_sequences)(lstm)
        if dropout>0: lstm = Dropout(dropout)(lstm)
    return lstm

def getFcnLayer(x, layer_sizes, dropout=-1):
    if isinstance(layer_sizes, int): layer_sizes=[layer_sizes]
    l=x
    for size in layer_sizes:
        l = Dense(size)(l)
        if dropout>0: l=Dropout(dropout)(l)
    return l

def getLstmAEModel(input_shape, lstm_size, num_layer):
    x = Input(shape=input_shape)
    decoder_input, decoder_l = None, None
    l = x
    for i in range(num_layer):
        if i == num_layer / 2 - 1:
            encoder = l = LSTM(lstm_size, name="embedding_layer", return_sequences=False)(l)
            l = RepeatVector(input_shape[0])(l)
            decoder_input = Input(shape=(lstm_size,))
            decoder_l = RepeatVector(input_shape[0])(decoder_input)
        elif i == num_layer - 1:
            l = LSTM(input_shape[1], return_sequences=True)(l)
            decoder_l = LSTM(input_shape[1], return_sequences=True)(decoder_l)
        else:
            l = LSTM(lstm_size, return_sequences=True)(l)
            if i > num_layer / 2 - 1:
                decoder_l = LSTM(lstm_size, return_sequences=True)(decoder_l)
    ae_model = Model(inputs=x, outputs=l)
    encoder_model = Model(inputs=x, outputs=encoder)
    decoder_model = Model(inputs=decoder_input, outputs=decoder_l)
    return ae_model, encoder_model, decoder_model

def getFCNAEModel(input_shape, layer_sizes, num_layer):
    x = Input(shape=input_shape)
    decoder_input, decoder_l = None, None
    l = x
    for i in range(num_layer):
        if i > num_layer / 2 - 1:
            decoder_l = Dense(layer_sizes[i], name="dense_{0}".format(i))(decoder_l)
        if i == num_layer / 2 - 1:
            decoder_l = decoder_input = Input(shape=(layer_sizes[i],))
            encoder = l = Dense(layer_sizes[i], name="embedding_layer")(l)
        else:
            l = Dense(layer_sizes[i], name="dense_{0}".format(i))(l)
    ae_model = Model(inputs=x, outputs=l)
    encoder_model = Model(inputs=x, outputs=encoder)
    decoder_model = Model(inputs=decoder_input, outputs=decoder_l)
    return ae_model, encoder_model, decoder_model