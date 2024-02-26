import logging
import typing
import json
import jsonschema
import pathlib
import urllib.parse
from jupyter_core.paths import jupyter_path

__version__ = "0.1"


class JupyterSchemaNotFound(Exception):
    """A exception type for missing schemas"""


class JupyterSchemaSourceNotFound(Exception):
    """"""


ROOT_SCHEMA_PATH: pathlib.Path = pathlib.Path(jupyter_path()[0]) / "schema"
ROOT_SCHEMA_URI: str = "https://schema.jupyter.org"


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


class Schema:
    """A Jupyter schema"""

    def __init__(self, filename: str) -> None:
        """Load a schema from JSON (.json), TOML (.toml) or YAML (.yaml) file.

        Parameters
        ----------
        filename : str
            Name of file containing schema.

        TODO: support loading from URI not just local filename.
        """
        self._filename = filename
        self._dict: dict[str, typing.Any] = {}

        suffix = pathlib.Path(filename).suffix
        if suffix == ".json":
            self._load_json()
        else:
            raise ValueError(f"Unrecognised file extension on {filename}")

    def _load_json(self):
        with open(self._filename, "r") as f:
            self._dict = json.load(f)

    def validate(self) -> None:
        """Validate this schema, raising an exception if invalid."""

        # TODO: Better consider type and text of exceptions.

        # Initially all schemas are written against the 2020-12 Draft.
        if not (meta_schema := self._dict.get("$schema")):
            raise RuntimeError(f"Schema {self._filename} does not contain '$schema'")
        elif meta_schema != "https://json-schema.org/draft/2020-12/schema":
            raise RuntimeError(
                f"Schema {self._filename} contains incorrect '$schema': {meta_schema}")

        jsonschema.Draft202012Validator.check_schema(self._dict)

        # Local schema filename must be consistent with the $id (published URI) property.
        if not (id := self._dict.get("$id")):
            raise RuntimeError(f"Schema {self._filename} must contain an '$id'")

        relative_path = pathlib.Path(self._filename).relative_to(ROOT_SCHEMA_PATH)
        expected_id = urllib.parse.urljoin(ROOT_SCHEMA_URI, str(relative_path))
        if id != expected_id:
            raise RuntimeError(f"Inconsistent schema path {self._filename} and URI {id}")

        # Schema path relative to root must contain version number exactly once.
        if not (version := self._dict.get("version")):
            raise RuntimeError(f"Schema {self._filename} must contain a 'version'")

        if (count := relative_path.parts.count(f"v{version}")) != 1:
            raise RuntimeError(
                f"Schema path {relative_path} must contain version number once not {count} times")
