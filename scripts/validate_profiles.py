#!/usr/bin/env python3
"""Validate Hermes profile metadata and skill wiring.

This intentionally checks semantic drift that plain `yaml.safe_load` misses:
- duplicate YAML keys
- profile.yaml structure
- declared skills that do not exist in the shared skill pool
- declared skills that are not reachable through the profile's skills/ symlinks
- invalid shared-skill frontmatter
- broken or absolute symlinks
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Any

import yaml


class UniqueKeyLoader(yaml.SafeLoader):
    """YAML loader that rejects duplicate mapping keys."""


def construct_mapping(loader: UniqueKeyLoader, node: yaml.nodes.MappingNode, deep: bool = False) -> dict[str, Any]:
    mapping: dict[str, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate key {key!r} at line {key_node.start_mark.line + 1}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        # UniqueKeyLoader subclasses yaml.SafeLoader; yaml.load is used here only
        # to reject duplicate keys while preserving safe construction semantics.
        data = yaml.load(path.read_text(), Loader=UniqueKeyLoader)
    except Exception as exc:  # noqa: BLE001 - CLI validator should report path + failure
        raise ValueError(f"{path}: invalid YAML: {exc}") from exc
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected YAML mapping, got {type(data).__name__}")
    return data


def extract_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(errors="replace")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError(f"{path}: frontmatter is not closed with ---")
    body = text[end + 5 :].strip()
    if not body:
        raise ValueError(f"{path}: missing body content")
    try:
        # UniqueKeyLoader subclasses yaml.SafeLoader; yaml.load is used here only
        # to reject duplicate keys while preserving safe construction semantics.
        fm = yaml.load(text[4:end], Loader=UniqueKeyLoader)
    except Exception as exc:  # noqa: BLE001
        raise ValueError(f"{path}: invalid frontmatter YAML: {exc}") from exc
    if not isinstance(fm, dict):
        raise ValueError(f"{path}: frontmatter must be a mapping")
    return fm


def skill_names_under(path: Path) -> set[str]:
    """Return skill names reachable under a skill root.

    pathlib's rglob does not reliably traverse symlinked directories on every
    platform, so profiles are handled by resolving each immediate entry first.
    Directory names are also counted because this repo sometimes links a skill
    category such as `architecture/` and declares that category in profile.yaml.
    """
    names: set[str] = set()
    if not path.exists():
        return names

    roots: list[Path]
    if path.name == "skills":
        roots = [entry.resolve() for entry in path.iterdir() if entry.is_dir()]
    else:
        roots = [path.resolve()]

    for root in roots:
        if not root.exists() or not root.is_dir():
            continue
        names.add(root.name)
        for skill_md in root.rglob("SKILL.md"):
            try:
                fm = extract_frontmatter(skill_md)
            except ValueError:
                # Let shared-skill validation report the detailed error.
                names.add(skill_md.parent.name)
                continue
            names.add(str(fm.get("name") or skill_md.parent.name))
    return names


def declared_skills(profile_yaml: dict[str, Any], profile_path: Path) -> set[str]:
    skills = profile_yaml.get("skills")
    if not isinstance(skills, dict):
        raise ValueError(f"{profile_path}: `skills` must be a mapping")
    declared: set[str] = set()
    for bucket in ("required", "recommended"):
        values = skills.get(bucket, [])
        if values is None:
            continue
        if not isinstance(values, list) or not all(isinstance(v, str) for v in values):
            raise ValueError(f"{profile_path}: `skills.{bucket}` must be a list of strings")
        declared.update(values)
    return declared


def reachable_profile_skills(profile_dir: Path) -> set[str]:
    skill_dir = profile_dir / "skills"
    if not skill_dir.exists():
        return set()
    return skill_names_under(skill_dir.resolve())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    profiles_dir = root / "profiles"
    skills_dir = root / "skills"
    errors: list[str] = []

    shared_skills = skill_names_under(skills_dir)

    # Shared skill frontmatter must be valid Hermes-style skill metadata.
    for skill_md in sorted(skills_dir.rglob("SKILL.md")):
        try:
            fm = extract_frontmatter(skill_md)
            name = fm.get("name")
            description = fm.get("description")
            if not isinstance(name, str) or not name.strip():
                errors.append(f"{skill_md.relative_to(root)}: missing non-empty frontmatter `name`")
            if not isinstance(description, str) or not description.strip():
                errors.append(f"{skill_md.relative_to(root)}: missing non-empty frontmatter `description`")
            elif len(description) > 1024:
                errors.append(f"{skill_md.relative_to(root)}: `description` exceeds 1024 characters")
        except ValueError as exc:
            errors.append(str(exc).replace(str(root) + os.sep, ""))

    for profile_dir in sorted(p for p in profiles_dir.iterdir() if p.is_dir()):
        rel = profile_dir.relative_to(root)
        for required_file in ("SOUL.md", "profile.yaml", "README.md", "AGENTS.md"):
            if not (profile_dir / required_file).is_file():
                errors.append(f"{rel}: missing {required_file}")

        profile_yaml_path = profile_dir / "profile.yaml"
        if not profile_yaml_path.exists():
            continue
        try:
            data = load_yaml(profile_yaml_path)
            declared = declared_skills(data, profile_yaml_path.relative_to(root))
        except ValueError as exc:
            errors.append(str(exc).replace(str(root) + os.sep, ""))
            continue

        missing_from_repo = sorted(declared - shared_skills)
        if missing_from_repo:
            errors.append(
                f"{profile_yaml_path.relative_to(root)}: declares skills not present in shared pool: "
                + ", ".join(missing_from_repo)
            )

        reachable = reachable_profile_skills(profile_dir)
        missing_from_profile = sorted(declared - reachable)
        if missing_from_profile:
            errors.append(
                f"{profile_yaml_path.relative_to(root)}: declares skills not reachable from profile skills/: "
                + ", ".join(missing_from_profile)
            )

    for link in sorted(profiles_dir.rglob("*")):
        if not link.is_symlink():
            continue
        target = os.readlink(link)
        if os.path.isabs(target):
            errors.append(f"{link.relative_to(root)}: symlink target is absolute: {target}")
        if not link.exists():
            errors.append(f"{link.relative_to(root)}: broken symlink -> {target}")

    if errors:
        print("Profile validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        f"Profile validation passed: {len(list(profiles_dir.iterdir()))} profiles, "
        f"{len(shared_skills)} shared skills."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
