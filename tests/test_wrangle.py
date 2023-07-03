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


@pytest.fixture(scope='session')
def file_col_name():
    return 'SourceFile'


def test_check_column(df, file_col_name):
    actual = wrangle.check_column(df=df, file_col_name=file_col_name, col_name='Aperture')
    expected = pd.read_csv('tests/fixtures/apertures.csv', dtype={'count': 'int64'})
    pd.testing.assert_frame_equal(actual, expected)


def test_check_column_front(df, file_col_name):
    actual = wrangle.check_column(df=df, file_col_name=file_col_name, col_name='Aperture', by_camera='Front')
    expected = pd.read_csv('tests/fixtures/front_apertures.csv', dtype={'count': 'int64'})
    pd.testing.assert_frame_equal(actual, expected)


def test_count_images_by_camera(df, file_col_name):
    actual = wrangle.count_images_by_camera(df=df, file_col_name=file_col_name)
    expected = pd.read_csv('tests/fixtures/totals.csv', dtype={'count': 'int64'})
    pd.testing.assert_frame_equal(actual, expected)


def test_get_cameras(df, file_col_name):
    assert sorted(set(wrangle.get_cameras(df=df, file_col_name=file_col_name))) == \
           ['Front', 'Telephoto', 'Ultra', 'Wide']


def test_get_models(df, file_col_name):
    assert list(set(wrangle.get_models(df=df, file_col_name=file_col_name))) == ["GN10"]


def test_get_phones(df, file_col_name):
    assert sorted(set(wrangle.get_phones(df=df, file_col_name=file_col_name))) == \
           ['GN10_1', 'GN10_10', 'GN10_2', 'GN10_3', 'GN10_4', 'GN10_5', 'GN10_6', 'GN10_7', 'GN10_8', 'GN10_9']


def test_get_scene_type(df, file_col_name):
    expected = sorted(set(wrangle.get_scene_type(df=df, file_col_name=file_col_name)))
    assert expected == ['Blank', 'Scene']
