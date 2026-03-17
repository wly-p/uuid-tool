import argparse
import sys
from enum import StrEnum

from .core import UUIDType, generate, validate


class _Cmd(StrEnum):
    GENERATE = "generate"
    VALIDATE = "validate"


_CMD_ALIASES: dict[_Cmd, list[str]] = {
    _Cmd.GENERATE: ["gen"],
    _Cmd.VALIDATE: ["val"],
}

_VERSION_CHOICES = [m.name.lower() for m in UUIDType]
_DEFAULT_COUNT = 1


class _Prog:
    NAME = "uuid-tool"
    DESC = "UUID generator and validator"
    CMD_DEST = "command"
    GUI_FLAG = "--gui"
    GUI_FLAG_SHORT = "-g"
    GUI_HELP = "Launch the graphical interface"


class _GenArgs:
    HELP = "Generate UUIDs"
    TYPE_FLAGS = ("--type", "-t")
    TYPE_METAVAR = "VERSION"
    TYPE_HELP = f"UUID version: {', '.join(_VERSION_CHOICES)} (default: {UUIDType.default().name.lower()})"
    COUNT_FLAGS = ("--count", "-n")
    COUNT_METAVAR = "N"
    COUNT_HELP = f"Number of UUIDs (default: {_DEFAULT_COUNT})"


class _ValArgs:
    HELP = "Validate UUIDs"
    UUIDS_DEST = "uuids"
    UUIDS_METAVAR = "UUID"
    UUIDS_HELP = "UUIDs to validate (or pipe via stdin)"


def _cmd_generate(args: argparse.Namespace) -> None:
    uuid_type = UUIDType.from_version(args.type) if args.type else UUIDType.default()
    results = generate(uuid_type, args.count)
    print("\n".join(results))


def _cmd_validate(args: argparse.Namespace) -> None:
    values = args.uuids if args.uuids else [line.strip() for line in sys.stdin]
    results = validate(values)

    for r in results:
        print(r)

    ok = sum(1 for r in results if r.valid)
    err = len(results) - ok
    print(f"\n{len(results)} total — {ok} valid, {err} invalid", file=sys.stderr)

    if err:
        sys.exit(1)


def run() -> None:
    parser = argparse.ArgumentParser(prog=_Prog.NAME, description=_Prog.DESC)
    parser.add_argument(_Prog.GUI_FLAG, _Prog.GUI_FLAG_SHORT, action="store_true", help=_Prog.GUI_HELP)
    sub = parser.add_subparsers(dest=_Prog.CMD_DEST)

    gen = sub.add_parser(_Cmd.GENERATE, aliases=_CMD_ALIASES[_Cmd.GENERATE], help=_GenArgs.HELP)
    gen.add_argument(*_GenArgs.TYPE_FLAGS, choices=_VERSION_CHOICES, metavar=_GenArgs.TYPE_METAVAR, help=_GenArgs.TYPE_HELP)
    gen.add_argument(*_GenArgs.COUNT_FLAGS, type=int, default=_DEFAULT_COUNT, metavar=_GenArgs.COUNT_METAVAR, help=_GenArgs.COUNT_HELP)

    val = sub.add_parser(_Cmd.VALIDATE, aliases=_CMD_ALIASES[_Cmd.VALIDATE], help=_ValArgs.HELP)
    val.add_argument(_ValArgs.UUIDS_DEST, nargs="*", metavar=_ValArgs.UUIDS_METAVAR, help=_ValArgs.UUIDS_HELP)

    args = parser.parse_args()

    if args.gui:
        from uuid_tool.gui.app import UUIDApp
        UUIDApp().mainloop()
        return

    if not args.command:
        parser.print_help()
        raise SystemExit(0)

    dispatch = {
        _Cmd.GENERATE.value: _cmd_generate,
        **{alias: _cmd_generate for alias in _CMD_ALIASES[_Cmd.GENERATE]},
        _Cmd.VALIDATE.value: _cmd_validate,
        **{alias: _cmd_validate for alias in _CMD_ALIASES[_Cmd.VALIDATE]},
    }
    dispatch[args.command](args)
