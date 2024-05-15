
import re

import numpy as np
import pandas as pd

from encode_individual import *


class Encoder:
    def __init__(self, data: pd.Series):
        self.data = data.copy()

    @staticmethod
    def _return_self(func):
        def wrapper(self, *args, **kwargs):
            out = func(self, *args, kwargs)
            if out:
                return out
            return self
        return wrapper

    @staticmethod
    def _assert_series(func):
        def wrapper(self, *args, **kwargs):
            assert isinstance(self.data, pd.Series)
            return func(self, *args, **kwargs)
        return wrapper

    @staticmethod
    def _assert_df(func):
        def wrapper(self, *args, **kwargs):
            assert isinstance(self.data, pd.DataFrame)
            return func(self, *args, **kwargs)
        return wrapper

    @_return_self
    def copy(self):
        self.data = self.data.copy()

    @_return_self
    @_assert_series
    def split(self, sep):
        self.data = self.data.str.split(sep)

    @_return_self
    @_assert_series
    def ones_select(self, base, mode_one):
        self.data.apply(one_select, base=base, mode_one=mode_one)

    @_return_self
    @_assert_series
    def lines_select(self, base, mode_one, mode_line):
        self.data.apply(line_select, base=base, mode_one=mode_one, mode_line=mode_line)

    @_return_self
    @_assert_series
    def one_hot(self):
        self.data = pd.get_dummies(self.data)
        print(f"the columns of {self} is:/n{self.data.columns}")

    @_return_self
    def show(self):
        print(self.data)

    def end(self):
        return self.data

