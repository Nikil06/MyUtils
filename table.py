"""
This module implements a table mapping.
"""
import json
from typing import Any, Literal, Optional, Callable
from pprint import pformat
import datetime
import decimal
import collections


class NonSupportedType(TypeError):
    """Exception for non-supported data types."""


class MissingDataError(ValueError):
    """Exception for missing data."""


class DuplicateValueError(ValueError):
    """Exception for duplicate values."""


class InvalidTypeError(TypeError):
    """Exception for invalid data types."""


class NullValueError(ValueError):
    """Exception for null values."""


class TableColumn:
    """Represents a column in a table."""
    _repr_to_type = {
        '<int>': int, '<float>': float,  # Numeric types
        '<str>': str,  # String types
        '<list>': list, '<tuple>': tuple,  # Sequence types
        '<dict>': dict,  # Mapping types
        '<bool>': bool,  # Boolean types
        '<None>': None,  # Null type
        # Date & Time types
        '<datetime.datetime>': datetime.datetime, '<datetime.date>': datetime.date, '<datetime.time>': datetime.time,
        # Decimal type
        '<decimal.Decimal>': decimal.Decimal,
        # Binary types
        '<bytes>': bytes, '<bytearray>': bytearray,
        # Collection types
        '<collections.Counter>': collections.Counter, '<collections.OrderedDict>': collections.OrderedDict,
    }
    _type_to_repr = {_type: _repr for _repr, _type in _repr_to_type.items()}

    def __init__(self, name: str, data_type: type, has_default: bool = False, default_data: Optional[Any] = None,
                 is_nullable: bool = False, is_primary_key: bool = False, is_unique: bool = False,
                 is_indexed: bool = False) -> None:
        """Initializes a TableColumn instance.

        Args:
            name (str): The name of the column.
            data_type (type): The data type of the column.
            has_default (bool): Whether the column has a default value.
            default_data (Optional[Any]): The default value of the column.
            is_nullable (bool): Whether the column allows NULL values.
            is_primary_key (bool): Whether the column is a primary key.
            is_unique (bool): Whether the column values must be unique.
            is_indexed (bool): Whether the column is indexed.
        """
        if is_primary_key:
            is_nullable = False
            is_unique = is_indexed = True

        self.name = name
        if data_type in TableColumn._type_to_repr.keys():
            self.data_type = data_type
        else:
            raise NonSupportedType(
                f"data_type: '{data_type}' is not supported. Use only from: \n{', '.join(TableColumn._type_to_repr.keys())}")
        self.is_nullable = is_nullable
        self.is_primary_key = is_primary_key
        self.is_unique = is_unique
        self.is_indexed = is_indexed
        self.has_default = has_default

        if has_default:
            is_default_valid, error = self.is_data_valid(default_data)
            if is_default_valid:
                self._default_data = default_data
            else:
                raise error

        if self.is_unique:
            self._unique_data = set()

    def is_data_valid(self, data: Any) -> tuple[bool, Optional[Exception]]:
        """Check if the given data is valid for the column.

        Args:
            data (Any): The data to be validated.

        Returns:
            Tuple[bool, Optional[Exception]]: Whether the data is valid or not and an error if not.
        """
        if data is not None and not isinstance(data, self.data_type):
            return False, InvalidTypeError(
                f"Invalid Data Type. Column '{self.name}' only accepts '{self.data_type}' type data. '{type(data)}' is not accepted")

        if data is None and not self.is_nullable:
            return False, NullValueError(f"Data cannot be null. Column '{self.name}' doesn't allow None values.")

        if self.is_unique and not self.is_nullable:
            if data in self._unique_data:
                return False, DuplicateValueError(
                    f"Data: '{data}' is not Unique. Given data already exists in the Column: '{self.name}'.")
        elif self.is_unique and self.is_nullable:
            if data is not None and data in self._unique_data:
                return False, DuplicateValueError(
                    f"Data: '{data}' is not Unique. Given data already exists in the Column: '{self.name}'.")

        return True, None

    def add_to_column(self, data: Any) -> None:
        """Add data to the column, updating unique data if applicable.

        Args:
            data (Any): The data to be added.
        """
        if self.is_unique:
            self._unique_data.add(data)

    def remove_from_column(self, data: Any) -> None:
        """Remove data from the column, updating unique data if applicable.

        Args:
            data (Any): The data to be removed.
        """
        if self.is_unique:
            if data in self._unique_data:
                self._unique_data.remove(data)
            else:
                raise MissingDataError(f"Data: {data} cannot be removed as it does not exist in Column: '{self.name}'.")

    @property
    def default_data(self) -> Any:
        """Get the default data of the column if the column has default or raises an exception.

        Returns:
            Any: The default data.
        """
        if self.has_default:
            return self._default_data
        else:
            raise ValueError(f"Column '{self.name}' does not have default data.")

    def get_column_info(self) -> str:
        """Get information about the column.

        Returns:
            str: Information about the column.
        """
        ret_str = f"<TableColumn> {self.name}\n"
        ret_str += f"\tname: {self.name}\n"
        ret_str += f"\thas_default: {self.has_default}"
        ret_str += f", default_data: {self.default_data}\n" if self.has_default else "\n"
        ret_str += f"\tis_nullable: {self.is_nullable}, is_unique: {self.is_unique}\n"
        ret_str += f"\tis_primary_key: {self.is_primary_key}, is_indexed: {self.is_indexed}\n"
        ret_str += f"\tunique_data: {self._unique_data}" if self.is_unique else ""
        return ret_str

    def as_dict(self) -> dict:
        """Convert the column to a dictionary.

        Returns:
            dict: A dictionary representation of the column.
        """
        ret_dict = {
            'name': self.name,
            'data_type': TableColumn._type_to_repr[self.data_type],  # Convert type to string for serialization
            'is_nullable': self.is_nullable,
            'is_primary_key': self.is_primary_key,
            'is_unique': self.is_unique,
            'is_indexed': self.is_indexed,
            'has_default': self.has_default
        }
        if self.has_default:
            ret_dict['default_data'] = self.default_data

        return ret_dict

    @classmethod
    def from_dict(cls, column_data: dict) -> 'TableColumn':
        """Create a TableColumn instance from a dictionary.

        Args:
            column_data (dict): The dictionary representation of the column.

        Returns:
            TableColumn: The created TableColumn instance.
        """
        column_data['data_type'] = cls._repr_to_type[column_data['data_type']]
        return cls(**column_data)

    def clone(self) -> 'TableColumn':
        """Create a clone of the column.

        Returns:
            TableColumn: The cloned TableColumn instance.
        """
        default_data = self.default_data if self.has_default else None
        return TableColumn(self.name, self.data_type, self.has_default, default_data, self.is_nullable,
                           self.is_primary_key, self.is_unique, self.is_indexed)


