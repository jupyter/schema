# [Schema](https://schema.jupyter.org)

JSON schemas for Jupyter.

## Url format

```
https://schema.jupyter.org/[subproject]/[schema-path]/[version].json
```

* `[component]` can be, e.g. `jupyter-lab`, `jupyter-server`, `jupyter-hub`, `jupyter-kernel`, `jupyter-notebook`, etc.
* `[version]` defines the version of the library for which you get the schema. Underspecified versions match the latest version of the unspecified part. For example `v1` matches the latest major release, `v1.1` matches the latest minor release, and `v1.1.1` matches an exact version.

## Install

The package included in this repo installs all of Jupyter's core schemas in
Jupyter's data directory, e.g. under `share/jupyter/schemas/`.

Install this package using:
```
pip install jupyter-schemas
```

This package also includes small Python package for fetching these schemas

For example, to get a list of all installed schemas, try:
```python
import jupyter_schemas

print(jupyter_schemas.list_schemas())
```

You can fetch the contents of a schemas from disk using:
```python
# Use the schema's URI to find it
uri = "https://schema.jupyter.org/jupyter_server/events/contents_service/v1"

# Load the schema
print(jupyter_schemas.get_jupyter_schema(uri))
```


