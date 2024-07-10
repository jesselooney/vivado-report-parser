import re


def parse_metadata(report_str: str):
    match = re.search('-+\n(?P<metadata>(?:\\|.*\n)*)-+', report_str)
    metadata_str = match.group('metadata')
    entries = metadata_str.split('\n')
    metadata = {}
    # Exclude the empty final element created by the trailing newline.
    for entry in entries[:-1]:
        [key, value] = entry.split(':', 1) # Split at only the first ':'
        metadata[key.strip(' |')] = value.strip()

    return metadata
