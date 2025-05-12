from enum import Enum


class SortDirection(str, Enum):
    ASCENDING = 'ascending'
    DESCENDING = 'descending'