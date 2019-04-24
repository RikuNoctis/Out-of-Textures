#!/usr/bin/env python3

import subprocess

if not __debug__:
    from src import constants
    pass
else:
    import constants
    pass


def convert_to_gxt(input_file: str, output_file: str, psp2gxt: str):
    subprocess.call(
        [
            constants.WINE,  # Wine, if running on Linux
            psp2gxt,  # Executable

            # Arguments - No whitespaces allowed
            '-v',
            '-i', input_file,
            '-o', output_file
        ],

        stderr=None,
        stdin=None,
        stdout=None
    )
    print('(Probably) wrote gxt file \'{0}\''.format(output_file))
    return
