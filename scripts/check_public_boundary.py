#!/usr/bin/env python3
"""Reject secrets and common environment-specific values in public manifests."""

from __future__ import annotations

import ipaddress
import pathlib
import re
import sys

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST_ROOTS = (ROOT / "components", ROOT / "clusters")
PRIVATE_NAME_PATTERNS = (
    re.compile(r"\.internal\b", re.IGNORECASE),
    re.compile(r"\.lan\b", re.IGNORECASE),
    re.compile(r"\.local\b", re.IGNORECASE),
)


def yaml_files() -> list[pathlib.Path]:
    files: list[pathlib.Path] = []
    for directory in MANIFEST_ROOTS:
        if directory.exists():
            files.extend(directory.rglob("*.yaml"))
            files.extend(directory.rglob("*.yml"))
    return sorted(set(files))


def private_ipv4_values(text: str) -> list[str]:
    candidates = re.findall(r"(?<![0-9.])(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?![0-9.])", text)
    private: list[str] = []
    for candidate in candidates:
        try:
            address = ipaddress.ip_address(candidate)
        except ValueError:
            continue
        if address.is_private and not address.is_loopback:
            private.append(candidate)
    return private


def main() -> int:
    failures: list[str] = []
    for path in yaml_files():
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT)

        for document in yaml.safe_load_all(text):
            if isinstance(document, dict) and document.get("kind") == "Secret":
                failures.append(f"{relative}: Kubernetes Secret objects are forbidden")

        for value in private_ipv4_values(text):
            failures.append(f"{relative}: private IPv4 address is forbidden: {value}")

        for pattern in PRIVATE_NAME_PATTERNS:
            if pattern.search(text):
                failures.append(f"{relative}: private DNS suffix matches {pattern.pattern}")

    if failures:
        print("Public repository boundary violations:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"Validated {len(yaml_files())} public manifest file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
