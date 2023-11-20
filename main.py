"""Incremental SHA-256 manifest and lexical term index for local documents."""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile

MAX_BYTES=1024*1024

def term_counts(text):return dict(Counter(re.findall(r"\w+",text.casefold())))


def check_manifest(manifest):
    if not isinstance(manifest,dict) or set(manifest) != {"version","documents"} or manifest["version"] != 1 or not isinstance(manifest["documents"],dict):
        raise ValueError("invalid manifest format")
    for name,record in manifest["documents"].items():
        if not isinstance(name,str) or Path(name).is_absolute() or ".." in Path(name).parts or not isinstance(record,dict) or set(record) != {"sha256","terms"}:
            raise ValueError("invalid document record")
        if not isinstance(record["sha256"],str) or not re.fullmatch(r"[0-9a-f]{64}",record["sha256"]) or not isinstance(record["terms"],dict):
            raise ValueError("invalid digest or term counts")
        if any(not isinstance(term,str) or type(count) is not int or count <= 0 for term,count in record["terms"].items()):
            raise ValueError("invalid term counts")


def update(directory,previous=None):
    directory=Path(directory).resolve()
    if not directory.is_dir():raise ValueError("document directory does not exist")
    previous=previous if previous is not None else {"version":1,"documents":{}}
    check_manifest(previous)
    old=previous["documents"];new={};changes={"added":[],"changed":[],"deleted":[],"unchanged":[],"skipped_symlinks":[]}
    for file in sorted(directory.rglob("*")):
        relative=file.relative_to(directory).as_posix()
        if file.is_symlink():
            changes["skipped_symlinks"].append(relative);continue
        if not file.is_file() or file.suffix.lower() not in {".txt",".md"}:continue
        if not file.resolve().is_relative_to(directory):raise ValueError("document resolves outside root")
        if file.stat().st_size > MAX_BYTES:raise ValueError(f"document exceeds size limit: {relative}")
        content=file.read_bytes()
        if len(content)>MAX_BYTES:raise ValueError(f"document exceeds size limit: {relative}")
        digest=hashlib.sha256(content).hexdigest()
        if relative in old and old[relative]["sha256"] == digest:
            new[relative]={"sha256":digest,"terms":dict(old[relative]["terms"])};changes["unchanged"].append(relative)
        else:
            new[relative]={"sha256":digest,"terms":term_counts(content.decode("utf-8"))}
            changes["changed" if relative in old else "added"].append(relative)
    changes["deleted"]=sorted(set(old)-set(new))
    return {"version":1,"documents":new},changes


def inverted(manifest):
    check_manifest(manifest)
    index={}
    for doc,record in manifest["documents"].items():
        for term,count in record["terms"].items():index.setdefault(term,{})[doc]=count
    return dict(sorted(index.items()))

