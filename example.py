import pandas as pd

import pyexifwrangle.wrangle as wrangle

path = 'tests/fixtures/exif.csv'
file_col_name = 'SourceFile'
df = pd.read_csv(path)

folders = wrangle.get_folders(df=df, file_col_name=file_col_name)

scene_types = wrangle.get_scene_type(df=df, file_col_name=file_col_name)

models = wrangle.get_models(df=df, file_col_name=file_col_name)

total = wrangle.count_images_by_camera(df=df, file_col_name=file_col_name)

check = wrangle.check_column(df=df, file_col_name=file_col_name, col_name='Aperture', by_camera='All')
