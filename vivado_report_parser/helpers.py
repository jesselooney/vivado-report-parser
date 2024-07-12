'''This module defines helper functions for using the library of parsers.'''

from typing import Callable

from vivado_report_parser.tables import parse_tables_report
from vivado_report_parser.metadata import get_generating_command

# Describes the appropriate parser to use for a Vivado report file generated
# by a given Tcl command.
parsers_by_generating_command = {
    'report_power': parse_tables_report,
    'report_utilization': parse_tables_report,
}


def get_parser(report_text: str) -> Callable:
    '''Returns the appropriate parser for the given report file.'''
    # TODO Expose parser options like ambiguous_parse_strategy for parse_tables_report
    command = get_generating_command(report_text)
    return parsers_by_generating_command.get(command)

