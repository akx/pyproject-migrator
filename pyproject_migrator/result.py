import dataclasses
from pathlib import Path

from pyproject_migrator import log


@dataclasses.dataclass
class Result:
    dest: dict = dataclasses.field(default_factory=dict)
    warnings: list[str] = dataclasses.field(default_factory=list)

    def warn(self, msg: str, path: Path) -> None:
        msg = f"{path}: {msg}"
        self.warnings.append(msg)
        log.warning(msg)

    def assign(self, key: str, value: object) -> None:
        dest = self.dest
        bits = key.split(".")
        final_key = bits.pop()
        for bit in bits:
            dest = dest.setdefault(bit, {})
        if final_key in dest:
            raise ValueError(f"Key {key} already exists")
        dest[final_key] = value

    def append(self, key: str, value: object) -> None:
        dest = self.dest
        bits = key.split(".")
        final_key = bits.pop()
        for bit in bits:
            dest = dest.setdefault(bit, {})
        dest.setdefault(final_key, []).append(value)
