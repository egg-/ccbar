# ccbar site — guide for AI agents

The ccbar homepage: a single-page static Astro site built on the
[Quarry](https://github.com/ondelva/astro-theme-quarry) theme (MIT), stripped down to what a
one-file tool's landing page needs. No content collections, no blog, no pricing — everything is
plain data in `src/pages/index.astro`.

## Commands

```bash
pnpm install
pnpm dev              # http://localhost:4321, styleguide at /styleguide (dev only)
pnpm build            # static output to dist/
pnpm preview          # serves dist/
pnpm check            # astro check (types)
pnpm lint
pnpm check:contrast   # WCAG AA for every colour token, light and dark
```

`pnpm check && pnpm lint && pnpm check:contrast && pnpm build` must pass after any change.

CI (`../../.github/workflows/docs-site-ci.yml`, at the repo root — GitHub only reads workflows
there, not from this directory) also runs Lighthouse and a link check against the build. Deploy
(`../../.github/workflows/docs-site-deploy.yml`) publishes `dist/` to GitHub Pages on push to
`main` under `docs/site/**`.

## Where to edit

| To change                                        | Edit                                                                            |
| ------------------------------------------------- | -------------------------------------------------------------------------------- |
| Page copy, sections, the status-line demo data     | `src/pages/index.astro`                                                          |
| Site name, description, URL, nav, footer, social   | `src/config.ts`                                                                   |
| Colours, measures, spacing                         | `src/styles/theme.css` (overrides `tokens.css` — don't edit that file directly)  |
| Header/footer/`<head>` markup                      | `src/components/common/*.astro`, `src/layouts/Base.astro`                        |
| The bordered "terminal" demo figure                | `src/components/sections/StatusLineFrame.astro`                                  |

## The one thing that will bite you: `base`

`astro.config.mjs` sets `base: '/ccbar/'` because this is a GitHub Pages **project** site
(`egg-.github.io/ccbar/`), not a user/org site or a custom domain. Astro does **not**
auto-rewrite a literal `href="/foo"` to include that base — only asset imports and
`Astro.url`/`Astro.site` are base-aware. Every internal link in this site is therefore either:

- page-relative (`href="."`, `href="favicon.svg"`, `href="sitemap-index.xml"`), or
- an in-page fragment (`href="#why"`)

Adding a link that starts with a bare `/` will silently point at the domain root instead of
`/ccbar/`. If the site ever moves to a custom domain or a user/org page, drop `base` from
`astro.config.mjs` — the relative links keep working unchanged.

## Design language (inherited from Quarry)

The **marginal index**: a numbered label that stays in the left margin while its section scrolls,
pure CSS (a counter, never typed) — `Section.astro`, `features.marginalIndex` in `config.ts`.
One measure, one accent colour, `--radius: 3px`. Don't reintroduce cards, shadows, gradients or a
second accent colour — that's what this theme exists to avoid.

## Do not

- Add a content collection, a blog, or a pricing page back. This site is intentionally one page;
  if it grows past that, reconsider whether Quarry (rather than Quarry Pro) is still the right
  base before adding scaffolding.
- Add a client-side framework, or link a CDN for a font, script or icon.
- Use a raw `<img>` for anything that can stay rules-and-mono-text (see `StatusLineFrame.astro`).
- Remove the skip link, focus rings, alt text or `aria-label`s.
- Reintroduce an absolute `href="/..."` internal link (see `base`, above).

## Workflow

1. Make the change.
2. Run `pnpm check && pnpm lint && pnpm check:contrast && pnpm build`, report the result.
3. For layout or colour work, check the page in the browser at 360px as well as desktop, light and
   dark.
