"""This module defines helper functions for using the library of parsers."""

from typing import Callable

from vivado_report_parser.tables import parse_tables_report
from vivado_report_parser.metadata import get_generating_command

# Describes the appropriate parser to use for a Vivado report file generated
# by a given Tcl command.
parsers_by_generating_command = {
    "report_power": parse_tables_report,
    "report_utilization": parse_tables_report,
}


def get_parser(report_text: str) -> Callable:
    """Returns the appropriate parser for the given report file.

    Reads the metadata section of the report_text and looks up the parser to use
    based on the name of the command that generated the report. If no parser is
    available, raises a NotImplementedError. Otherwise, returns the parser
    function.

    Args:
        report_text: The text of a Vivado report file.
    Returns:
        A Callable f such that f(report_text) succeeds and returns a dictionary
        representing the parsed report file, with semantics corresponding to the
        parser used.
    Raises:
        NotImplementedError: If this library does not implement a parser for the
          kind of report given.
    """
    # TODO Expose parser options like ambiguous_parse_strategy for parse_tables_report
    command = get_generating_command(report_text)
    parser = parsers_by_generating_command.get(command)
    if parser is None:
        raise NotImplementedError(
            "No parser is currently available for this report type."
        )
    else:
        return parser
