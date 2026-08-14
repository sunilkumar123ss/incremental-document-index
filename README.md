# Incremental local document index

Runnable educational demo/starter with synthetic examples.

Hashes UTF-8 `.txt` and `.md` files, detects additions/changes/deletions, and builds a lexical inverted index with per-document term counts. Unchanged files reuse the prior token counts. Symlinked files are skipped, each file is limited to 1 MiB, and malformed prior manifests are rejected. Use `--directory ./documents --state index.json --query "voice"` to persist and query the manifest. Atomic replacement prevents partial JSON writes; concurrent writer coordination is out of scope.

## Run

Python 3.10+; standard library only. From this directory:

```sh
python3 main.py
python3 main.py --help
python3 -m unittest -v
```

No network requests, credentials, or paid services are used. Any model/provider integration would be a separate adapter. Read `main.py` for the public functions and `test_main.py` for success/failure invariants. Fixture content is synthetic.

## Scope

This is an educational implementation with synthetic fixtures. Run the tests and inspect the documented limits before adapting it.

## Repository checks

```sh
python3 verify.py
```

This runs the isolated test suite, synthetic example, and CLI help. The included GitHub Actions workflow repeats these checks when the repository is published. No hosted CI result is claimed by the local verification report.
