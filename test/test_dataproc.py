from dataproc.seq.seqfactory import *
from dataproc.seq.seqproc import SeqDP
from dataproc.seq.seqdb import *
from dataproc.seq.seqfactory import *
import matplotlib.pyplot as plt

def test_seqdb():
    y = get_stock("000001.csv")
    print(y.shape)
    print(np.mean(y), np.var(y))
    plt.plot(np.squeeze(y))
    plt.show()
#
# def test_seqfactory():
#     seqf = SeqDataFactory()
#     seq = seqf.get_data("stock", n_seq=10, filename="000001.csv", column_indexes=["closing"])
#     plt.plot(seq)
#     plt.show()

def test_multifactory():
    norms = [SeqDP.get_minmax_normalizer()]
    seqf = MultistepPredDataFactory(seq_normalizers=norms, if_win_normalized=True)
    x, y = seqf.get_data("stock", n_xseq=10, n_yseq=3, dis=7, filename="000001.csv", column_indexes=["closing","opening"], y_column=[0, 1])
    print(x.shape, y.shape)
    i = 666
    print(x[i])
    print(y[i])
    print(seqf.rawy.shape)
    print(seqf.rawy[i])
    print(seqf.inverse_y([y[i]], start=i, end=i+1))


if __name__ == "__main__":
    test_seqdb()