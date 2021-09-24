import os
import sys
import glob
import argparse
import ezdxf
import fiona
import pandas as pd
from ezdxf.addons import Importer


def main():
    settings_dict = inputs()
    settings_dict = validation(settings_dict)
    merger(settings_dict)


# Initialize user inputs
def inputs():
    parser = argparse.ArgumentParser()

    # Required parameters
    parser.add_argument('-i', '--input', dest='input_folder', \
        help='Type input folder path', required=True)
    parser.add_argument('-t', '--type', dest='file_type', \
        choices=['txt', 'csv', 'dxf', 'shp'], \
        help='Type input file type: txt, csv, dxf, shp', required=True)

    # Optional parameters
    parser.add_argument('-o', '--output', dest='output_folder', \
        help='Type output folder path', required=False)
    parser.add_argument('-n', '--name', dest='file_name', \
        help='Type output filename with no extension', required=False)

    args = parser.parse_args()

    # Store parameters into dict
    settings_dict = {}
    settings_dict['INPUT_FOLDER'] = args.input_folder
    settings_dict['OUTPUT_FOLDER'] = args.output_folder
    settings_dict['FILE_TYPE'] = args.file_type
    settings_dict['FILE_NAME'] = args.file_name

    return settings_dict


# Basic input validation
def validation(settings_dict):
    if os.path.isdir(settings_dict['INPUT_FOLDER']):
        files_to_be_merged = glob.glob(os.path.join(settings_dict['INPUT_FOLDER'], f'*.{settings_dict["FILE_TYPE"]}'))

        if len(files_to_be_merged) == 1:
            print(f'Only one {settings_dict["FILE_TYPE"]} found - Needs 2 or more')
            sys.exit(1)
        elif len(files_to_be_merged) == 0:
            print(f'No {settings_dict["FILE_TYPE"]} files found')
            sys.exit(1)
        else:
            settings_dict['INPUT_FILES'] = files_to_be_merged
    else:
        print(f'{settings_dict["INPUT_FOLDER"]} is not a folder')
        sys.exit(1)

    if settings_dict['OUTPUT_FOLDER'] == None:
        settings_dict['OUTPUT_FOLDER'] = settings_dict['INPUT_FOLDER']
    else:
        if not os.path.isdir(settings_dict['OUTPUT_FOLDER']):
            try:
                os.makesdirs(settings_dict['OUTPUT_FOLDER'])
            except Exception:
                print('Unable to create output folder')
                sys.exit(1)
        else:
            if not os.access(settings_dict['OUTPUT_FOLDER'], os.W_OK):
                print('No write permission in the output folder')
                sys.exit(1)

    if settings_dict['FILE_NAME'] == None:
        settings_dict['FILE_NAME'] = f'merged.{settings_dict["FILE_TYPE"]}'
    else:
        settings_dict['FILE_NAME'] = f'{settings_dict["FILE_NAME"]}.{settings_dict["FILE_TYPE"]}'

    return settings_dict


def merger(settings_dict):
    settings_dict['OUTPUT_FILE'] = os.path.join(settings_dict['OUTPUT_FOLDER'], settings_dict['FILE_NAME'])

    try:
        if settings_dict['FILE_TYPE'] == 'txt':
            txt_merger(settings_dict)
        elif settings_dict['FILE_TYPE'] == 'csv':
            csv_merger(settings_dict)
        elif settings_dict['FILE_TYPE'] == 'dxf':
            dxf_merger(settings_dict)
        elif settings_dict['FILE_TYPE'] == 'shp':
            shapefile_merger(settings_dict)
    except Exception as e:
        print(e)
        print(f'Unable to merge {settings_dict["FILE_TYPE"]} files')


# Merge input TXTs
def txt_merger(settings_dict):
    with open(settings_dict['OUTPUT_FILE'], 'wb') as outfile:
        for f in settings_dict['INPUT_FILES']:
            with open(f, "rb") as infile:
                outfile.write(infile.read())


# Merge input CSVs
def csv_merger(settings_dict):
    combined_csv = pd.concat([pd.read_csv(f, encoding= 'unicode_escape') for f in settings_dict["INPUT_FILES"]])
    combined_csv.to_csv(settings_dict['OUTPUT_FILE'], index=False)


# Merge input DXFs
def dxf_merger(settings_dict):
    dxfs = settings_dict['INPUT_FILES']

    base_dxf = ezdxf.readfile(dxfs[0])
    del dxfs[0]

    for dxf in dxfs:
        merge_dxf = ezdxf.readfile(dxf)

        importer = Importer(merge_dxf, base_dxf)
        # import all entities from source modelspace into target modelspace
        importer.import_modelspace()
        # import all required resources and dependencies
        importer.finalize()

    base_dxf.saveas(settings_dict['OUTPUT_FILE'])


def shapefile_merger(settings_dict):
    shps = settings_dict['INPUT_FILES']

    outputfilename = os.path.basename(settings_dict['OUTPUT_FILE'])

    meta = fiona.open(shps[0]).meta
    with fiona.open(settings_dict["OUTPUT_FILE"], 'w', **meta) as output:
        for shp in shps:
            for features in fiona.open(shp):
                output.write(features)


if __name__ == '__main__':
    main()
