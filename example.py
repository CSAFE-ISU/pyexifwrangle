import pyexifwrangle.wrangle as wrangle


test_df = wrangle.get_exif(input_dir='tests/fixtures/images', output_csv='tests/fixtures/get_exif.csv')


path = 'tests/fixtures/exif_s21.csv'
filename_col = 'SourceFile'

df = wrangle.read_exif(path, filename_col=filename_col)
df = wrangle.filename2columns(df=df, filename_col=filename_col,
                              columns=['model', 'phone', 'scene_type', 'camera', 'image'])

missing = wrangle.check_missing_exif(df=df, column='Aperture').reset_index(drop=True)

counts = wrangle.count_images_by_columns(df=df, columns=['model', 'phone', 'scene_type', 'camera'])

checks = wrangle.count_images_by_columns(df=df,
                                         columns=['model', 'phone', 'scene_type', 'camera', 'Aperture', 'ImageSize'],
                                         sort=['model', 'camera', 'phone', 'scene_type'])
