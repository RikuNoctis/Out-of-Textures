#!/usr/bin/env python3

import os

if not __debug__:
    from src.constants import FileType, FileTypes
    from src import constants, gxt
    pass
else:
    from constants import FileType, FileTypes
    import constants, gxt
    pass


def merge_texture_files(matching: list, output_dir: str, psp2gxt: str):
    for match in matching:
        input_match = match[0][0]
        original_match = match[1][0]

        print('Merging input texture file \"{0}\" and original texture file \"{1}\"'.format(input_match[1], original_match[1]))

        output_file_gxt = convert_to_gxt(input_match, output_dir, psp2gxt)
        phyre_header = extract_phyre_header(original_match[0].file_type, original_match[1])

        if phyre_header is None:
            print('Failed to merge texture files! Original: \"{0}\", Input: \"{1}\"'.format(original_match[1], input_match[1]))
            continue

        inject_phyre_header(original_match[1], output_dir, input_match, phyre_header, output_file_gxt)
        continue
    return


def convert_to_gxt(input_match: list, output_dir: str, psp2gxt: str):
    input_file = input_match[1]

    input_separator_index = input_file.index(constants.FILE_PATH_SEPARATOR)
    if input_separator_index != -1:
        output_file = output_dir + constants.FILE_PATH_SEPARATOR + input_file[input_separator_index + 1:]
        pass
    else:
        output_file = output_dir + constants.FILE_PATH_SEPARATOR + input_file
        pass

    output_file_extension_index = output_file.index('.')
    if output_file_extension_index != -1:
        output_file = output_file[:output_file_extension_index]
        pass

    output_file += '.gxt'

    gxt.convert_to_gxt(input_file, output_file, psp2gxt)
    return output_file


def check_phyre_header(original_file_buffer, original_file_type: FileType):
    if (original_file_buffer[0x00:len(original_file_type.header)] != original_file_type.header) or original_file_type != FileTypes.DDS_PHYRE.file_type:
        print('Given original file is not a .dds.phyre file! Original File: {0}'.format(original_file_type))
        return 1
    return 0


def extract_phyre_header(original_file_type: FileType, original_file: str):
    opened_original_file = open(original_file, 'r+b')
    original_file_buffer = opened_original_file.read()
    opened_original_file.close()

    code = check_phyre_header(original_file_buffer, original_file_type)
    if code == 1:  # Error code
        print('Could not extract the phyre header due to Original file not being a phyre file!')
        print('Original file: {0}'.format(original_file))
        return None

    indexed = original_file_buffer.index(b'GXT')

    if indexed == -1:
        print('Could not find index of bytes \'GXT\'! Original file: {0}'.format(original_file))
        return None

    print('Found bytes \'GXT\' at index {0} in original file \"{1}\"'.format('0x' + hex(indexed)[2:].upper(), original_file))

    extracted_phyre_header = original_file_buffer[:indexed]
    return extracted_phyre_header


def inject_phyre_header(original_file_path: str, output_dir: str, input_match: list, phyre_header: bytes, output_file_gxt_path: str):
    output_file_gxt_bytes = open(output_file_gxt_path, 'r+b')
    output_gxt_read_bytes: bytes = output_file_gxt_bytes.read()
    output_file_gxt_bytes.close()

    output_dds_phyre_bytes = phyre_header + output_gxt_read_bytes

    original_file_index = original_file_path.rindex('/')
    if original_file_index != -1:
        output_file_dds_phyre_path = original_file_path[original_file_index + 1:]
        pass
    else:
        output_file_dds_phyre_path = original_file_path
        pass

    output_file_dds_phyre_path = output_dir + constants.FILE_PATH_SEPARATOR + output_file_dds_phyre_path

    if os.path.isfile(output_file_dds_phyre_path):  # dds.phyre texture file already exists - delete
        os.remove(output_file_dds_phyre_path)
        pass

    output_file_dds_phyre = open(output_file_dds_phyre_path, 'x+b')
    output_file_dds_phyre.write(output_dds_phyre_bytes)
    output_file_dds_phyre.close()

    print('Wrote .dds.phyre texture file \"{0}\"\n'.format(output_file_dds_phyre_path))
    pass