class Table:
    """Represents a table."""

    def __init__(self, columns: list[TableColumn]) -> None:
        """Initialize a Table instance.

        Args:
            columns (List[TableColumn]): List of columns in the table.
        """
        self.columns = columns
        self.degree = len(columns)

        for column in columns:
            if column.is_primary_key:
                self.primary_column = column
                self.primary_column.is_nullable = False
                self.primary_column.is_unique = self.primary_column.is_indexed = True
                break
        else:
            raise ValueError(
                "No primary column found in table. Atleast one of the columns should have is_primary_key=True.")

        self.primary_hash: dict[Any, dict[str, Any]] = {}
        self.index_hash: dict[str, dict[Any, set]] = {column.name: {} for column in self.columns if
                                                      column.is_indexed and not column.is_primary_key}
        self.row_order: list[Any] = []

    def add_row(self, take_default: bool = False, **row_dict: dict[str, Any]) -> None:
        """Add a row to the table.

        Args:
            take_default (bool): Whether to use default values for missing data.
            **row_dict (Any): Key-value pairs representing the row data.
        """
        for column in self.columns:
            if column.name not in row_dict and take_default:
                row_dict[column.name] = column.default_data
            elif column.name not in row_dict and not take_default:
                raise MissingDataError(f"Missing value for column: {column.name}")

            is_data_valid, error = column.is_data_valid(row_dict[column.name])
            if not is_data_valid:
                raise error

        for column in self.columns:
            column.add_to_column(row_dict[column.name])

        self.row_order.append(row_dict[self.primary_column.name])
        self.update_row_hash(row_dict)

    def delete_row(self, primary_key: Any) -> None:
        """Delete a row from the table.

        Args:
            primary_key (Any): The primary key of the row to be deleted.
        """
        if primary_key in self.primary_hash:
            row_dict = self.primary_hash.pop(primary_key)
            for column in self.columns:
                column.remove_from_column(row_dict[column.name])
                if column.is_indexed and column != self.primary_column:
                    value = row_dict[column.name]
                    self.index_hash[column.name][value].remove(primary_key)
                    if len(self.index_hash[column.name][value]) < 1:
                        del self.index_hash[column.name][value]
            self.row_order.remove(primary_key)
        else:
            raise MissingDataError(f"No row with primary key '{primary_key}' found.")

    def update_row(self, primary_key: Any, **row_dict: dict[str, Any]) -> None:
        """Update a row in the table.

        Args:
            primary_key (Any): The primary key of the row to be updated.
            **row_dict (Any): Key-value pairs representing the updated row data.
        """
        row_dict[self.primary_column.name] = primary_key

        if not (primary_key in self.primary_hash):
            raise MissingDataError(f"No row with primary key '{primary_key}' found.")

        old_row = self.primary_hash[primary_key]
        new_row = {}
        for column in self.columns:
            if column.name not in row_dict:
                new_row[column.name] = old_row[column.name]
            else:
                new_row[column.name] = row_dict[column.name]

        for column in self.columns:
            old_value = old_row[column.name]
            new_value = new_row[column.name]

            if column.is_indexed and old_value != new_value:
                column.remove_from_column(old_value)
                column.add_to_column(new_value)
                if new_value in self.index_hash[column.name]:
                    self.index_hash[column.name][new_value].add(primary_key)
                else:
                    self.index_hash[column.name][new_value] = {primary_key}

                if len(self.index_hash[column.name][old_value]) == 1:
                    self.index_hash[column.name].pop(old_value)
                else:
                    self.index_hash[column.name][old_value].remove(primary_key)

        self.primary_hash[primary_key] = new_row

    def update_row_hash(self, row_dict: dict[str, Any]) -> None:
        """Update the hash when a row is added or updated.

        Args:
            row_dict: Key-value pairs representing the row data.
        """
        primary_key = row_dict[self.primary_column.name]
        for column_name, column_hash in self.index_hash.items():
            if column_name != self.primary_column.name:
                value = row_dict[column_name]
                if value in column_hash:
                    self.index_hash[column_name][value].add(primary_key)
                else:
                    self.index_hash[column_name][value] = {primary_key}
        self.primary_hash[row_dict[self.primary_column.name]] = row_dict

    def update_full_hash(self) -> None:
        """Update the entire hash for all rows in the table."""
        for row in self.primary_hash.values():
            self.update_row_hash(row)

    def save_table_as_json(self, path: str) -> None:
        """Save the table as a JSON file.

        Args:
            path (str): The path to the JSON file.
        """
        data = {
            'columns': [col.as_dict() for col in self.columns],
            'rows': list(self.primary_hash.values()),
            'row_order': self.row_order
        }

        with open(path, 'w') as file:
            json.dump(data, file)

    @classmethod
    def load_table_from_json(cls, path: str) -> 'Table':
        """Load a table from a JSON file.

        Args:
            path (str): The path to the JSON file.

        Returns:
            Table: The loaded table.
        """
        with open(path, 'r') as file:
            data = json.load(file)

            columns_data = data.get('columns', [])
            columns = [TableColumn.from_dict(col_data) for col_data in columns_data]
            table = cls(columns=columns)

            for row in data.get('rows', []):
                table.add_row(**row)

            table.row_order = data['row_order']
            return table

    def get_table_render(self, style: Literal['simple', 'sql_style'] = "sql_style") -> str:
        """Get a rendered representation of the table.

        Args:
            style (Literal['simple', 'sql_style']): The rendering style.

        Returns:
            str: The rendered table.
        """
        return RenderTable(self, style).get_render()

    def get_table_info(self) -> str:
        """Get a detailed information string about the table.

        Returns:
            str: Information about the table.
        """
        ret_str = f"{'=' * 75}\n"
        ret_str += f"Primary Hash {'-' * 30}\n"
        ret_str += f"{pformat(self.primary_hash, indent=4, compact=True)}\n"
        ret_str += f"Index Hash {'-' * 30}\n"
        ret_str += f"{pformat(self.index_hash, indent=4, compact=True)}\n"
        ret_str += f"Columns {'-' * 30}\n"
        for column in self.columns:
            ret_str += column.get_column_info() + "\n"
        ret_str += f"{'=' * 75}"

        return ret_str

    def sort_rows(self, key: Optional[Callable[[dict], Any]] = None, reverse=False) -> None:
        """Sort the rows of the table.

        Args:
            key (Optional[Callable[[dict], Any]]): A function to determine the sorting key.
            reverse (bool): Whether to sort in reverse order.
        """
        self.row_order = sorted(self.row_order, key=lambda k: key(self.primary_hash[k]), reverse=reverse)

    def filter_rows(self, condition: Callable[[dict], bool],
                    output_format: Literal['TableFormat', 'ListFormat'] = 'TableFormat') -> 'Table' | list[dict[str, Any]]:
        """Filter the rows of the table based on a condition.

        Args:
            condition (Callable[[dict], bool]): The filtering condition.
            output_format (Literal['TableFormat', 'ListFormat']): Whether to return a table with filtered rows or a list of
            filtered row dictionaries.

        Returns:
            Table or list[dict]: A new table containing the filtered rows or a list of filtered row dictionaries.
        """
        filtered_keys = [key for key in self.row_order if condition(self.primary_hash[key])]
        filtered_rows = [self.primary_hash[key] for key in filtered_keys]

        if output_format == 'TableFormat':
            ret_table = Table(columns=[column.clone() for column in self.columns])
            for row in filtered_rows:
                ret_table.add_row(**row)
            return ret_table

        elif output_format == 'ListFormat':
            return filtered_rows


