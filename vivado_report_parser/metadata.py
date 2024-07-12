'''Provides functions for parsing the metadata headers of Vivado report files.'''
import re


def parse_metadata(report_text: str) -> dict:
    '''Parses the metadata section at the top of Vivado report files.
    
    Args:
        report_text: The full text of a Vivado report file.
    Returns:
        A dictionary whose keys are the metadata properties described in the
        table at the top of the file. For example,

        ---------------------------------------------
        | ...              : ...
        | Date             : Wed Jul 10 12:18:20 2024
        | ...              : ...
        ---------------------------------------------

        gets parsed as:

        {
            'Date': 'Wed Jul 10 12:18:20 2024',
            ... 
        }
    '''
    match = re.search(r'-+\r?\n(?P<metadata>(?:\|.*\r?\n)*)-+', report_text)
    assert match is not None, 'regex should match metadata section of report'
    metadata_text = match['metadata']
    lines = metadata_text.strip().split('\n')
    metadata = {}
    for line in lines: 
        [key, value] = line.split(':', 1) # Split at only the first ':'
        metadata[key.strip(' |')] = value.strip()

    return metadata


def get_generating_command(report_text: str) -> str:
    '''Return the Tcl command used to generate the given report.'''
    return parse_metadata(report_text)['Command'].split()[0]

