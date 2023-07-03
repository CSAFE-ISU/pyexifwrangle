import pandas as pd

import pyexifwrangle.wrangle as wrangle

path = 'tests/fixtures/exif.csv'
df = pd.read_csv(path)

folders = wrangle.get_folders(df=df)

scene_types = wrangle.get_scene_type(df=df)

models = wrangle.get_models(df=df)

phones = wrangle.get_phones(df=df)
