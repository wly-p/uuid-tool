import re
import pytest
from uuid_tool.core import UUIDType, ValidationResult, generate, validate

UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
    re.IGNORECASE,
)


class TestUUIDType:
    def test_default_is_v4(self):
        assert UUIDType.default() is UUIDType.V4

    @pytest.mark.parametrize("uuid_type", list(UUIDType))
    def test_generate_format(self, uuid_type):
        result = uuid_type.generate()
        assert UUID_RE.match(result), f"{uuid_type.name} generated invalid UUID: {result}"

    @pytest.mark.parametrize("version,expected", [
        ("v1", UUIDType.V1),
        ("V1", UUIDType.V1),
        ("1",  UUIDType.V1),
        ("v4", UUIDType.V4),
        ("4",  UUIDType.V4),
        ("v6", UUIDType.V6),
        ("v7", UUIDType.V7),
        ("v8", UUIDType.V8),
    ])
    def test_from_version(self, version, expected):
        assert UUIDType.from_version(version) is expected

    def test_from_version_invalid_raises(self):
        with pytest.raises(StopIteration):
            UUIDType.from_version("v99")

    def test_from_label(self):
        assert UUIDType.from_label("UUID v4 (Random)") is UUIDType.V4

    def test_labels(self):
        labels = UUIDType.labels()
        assert len(labels) == len(UUIDType)
        assert "UUID v4 (Random)" in labels
        assert "UUID v6 (Time-reordered)" in labels
        assert "UUID v7 (Unix Epoch)" in labels
        assert "UUID v8 (Custom)" in labels


class TestGenerate:
    def test_returns_correct_count(self):
        results = generate(UUIDType.V4, 5)
        assert len(results) == 5

    def test_all_valid_format(self):
        for uuid_str in generate(UUIDType.V4, 10):
            assert UUID_RE.match(uuid_str)

    def test_zero_count(self):
        assert generate(UUIDType.V4, 0) == []

    @pytest.mark.parametrize("uuid_type", list(UUIDType))
    def test_all_versions_generate(self, uuid_type):
        results = generate(uuid_type, 3)
        assert len(results) == 3


class TestValidate:
    VALID_V4 = "550e8400-e29b-41d4-a716-446655440000"
    VALID_V1 = "6ba7b810-9dad-11d1-80b4-00c04fd430c8"
    VALID_V7 = "01956fac-b4b3-7c1b-9ae2-8a32e58de2c5"

    def test_valid_uuid(self):
        results = validate([self.VALID_V4])
        assert len(results) == 1
        assert results[0].valid is True
        assert results[0].version == 4

    def test_valid_v1_uuid(self):
        results = validate([self.VALID_V1])
        assert results[0].valid is True
        assert results[0].version == 1

    def test_invalid_uuid(self):
        results = validate(["not-a-uuid"])
        assert results[0].valid is False
        assert results[0].version is None

    def test_empty_lines_skipped(self):
        results = validate(["", "  ", self.VALID_V4])
        assert len(results) == 1

    def test_valid_v7_uuid(self):
        results = validate([self.VALID_V7])
        assert results[0].valid is True
        assert results[0].version == 7

    def test_mixed_valid_invalid(self):
        results = validate([self.VALID_V4, "bad", self.VALID_V1])
        assert sum(1 for r in results if r.valid) == 2
        assert sum(1 for r in results if not r.valid) == 1

    def test_strips_whitespace(self):
        results = validate([f"  {self.VALID_V4}  "])
        assert results[0].valid is True

    def test_empty_list(self):
        assert validate([]) == []


class TestValidationResult:
    def test_str_valid(self):
        r = ValidationResult(value="abc", valid=True, version=4)
        assert "✓" in str(r)
        assert "abc" in str(r)
        assert "v4" in str(r)

    def test_str_invalid(self):
        r = ValidationResult(value="bad", valid=False, version=None)
        assert "✗" in str(r)
        assert "bad" in str(r)
