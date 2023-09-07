import pyexifwrangle.wrangle as wrangle


# create fixture with get_exif(). Only uses three images to keep package size small.
df = wrangle.get_exif(input_dir='tests/fixtures/images', output_csv='tests/fixtures/get_exif.csv')
df.to_csv('tests/fixtures/get_exif.csv', index=False)

# make csv smaller - sample 10 images per camera and select s21_1 and s21_2 only
path = 'tests/fixtures/exif_s21.csv'
df = wrangle.read_exif(path)
df = wrangle.filename2columns(df=df,
                              columns=['model', 'phone', 'scene_type', 'camera', 'image'])
df = df.groupby(['model', 'phone', 'scene_type', 'camera']).sample(n=10).reset_index(drop=True)
keep = ['s21_1', 's21_2']
df = df.query('phone in @keep').reset_index(drop=True)
df.to_csv('tests/fixtures/exif_s21.csv', index=False)

# load smaller csv
df = wrangle.read_exif(path)
df = wrangle.filename2columns(df=df,
                              columns=['model', 'phone', 'scene_type', 'camera', 'image'])
df.to_csv('tests/fixtures/exif_s21_columns.csv', index=False)

missing = wrangle.check_missing_exif(df=df, column='Aperture').reset_index(drop=True)
missing.to_csv('tests/fixtures/missing.csv', index=False)

counts = wrangle.count_images_by_columns(df=df, columns=['model', 'phone', 'scene_type', 'camera'])
counts.to_csv('tests/fixtures/counts.csv', index=False)

aperture = wrangle.count_images_by_columns(df=df, columns=['model', 'phone', 'scene_type', 'camera', 'Aperture'],
                                           sort=['model', 'camera', 'phone', 'scene_type'])
aperture.to_csv('tests/fixtures/aperture_sorted.csv', index=False)

filtered_all = wrangle.find_images(df=df, filter_dict={'phone': 's21_1', 'Aperture': 2.2})
filtered_all.to_csv('tests/fixtures/found_images_all_columns.csv', index=False)

filtered = wrangle.find_images(df=df, filter_dict={'phone': 's21_1', 'Aperture': 2.2},
                               return_columns=['model', 'phone', 'scene_type', 'camera', 'image'])
filtered.to_csv('tests/fixtures/found_images.csv', index=False)
