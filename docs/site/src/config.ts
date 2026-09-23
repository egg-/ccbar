// src/config.ts — single entry point for site settings. Everything site-specific lives here; never hardcode in components.
export const site = {
  name: 'ccbar',
  description: 'A one-file status line for Claude Code. No daemon, no cache, no network, no dependencies.',
  url: 'https://egg-.github.io/ccbar/',
  locale: 'en',
  author: 'egg',
  defaultOgImage: 'og-default.png',
} as const;

export const nav = {
  header: [
    { label: 'Why', href: '#why' },
    { label: 'Reading the bar', href: '#reading' },
    { label: 'Install', href: '#install' },
  ],
  cta: { label: 'View on GitHub', href: 'https://github.com/egg-/ccbar' },
  footer: [
    {
      title: 'ccbar',
      links: [
        { label: 'Why', href: '#why' },
        { label: 'Reading the bar', href: '#reading' },
        { label: 'Install', href: '#install' },
      ],
    },
    {
      title: 'Project',
      links: [
        { label: 'Source', href: 'https://github.com/egg-/ccbar' },
        { label: 'License (MIT)', href: 'https://github.com/egg-/ccbar/blob/main/LICENSE' },
      ],
    },
  ],
  social: [{ label: 'GitHub', href: 'https://github.com/egg-/ccbar', icon: 'lucide:github' }],
} as const;

export const seo = {
  titleTemplate: '%s · ccbar',
  twitterHandle: '',
  jsonLd: { type: 'Organization' as 'Person' | 'Organization', name: site.name },
};

export const features = {
  darkMode: true,
  // The signature: numbered labels that stay in the left margin while a section
  // scrolls. Off puts the label inline above the section heading instead.
  marginalIndex: true,
};

export const analytics = {
  provider: null as null | 'plausible' | 'ga4' | 'umami',
  id: '',
  host: '',
};
