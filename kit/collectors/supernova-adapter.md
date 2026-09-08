---
title: Supernova adapter
kit: design-system-value-kit
artifact: collectors/supernova-adapter
date: 2026-09-08
classification: unclassified
status: gated - awaiting access
---

# Supernova adapter

**STATUS: gated - awaiting access.**

Design-system structure and documentation coverage from the documentation
platform's read API. No documentation-platform MCP is connected in this
environment, so this is a reference collector against the vendor read surface,
run by the operator with their own token.

The reference script is `supernova_adapter.py`. This page is its spec. The
script runs a credential-free dry-run today and a live read once the operator
fills the config and flips the status.

## Gate

The read needs a **Supernova account and a personal access token**, generated
from the account's profile settings. Until that exists, this adapter stays gated
and its rows are marked `source-gap` on the map. This is an access gate the
operator must clear before any live read.

## What it fills, and its honest limit

The vendor's first-party programmatic surface is a JavaScript/TypeScript SDK
(package `@supernovaio/sdk`) plus a CLI. A read returns the version's tokens,
assets, components, and documentation structure and content.

Into artifact 02:

- Token, asset, and component inventory maps to `dim_component` as a
  documentation-platform-side mirror of the structure, useful where the
  documentation platform, not the design tool, is the system of record.
- Documentation coverage (which components and tokens have a documentation page)
  is a documented-vs-undocumented signal. The current data model has no
  documentation-coverage table, so this lands as a candidate column, recorded on
  the map as a schema gap rather than a filled slot.

**The honest limit:** the documented read surface returns structure and content,
not an adoption-over-time or health time series. Where the operator wants
documentation traffic or a health trend, that is a product-UI feature with no
documented public read API and stays a `source-gap` even within this source. Do
not promise an executive an automated adoption series from this adapter without
first confirming a read API for it against current vendor docs.

## CONFIG block (fill this, then flip STATUS)

The authoritative copy lives at the top of `supernova_adapter.py`. The token is
read from the named environment variable at run time and never stored.

```
STATUS = "gated"   # -> "active" when access is granted

CONFIG = {
    "token_env_var":    "SUPERNOVA_API_TOKEN",     # NAME only, never a token
    "api_base":         "https://api.supernova.io", # confirm against vendor docs
    "workspace_id":     "",
    "design_system_id": "",
    "version_id":       "",   # empty means the latest version
    "auth_style":       "personal-access-token",
}
```

The activation slots someone fills later are the workspace, design-system, and
version ids, the token in the named environment variable, and the `STATUS` flag.
No structural rewrite.

## Read shape

The SDK wraps the transport; the reads are named at method level:

```
version.components()      -> design components in the version
version.tokens()          -> design tokens in the version
version.assets()          -> assets in the version
version.documentation()   -> documentation structure and content (block or markdown)
```

The single seam in the script is `_read(surface, token)`; wire it to the vendor
SDK (Node) or the data endpoint the SDK wraps, authenticating with the personal
access token.

## Response to 02 transform

- `components`, `tokens`, and `assets` map to `dim_component` rows with the
  matching `kind`, via `transform_inventory()`.
- `documentation` maps to a documented-vs-undocumented count via
  `transform_doc_coverage()`, flagged as a schema gap because 02 has no table
  for it yet.

Both transforms return rows keyed to the target and are directly testable.

## Dry-run branch

Running the script with no flag runs `dry_run()`, which needs no token and no
network:

Commands follow the three-line form in `../../SETUP.md` (interpreter, working directory, invocation); the working directory is this folder.

```
python3 supernova_adapter.py            # credential-free dry-run
python3 supernova_adapter.py --live     # gated: refuses until STATUS=active
```

While gated, `--live` refuses with a clear message and touches no credentials.

## Reality-check note for the technical playbook

The auth method and the read surface here were confirmed against the Supernova
developer docs on 2026-09-08 (SDK read of tokens, assets, components, and
documentation; personal-access-token auth). If a future check finds a documented
adoption or health read API, or that the SDK method names or data-API base have
moved, hand the correction to the maintainer of `04-instrumentation-playbook.md`
rather than editing that file from here.
