import os
import pandas as pd
import pytest


from pyexifwrangle import wrangle


# @pytest.fixture(scope="session")
# def temp_output_dir(tmp_path_factory):
#     """Make a temporary directory"""
#     return tmp_path_factory.mktemp("output")


@pytest.fixture(scope='session')
def filename_col():
    return 'SourceFile'


@pytest.fixture(scope='session')
def df(filename_col):
    return wrangle.read_exif(path='tests/fixtures/exif_s21.csv', filename_col=filename_col)


def test_filename2columns(df, filename_col):
    """Check that filename2columns() adds the correct columns."""
    actual = wrangle.filename2columns(df=df, filename_col=filename_col, columns=['model', 'phone', 'scene_type',
                                                                                 'camera', 'image'])
    expected = pd.read_csv('tests/fixtures/exif_s21_columns.csv')
    pd.testing.assert_frame_equal(actual, expected, check_dtype=False)


def test_check_missing_exif(df):
    actual = wrangle.check_missing_exif(df=df, column='Aperture').reset_index(drop=True)
    # change dtype from object to int64 or float64 so test passes
    actual['ImageHeight'] = actual['ImageHeight'].astype('int64')
    actual['ImageWidth'] = actual['ImageWidth'].astype('int64')
    actual['MaxApertureValue'] = actual['MaxApertureValue'].astype('float64')
    actual['Megapixels'] = actual['Megapixels'].astype('float64')
    actual['ScaleFactor35efl'] = actual['ScaleFactor35efl'].astype('float64')
    actual['SubSecTimeDigitized'] = actual['SubSecTimeDigitized'].astype('float64')
    actual['ThumbnailLength'] = actual['ThumbnailLength'].astype('float64')
    actual['ThumbnailOffset'] = actual['ThumbnailOffset'].astype('float64')
    actual['XResolution'] = actual['XResolution'].astype('float64')
    # load expected
    expected = pd.read_csv('tests/fixtures/missing.csv')
    pd.testing.assert_frame_equal(actual, expected, check_dtype=False)


def test_count_images_by_columns(df):
    actual = wrangle.count_images_by_columns(df=df, columns=['model', 'phone', 'scene_type', 'camera'])
    expected = pd.read_csv('tests/fixtures/counts.csv')
    pd.testing.assert_frame_equal(actual, expected)


def test_count_images_by_columns_sorted(df):
    actual = wrangle.count_images_by_columns(df=df, columns=['model', 'phone', 'scene_type', 'camera', 'Aperture'],
                                             sort=['model', 'camera', 'phone', 'scene_type'])
    expected = pd.read_csv('tests/fixtures/aperture_sorted.csv')
    pd.testing.assert_frame_equal(actual, expected)

# def test_check_column(df, filename_col):
#     actual = wrangle.check_columns(df=df, filename_col=filename_col, col_names=['Aperture'])
#     expected = pd.read_csv('tests/fixtures/apertures.csv', dtype={'count': 'int64'})
#     pd.testing.assert_frame_equal(actual, expected)


# def test_check_column_front(df, filename_col):
#     actual = wrangle.check_columns(df=df, filename_col=filename_col, col_names=['Aperture'], by_camera=['Front'])
#     expected = pd.read_csv('tests/fixtures/front_apertures.csv', dtype={'count': 'int64'})
#     pd.testing.assert_frame_equal(actual, expected)




# def test_find_images_using_defaults(df, filename_col):
#     actual = wrangle.find_images(df=df, filename_col=filename_col, col_name='Aperture', col_values=[2.4])
#     assert actual.shape[0] == 2117


# def test_find_images_by_phone_camera_scene(df, filename_col):
#     actual = wrangle.find_images(df=df, filename_col=filename_col, col_name='Aperture', col_values=[2.2],
#                                  phone='GN10_7',
#                                  camera='Front', scene_type='Blank')
#     assert actual.images[0] == '20230615_095320_100.jpg'


# def test_get_cameras(df, filename_col):
#     assert sorted(set(wrangle.get_cameras(df=df, filename_col=filename_col))) == \
#            ['Front', 'Telephoto', 'Ultra', 'Wide']
#
#
# def test_get_models(df, filename_col):
#     assert list(set(wrangle.get_models(df=df, filename_col=filename_col))) == ["GN10"]
#
#
# def test_get_phones(df, filename_col):
#     assert sorted(set(wrangle.get_phones(df=df, filename_col=filename_col))) == \
#            ['GN10_1', 'GN10_10', 'GN10_2', 'GN10_3', 'GN10_4', 'GN10_5', 'GN10_6', 'GN10_7', 'GN10_8', 'GN10_9']
#
#
# def test_get_scene_type(df, filename_col):
#     expected = sorted(set(wrangle.get_scene_type(df=df, filename_col=filename_col)))
#     assert expected == ['Blank', 'Scene']
#
#
# def test_run_checks_for_model_wo_camera_fields(df, filename_col, temp_output_dir):
#     wrangle.run_checks_for_model(df=df, filename_col=filename_col, model_name='Note10',
#                                  all_fields=['DigitalZoomRatio', 'ExposureMode'], output_dir=temp_output_dir)
#     actual = sorted(os.listdir(temp_output_dir))
#     assert actual == ['Note10_DigitalZoomRatio.csv', 'Note10_ExposureMode.csv', 'Note10_image_counts.csv',
#                       'Note10_missing_EXIF.csv']
#
#
# def test_run_checks_for_model_w_camera_fields(df, filename_col, temp_output_dir):
#     wrangle.run_checks_for_model(df=df, filename_col=filename_col, model_name='Note10',
#                                  all_fields=['DigitalZoomRatio', 'ExposureMode'],
#                                  camera_fields=['Aperture', 'ImageSize'],
#                                  cameras=['Front', 'Telephoto', 'Ultra', 'Wide'], output_dir=temp_output_dir)
#     actual = sorted(os.listdir(temp_output_dir))
#     assert actual == ['Note10_Aperture_Front.csv', 'Note10_Aperture_Telephoto.csv', 'Note10_Aperture_Ultra.csv',
#                       'Note10_Aperture_Wide.csv', 'Note10_DigitalZoomRatio.csv', 'Note10_ExposureMode.csv',
#                       'Note10_ImageSize_Front.csv', 'Note10_ImageSize_Telephoto.csv', 'Note10_ImageSize_Ultra.csv',
#                       'Note10_ImageSize_Wide.csv', 'Note10_image_counts.csv', 'Note10_missing_EXIF.csv']
