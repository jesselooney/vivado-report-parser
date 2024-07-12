'''Provides a function for parsing Vivado tables-style report files.'''

from enum import Enum
import re


class TableKind(Enum):
    TABLE = 1
    DICTIONARY = 2


def parse_table(table_text: str, *,
                ambiguous_parse_strategy: TableKind = TableKind.DICTIONARY) -> list | dict:
    '''Parses a Vivado power report-style table.

    Parses a kind of text-based table found in Vivado report files such as
    utilization or power reports. These tables have borders made of the
    following characters: '+', '-', and '|', and may either be true "table"
    tables or "dictionary" tables.
        True tables have a header on their second line, offset by table
    dividers above and below, that specifies the column names. The remaining
    rows represent records that specify values for these columns.
        Dictionary tables are not really tables. Rather, they have two columns,
    with the left column specifying keys and the right column specifying the
    corresponding values for those keys.
        A two-column table with only one interior line may either be an empty
    true table or a dictionary table with one key. Which parse strategy is
    used is controlled by the value of parse_ambiguous_as.

    Args:
        table_text: A string containing the Vivado report table to parse. The
          first and last characters must each be '+'.
        ambiguous_parse_strategy: The parse strategy to use if it is impossible
          to determine which kind of table the given string represents.

    Returns:
        A list of dictionaries mapping column names to values for each record in
        the table if it is a true table, or a dictionary mapping keys in the
        left column to values in the right column if the table is a dictionary
        table. For example, if table_text is a true table:

        [
            {'id': '0', 'name': 'foo'},
            {'id': '1', 'name': 'bar'}
        ]

        If instead table_text is a dictionary table:

        {
            'id': '0',
            'name': 'foo'
        }

        In either case, the keys and values of the dictionaries are always
        strings. These strings are taken directly from the input string and
        receive no treatment other than stripping the whitespace off the ends.
    '''
    # TODO: replace assertions with exceptions
    assert table_text[0] == '+' and table_text[-1] == '+', "A table must start and end with a '+'"
    lines = table_text.split('\n')
    assert len(lines) >= 3, 'A table should have at least three lines: two dividers and one line of content.'

    # Remove the divider lines at the top and bottom of the table.
    del lines[0]
    del lines[-1]

    # If the second line inside the table is NOT a divider line, then we expect
    # the table to be a dictionary table. If this is not the case, we know the
    # table is a true table and we can safely delete the divider line. If
    # instead the table does not have a second line, it may either be a
    # dictionary or a true table, so we withold judgment until later parsing.
    table_kind: TableKind | None = None
    if len(lines) > 1:
        if not set(lines[1].strip()).issubset(set('+-')):
            table_kind = TableKind.DICTIONARY
        else:
            table_kind = TableKind.TABLE
            del lines[1]

    # Split and clean the remaining lines so that rows becomes a 2D list
    # containing every cell in the table.
    rows = []
    for line in lines:
        fields = line.strip('|\r\n').split('|')
        rows.append([field.strip() for field in fields])

    column_count = len(rows[0])
    assert all(len(row) == column_count for row in rows), 'Every row should have the same number of columns.'
    if table_kind == TableKind.DICTIONARY:
        assert column_count == 2, 'A dictionary table should have exactly two columns.'

    # We can resolve the table's kind if it has more than two columns.
    if table_kind is None and column_count > 2:
        table_kind = TableKind.TABLE

    # If we still don't know what kind of table this is, then use the
    # ambiguous_parse_strategy.
    if table_kind is None:
        table_kind = ambiguous_parse_strategy

    if table_kind == TableKind.DICTIONARY:
        return dict(rows)
    elif table_kind == TableKind.TABLE:
        table_header = rows[0]
        return [dict(zip(table_header, row)) for row in rows[1:]]
    else:
        # This case is impossible unless we change the TableKind enum.
        raise Exception(f'table_kind was neither TableKind.DICTIONARY nor TableKind.TABLE: {table_kind=}')


def parse_tables_report(report_text: str,
                        ambiguous_parse_strategy: TableKind = TableKind.DICTIONARY) -> dict:
    '''Parses a Vivado tables-style report.

    Parses a Vivado report in the "tables" style, such as a utilization or
    power report. This style of report has a metadata section at the top which
    is common to many kinds of Vivado report. The metadata section is ignored
    by this function, but can be extracted using the parse_metadata function in
    the metadata module.
        The remainder of this style of report consists of a table of contents
    and then some sections with numbered headers underlined by hyphens. Each
    section may contain a table. Each section that has a table will be reported
    by this function.

    Args:
        report_text: The full text of a Vivado tables-style report file.
        ambiguous_parse_strategy: The parse strategy used for all ambiguous
          tables found in the report. See the _parse_table function in this
          module for details.
    Returns:
        A dictionary whose keys are the names (excluding section number) of
        those sections in the report which have a table in them. The value for
        a given key is either a list or a dictionary; it is the return value
        of _parse_table applied to the text of the table found in the section
        the key represents. The section hierarchy is flattened---for example, if
        the section '1. Settings' has a subsection '2.1 Environment', then the
        resulting dictionary will look like:

        {
            'Settings': ...,
            'Environment': ...
        }

        so that both section and subsection live at the top level of the
        dictionary.
    '''
    # The following regex attempts to find tables inside sections of the
    # report, which generally look like this:
    #
    #
    #     3.1 Section Title
    #     -----------------
    #
    #     +-----------+-----------+-----+
    #     | col1_name | col2_name | ... |
    #     +-----------+-----------+-----+
    #     | col1_val1 | col2_val2 | ... |
    #     | col2_val2 | col2_val2 | ... |
    #     | ...       | ...       | ... |
    #     +-----------+-----------+-----+
    #
    matches = re.findall(
        r'\n[\d\.]* (?P<section_title>.+)\r?\n-+\r?\n\r?\n(?P<section_table>(?:[+|].*\r?\n)+)',
        report_text
    )

    return {title.strip(): parse_table(table.strip()) for title, table in matches}
