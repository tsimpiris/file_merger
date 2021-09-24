# File Merger - v0.0.1

### Overview
A CLI tool that looks in the input folder for TXT, CSV, DXF or SHP files and outputs a merged file in the given location

### Requirements
See requirements.txt

### Inputs
+ Input folder (Folder Path)
+ Output folder
+ Input file type [txt, csv, dxf or shp]
+ Output filename (with no extension)

### Outputs
+ A merged txt, csv, dxf or shp file depending on the user inputs

### Usage
Type the following in the command line:
```shell
> merger.py -i <inputfolder> -o <output_folder> -t <txt, csv, dxf or shp> -n <filename>
```

### Note
Use the tool at your own risk as it hasn't been tested yet
