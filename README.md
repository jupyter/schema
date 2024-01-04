# [Schema](https://schema.jupyter.org)

JSON schemas for Jupyter.

## Url format

```
https://schema.jupyter.org/[subproject]/[schema-path]/[version].json
```

* `[component]` can be, e.g. `jupyter-lab`, `jupyter-server`, `jupyter-hub`, `jupyter-kernel`, `jupyter-notebook`, etc.
* `[version]` defines the version of the library for which you get the schema. Underspecified versions match the latest version of the unspecified part. For example `v1` matches the latest major release, `v1.1` matches the latest minor release, and `v1.1.1` matches an exact version.

## Install

```
pip install jupyter-schema
```
