# PartnerTap API

Official documentation and example code for integrating with the PartnerTap API.

**Docs site:** [https://partnertap.github.io/partnertap_api_docs/](https://partnertap.github.io/partnertap_api_docs/)

## Repository Structure

- **`/src/content/docs/guides`** — API documentation and guides (rendered by [Starlight](https://starlight.astro.build/))
- **`/src/content/docs/examples`** — Code example documentation
- **`/examples`** — Sample source code organized by programming language
- **`/src/content/docs`** — Original markdown documentation source files (archived)

## Local Development

```bash
npm install
npm run dev       # Start dev server at localhost:4321
npm run build     # Build static site to ./dist
npm run preview   # Preview the production build
```

## Deployment

The site deploys automatically to GitHub Pages on every push to `main` via GitHub Actions.

> **Setup required:** In the repo's GitHub Settings > Pages, set the source to **GitHub Actions**.

## Examples

Working examples are available in [`/examples`](./examples), organized by language.

- **[Python](./examples/python/README.md)** — Export matched accounts to CSV, discover available report columns

## License

This repository is licensed under the [MIT License](./LICENSE) — use, fork, and adapt the examples freely, including for commercial purposes.

## Questions

Open an issue in this repo for documentation feedback or example requests.


test
