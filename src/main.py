#!/usr/bin/env python3

import argparse
import os
import glob

if not __debug__:  # Dev workspace
    from src import constants, merger
    from src.constants import FileTypes
    pass
else:
    import constants, merger
    from constants import FileTypes
    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', dest='input', required=True, help='Input directory - Contains .dds or .tga files')
    parser.add_argument('--output', dest='output', required=True, help='Output directory - Outputs .gxt and .dds.phyre texture files')
    parser.add_argument('--original', dest='original', required=True, help='Directory containing the original .dds.phyre texture files')
    parser.add_argument('--psp2gxt', dest='psp2gxt', required=True, help='Executable \'psp2gxt.exe\' - This is required')
    args = parser.parse_args()

    _input = args.input
    output = args.output
    original = args.original
    psp2gxt = args.psp2gxt

    print('Out-of-Textures made by Master801')
    print('Version: {0}\n'.format(constants.VERSION))

    if not os.path.isdir(_input):
        print('Input directory does not exist!')
        return
    if not os.path.isdir(output):
        print('Output directory does not exist!')
        return
    if not os.path.isdir(original):
        print('Original directory does not exist!')
        return
    if not os.path.isfile(psp2gxt):
        print('Executable \'psp2gxt.exe\' does not exist.')
        return

    input_files = dict()
    input_files.update({FileTypes.DXT5: find_files(FileTypes.DXT5, _input)})
    input_files.update({FileTypes.ARGB8: find_files(FileTypes.ARGB8, _input)})

    original_files = find_files(FileTypes.DDS_PHYRE, original)

    matching = list()
    for a_file_type in FileTypes:
        input_file_list = input_files.get(a_file_type)

        if input_file_list is None:
            # No input files - Skip
            continue

        for a_input_file in input_file_list:
            input_separator_index = a_input_file.index(constants.FILE_PATH_SEPARATOR)

            if input_separator_index != -1:
                new_input_name = a_input_file[input_separator_index + 1:]
                pass
            else:
                new_input_name = a_input_file
                pass

            input_extension_index = new_input_name.index('.')
            if input_extension_index != -1:
                input_extension = new_input_name[input_extension_index + 1:]
                new_input_name = new_input_name[:input_extension_index]
                pass
            else:
                print('Couldn\'t find extension of input file \"{0}\"!'.format(a_input_file))
                break

            input_file_type = None
            if input_extension is not None:
                for ft in FileTypes:
                    if input_extension == ft.file_type.extension:
                        input_file_type = ft
                        break
                    continue
                pass

            if input_file_type is None:
                print('No file type detected for input file \"{0}\"!'.format(a_input_file))
                break

            for a_original_file in original_files:
                original_separator_index = a_original_file.rindex(constants.FILE_PATH_SEPARATOR)
                if original_separator_index != -1:
                    new_original_name = a_original_file[original_separator_index + 1:]
                    pass
                else:
                    new_original_name = a_original_file
                    pass

                original_extension_index = new_original_name.index('.')
                if original_extension_index != -1:
                    new_original_name = new_original_name[:original_extension_index]
                    pass

                if new_input_name == new_original_name:
                    matching.append(
                        [
                            [
                                [input_file_type, a_input_file]
                            ],
                            [
                                [FileTypes.DDS_PHYRE, a_original_file]
                            ]
                        ]
                    )
                    pass

                pass
            continue

        continue

    len_matching = len(matching)
    if len_matching > 0:
        plural = 'es'
        if len_matching is 1:
            plural = ''
            pass
        print('Found {0} match{1}\n'.format(len_matching, plural))
        pass
    else:
        print('Found no matches\n')
        return

    merger.merge_texture_files(matching, output, psp2gxt)
    return


def find_files(file_type, _dir):
    got_files = []
    for root, subdirs, files in os.walk(_dir):
        if len(files) < 1:  # Skip dirs with no files
            continue
        if isinstance(file_type, FileTypes):
            for a_file_type in glob.iglob(root + constants.FILE_PATH_SEPARATOR + '*.' + file_type.file_type.extension):
                got_files.append(a_file_type)
                continue
            pass
        continue
    return got_files


if __name__ == '__main__':
    main()
    pass
