import pandas as pd
import pytest


from pyexifwrangle import wrangle


# @pytest.fixture(scope="session")
# def temp_main_dir(tmp_path_factory):
#     """Make a temporary directory"""
#     return tmp_path_factory.mktemp("main_dir")


@pytest.fixture(scope='session')
def df():
    return pd.read_csv('tests/fixtures/exif.csv')


def test_get_scene_type(df):
    expected = sorted(set(wrangle.get_scene_type(df=df)))
    assert expected == ['Blank', 'Scene']


def test_get_models(df):
    assert list(set(wrangle.get_models(df=df))) == ["GN10"]


def test_get_phones(df):
    assert sorted(set(wrangle.get_phones(df=df))) == \
           ['GN10_1', 'GN10_10', 'GN10_2', 'GN10_3', 'GN10_4', 'GN10_5', 'GN10_6', 'GN10_7', 'GN10_8', 'GN10_9']
