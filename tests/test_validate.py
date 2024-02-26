import pytest

from jupyter_schemas import list_schema_paths, Schema


@pytest.mark.parametrize("schema_path", list_schema_paths())
def test_validate_schema(schema_path):
    schema = Schema(schema_path)
    schema.validate()


# TODO: tests to cover all failure modes of Schema.validate(). Will need invalid schemas to test.
