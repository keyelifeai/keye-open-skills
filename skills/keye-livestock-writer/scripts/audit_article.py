#!/usr/bin/env python3
"""Deterministically audit article metadata and claim-ledger traceability."""
from __future__ import annotations

import argparse
import ipaddress
import json
import re
from pathlib import Path
from urllib.parse import urlparse

from common import DEFAULT_WORKSPACE, load_brand, workspace_errors, workspace_path


REQUIRED_METADATA = ("title", "date", "species", "life_stage", "audience", "status", "evidence_ledger", "brand_name", "main_products")
PUBLIC_REQUIRED_METADATA = ("workflow_version", "editorial_mode", "evidence_matrix", "search_log")
EDITORIAL_MODES = {"evidence-landscape", "study-in-context", "technical-explainer"}
PUBLIC_BOUND_FILES = {"evidence_matrix": "evidence-matrix.md", "search_log": "search-log.md"}
PUBLIC_STATIC_FILES = ("brief.md", "outline.md", "review.md")
UNRESOLVED_MARKERS = ("TODO", "TBD", "待填写", "待核实", "{{", "}}")
LEDGER_COLUMNS = ("Claim", "Source locator", "Source class", "Public-use decision", "Verification state", "Support type", "Reviewer note")
SOURCE_CLASSES = {"user_document", "external_url"}
PUBLIC_USE_DECISIONS = {"review-required", "do-not-use"}
SUPPORT_TYPES = {"direct-evidence", "inference"}


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if len(lines) < 3 or lines[0] != "---":
        raise ValueError("frontmatter must start with ---")
    metadata: dict[str, str] = {}
    for line in lines[1:]:
        if line == "---":
            return metadata
        if not line or line[:1].isspace():
            raise ValueError("frontmatter lines must be unindented top-level scalars")
        match = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_-]*):[ \t]*(.*)", line)
        if match is None:
            raise ValueError(f"invalid frontmatter line: {line}")
        key, value = match.groups()
        if key in metadata:
            raise ValueError(f"duplicate frontmatter key: {key}")
        if not value or value.startswith(("|", ">", "[", "{")):
            raise ValueError(f"frontmatter value for {key} must be a non-empty simple scalar")
        if not value.startswith('"') and not re.fullmatch(r"[\w./ -]+", value):
            raise ValueError(f"frontmatter {key}: quote special characters with JSON double quotes")
        if value.startswith('"'):
            try:
                parsed = json.loads(value)
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid JSON-quoted frontmatter value for {key}") from exc
            if not isinstance(parsed, str):
                raise ValueError(f"frontmatter value for {key} must be a string")
            if not parsed:
                raise ValueError(f"frontmatter value for {key} must not be empty")
            value = parsed
        if not value or any(not char.isprintable() for char in value):
            raise ValueError(f"frontmatter value for {key} must be non-empty and printable")
        metadata[key] = value
    raise ValueError("frontmatter is missing closing ---")


