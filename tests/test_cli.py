import logging
from pathlib import Path
from pyproject_migrator.cli import cli

import tomlkit

victim_path = Path(__file__).parent / "victim"


def test_cli(monkeypatch, capsys, caplog, snapshot):
    caplog.set_level(logging.INFO)
    monkeypatch.setattr("sys.argv", ["tool", str(victim_path)])
    cli()
    # Snip out pathnames for snapshot comparison...
    messages = sorted(m.partition(": ")[-1] for m in caplog.messages)
    assert messages == snapshot(name="log")
    assert "setuptools sections ['metadata', 'options']" in caplog.text
    assert "flake8-related sections ['flake8']" in caplog.text
    parsed = tomlkit.loads(capsys.readouterr()[0])
    assert parsed == snapshot(name="result")
