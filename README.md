# Out-of-Textures


## Info

Automatically converts and cuts `.tga` and `.dds` texture files that are extracted from the original `.dds.phyre` into new `.dds.phyre` texture files.<br/>
Make sure that the input `.tga` and `.dds` files correspond to the original `.dds.phyre` texture files or the output texture file will not be usable.<br/>
Texture file `.tga` is for `ARGB8` `.dds.phyre` texture files.<br/>
Texture file `.dds` is for `DXT5` `.dds.phyre` texture files.

Please give credit where it's due if using my tool.


## Before using:

Install [Python](https://www.python.org/downloads/) (project is built with [3.7.3](https://www.python.org/downloads/release/python-373/))</br>


## Usage

#### Arguments:
- `--input` [`INPUT_DIRECTORY`] - Input directory - Contains .dds or .tga files
- `--output` [`OUTPUT_DIRECTORY`] - Output directory - Outputs .gxt and .dds.phyre texture files
- `--original` [`ORIGINAL_DIRECTORY`] - Directory containing the original .dds.phyre texture files
- `--psp2gxt` [`psp2gxt_EXECUTABLE`] - Executable \'psp2gxt.exe\' - This is required

#### Example usage:
```
python main.py --input INPUT_DIRECTORY --original ORIGINAL_DIRECTORY --output OUTPUT_DIRECTORY --psp2gxt psp2gxt.exe
```

#### Tested on:
- Linux (Fedora 29) - Python 3.7.3
