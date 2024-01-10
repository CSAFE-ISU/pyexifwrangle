# Wrangle EXIF Data in Python

A Python package for wrangling EXIF data extracted from images using Phil Harvey's EXIFTool.

## Set-up
### Install pyexifwrangle with pip

```bash
$ pip install pyexifwrangle
```

### Install Phil Harvey's EXIFTool
Install Phil Harvey's EXIFTool from https://exiftool.org/. This site has installation instructions if you need them.

## Usage
### Get EXIF data
After installing EXIFTool, you can extract EXIF data from every image in a folder, including subdirectories, save the 
results in a csv file, and return the results in a Pandas DataFrame. 

The *filename_col* is the name of the column that contains the image filenames. The function `get_exif` extracts and saves the EXIF data using ExifTool then runs the function `read_exif` to load the EXIF data into a Pandas DataFrame. The filename column is checked for files that start with "." and if any such files are found they are deleted from the DataFrame.

```python
import pyexifwrangle.wrangle as wr

df = wr.get_exif(input_dir='path/to/images', output_csv='path/to/output.csv', filename_col='SourceFile')
```

### Load the EXIF data
If you already used `get_exif` to extract and save the EXIF to a csv file, you can use `read_exif` to
load the csv file into a DataFrame. In this case, the output of `get_exif` is the same as the output
from `read_exif`.

```python
import pyexifwrangle.wrangle as wr

df = wr.read_exif(path='path/to/output.csv', filename_col='SourceFile', encoding='utf-8')
```
The function `read_exif` uses the Pandas package to load the csv file into a DataFrame. The parameter *filename_col* is the name of the column that contains the filenames of the images. Any filenames that start with "." are deleted from the DataFrame.

The function `read_exif` uses the `pandas.read_csv` to load the csv file. In most cases the default encoding 'utf-8' worked on the EXIF data, but occasionally I have needed to change the encoding. The encoding argument is passed onto `pandas.read_csv`. 

### Make columns from folder names
I often organize my images into folders and sub-folders, and I usually want to capture the folder names in columns in the DataFrame. The function `filename2columns` does this for me. 

For example one of my projects has the following folder tree:
```
├── Samsung_phones  # main directory
│   ├── s21  # model
│   │   ├── s21_1  # phone name
│   │   │ 	├── blank  # scene type
│   │   │	│	├── front  # camera
│   │   │	│	│	├──image1.jpg
│   │   │	│	│	├──image2.jpg
│   │   │	│	│	├──...
│   │   │	│	├── telephoto
│   │   │	│	│	├──image1.jpg
│   │   │	│	│	├──image2.jpg
│   │   │	│	│	├──...
│   │   │	│	├── ultra
│   │   │	│	│	├──image1.jpg
│   │   │	│	│	├──image2.jpg
│   │   │	│	│	├──...
│   │   │	│	├── wide
│   │   │	│	│	├──image1.jpg
│   │   │	│	│	├──image2.jpg
│   │   │	│	│	├──...
│   │   │ 	├── natural
│   │   │	│	├── front  
│   │   │	│	├── telephoto
│   │   │	│	├── ultra
│   │   │	│	├── wide
│   │   ├── s21_2 
│   │   │ 	├── blank
│   │   │	│	├── front
│   │   │	│	├── telephoto
│   │   │	│	├── ultra
│   │   │	│	├── wide
│   │   │ 	├── natural
│   │   │	│	├── front  
│   │   │	│	├── telephoto
│   │   │	│	├── ultra
│   │   │	│	├── wide
```
Extract the folder names from the images' absolute filepaths and make a new column for each folder.
```python
df = wr.filename2columns(df=df, filename_col='SourceFile', columns=['model', 'phone', 'scene_type', 'camera', 'image'])
```

### Search for missing EXIF data
Find images missing a specific EXIF data column. For example, search the DataFrame for images that don't have an Aperture.
```python
missing = wr.check_missing_exif(df=df, column='Aperture')
```

### Count images per group(s)
Group images by column(s) and count the number of images per group.
```python
counts = wr.count_images_by_columns(df=df, columns=['model', 'phone', 'scene_type', 'camera'])
```
Optionally, you can sort the output of *count_images_by_columns*
```python
counts_sorted = wr.count_images_by_columns(df=df, columns=['model', 'phone', 'scene_type', 'camera'], sorted=
['phone', 'camera', 'Aperture'])
```

### Wipe GPS Information from the EXIF data
Delete all GPS related tags from an image's EXIF data with `wipe_gps`. This function removes GPS information from the EXIF data stored in the image file itself. The image itself is not changed; only its EXIF data is changed.

This function DOES NOT delete GPS information from an EXIF csv file that has already been saved with `get_exif`, nor does it delete GPS information from a DataFrame that is currently loaded in Python. Rerun `get_exif` to generate an EXIF csv file and DataFrame without GPS data.
```python
wr.wipe_gps(path='path/to/image.jpg')
```
