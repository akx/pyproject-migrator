import logging
from pathlib import Path
from pyproject_migrator.cli import cli

import tomlkit

victim_path = Path(__file__).parent / "victim"


def test_cli(monkeypatch, capsys, caplog):
    caplog.set_level(logging.INFO)
    monkeypatch.setattr("sys.argv", ["tool", str(victim_path)])
    cli()
    assert "setuptools sections ['metadata', 'options']" in caplog.text
    assert "flake8-related sections ['flake8']" in caplog.text
    parsed = tomlkit.loads(capsys.readouterr()[0])
    assert parsed == {
        "tool": {
            "isort": {"profile": "black", "multi_line_output": 3},
            "pytest": {
                "ini_options": {
                    "norecursedirs": ["bower_components", "node_modules", "foo", "bar"],
                    "doctest_optionflags": [
                        "NORMALIZE_WHITESPACE",
                        "IGNORE_EXCEPTION_DETAIL",
                        "ALLOW_UNICODE",
                    ],
                    "filterwarnings": ["error", "default:Exception ignored.*FileIO.*"],
                }
            },
            "mypy": {
                "python_version": "3.5",
                "check_untyped_defs": False,
                "no_implicit_optional": True,
                "warn_unused_configs": True,
                "warn_redundant_casts": False,
                "warn_unused_ignores": False,
                "warn_no_return": True,
                "warn_return_any": True,
                "warn_unreachable": True,
                "implicit_reexport": False,
                "strict_equality": True,
                "show_error_context": True,
                "show_column_numbers": True,
                "show_error_codes": True,
                "pretty": True,
                "overrides": [{"module": "colors", "ignore_missing_imports": True}],
            },
        }
    }
