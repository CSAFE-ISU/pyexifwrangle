import pandas as pd

import pyexifwrangle.wrangle as wrangle

path = 'tests/fixtures/exif.csv'
file_col_name = 'SourceFile'
df = wrangle.read_exif(path=path, file_col_name=file_col_name)

total = wrangle.count_images_by_camera(df=df, file_col_name=file_col_name)
total.to_csv("tests/fixtures/totals.csv", index=False)

ap = wrangle.check_column(df=df, file_col_name=file_col_name, col_name='Aperture')
ap.to_csv("tests/fixtures/apertures.csv", index=False)

ap = wrangle.check_column(df=df, file_col_name=file_col_name, col_name='Aperture', by_camera='Front')
ap.to_csv("tests/fixtures/front_apertures.csv", index=False)
