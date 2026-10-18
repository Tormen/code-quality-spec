---
applyTo: "**/*.sh"
---

# Shell

<!-- rendered by tools/render-adapters from SPEC.md fffb136c0770; do not edit here -- edit the spec and re-render -->

## Mechanical checks

`shellcheck -s <shebang dialect>`, `<shell> -n`; a gate refuses GNU-only flags in a script that targets BSD userland (`head -N`, `sed -r`, `grep -P`, `xargs -r`, `date -d`, `find -printf`, `stat -c`)

The `secret` and `crash-safe` checks of the repo-wide instructions apply with particular force in shell: no secret literal in a command, every write via a temporary file and rename.
