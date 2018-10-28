#%run -m pytest
#python -m pytest
#Ctrl Shift F10 (to execute on Pycharm)

import pandas as pd
import pickle
from datetime import datetime, timedelta
import pytest
from DataFrameDict import DataFrameDict

with open('data/Pred_Cifra_csv_in_df.pkl', 'rb') as f:
    df_ops, df_history, df_op_lines = pickle.load(f)

ops = DataFrameDict(df_ops, datetime(2018, 6, 28))
ops2 = DataFrameDict(df_ops, datetime(2018, 6, 1))


def num_differences_between_df(df1, df2):
    df_test = df1.fillna(0) != df2.fillna(0)
    return df_test.sum().sum()


def test_init_parameters():

    ops_test = DataFrameDict()
    assert isinstance(ops_test, DataFrameDict)


def test_init_wrong_parameters():

    with pytest.raises(ValueError):
        ops_test = DataFrameDict('str', 'str2')


def test_assign_later_wrong_parameters():

    with pytest.raises(ValueError):
        ops_test = DataFrameDict()
        ops_test._check_and_add_new_df('str2', 'str')


def test_df_initial_equals_get_df_in_date():

    df_initial = df_ops
    df_get = ops._get_df_in_date(datetime(2018, 6, 28))
    df_getitem = ops[datetime(2018, 6, 28)]
    df_getitem_by_int = ops[0]

    assert num_differences_between_df(df_initial, df_get) == 0
    assert num_differences_between_df(df_initial, df_getitem) == 0
    assert num_differences_between_df(df_initial, df_getitem_by_int) == 0


def test_set_get():

    ops_set = DataFrameDict(df_ops, datetime(2018, 6, 1))
    ops_set[datetime(2018,1,1)] = df_ops

    df_get = ops_set[datetime(2018,1,1)]

    assert num_differences_between_df(df_ops, df_get) == 0


def test_len_ops():
    assert len(ops) == 1


def test_contains():
    assert datetime(2018, 6, 28) in ops


def test_iterator():
    for df in ops:
        assert isinstance(df, pd.DataFrame)


def test_sum_df():
    global ops
    ops = ops + ops2

    assert len(ops) == 2
    assert datetime(2018, 6, 28) in ops
    assert datetime(2018, 6, 1) in ops


def test_not_sum_equal_df_dates():

    with pytest.raises(ValueError):
        opssum = ops2 + ops2


def test_delete_index():
    global ops

    ops += DataFrameDict(df_ops, datetime(2018, 1, 1))
    del ops[0]

    len_parcial = 0
    for df in ops:
        len_parcial += len(df)

    assert len(ops) == 2
    assert len_parcial == len(ops.df_all_dates)


def test_delete_date():
    global ops

    ops += DataFrameDict(df_ops, datetime(2018, 1, 1))
    del ops[datetime(2018, 1, 1)]

    len_parcial = 0
    for df in ops:
        len_parcial += len(df)

    assert len(ops) == 2
    assert len_parcial == len(ops.df_all_dates)


def test_get_df_in_date_returns_exception():

    with pytest.raises(ValueError):
        df = ops[datetime(1000, 1, 1)]