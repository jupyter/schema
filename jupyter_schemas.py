import logging
import typing
import json
import pathlib
import urllib.parse
from jupyter_core.paths import jupyter_path

__version__ = "0.1"


class JupyterSchemaNotFound(Exception):
    """A exception type for missing schemas"""


class JupyterSchemaSourceNotFound(Exception):
    """"""


ROOT_SCHEMA_PATH: pathlib.Path = pathlib.Path(jupyter_path()[0]) / "schema"


def schema_path(schema_uri: str) -> pathlib.Path:
    parts = urllib.parse.urlparse(schema_uri)
    # Make sure this is a relative path
    relpath = parts.path.lstrip("/")
    return (ROOT_SCHEMA_PATH / relpath).with_suffix(".json")


def get_jupyter_schema(schema_uri: str) -> str:
    """Returns the schema as a string."""
    path = schema_path(schema_uri)
    if not path.exists():
        raise JupyterSchemaNotFound(f"Could not locate schema {schema_uri}")
    return path.read_text()


def list_schema_paths(project: typing.Optional[str] = None) -> typing.List[str]:
    """Return a list of all found Jupyter schema filepaths."""
    project_path = ROOT_SCHEMA_PATH
    if project:
        project_path /= project

    if not project_path.exists():
        raise JupyterSchemaSourceNotFound(f"Could not locate schemas for {project}.")

    return [str(f) for f in project_path.rglob("*") if f.is_file()]


def list_schemas(project: typing.Optional[str] = None) -> typing.List[str]:
    """Return a list of all found Jupyter schema URIs."""
    schema_files = list_schema_paths()
    schema_uris = []
    for fpath in schema_files:
        try:
            with open(fpath, "r") as f:
                schema = json.load(f)
                schema_uris.append(schema["$id"])
        except KeyError:
            logging.warning(f"Could not find an ID/URI in {fpath}.")
            pass
    return schema_uris
