import pyexifwrangle.wrangle as wrangle


path = 'tests/fixtures/exif.csv'
file_col_name = 'SourceFile'
df = wrangle.read_exif(path, file_col_name=file_col_name)

all_fields = ['DigitalZoomRatio', 'ExposureMode']
camera_fields = ['Aperture', 'ImageSize']
wrangle.run_checks_for_model(df=df, file_col_name=file_col_name, model_name='Note10',
                             all_fields=all_fields, camera_fields=camera_fields, output_dir='data')
