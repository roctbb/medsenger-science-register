import enum


class RecordType(str, enum.Enum):
    INTEGER = 'integer'
    FLOAT = 'float'
    STRING = 'string'
    TEXT = 'text'
    DATE = 'date'
    ENUM = 'enum'
