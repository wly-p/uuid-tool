import re
import uuid
from dataclasses import dataclass
from enum import Enum


class UUIDType(Enum):
    V1 = ("UUID v1 (Time-based)", lambda: uuid.uuid1())
    V3 = ("UUID v3 (MD5 Namespace)", lambda: uuid.uuid3(uuid.NAMESPACE_DNS, str(uuid.uuid4())))
    V4 = ("UUID v4 (Random)", lambda: uuid.uuid4())
    V5 = ("UUID v5 (SHA-1 Namespace)", lambda: uuid.uuid5(uuid.NAMESPACE_DNS, str(uuid.uuid4())))
    V6 = ("UUID v6 (Time-reordered)", lambda: uuid.uuid6())
    V7 = ("UUID v7 (Unix Epoch)", lambda: uuid.uuid7())
    V8 = ("UUID v8 (Custom)", lambda: uuid.uuid8())

    def __init__(self, label: str, factory):
        self.label = label
        self._factory = factory

    def generate(self) -> str:
        return str(self._factory())

    @classmethod
    def labels(cls) -> list[str]:
        return [m.label for m in cls]

    @classmethod
    def from_label(cls, label: str) -> "UUIDType":
        return next(m for m in cls if m.label == label)

    @classmethod
    def from_version(cls, version: str) -> "UUIDType":
        key = version.upper().lstrip("V")
        return next(m for m in cls if m.name == f"V{key}")

    @classmethod
    def default(cls) -> "UUIDType":
        return cls.V4


_UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
    re.IGNORECASE,
)
_VERSION_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-([1-8])[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class ValidationResult:
    value: str
    valid: bool
    version: int | None

    def __str__(self) -> str:
        if self.valid:
            return f"✓  {self.value}  [v{self.version}]"
        return f"✗  {self.value}"


def generate(uuid_type: UUIDType, count: int) -> list[str]:
    return [uuid_type.generate() for _ in range(count)]


def validate(values: list[str]) -> list[ValidationResult]:
    results = []
    for raw in values:
        value = raw.strip()
        if not value:
            continue
        if _UUID_RE.match(value):
            m = _VERSION_RE.match(value)
            version = int(m.group(1)) if m else None
            results.append(ValidationResult(value=value, valid=True, version=version))
        else:
            results.append(ValidationResult(value=value, valid=False, version=None))
    return results
