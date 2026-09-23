# Third-Party Notices

This theme bundles the following third-party assets. Each is used under its own license.
Update this file whenever an asset is added or removed.

| Asset          | Type  | Source                                           | License | Notice / attribution                         |
| -------------- | ----- | ------------------------------------------------ | ------- | -------------------------------------------- |
| Public Sans    | Font  | https://fonts.google.com/specimen/Public+Sans    | OFL 1.1 | Copyright The Public Sans Project Authors    |
| JetBrains Mono | Font  | https://fonts.google.com/specimen/JetBrains+Mono | OFL 1.1 | Copyright The JetBrains Mono Project Authors |
| Lucide         | Icons | https://lucide.dev                               | ISC     | Copyright (c) Lucide Contributors            |

Both faces are served by the Astro fontsource provider at build time (`fonts:` in
`astro.config.mjs`), latin subset, from the `@fontsource` packages in `package.json`.

The syntax colouring is Shiki with a theme built from this theme's own tokens
(`codeTheme` in `astro.config.mjs`); no third-party colour scheme is bundled.

This site is built on the [Quarry](https://github.com/ondelva/astro-theme-quarry) theme by
ondelva (MIT), with the demo marketing content replaced by ccbar's own.
