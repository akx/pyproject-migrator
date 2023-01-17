# pyproject-migrator

[![PyPI - Version](https://img.shields.io/pypi/v/pyproject-migrator.svg)](https://pypi.org/project/pyproject-migrator)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyproject-migrator.svg)](https://pypi.org/project/pyproject-migrator)

-----

## What is this?

This tool helps with converting `setup.cfg` (and other configuration files such as `mypy.ini`)
to a single `pyproject.toml` file.


## Installation

You can install the project from Pip with

```console
pip install pyproject-migrator
```

but it may be more useful to use `pipx`[pipx] to run it as a tool; if you prefer to do that, just substitute
`pipx run pyproject-migrator` for `pyproject-migrator` in the examples below.

## Usage

The tool can be run against a number of files or directories, but these files are considered to be part of
the same project. The tool will then attempt to merge these into a single `pyproject.toml` file fragment.

```console
$ pyproject-migrator setup.cfg mypy.ini
```
or
```console
$ pyproject-migrator .
```

The tool will output a chunk of TOML you can copy-paste (or `>>` redirect) into your `pyproject.toml` file.

It may also output a number of warnings about configuration that could not be converted.

Some of these are because the tool does not yet support the option, but others are because there is no
direct equivalent in the TOML format. In these cases, you will need to manually convert the option.

## Supported configuration

The tool currently supports the following configuration:

* codespell (in setup.cfg)
* coverage (in setup.cfg)
* isort (in setup.cfg)
* mypy (in setup.cfg and mypy.ini)
* pylint (in setup.cfg)
* pytest (in setup.cfg)

Explicitly unsupported is

* flake8 (because it [currently explicitly does not support pyproject.toml][flake8-234])
* setuptools (because there are a number of approaches to take to map it into pyproject.toml)
* Sphinx's `build_sphinx` section
* tox (because there is no other TOML mapping than splatting INI config in there, ew)

Other tools that emit "Unknown section" currently include,
but are not limited to (based on the setup.cfgs I had at hand):

* babel (extract_messages, extractors, mappings) (see https://github.com/python-babel/babel/issues/777)
* bumpversion
* nosetests
* pbr
* prequ
* pyscaffold
* versioneer
* vpip
* zest.releaser

## License

`pyproject-migrator` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

[pipx]: https://pypa.github.io/pipx/
[flake8-234]: https://github.com/PyCQA/flake8/issues/234
