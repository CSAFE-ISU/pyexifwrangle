import os
import pandas as pd
import pytest


from pyexifwrangle import wrangle


@pytest.fixture(scope="session")
def temp_output_dir(tmp_path_factory):
    """Make a temporary directory"""
    return tmp_path_factory.mktemp("output")


@pytest.fixture(scope='session')
def file_col_name():
    return 'SourceFile'


@pytest.fixture(scope='session')
def df(file_col_name):
    return wrangle.read_exif(path='tests/fixtures/exif.csv', file_col_name=file_col_name)


def test_check_column(df, file_col_name):
    actual = wrangle.check_columns(df=df, file_col_name=file_col_name, col_names=['Aperture'])
    expected = pd.read_csv('tests/fixtures/apertures.csv', dtype={'count': 'int64'})
    pd.testing.assert_frame_equal(actual, expected)


def test_check_column_front(df, file_col_name):
    actual = wrangle.check_columns(df=df, file_col_name=file_col_name, col_names=['Aperture'], by_camera=['Front'])
    expected = pd.read_csv('tests/fixtures/front_apertures.csv', dtype={'count': 'int64'})
    pd.testing.assert_frame_equal(actual, expected)


def test_count_images_by_camera(df, file_col_name):
    actual = wrangle.count_images_by_camera(df=df, file_col_name=file_col_name)
    expected = pd.read_csv('tests/fixtures/totals.csv', dtype={'count': 'int64'})
    pd.testing.assert_frame_equal(actual, expected)


def test_find_images_using_defaults(df, file_col_name):
    actual = wrangle.find_images(df=df, file_col_name=file_col_name, col_name='Aperture', col_values=[2.4])
    assert actual.shape[0] == 2117


def test_find_images_by_phone_camera_scene(df, file_col_name):
    actual = wrangle.find_images(df=df, file_col_name=file_col_name, col_name='Aperture', col_values=[2.2],
                                 phone='GN10_7',
                                 camera='Front', scene_type='Blank')
    assert actual.images[0] == '20230615_095320_100.jpg'


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


def test_run_checks_for_model_wo_camera_fields(df, file_col_name, temp_output_dir):
    wrangle.run_checks_for_model(df=df, file_col_name=file_col_name, model_name='Note10',
                                 all_fields=['DigitalZoomRatio', 'ExposureMode'], output_dir=temp_output_dir)
    actual = sorted(os.listdir(temp_output_dir))
    assert actual == ['Note10_DigitalZoomRatio.csv', 'Note10_ExposureMode.csv', 'Note10_image_counts.csv',
                      'Note10_missing_EXIF.csv']


def test_run_checks_for_model_w_camera_fields(df, file_col_name, temp_output_dir):
    wrangle.run_checks_for_model(df=df, file_col_name=file_col_name, model_name='Note10',
                                 all_fields=['DigitalZoomRatio', 'ExposureMode'],
                                 camera_fields=['Aperture', 'ImageSize'],
                                 cameras=['Front', 'Telephoto', 'Ultra', 'Wide'], output_dir=temp_output_dir)
    actual = sorted(os.listdir(temp_output_dir))
    assert actual == ['Note10_Aperture_Front.csv', 'Note10_Aperture_Telephoto.csv', 'Note10_Aperture_Ultra.csv',
                      'Note10_Aperture_Wide.csv', 'Note10_DigitalZoomRatio.csv', 'Note10_ExposureMode.csv',
                      'Note10_ImageSize_Front.csv', 'Note10_ImageSize_Telephoto.csv', 'Note10_ImageSize_Ultra.csv',
                      'Note10_ImageSize_Wide.csv', 'Note10_image_counts.csv', 'Note10_missing_EXIF.csv']
