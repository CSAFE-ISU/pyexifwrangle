import pyexifwrangle.wrangle as wrangle


path = 'tests/fixtures/exif.csv'
file_col_name = 'SourceFile'
df = wrangle.read_exif(path, file_col_name=file_col_name)

# Are any images missing EXIF data?
missing = wrangle.check_missing_exif(df=df)

# Do all cameras have 100 images?
total = wrangle.count_images_by_camera(df=df, file_col_name=file_col_name)

# Is the aperture the same for each type of camera?
front = wrangle.check_column(df=df, file_col_name=file_col_name, col_name='Aperture', by_camera='Front')
telephoto = wrangle.check_column(df=df, file_col_name=file_col_name, col_name='Aperture', by_camera='Telephoto')
wide = wrangle.check_column(df=df, file_col_name=file_col_name, col_name='Aperture', by_camera='Wide')
ultra = wrangle.check_column(df=df, file_col_name=file_col_name, col_name='Aperture', by_camera='Ultra')
