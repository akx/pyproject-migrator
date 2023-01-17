import argparse
import logging
import sys
from pathlib import Path

import tomlkit

from pyproject_migrator.convert import CONFIG_FILES, process_file
from pyproject_migrator.result import Result


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("src", nargs="+", help="Source files/directories")
    return ap.parse_args()


def cli() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = parse_args()
    res = Result()
    for src in args.src:
        pth = Path(src)
        if pth.is_dir():
            for config_file_name in CONFIG_FILES:
                config_file = pth / config_file_name
                if config_file.exists():
                    process_file(res, config_file)
        elif pth.is_file():
            process_file(res, pth)
    tomlkit.dump(res.dest, sys.stdout)
