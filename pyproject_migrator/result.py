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
        dest, final_key = self._find_dest(key)
        if final_key in dest:
            raise ValueError(f"Key {key} already exists")
        dest[final_key] = value

    def append(self, key: str, value: object) -> None:
        dest, final_key = self._find_dest(key)
        dest.setdefault(final_key, []).append(value)

    def merge(self, t_key: str, vals: dict, *, path: Path) -> None:
        dest, final_key = self._find_dest(t_key)
        dest = dest.setdefault(final_key, {})
        for key, value in vals.items():
            if isinstance(value, list):
                if key in dest:
                    self.warn(
                        f"Appending values in {t_key}->{key}; make sure the order is correct",
                        path,
                    )
                dest.setdefault(key, []).extend(value)
            elif isinstance(value, dict):
                dest.setdefault(key, {}).update(value)
            else:
                if key in dest:
                    self.warn(
                        f"Overwriting {t_key}->{key} (previously {dest[key]!r}) with {value!r}",
                        path,
                    )
                dest[key] = value

    def _find_dest(self, key: str) -> tuple[dict, str]:
        dest = self.dest
        bits = key.split(".")
        final_key = bits.pop()
        for bit in bits:
            dest = dest.setdefault(bit, {})
        return dest, final_key
