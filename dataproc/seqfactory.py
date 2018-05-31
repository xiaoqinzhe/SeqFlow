"""
A factory set that produces data
"""

from dataproc.seqproc import SeqDP
from dataproc import seqdb
import copy
import numpy as np

class SeqDataFactory:
    """Sequence
    Note:
        Parameter
        ---------
        **data_params : optional
            the parameters that different datasets can use.
            (1) for stock data: column_indexes; start_time, end_time
            (2) for sunspot: start_time, end_time
            (3) for temperature: None
    """

    def __init__(self, seq_normalizers=None, if_win_normalized=False):
        """
        Initialize sequence processing env
        :param normalizator:
        :param smoothor:
        """
        self.seqdp = SeqDP()
        self.if_seq_normalized = (seq_normalizers is not None)
        self.seq_normalizers = seq_normalizers
        self.if_win_normalized = if_win_normalized
        self.win_normalizer = None
        if self.if_win_normalized: self.win_normalizer=self.seqdp.get_win_normalizer()
        self.rawx, self.rawy = None, None
        self.x, self.y = None, None

    @classmethod
    def get_seq_data(cls, dataset_name,  **data_params):
        """
        get data in terms of dataset_name
        :param dataset_name: str
            dataset name.
        :param filename: str, optional, default None
            if dataset is stock or any other category, it means the specified file.
        :return: array-like
        """
        filename = data_params.get('filename')
        column_indexes = data_params.get('column_indexes')
        start_time = data_params.get('start_time')
        end_time = data_params.get('end_time')
        seq = None
        if dataset_name == "stock":
            if filename is None: raise AttributeError("filename should not be None for stock dataset")
            seq = seqdb.get_stock(filename, column_indexes, start_time, end_time)
        elif dataset_name == "sunspot":
            seq = seqdb.get_sunspot(start_time, end_time)
        elif dataset_name == "temperature":
            seq = seqdb.get_temperature()
        return seq

    def _get_raw_data(self, dataset_name, **data_params):
        return self.get_seq_data(dataset_name, **data_params)

    def _preproc_data(self, **data_params):
        if self.if_seq_normalized:
            for norm in self.seq_normalizers: self.x = norm.fit_transform(self.x)

    def _postproc_data(self, **data_params):
        return

    def inverse_data(self, x):
        if self.if_seq_normalized:
            for i in range(len(self.seq_normalizers)): x = self.seq_normalizers[-i-1].inverse_transform(x)
        return x

    def get_data(self, dataset_name, **data_params):
        self.x = self.rawx = self._get_raw_data(dataset_name, **data_params)
        self._preproc_data()
        self._postproc_data()
        return self.x

class MultstepPredDataFactory(SeqDataFactory):
    def __init__(self, seq_normalizers=None, if_win_normalized=False):
        super(MultstepPredDataFactory, self).__init__(seq_normalizers, if_win_normalized)
        self.dis = 1
        self.n_xseq = 1
        self.n_yseq = 1

    def _get_raw_data(self, dataset_name, **data_params):
        if isinstance(dataset_name, str):
            # one dataset prediction
            self.rawx = self.get_seq_data(dataset_name, **data_params)
            y_column = data_params.get("y_column", [0])
            self.rawy = copy.copy(self.rawx[:, y_column])
        elif isinstance(dataset_name, list):
            # two list of dataset
            for k in range(2):
                x = None
                for i in range(len(dataset_name[k])):
                    params = {}
                    if data_params.get("filename") is not None: params["filename"] = data_params.get("filename")[k][i]
                    if data_params.get("column_indexes") is not None: params["column_indexes"] = data_params.get("column_indexes")[k][i]
                    if data_params.get("start_time") is not None: params["start_time"] = data_params.get("start_time")[k][i]
                    if data_params.get("end_time") is not None: params["end_time"] = data_params.get("end_time")[k][i]
                    _x = self.get_seq_data(dataset_name[0][i], **params)
                    if x is not None: x = np.concatenate([x, _x])
                    else: x = _x
                if k==0: self.rawx = x
                else: self.rawy = x
        else: raise AttributeError("dataset_names should be str or list like [[], []]")
        if len(self.rawy.shape) == 1: self.rawy = np.reshape(self.rawy, (-1, 1))
        return self.rawx, self.rawy

    def _preproc_data(self, **data_params):
        if self.if_seq_normalized:
            for norm in self.seq_normalizers:
                self.x = norm.fit_transform(self.x)
                self.y = norm.fit_transform(self.y)

    def _postproc_data(self, **data_params):
        self.x, self.y = self.seqdp.windowing_xy(self.x, self.y, self.n_xseq, self.dis, n_yseq=self.n_yseq)
        self.rawy = self.rawy[self.n_xseq+self.dis-1:]
        self.rawy = self.seqdp.windowing_x(self.rawy, self.n_yseq)
        if self.if_win_normalized:
            b = data_params.get("normalized_ybase", [i for i in range(len(self.x[0][0]))])
            self.x, self.y = self.win_normalizer.fit_transform(self.x, self.y, ybase=b)

    def inverse_y(self, y, start=0, end=None):
        if not isinstance(y, np.ndarray): y = np.array(y)
        if self.if_win_normalized: y = self.win_normalizer.inverse_transform(y, start, end)
        if self.if_seq_normalized:
            for i in range(len(self.seq_normalizers)):
                if isinstance(y[0][0], np.ndarray):
                    for j in range(len(y)): y[j] = self.seq_normalizers[-i-1].inverse_transform(y[j])
                else: y = self.seq_normalizers[-i-1].inverse_transform(y)
        return y

    def get_rawy(self, start=0, end=None):
        if end is None: end = len(self.y)
        return self.rawy[start:end]

    def get_rawytest(self, split_rate=0.9):
        return self.get_rawy(int(split_rate*len(self.y)))

    def get_data(self, dataset_name, n_xseq=1, dis=1, n_yseq=1, **data_params):
        self.dis = dis
        self.n_xseq = n_xseq
        self.n_yseq = n_yseq
        self.x, self.y = self.rawx, self.rawy = self._get_raw_data(dataset_name, **data_params)
        self._preproc_data(**data_params)
        self._postproc_data(**data_params)
        return self.x, self.y

# def get_ae_data(self, dataset_name, n_seq = 5, **data_params):
#     y = self.get_seq_data(dataset_name, **data_params)
#     dy = self.seqdp.windowing_x(y, n_seq)
#     print(dy.shape)
#     dy = self.seqdp.normalize_window_afe(dy)
#     return dy, dy