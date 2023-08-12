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