class RenderTable:
    """Renders a table in various styles."""

    def __init__(self, table: Table, style: Literal['simple', 'sql_style']) -> None:
        """Initialize a RenderTable instance.

        Args:
            table (Table): The table to be rendered.
            style (Literal[SIMPLE_STYLE, SQL_STYLE]): The rendering style.
        """
        self.headers = [column.name for column in table.columns]

        rows = [table.primary_hash[primary_key] for primary_key in table.row_order]
        self.rows = [list(map(str, [row[col] for col in self.headers])) for row in rows]

        self.column_widths = [max(len(cell) for cell in column) for column in zip(self.headers, *self.rows)]

        self.style = style

        self.number_of_columns = table.degree

    def get_render(self) -> str:
        """Get the rendered representation of the table based on the selected style.

        Returns:
            str: The rendered table.
        """
        match self.style:
            case 'simple':
                return self.render_simple()
            case 'sql_style':
                return self.render_sql_style()

    def render_simple(self) -> str:
        """Render the table in a simple style.

        Returns:
            str: The rendered table.
        """
        col_sep = ['| ', ' | ', ' |']
        row_sep = [' ', '=', ' ']
        rows = []
        seperator = row_sep[0] + (sum(self.column_widths) +
                                  len(col_sep[1]) * self.number_of_columns - 1) * row_sep[1] + row_sep[2]
        if self.headers:
            header_row = [f"{self.headers[i]:<{self.column_widths[i]}}" for i in range(self.number_of_columns)]
            header = col_sep[0] + col_sep[1].join(header_row) + col_sep[2]
            rows += [seperator, header, seperator]
        else:
            rows += [seperator]

        for row in self.rows:
            row_data = [f"{row[i]:<{self.column_widths[i]}}" for i in range(self.number_of_columns)]
            rows.append(col_sep[0] + col_sep[1].join(row_data) + col_sep[2])

        rows += [seperator]

        return "\n".join(rows)

    def render_sql_style(self) -> str:
        """Render the table in SQL style.

        Returns:
            str: The rendered table.
        """
        col_sep = ['| ', ' | ', ' |']
        row_sep = ['+-', '-', '-+']
        rows = []
        seperator = row_sep[0] + (sum(self.column_widths) +
                                  len(col_sep[1]) * self.number_of_columns - 3) * row_sep[1] + row_sep[2]
        if self.headers:
            header_row = [f"{self.headers[i]:<{self.column_widths[i]}}" for i in range(self.number_of_columns)]
            header = col_sep[0] + col_sep[1].join(header_row) + col_sep[2]
            rows += [seperator, header, seperator]
        else:
            rows += [seperator]

        for row in self.rows:
            row_data = [f"{row[i]:<{self.column_widths[i]}}" for i in range(self.number_of_columns)]
            rows.append(col_sep[0] + col_sep[1].join(row_data) + col_sep[2])

        rows += [seperator]

        return "\n".join(rows)
