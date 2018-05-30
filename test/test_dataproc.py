from dataproc.seqdb import *
import matplotlib.pyplot as plt
from dataproc.seqfactory import *
from sklearn.preprocessing import MinMaxScaler

# def test_seqdb():
#     y = get_stock("000001.csv")
#     print(y.shape)
#     print(np.mean(y), np.var(y))
#     plt.plot(np.squeeze(y))
#     plt.show()
#
# def test_seqfactory():
#     seqf = SeqDataFactory()
#     seq = seqf.get_data("stock", n_seq=10, filename="000001.csv", column_indexes=["closing"])
#     plt.plot(seq)
#     plt.show()

def test_multifactory():
    seqf = MultstepPredDataFactory(seq_normalizer=MinMaxScaler())
    x, y = seqf.get_data("stock", 10, 2, n_yseq=3, filename="000001.csv", column_indexes=["closing", "opening"], y_column = [0, 1])
    print(x.shape, y.shape)


