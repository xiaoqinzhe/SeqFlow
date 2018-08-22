"""
Base Model
"""
import config.config as config
from util.util import check_path

__all__=["BaseModel", "KerasModel"]

class BaseModel:
    def __init__(self, input_dim, output_dim, is_train=True, saved_model_path="default/default.h5"):
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.is_train = is_train
        self.saved_model_path = config.configs['model_stored_path'] + saved_model_path
        check_path(self.saved_model_path, is_create=True)
        self.compiled = False
        self.init_model()
        if not is_train:
            self.restore_model()

    def init_model(self):
        return

    def compile_model(self):
        return

    def train(self, x, y=None):
        return

    def test(self, x, y=None):
        return

    def predict(self, x):
        return None

    def restore_model(self):
        return

class KerasModel(BaseModel):
    def __init__(self, input_dim, output_dim, is_train=True, saved_model_path="default/default.h5"):
        self.model = None
        super(KerasModel, self).__init__(input_dim, output_dim, is_train, saved_model_path)

    def init_model(self):
        return

    def compile_model(self, optimizer="adam", loss="mse", metrics=None):
        self.model.compile(optimizer=optimizer, loss=loss, metrics=metrics)

    def train(self, x, y, batch_size=None, epochs=1, verbose=1, callbacks=None, validation_split=0, shuffle=True, saved_model=True):
        if not self.is_train: return
        if not self.compiled: self.compile_model()
        self.model.fit(x, y, batch_size=batch_size, epochs=epochs, verbose=verbose, callbacks=callbacks, validation_split=validation_split, shuffle=shuffle)
        if saved_model: self.model.save(self.saved_model_path)

    def test(self, x, y, verbose=1):
        return self.model.evaluate(x, y, verbose=verbose)

    def predict(self, x):
        return self.model.predict(x)

    def restore_model(self):
        self.model.load_weights(self.saved_model_path)

    def get_model(self):
        return self.model