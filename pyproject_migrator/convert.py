import configparser
import re
from pathlib import Path

from pyproject_migrator.result import Result

CONFIG_FILES = {"setup.cfg", "mypy.ini"}


def massage_value(value, key, *, ws_split_keys):
    if key in ws_split_keys:
        return [v for v in value.split() if v]
    if isinstance(value, str):
        if "\n" in value:
            return [v for v in value.splitlines() if v]
        if value.lower() == "true":
            return True
        if value.lower() == "false":
            return False
        if value.isnumeric():
            return int(value)
    return value


def translate_config(config, *, ws_split_keys=()):
    return {
        key: massage_value(value, key, ws_split_keys=ws_split_keys)
        for key, value in config.items()
    }


FLAKE8_SECTION_RE = re.compile(r"flake8.*|pep8|py(code|doc)style|pep257")
TOX_SECTION_RE = re.compile(r"testenv.*|tox.*")
SETUPTOOLS_SECTION_RE = re.compile(
    r"[bs]dist.*|"
    r"aliases|"
    r"build_ext|"
    r"egg_info|"
    r"entry_points|"
    r"extras|"
    r"files|"
    r"install|"
    r"metadata|"
    r"options.*|"
    r"paths|"
    r"upload_docs|"
    r"wheel"
)


def process_config_file(res: Result, pth: Path):
    config = configparser.ConfigParser()
    config.read(pth)
    setuptools_sections = {}
    flake8_sections = {}
    tox_sections = {}

    for section in config.sections():
        if section == "mypy":
            res.assign("tool.mypy", translate_config(config[section]))
            continue

        if section.startswith("mypy-"):
            res.append(
                "tool.mypy.overrides",
                {
                    "module": section[5:],
                    **translate_config(config[section]),
                },
            )
            continue

        if section.endswith("pytest"):
            translated = translate_config(
                config[section],
                ws_split_keys={"addopts", "norecursedirs", "doctest_optionflags"},
            )
            res.assign("tool.pytest.ini_options", translated)
            continue
        if section.endswith("isort"):
            translated = translate_config(
                config[section],
                ws_split_keys={"skip"},
            )
            res.assign("tool.isort", translated)
            continue

        if section.startswith("coverage"):
            res.assign(
                f"tool.{section.replace(':', '.')}", translate_config(config[section])
            )
            continue

        if section.startswith("pylint"):
            res.assign(
                f"tool.{section.replace(':', '.')}", translate_config(config[section])
            )
            continue

        if section == "codespell":
            res.assign("tool.codespell", translate_config(config[section]))
            continue

        if section == "build_sphinx":
            res.warn(
                "The build_sphinx section is not supported, "
                "and support will be removed with Sphinx 7 anyway. "
                "See https://www.sphinx-doc.org/en/master/usage/advanced/setuptools.html",
                pth,
            )
            continue

        if TOX_SECTION_RE.match(section):
            tox_sections[section] = config[section]
            continue

        if FLAKE8_SECTION_RE.match(section):
            flake8_sections[section] = config[section]
            continue

        if SETUPTOOLS_SECTION_RE.match(section):
            setuptools_sections[section] = config[section]
            continue

        res.warn(f"unknown section {section}", path=pth)

    if setuptools_sections:
        # TODO: we could allow setting a target toolset and port these.
        res.warn(
            f"setuptools sections {sorted(setuptools_sections.keys())}; porting depends on which toolset to use. "
            "For example, hatch (https://pypi.org/project/hatch/) can port metadata to pyproject.toml.",
            path=pth,
        )

    if flake8_sections:
        res.warn(
            f"flake8-related sections {sorted(flake8_sections.keys())}; porting depends on which toolset to use. "
            "If you're transitioning to ruff, see https://pypi.org/project/flake8-to-ruff/",
            path=pth,
        )

    if tox_sections:
        res.warn(
            f"tox-related sections {sorted(tox_sections.keys())}; tox does not currently support pyproject.toml "
            f"except by way of `legacy_tox_in`; see https://tox.wiki/en/4.3.3/config.html#pyproject-toml",
            path=pth,
        )


def process_file(res: Result, pth: Path):
    if pth.name in CONFIG_FILES:
        process_config_file(res, pth)
        return
    raise NotImplementedError(f"Can't process {pth}")
