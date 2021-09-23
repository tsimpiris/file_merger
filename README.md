# File Merger v0.0.1

### Overview
A CLI tool that looks in the input folder for TXT, CSV or DXF files and outputs a merged file in the given location

### Requirements
See requirements.txt

### Developer
Ioannis Tsimpiris

### Inputs
+ Input folder (Folder Path)
+ Output folder
+ Input file type [txt, csv or dxf]
+ Output filename (with no extension)

### Outputs
+ A merged txt, csv or dxf file depending on the user inputs

### Usage
Type the following in the command line:
```shell
> merger.py -i <inputfolder> -o <output_folder> -t <txt, csv or dxf> -n <filename>
```
