# ccbar site

The homepage for [ccbar](https://github.com/egg-/ccbar), built with Astro on the
[Quarry](https://github.com/ondelva/astro-theme-quarry) theme (MIT). Deployed to GitHub Pages at
<https://egg-.github.io/ccbar/>.

## Develop

Node.js 22.12+ and pnpm (`npm i -g pnpm`; `package.json` pins the exact version).

```sh
pnpm install
pnpm dev
```

`pnpm dev` also serves `/styleguide` — every colour token and type size on one page. Dev-only,
not part of the build.

## Build

```sh
pnpm build
pnpm preview
```

Search for build output isn't used here; `pnpm build` writes static HTML to `dist/`.

## Content

Everything on the page is plain data in `src/pages/index.astro` — no content collection, no
markdown. Site-wide settings (name, nav, social links) live in `src/config.ts`.

## Deploy

`.github/workflows/docs-site-deploy.yml` at the repo root builds and publishes `dist/` to GitHub
Pages on every push to `main` that touches `docs/site/**`. `docs-site-ci.yml` runs type-check,
lint, contrast check, build, Lighthouse and a link check on the same trigger plus pull requests.

`base` in `astro.config.mjs` is set to `/ccbar/` because this is a GitHub Pages project site
(`egg-.github.io/ccbar`, not a user/org site or a custom domain). Internal links in the theme are
either page-relative (`.`, `favicon.svg`) or in-page fragments (`#why`) so they work under that
base without extra plumbing — an absolute root path like `/foo` would not.

## License

MIT, see [LICENSE](LICENSE) (the theme code). Third-party assets:
[THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md). ccbar itself is MIT-licensed separately — see
the [repo root](../../LICENSE).