def under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def metadata_path(value: str, workspace: Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = workspace / path
    return path.resolve()


def is_separator_row(fields: list[str]) -> bool:
    return len(fields) == len(LEDGER_COLUMNS) and all(re.fullmatch(r":?-{3,}:?", field) for field in fields)


def rows_from_ledger(text: str) -> tuple[list[tuple[int, list[str]]], list[str]]:
    rows = []
    failures = []
    header_line = None
    separator_line = None
    data_seen = False
    for line_number, line in enumerate(text.splitlines(), start=1):
        if "|" not in line:
            continue
        if line[:1].isspace() and line.lstrip().startswith("|"):
            failures.append(f"ledger line {line_number}: indented table row is not canonical")
            continue
        if not line.startswith("|"):
            failures.append(f"ledger line {line_number}: omitted leading table pipe")
            continue
        if not line.endswith("|"):
            failures.append(f"ledger line {line_number}: omitted trailing table pipe")
            continue
        fields = [item.strip() for item in line[1:-1].split("|")]
        if tuple(fields) == LEDGER_COLUMNS:
            if header_line is not None:
                failures.append(f"ledger line {line_number}: duplicate canonical header")
            elif separator_line is not None or data_seen:
                failures.append(f"ledger line {line_number}: canonical header is out of order")
            else:
                header_line = line_number
            continue
        if is_separator_row(fields):
            if header_line is None:
                failures.append(f"ledger line {line_number}: separator appears before canonical header")
            elif separator_line is not None:
                failures.append(f"ledger line {line_number}: duplicate canonical separator")
            elif data_seen:
                failures.append(f"ledger line {line_number}: separator appears after data")
            else:
                separator_line = line_number
            continue
        if len(fields) == len(LEDGER_COLUMNS) and all(field and set(field) <= {"-", ":"} for field in fields):
            failures.append(f"ledger line {line_number}: invalid Markdown separator row")
            continue
        if header_line is None:
            failures.append(f"ledger line {line_number}: data row appears before canonical header")
            continue
        if separator_line is None:
            failures.append(f"ledger line {line_number}: data row appears before canonical separator")
            continue
        rows.append((line_number, fields))
        data_seen = True
    if header_line is None:
        failures.append("ledger line 1: missing canonical seven-column header")
    if separator_line is None:
        failures.append(f"ledger line {header_line or 1}: missing canonical separator")
    return rows, failures


def external_url_error(locator: str) -> str | None:
    if any(char.isspace() or ord(char) < 32 or ord(char) == 127 for char in locator):
        return "external URL evidence must not contain whitespace or control characters"
    if "\\" in locator:
        return "external URL evidence must not contain backslash authority ambiguity"
    try:
        parsed = urlparse(locator)
        port = parsed.port
        hostname = parsed.hostname
    except ValueError:
        return "external URL evidence has malformed host or port syntax"
    if parsed.scheme.lower() not in {"http", "https"} or not hostname:
        return "external URL evidence requires a valid http or https URL with a host"
    if parsed.username is not None or parsed.password is not None:
        return "external URL evidence must not contain credentials"
    host_port = parsed.netloc
    if host_port.startswith("["):
        closing = host_port.find("]")
        if closing < 0:
            return "external URL evidence has malformed host or port syntax"
        try:
            ipaddress.IPv6Address(host_port[1:closing])
        except ValueError:
            return "external URL evidence bracketed host must be an IPv6 literal"
        port_tail = host_port[closing + 1:]
    else:
        port_tail = ":" + host_port.rsplit(":", 1)[1] if host_port.count(":") == 1 else ""
    if port_tail and (not port_tail.startswith(":") or not port_tail[1:]):
        return "external URL evidence has malformed host or port syntax"
    if port is not None and not 1 <= port <= 65535:
        return "external URL evidence port must be in 1..65535"
    try:
        ipaddress.ip_address(hostname)
        return None
    except ValueError:
        pass
    if re.fullmatch(r"\d+(?:\.\d+){1,3}", hostname):
        return "external URL evidence hostname is an invalid IPv4 literal"
    try:
        ascii_hostname = hostname.encode("idna").decode("ascii")
    except UnicodeError:
        return "external URL evidence hostname is not valid IDNA"
    if re.fullmatch(r"[0-9.]+", ascii_hostname):
        return "external URL evidence hostname is an invalid IPv4 literal"
    if len(ascii_hostname) > 253:
        return "external URL evidence hostname is too long"
    for label in ascii_hostname.split("."):
        if not label or len(label) > 63 or not re.fullmatch(r"[A-Za-z0-9-]+", label) or label.startswith("-") or label.endswith("-"):
            return "external URL evidence hostname has an invalid label"
    return None


def validate_row(fields: list[str], workspace: Path) -> list[str]:
    failures: list[str] = []
    if len(fields) != len(LEDGER_COLUMNS):
        return [f"evidence ledger row must have exactly {len(LEDGER_COLUMNS)} fields"]
    if any(not field for field in fields):
        return ["evidence ledger row fields must all be non-empty"]
    _, locator, source_class, decision, verification_state, support_type, _ = fields
    if source_class not in SOURCE_CLASSES:
        failures.append("source class must be user_document or external_url")
    if decision not in PUBLIC_USE_DECISIONS:
        failures.append("public-use decision must be review-required or do-not-use")
    if verification_state != "verified":
        failures.append("verification state must be verified")
    if support_type not in SUPPORT_TYPES:
        failures.append("support type must be direct-evidence or inference")
    if decision == "do-not-use":
        failures.append("do-not-use evidence must be removed before final audit")

    if decision != "review-required":
        failures.append("all evidence must remain review-required")
    if source_class == "user_document":
        path_text, separator, section = locator.partition("#")
        if not separator or not path_text.strip() or not section.strip():
            failures.append("user document requires a re-findable path#section locator")
        else:
            path = Path(path_text)
            if not path.is_absolute():
                path = workspace / path
            if not path.is_file():
                failures.append("user document locator must refer to an existing file")
    elif source_class == "external_url":
        url_error = external_url_error(locator)
        if url_error:
            failures.append(url_error)
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("article", type=Path)
    parser.add_argument("evidence_ledger", type=Path)
    parser.add_argument("--workspace", type=Path, default=DEFAULT_WORKSPACE)
    args = parser.parse_args()
    failures: list[str] = []
    try:
        workspace = workspace_path(args.workspace)
        failures.extend(workspace_errors(workspace))
    except ValueError as exc:
        print(f"AUDIT FAIL: {exc}")
        return 1
    article = args.article.absolute()
    ledger = args.evidence_ledger.absolute()
    expected_ledger = workspace / "work" / article.stem / "evidence.md"
    if article.is_symlink() or not article.is_file() or article.parent.resolve() != workspace / "articles":
        failures.append("article must be a real file directly under workspace/articles")
    if ledger.is_symlink() or not ledger.is_file() or ledger.resolve() != expected_ledger:
        failures.append("evidence ledger must be work/<article-name>/evidence.md")
    if expected_ledger.parent.is_symlink():
        failures.append("work package must not be a symlink")
    if failures:
        print("AUDIT FAIL")
        print("\n".join(f"- {failure}" for failure in failures))
        return 1
    article = article.resolve()
    ledger = ledger.resolve()
    article_text = article.read_text(encoding="utf-8")
    ledger_text = ledger.read_text(encoding="utf-8")
    try:
        metadata = parse_frontmatter(article_text)
    except ValueError as exc:
        failures.append(str(exc))
        metadata = {}
    for key in REQUIRED_METADATA:
        if not metadata.get(key):
            failures.append(f"article frontmatter missing {key}")
    if metadata.get("status") not in {"review", "final"}:
        failures.append("article status must be review or final")
    bound_ledger = metadata.get("evidence_ledger")
    if bound_ledger:
        if metadata_path(bound_ledger, workspace) != ledger:
            failures.append("article evidence_ledger must resolve to the evidence-ledger argument")

    audited_texts = {"article": article_text, "evidence ledger": ledger_text}
    workflow_version = metadata.get("workflow_version")
    if workflow_version is None:
        failures.append("workflow_version is required")
    else:
        if workflow_version != "public-1":
            failures.append("workflow_version must be public-1")
        for key in PUBLIC_REQUIRED_METADATA:
            if not metadata.get(key):
                failures.append(f"article frontmatter missing {key}")
        if metadata.get("editorial_mode") not in EDITORIAL_MODES:
            failures.append("editorial_mode must be evidence-landscape, study-in-context, or technical-explainer")
        run_dir = ledger.parent
        if run_dir.name != article.stem:
            failures.append("public-1 article and work package names must match")
        if not run_dir.is_dir() or run_dir.is_symlink() or not under(run_dir, workspace / "work"):
            failures.append("public-1 work package must be a real directory under workspace/work")
        for field, filename in PUBLIC_BOUND_FILES.items():
            expected_path = run_dir / filename
            value = metadata.get(field)
            if value and metadata_path(value, workspace) != expected_path:
                failures.append(f"article {field} must resolve to work package {filename}")
            if not expected_path.is_file() or expected_path.is_symlink():
                failures.append(f"public-1 work package missing real file: {filename}")
            else:
                audited_texts[filename] = expected_path.read_text(encoding="utf-8")
        for filename in PUBLIC_STATIC_FILES:
            path = run_dir / filename
            if not path.is_file() or path.is_symlink():
                failures.append(f"public-1 work package missing real file: {filename}")
            else:
                audited_texts[filename] = path.read_text(encoding="utf-8")

    for marker in UNRESOLVED_MARKERS:
        locations = [name for name, text in audited_texts.items() if marker in text]
        if locations:
            failures.append(f"unresolved marker found: {marker} in {', '.join(locations)}")
            break

    rows, syntax_failures = rows_from_ledger(ledger_text)
    failures.extend(syntax_failures)
    if not rows:
        failures.append("evidence ledger needs at least one data row")
    try:
        brand = load_brand(ledger.parent / "brand.json")
        for key in ("brand_name", "main_products"):
            if metadata.get(key) != brand[key]:
                failures.append(f"article {key} must match the run brand snapshot")
    except (OSError, ValueError) as exc:
        failures.append(f"brand snapshot: {exc}")
    valid_rows = 0
    for line_number, fields in rows:
        row_failures = validate_row(fields, workspace)
        if row_failures:
            failures.extend(f"ledger line {line_number}: {failure}" for failure in row_failures)
        else:
            valid_rows += 1
    if not valid_rows:
        failures.append("evidence ledger needs at least one complete canonical row")
    if failures:
        print("AUDIT FAIL")
        print("\n".join(f"- {failure}" for failure in dict.fromkeys(failures)))
        return 1
    print(f"AUDIT PASS: article={article.name} evidence_rows={valid_rows}")
    print("Deterministic checks passed; scientific truth and required human review remain open.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
