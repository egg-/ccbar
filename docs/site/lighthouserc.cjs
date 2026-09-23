// Lighthouse CI. Points at a `pnpm preview` server the CI step starts beforehand, not
// `staticDistDir` -- this site has `base: '/ccbar/'` set (GitHub Pages project site), and
// Lighthouse's own static server ignores that base, so it would serve every page unstyled
// (every asset URL in the HTML is base-prefixed and 404s against a server rooted at `dist`).
// The page list filters itself: delete a page and it drops out of the run instead of
// failing it with a confusing 404. Add your own pages here as you write them.
const { existsSync } = require('node:fs');

const DIST = 'dist';
const ORIGIN = 'http://127.0.0.1:4321/ccbar';

const PAGES = ['/index.html'];

const file = (p) => `${DIST}${p}`;
const built = PAGES.filter((p) => existsSync(file(p)));
// Never hand Lighthouse an empty list; the home page is always there.
const pages = built.length ? built : ['/index.html'];
const url = pages.map((p) => `${ORIGIN}${p.replace(/index\.html$/, '')}`);

module.exports = {
  ci: {
    collect: {
      url,
      numberOfRuns: 3,
    },
    assert: {
      assertions: {
        'categories:performance': [
          'error',
          {
            minScore: 0.95,
          },
        ],
        'categories:accessibility': [
          'error',
          {
            minScore: 0.95,
          },
        ],
        'categories:best-practices': [
          'error',
          {
            minScore: 0.95,
          },
        ],
        'categories:seo': [
          'error',
          {
            minScore: 0.95,
          },
        ],
      },
    },
  },
};
