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

    def __init__(self, seq_normalizers=None):
        """
        Initialize sequence processing env
        :param normalizator:
        :param smoothor:
        """
        self.seqdp = SeqDP()
        self.if_seq_normalized = (seq_normalizers is not None)
        self.seq_normalizers = seq_normalizers
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

    def _preproc_data(self):
        if self.if_seq_normalized:
            for norm in self.seq_normalizers: self.x = norm.fit_transform(self.x)

    def _postproc_data(self):
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
    def __init__(self, seq_normalizers=None, win_normalizer=None):
        super(MultstepPredDataFactory, self).__init__(seq_normalizers=seq_normalizers)
        self.if_win_normalized = (win_normalizer is not None)
        self.win_normalizer = win_normalizer

    def _get_raw_data(self, dataset_name, **data_params):
        self.rawx = self.get_seq_data(dataset_name, **data_params)
        y_column = data_params.get("y_column", [0])
        self.rawy = copy.copy(self.x[:, y_column])
        if len(self.rawy.shape) == 1: self.rawy = np.reshape(self.rawy, (-1, 1))
        return self.rawx, self.rawy

    def _preproc_data(self, **data_params):
        if self.if_seq_normalized:
            for norm in self.seq_normalizers:
                self.x = norm.fit_transform(self.x)
                self.y = norm.fit_transform(self.y)

    def _postproc_data(self, n_xseq, dis, n_yseq):
        self.x, self.y = self.seqdp.windowing_xy(self.x, self.y, n_xseq, dis, n_yseq=n_yseq)
        if self.if_win_normalized:
            self.x, self.y = self.win_normalizer.fit_transform(self.x, self.y)

    def inverse_data(self, x):
        if self.if_win_normalized: x = self.win_normalizer.inverse_transform(x)
        super(MultstepPredDataFactory, self).inverse_data(x)

    def get_data(self, dataset_name, n_xseq, dis, n_yseq=1, **data_params):
        self.x, self.y = self.rawx, self.rawy = self._get_raw_data(dataset_name, **data_params)
        self._preproc_data(**data_params)
        self._postproc_data(n_xseq, dis, n_yseq)
        return self.x, self.y

# def get_ae_data(self, dataset_name, n_seq = 5, **data_params):
#     y = self.get_seq_data(dataset_name, **data_params)
#     dy = self.seqdp.windowing_x(y, n_seq)
#     print(dy.shape)
#     dy = self.seqdp.normalize_window_afe(dy)
#     return dy, dy