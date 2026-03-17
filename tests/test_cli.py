import pytest
from unittest.mock import patch
from uuid_tool.cli import run


def invoke(*args):
    with patch("sys.argv", ["uuid-tool", *args]):
        run()


class TestGenerate:
    def test_default_count(self, capsys):
        invoke("generate")
        out = capsys.readouterr().out.strip().splitlines()
        assert len(out) == 1

    def test_custom_count(self, capsys):
        invoke("generate", "--count", "3")
        out = capsys.readouterr().out.strip().splitlines()
        assert len(out) == 3

    def test_alias_gen(self, capsys):
        invoke("gen", "-n", "2")
        out = capsys.readouterr().out.strip().splitlines()
        assert len(out) == 2

    @pytest.mark.parametrize("version", ["v1", "v3", "v4", "v5"])
    def test_type_flag(self, version, capsys):
        invoke("generate", "--type", version, "-n", "1")
        out = capsys.readouterr().out.strip()
        assert len(out) == 36  # UUID string length

    def test_invalid_type_exits(self):
        with pytest.raises(SystemExit):
            invoke("generate", "--type", "v99")


class TestValidate:
    VALID = "550e8400-e29b-41d4-a716-446655440000"
    INVALID = "not-a-uuid"

    def test_valid_uuid(self, capsys):
        invoke("validate", self.VALID)
        out = capsys.readouterr().out
        assert "✓" in out

    def test_invalid_uuid_exits_1(self, capsys):
        with pytest.raises(SystemExit) as exc:
            invoke("validate", self.INVALID)
        assert exc.value.code == 1

    def test_alias_val(self, capsys):
        invoke("val", self.VALID)
        out = capsys.readouterr().out
        assert "✓" in out

    def test_mixed_exits_1(self, capsys):
        with pytest.raises(SystemExit) as exc:
            invoke("validate", self.VALID, self.INVALID)
        assert exc.value.code == 1

    def test_all_valid_no_exit(self, capsys):
        invoke("validate", self.VALID)  # should not raise


class TestNoArgs:
    def test_no_command_prints_help_and_exits_0(self, capsys):
        with pytest.raises(SystemExit) as exc:
            invoke()
        assert exc.value.code == 0
