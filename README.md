# Sumi Browser

A minimal, plugin-extensible browser built on Firefox.

Sumi keeps only what every user needs in its core, and leaves everything else to plugins and the community.

## Philosophy

- **Anti-Bloat** — If even one user would be annoyed by a feature, it doesn't belong in the core
- **Externalize** — We maintain the foundation; features are built by the community
- **Permissive** — Plugins can modify anything, even core UI — just like Minecraft mods

## Features

- Vertical tabs with collapsible sidebar
- Command palette (Ctrl+T)
- Split view
- Dark theme by default
- Full Firefox extension support

## Building

Requires: Node.js, Python, Rust, Visual Studio C++ Build Tools, MozillaBuild, 7-Zip

```bash
npm install
npm run init    # Download Firefox source + bootstrap + apply patches
npm run build   # Full build (~40 min)
npm start       # Launch
```

After `surfer reset`, re-apply engine patches:

```bash
python scripts/apply-engine-patches.py
```

## Development

```bash
npm run build:ui        # Rebuild UI changes only (fast)
npm run export <file>   # Save engine/ changes as patches
npm run import          # Apply patches to engine/
npm run status          # Show pending changes in engine/
```

See [CLAUDE.md](CLAUDE.md) for the full development guide.

## License

[MPL-2.0](https://www.mozilla.org/en-US/MPL/2.0/)
