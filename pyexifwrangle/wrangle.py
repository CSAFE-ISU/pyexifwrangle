def get_files(df):
    """Get list of files names from the exif data frame"""
    return df.SourceFile.to_list()


def get_folders(df):
    """Extract folder names as a list from the files names in the exif data frame"""
    files = get_files(df=df)
    return [s.split('/')[-2] for s in files]


def get_models(df):
    """Get phone models as a list from the files names in the exif data frame, assuming that the folders use the
    naming convention '<model> <device> <camera>- <scene type>'"""
    folders = get_folders(df=df)
    strings = [s.split('-')[0].strip() for s in folders]
    return [s.split(' ')[0].strip() for s in strings]


def get_phones(df):
    """Get phone (model_device) as a list from the files names in the exif data frame, assuming that the folders use the
    naming convention '<model> <device> <camera>- <scene type>'"""
    folders = get_folders(df=df)
    strings = [s.split('-')[0].strip() for s in folders]
    return [s.split(' ')[0].strip() + '_' + s.split(' ')[1].strip() for s in strings]


def get_scene_type(df):
    """Extract scene type from folder names, assuming that the folders use the naming convention '<model> <device>
    <camera>-
    <scene type>'"""
    folders = get_folders(df=df)
    return [s.split('-')[-1].strip() for s in folders]
