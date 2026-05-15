# Agent Showcase

Static publishing repo for two interview-facing pages:

- `agent-eval/`: agent evaluation showcase
- `agent-dev/`: Task Forge v2 showcase

The root `index.html` is generated from `index.json` by the top-level
`build_showcase.py`. The two subpages now also keep their own local source files
and build scripts in this repo, so one top-level command can rebuild all three
pages.

## Rebuild

```bash
python build_showcase.py
```

If you also want to refresh subpage source files from the sibling
`Agent_info_flow` workspace before rebuilding:

```bash
python build_showcase.py --sync-sources
```

If only the landing page changed:

```bash
python build_showcase.py --skip-subpages
```
