import os
import pandas as pd


def check_columns(df, file_col_name, col_names, by_camera='All'):
    """
    Count the number of images grouped by phone, camera, scene type, and col_names.

    :param df: Pandas data frame of EXIF data
    :param file_col_name: (str) Name of the column that contains the file names
    :param col_names: List of column(s) to group images by in addition to phone, camera, scene type
    :param by_camera: (str) Either 'All', 'Front', 'Telephoto', 'Ultra', or 'Wide'
    :return: Pandas data frame
    """

    # create data frame
    phones = get_phones(df=df, file_col_name=file_col_name)
    cameras = get_cameras(df=df, file_col_name=file_col_name)
    scene_types = get_scene_type(df=df, file_col_name=file_col_name)
    new_df = pd.DataFrame({'phones': phones, 'cameras': cameras, 'scene_types': scene_types})

    for col in col_names:
        new_df['new'] = get_column(df=df, col_name=col)
        new_df = new_df.rename(columns={'new': col})

    # filter by camera
    if by_camera != 'All':
        new_df = new_df.query("cameras == @by_camera")

    # group and count
    new_df = new_df.groupby(new_df.columns.to_list()).size().reset_index()
    new_df = new_df.rename(columns={0: 'count'})
    return new_df


def check_missing_exif(df, file_col_name):
    # filter for images with no aperture
    df = df.query('Aperture.isnull()', engine='python')

    # create data frame
    phones = get_phones(df=df, file_col_name=file_col_name)
    cameras = get_cameras(df=df, file_col_name=file_col_name)
    scene_types = get_scene_type(df=df, file_col_name=file_col_name)
    images = get_images(df=df, file_col_name=file_col_name)
    df = pd.DataFrame({'phones': phones, 'cameras': cameras, 'scene_types': scene_types, 'images': images})

    return df


def count_images_by_camera(df, file_col_name):
    """
    Count the number of images grouped by phone, camera, and scene type.

    :param df: Pandas data frame of EXIF data
    :param file_col_name: (str) Name of the column that contains the file names
    :return: Pandas data frame
    """

    # create data frame
    phones = get_phones(df=df, file_col_name=file_col_name)
    cameras = get_cameras(df=df, file_col_name=file_col_name)
    scene_types = get_scene_type(df=df, file_col_name=file_col_name)
    df = pd.DataFrame({'phones': phones, 'cameras': cameras, 'scene_types': scene_types})

    # group and count
    df = df.groupby(['phones', 'cameras', 'scene_types']).size().reset_index()
    df = df.rename(columns={0: 'count'})
    return df


def get_cameras(df, file_col_name):
    """Get cameras as a list from the files names in the exif data frame, assuming that the folders use the
    naming convention '<model> <device> <camera>- <scene type>'"""
    folders = get_folders(df=df, file_col_name=file_col_name)
    strings = [s.split('-')[0].strip() for s in folders]
    return [s.split(' ')[2].strip() for s in strings]


def get_column(df, col_name):
    """Extract column from data frame as list"""
    return df[col_name].to_list()


def get_folders(df, file_col_name):
    """Extract folder names as a list from the files names in the exif data frame"""
    files = get_column(df=df, col_name=file_col_name)
    return [s.split('/')[-2] for s in files]


def get_images(df, file_col_name):
    """Extract image names as a list from the files names in the exif data frame"""
    files = get_column(df=df, col_name=file_col_name)
    return [s.split('/')[-1] for s in files]


def get_models(df, file_col_name):
    """Get phone models as a list from the files names in the exif data frame, assuming that the folders use the
    naming convention '<model> <device> <camera>- <scene type>'"""
    folders = get_folders(df=df, file_col_name=file_col_name)
    strings = [s.split('-')[0].strip() for s in folders]
    return [s.split(' ')[0].strip() for s in strings]


def get_phones(df, file_col_name):
    """Get phone (model_device) as a list from the files names in the exif data frame, assuming that the folders use the
    naming convention '<model> <device> <camera>- <scene type>'"""
    folders = get_folders(df=df, file_col_name=file_col_name)
    strings = [s.split('-')[0].strip() for s in folders]
    return [s.split(' ')[0].strip() + '_' + s.split(' ')[1].strip() for s in strings]


def get_scene_type(df, file_col_name):
    """Extract scene type from folder names, assuming that the folders use the naming convention '<model> <device>
    <camera>-
    <scene type>'"""
    folders = get_folders(df=df, file_col_name=file_col_name)
    return [s.split('-')[-1].strip() for s in folders]


def find_images(df, file_col_name, col_name, col_values, phone=None, camera=None, scene_type=None):
    """
    :param df: Pandas data frame of EXIF data
    :param file_col_name: (str) Name of the column that contains the file names
    :param col_name: (str) Name of column to filter
    :param col_values: List of values to filter for
    :param phone: Optional list of phones to filter for
    :param camera: Optional list of cameras to filter for
    :param scene_type: Optional list of scene types to filter for
    :return: Pandas data frame
    """
    # create data frame
    phones = get_phones(df, file_col_name)
    cameras = get_cameras(df, file_col_name)
    scene_types = get_scene_type(df, file_col_name)
    images = get_images(df, file_col_name)
    col = get_column(df, col_name)
    df = pd.DataFrame({'phones': phones, 'cameras': cameras, 'scene_types': scene_types, 'col': col, 'images': images})

    # optional filters
    if phone is not None:
        df = df.query('phones in @phone')
    if camera is not None:
        df = df.query('cameras in @camera')
    if scene_type is not None:
        df = df.query('scene_types in @scene_type')

    # filter
    df = df.query('col in @col_values').reset_index()
    return df


def read_exif(path, file_col_name):
    df = pd.read_csv(path)

    files = get_column(df=df, col_name=file_col_name)
    images = pd.Series([s.split('/')[-1].strip() for s in files])

    # drop file names that start with '.'
    df = df[~images.str.startswith('.')]

    return df


def run_checks_for_model(df, file_col_name, model_name, all_fields, camera_fields, cameras, output_dir):
    """
    :param df: Pandas data frame of EXIF data for a single model of phone
    :param file_col_name: Name of column that contains the image file names
    :param model_name: Name of phone model
    :param all_fields: List of name(s) of columns to check with images from all camera types grouped together
    :param camera_fields: List of name(s) of columns to check with images grouped by camera type
    :param cameras: List of cameras
    :param output_dir: File path to directory that will store output csv files
    """

    # Are any images missing EXIF data?
    missing = check_missing_exif(df=df, file_col_name=file_col_name)
    missing.to_csv(os.path.join(output_dir, model_name + '_missing_EXIF.csv'), index=False)

    # Count images per phone, camera, and scene type
    total = count_images_by_camera(df=df, file_col_name=file_col_name)
    total.to_csv(os.path.join(output_dir, model_name + '_image_counts.csv'), index=False)

    # Check other fields
    for f in all_fields:
        temp_df = check_columns(df=df, file_col_name=file_col_name, col_names=[f], by_camera='All')
        temp_df.to_csv(os.path.join(output_dir, model_name + '_' + f + '.csv'), index=False)

    # Check aperture and image size by camera
    for f in camera_fields:
        for c in cameras:
            temp_df = check_columns(df=df, file_col_name=file_col_name, col_names=[f], by_camera=c)
            temp_df.to_csv(os.path.join(output_dir, model_name + '_' + f + '_' + c + '.csv'), index=False)
