# Agent Showcase

Static publishing repo for two interview-facing pages:

- `agent-eval/`: agent evaluation showcase
- `agent-dev/`: Task Forge v2 showcase

The root `index.html` is generated from `index.json` by `build_showcase.py`.
Running the builder from this repo also syncs the two subpages from the sibling
`Agent_info_flow` workspace.

## Rebuild

```bash
python build_showcase.py
```

If the subpages are already synced and only the landing page changed:

```bash
python build_showcase.py --skip-sync
```
