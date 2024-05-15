
import re
from typing import Literal


def _exclude_na(func):
    def wrapper(one, *args, **kwargs):
        if not one:
            return False
        return func(one, *args, **kwargs)
    return wrapper


_MODE_ONE = Literal["is", "in", "re"]


class _OneSelect:
    @staticmethod
    def mode_one(one, base, mode_one):
        match mode_one:
            case "is":
                return _OneSelect.mode_one_is(one, base)
            case "in":
                return _OneSelect.mode_one_in(one, base)
            case "re":
                return _OneSelect.mode_one_in(one, base)
            case _:
                raise ValueError(f"invalid mode_one {mode_one}")

    @staticmethod
    @_exclude_na
    def mode_one_is(one, base):
        if base == one:
            return True

    @staticmethod
    @_exclude_na
    def mode_one_in(one, base):
        if base in one:
            return True

    @staticmethod
    @_exclude_na
    def mode_one_re(one, base):
        assert isinstance(one, str)
        pattern = re.compile(base)
        if pattern.match(one):
            return True


def one_select(one, base, mode_one: _MODE_ONE):
    if _OneSelect.mode_one(one, base, mode_one):
        return one


_MODE_LINE = Literal["direct", "first", "all", "auto"]


class _LineSelect:
    @staticmethod
    def mode_line(line, base, mode_one, mode_line):
        match mode_line:
            case "direct":
                return _LineSelect.mode_line_direct(line, base, mode_one)
            case "first":
                return _LineSelect.mode_line_first(line, base, mode_one)
            case "all":
                return _LineSelect.mode_line_all(line, base, mode_one)
            case "auto":
                mode_line = _LineSelect.mode_line_auto(line)
                return _LineSelect.mode_line(line, base, mode_one, mode_line)
            case _:
                raise ValueError(f"invalid mode_line {mode_line}")

    @staticmethod
    def mode_line_direct(line, base, mode_one):
        if _OneSelect.mode_one(line, base, mode_one):
            return [line]

    @staticmethod
    def mode_line_first(line, base, mode_one):
        assert isinstance(line, list)
        for one in line:
            if _OneSelect.mode_one(one, base, mode_one):
                return [one]

    @staticmethod
    def mode_line_all(line, base, mode_one):
        assert isinstance(line, list)
        return_line = list()
        for one in line:
            if _OneSelect.mode_one(one, base, mode_one):
                return_line.append(one)
        return return_line

    @staticmethod
    def mode_line_auto(line):
        match line:
            case list():
                return "all"
            case str():
                return "direct"
            case _:
                raise TypeError(f"mode_line: auto can't deal with {line}")


def line_select(line, base, mode_one: _MODE_ONE, mode_line: _MODE_LINE) -> list:
    return _LineSelect.mode_line(line, base, mode_one, mode_line)


if __name__ == "__main__":
    ...
