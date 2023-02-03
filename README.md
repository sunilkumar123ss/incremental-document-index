# Incremental local document index

> **Disclosed reconstruction prepared on 24 October 2026.** The recorded Git dates are synthetic, not dates of past development. See [HISTORY.md](HISTORY.md).

This is an incomplete stage in a tutorial reconstruction of an already-completed reference implementation. Source, fixtures, tests, command-line behavior and verification are introduced in later stages. Only the final branch tip contains the complete documented package.

## Intended scope of the final example

Hashes UTF-8 `.txt` and `.md` files, detects additions/changes/deletions, and builds a lexical inverted index with per-document term counts. Unchanged files reuse the prior token counts. Symlinked files are skipped, each file is limited to 1 MiB, and malformed prior manifests are rejected. Use `--directory ./documents --state index.json --query "voice"` to persist and query the manifest. Atomic replacement prevents partial JSON writes; concurrent writer coordination is out of scope.

All examples are synthetic and educational. This reconstruction does not establish historical employment, deployment, usage, or production benchmarks.
