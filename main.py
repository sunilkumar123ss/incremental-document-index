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

