# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import _init_paths
from model.seq.lstm import LSTMKModel
from dataproc.seq.seqfactory import MultistepPredDataFactory
from dataproc.seq.seqproc import SeqDP
from sklearn.model_selection import train_test_split
from visual.seqvisual import SeqPredDataVisual

norms = [SeqDP.get_minmax_normalizer()]
seqf = MultistepPredDataFactory(seq_normalizers=None, if_win_normalized=True)
x, y = seqf.get_data("stock", n_xseq=10, n_yseq=1, dis=3, filename="000001.csv",
                         column_indexes=["closing", "opening"], y_column=[0, 1])

def test_lstmkmodel():
    train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.1, shuffle=False)
    model = LSTMKModel(input_dim=x.shape[1:3], output_dim=2, lstm_size=10, num_layers=1, is_train=False, dropout=-1, return_sequence=False)
    model.compile_model()
    model.train(train_x, train_y, batch_size=100, epochs=10, verbose=2)
    print(model.test(test_x, test_y))
    pred_y = model.predict(test_x)
    ry, py = seqf.get_raw_ytest_ypred(pred_y, 0.1)
    print(ry.shape, py.shape)
    SeqPredDataVisual.plot_series(ry, py)

if __name__=="__main__":
    test_lstmkmodel()