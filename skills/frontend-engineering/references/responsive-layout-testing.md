# Frontend Engineering Methodology Reference

> Comprehensive reference covering responsive layout systems, breakpoint strategy,
> cross-device testing, and frontend testing patterns (component, integration,
> visual regression, accessibility, and test data management).
>
> Compiled: June 2026

---

## Table of Contents

1. [Responsive Layout Systems](#1-responsive-layout-systems)
2. [Breakpoint Strategy](#2-breakpoint-strategy)
3. [Cross-Device Testing Methodology](#3-cross-device-testing-methodology)
4. [Frontend Testing Overview](#4-frontend-testing-overview)
5. [Component Testing](#5-component-testing)
6. [Integration Testing](#6-integration-testing)
7. [Visual Regression Testing](#7-visual-regression-testing)
8. [Accessibility Testing](#8-accessibility-testing)
9. [Test Data Management](#9-test-data-management)

---

## 1. Responsive Layout Systems

### Core Philosophy

> **"CSS Grid is for layout; Flexbox is for alignment."**
>
> Use the right tool for the dimensionality of the problem.

Modern CSS provides three layout primitives, each suited to different concerns.
The modern approach combines all three rather than choosing one.

### 1.1 CSS Grid — Two-Dimensional Layout

**Best for:** Page-level structure, complex multi-axis layouts, precise spatial
control, and layouts where rows AND columns matter simultaneously.

| Use Case | Example |
|---|---|
| Full-page templates | Header, sidebar, main, footer regions |
| Card grids | Gallery, dashboard, e-commerce listings |
| Overlapping elements | Hero sections, magazine layouts |
| Gap-native layouts | `gap` property avoids margin hacks |
| Fraction-based sizing | `fr` units, `minmax()`, `auto-fill`/`auto-fit` |

**Key patterns:**

```css
/* Responsive grid without media queries */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(16rem, 1fr));
  gap: 1rem;
}

/* Named grid areas for page layout */
.page {
  display: grid;
  grid-template-areas:
    "header  header"
    "sidebar main"
    "footer  footer";
  grid-template-columns: 1fr 3fr;
}
```

**When to choose Grid over Flexbox:**
- You need control over both rows and columns simultaneously
- You want explicit placement (grid-column / grid-row)
- You have a predefined layout structure (layout-first design)
- You need overlapping elements without hacks
- You're building page-level templates

### 1.2 Flexbox — One-Dimensional Alignment

**Best for:** Component-level layouts, linear sequences, dynamic content flow,
centering, and distributing items along a single axis.

| Use Case | Example |
|---|---|
| Navigation bars | Horizontal link lists, toolbars |
| Card internal layout | Row of label + value, button groups |
| Centering | Vertically/horizontally centering content |
| Dynamic wrapping | Tags, chips, badge lists |
| Flexible spacing | `justify-content: space-between` on footers |
| Reordering | `order` property for responsive reflow |

**Key patterns:**

```css
/* Centering */
.container {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Responsive wrapping */
.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

/* Holy grail of spacing */
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
```

**When to choose Flexbox over Grid:**
- Content flows in one direction (row OR column, not both)
- Item sizes are unknown and should determine layout (content-first design)
- You need simple centering or alignment
- You're building reusable UI components (buttons, navs, toolbars)
- Items need to wrap to the next line naturally

### 1.3 Container Queries — Component-Level Responsiveness

**Best for:** Reusable components that must adapt to their parent container's
size rather than the viewport. The paradigm shift from viewport-centric to
container-centric design.

```css
/* Establish containment context */
.card-grid {
  container-type: inline-size;
  container-name: cards;
}

/* Query against the container */
@container cards (width >= 30rem) {
  .card {
    display: grid;
    grid-template: "media body" auto / 2fr 3fr;
  }
  .card__media {
    block-size: 100%;
    object-fit: cover;
  }
}

@container cards (width >= 60rem) {
  .card {
    grid-template: "media body aside" auto / 1fr 2fr 1fr;
  }
}
```

**Container units:**
| Unit | Meaning |
|---|---|
| `cqw` | 1% of container width |
| `cqh` | 1% of container height |
| `cqi` | 1% of container inline size |
| `cqb` | 1% of container block size |
| `cqmin` | Smaller of `cqi` and `cqb` |
| `cqmax` | Larger of `cqi` and `cqb` |

**Style queries** (CSS 2025): Conditionally style based on a container's custom
properties or state.

```css
@container style(--density: compact) {
  .card { padding: 0.75rem; gap: 0.5rem; }
}

@container style(--theme: surface) {
  .card { background: #fff; color: #111; }
}
```

**When to use container queries:**
- The same component appears in multiple contexts (sidebar vs. main content)
- You want truly reusable design-system components
- Component breakpoints differ from page-level breakpoints
- You need to scale typography relative to the component, not the viewport

**Progressive enhancement pattern:**

```css
/* Base — works everywhere */
.card { display: block; }

/* Enhancement — only if supported */
@supports (container-type: inline-size) {
  .card-wrapper { container-type: inline-size; }
  @container (width >= 25rem) {
    .card { display: grid; grid-template-columns: 1fr 2fr; }
  }
}
```

### 1.4 Decision Matrix: Grid vs. Flexbox vs. Container Queries

| Criterion | CSS Grid | Flexbox | Container Queries |
|---|---|---|---|
| **Dimensionality** | 2D (rows + cols) | 1D (row OR col) | N/A (context only) |
| **Primary use** | Page layout | Component alignment | Component adaptation |
| **Content vs. layout driven** | Layout-first | Content-first | Container-driven |
| **Gap support** | Native `gap` | Native `gap` | Via host layout |
| **Overlap support** | Native (grid placement) | Not designed for | Not applicable |
| **Reordering** | Via placement | Via `order` | N/A |
| **Responsive technique** | `auto-fill`/`minmax()` + MQ | `flex-wrap` + MQ | `@container` queries |
| **Browser support** | Universal | Universal | ~90%+ (2026) |
| **Reusable components** | Possible, but rigid | Good | Best fit |

### 1.5 Modern Fluid Layout Toolkit (2025+)

Beyond the three primitives, modern CSS offers fluid sizing tools that reduce
or eliminate media queries:

```css
/* Fluid typography */
h1 { font-size: clamp(1.5rem, 2.5vw + 1rem, 3rem); }

/* Fluid grid columns */
.grid { grid-template-columns: repeat(auto-fill, minmax(clamp(12rem, 30%, 24rem), 1fr)); }

/* Intrinsic sizing with aspect-ratio */
.card { aspect-ratio: 16 / 9; }

/* Logical properties for RTL support */
.card { margin-inline: 1rem; padding-block: 2rem; }
```

---

## 2. Breakpoint Strategy

### 2.1 Device-Agnostic vs. Content-Driven

**The industry consensus in 2025-2026 is: content-driven breakpoints, not
device-based presets.**

| Approach | Description | Verdict |
|---|---|---|
| **Device-agnostic** | Breakpoints at key widths where content breaks (e.g., 480px, 768px, 1024px) | Legacy best practice — better than fixed device targeting, but still viewport-centric |
| **Content-driven** | Breakpoints determined by the content itself — resize until it looks wrong, then add a breakpoint | Modern best practice |
| **Container-driven** | Breakpoints live on components via `@container`, not the viewport | Cutting edge (2025+) |

### 2.2 The Problem With Fixed Breakpoints

Traditional breakpoint strategy used device classes:

```css
/* Avoid: device-specific */
@media (max-width: 575px)   { /* phones */ }
@media (min-width: 576px)   { /* tablets */ }
@media (min-width: 992px)   { /* laptops */ }
@media (min-width: 1200px)  { /* desktops */ }
```

This fails because:
- New devices appear constantly (foldables, ultra-wides, 2-in-1s)
- The same component might need different breakpoints in different contexts
- It couples layout logic to arbitrary screen widths that may not match actual content needs

### 2.3 Content-Driven Breakpoint Strategy

**Methodology:**

1. **Design in the browser** — resize gradually; stop every time the layout breaks
2. **Add a breakpoint at each breaking point**, naming it after what breaks, not the pixel value
3. **Use `rem` not `px`** for breakpoints — respects user font-size preferences
4. **Prefer fluid techniques first** (clamp, minmax, auto-fill) before adding media queries

```css
/* Good: content-driven breakpoints in rem */
/* Breakpoints at 30rem, 48rem, 64rem */

/* Prefer: fluid techniques before media queries */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(18rem, 1fr));
}

/* Only add media queries when fluid isn't enough */
@media (width >= 64rem) {
  .card-grid { grid-template-columns: repeat(3, 1fr); }
}
```

### 2.4 Recommended Breakpoint Ranges

Not fixed values, but ranges where content typically breaks:

| Range (approx) | Common name | Behaviour |
|---|---|---|
| < 30rem (~480px) | Single-column | Stack everything |
| 30-48rem (~480-768px) | Narrow | 2-column grids possible |
| 48-64rem (~768-1024px) | Medium | 3-column layouts, sidebars |
| 64-90rem (~1024-1440px) | Wide | Full layouts, multi-column |
| > 90rem (~1440px) | Extra-wide | Max-width constraints, whitespace |

> **Key insight:** These are guidelines, not dogma. Let YOUR content determine
> the exact values. A data table might need 50rem; a long-form article might
> need only 35rem.

### 2.5 Modern Media Query Syntax

CSS Media Queries Level 4+ introduced range syntax (widely supported in 2025):

```css
/* Old syntax */
@media (min-width: 768px) and (max-width: 1024px) { }

/* New range syntax — cleaner */
@media (768px <= width <= 1024px) { }
@media (width >= 48rem) { }
@media (width < 30rem) { }
```

### 2.6 Preference Queries (Accessibility-Aware)

Beyond size, modern responsive design queries user preferences:

```css
/* Respect reduced motion */
@media (prefers-reduced-motion: reduce) {
  * { animation-duration: 0.01ms !important; }
}

/* Respect reduced transparency */
@media (prefers-reduced-transparency: reduce) {
  .glass { background: solid; }
}

/* Respect dark mode */
@media (prefers-color-scheme: dark) {
  :root { --bg: #111; --text: #eee; }
}

/* Respect increased contrast */
@media (prefers-contrast: more) {
  .card { border: 2px solid; }
}
```

---

## 3. Cross-Device Testing Methodology

### 3.1 Test Pyramid for Responsive Design

```
        /\
       /  \         Manual device testing
      / M  \        (real hardware for critical paths)
     / a  u \
    / n  a  \      Device-emulation E2E
   / u  l    \     (Playwright emulation matrix)
  / a  t  e   \
 / l  e  s  t  \
/_______________\   Automated layout-safe checks
                   (container queries, fluid validation)
```

### 3.2 Device Emulation Matrix (Playwright/Cypress)

Define your test matrix based on actual user analytics. Common strategy:

```javascript
// Playwright config — device emulation
const devices = [
  { name: 'iPhone 15', width: 390, height: 844, deviceScaleFactor: 3 },
  { name: 'Pixel 8', width: 412, height: 915, deviceScaleFactor: 2.625 },
  { name: 'iPad Air', width: 820, height: 1180, deviceScaleFactor: 2 },
  { name: 'Desktop 1440', width: 1440, height: 900, deviceScaleFactor: 1 },
  { name: 'Desktop 1920', width: 1920, height: 1080, deviceScaleFactor: 1 },
];
```

### 3.3 Responsive Testing Checklist

| Check | Method | Tooling |
|---|---|---|
| Content doesn't overflow | Automated CSS assertion | Playwright `toHaveCSS` |
| Touch targets >= 44px | Automated size check | Playwright bounding box |
| No horizontal scrollbar | Visual regression | Percy / Chromatic |
| Font size >= 16px (iOS zoom) | Emulation check | Safari/iOS device |
| Tap targets don't overlap | Layout check | axe-core / manual |
| All interactive elements work on touch | E2E test | Playwright touch emulation |
| Viewport meta tag present | Lint check | Lighthouse |

### 3.4 Real Device Testing Strategy

**Automated emulation covers ~80% of responsive bugs.** Real devices are needed for:

1. **Touch interactions** — hover states, drag, swipe, force touch
2. **Hardware-specific** — notch, dynamic island, camera cutouts, safe areas
3. **Performance** — real CPU/memory constraints, network throttling
4. **Rendering differences** — Safari vs. Chrome font rendering, sub-pixel differences

**Practical approach:**
- **CI/CD:** Emulation matrix (Playwright + devices)
- **Pull request review:** Visual regression (Percy/Chromatic)
- **Pre-release:** Real device cloud (BrowserStack / Sauce Labs / AWS Device Farm)
- **Critical paths:** Physical devices owned by the team

### 3.5 Environment Simulation

```javascript
// Playwright — responsive + environment simulation
test('homepage on slow 3G', async ({ page }) => {
  await page.emulate({ viewport: { width: 390, height: 844 } });
  await page.context().addInitScript(() => {
    // Simulate reduced motion
    window.matchMedia = (query) => ({
      matches: query.includes('reduce-motion'),
      media: query,
      addListener: () => {},
      removeListener: () => {},
    });
  });
  await page.goto('/', { waitUntil: 'networkidle' });
  // assertions...
});
```

---

## 4. Frontend Testing Overview

### 4.1 The Testing Trophy (Modern Frontend)

Replace the traditional "testing pyramid" with Kent C. Dodds' **Testing Trophy**,
which better reflects frontend priorities:

```
    /\
   /  \        Static analysis (TypeScript, ESLint)
  /    \       Unit/Component tests (Vitest + Testing Library)
 /      \      Integration tests (Playwright / Cypress)
/________\     E2E tests (critical user journeys only)
```

**Static analysis** catches type errors and lint issues at compile time.
**Component tests** verify isolated UI behaviour.
**Integration tests** (the bulk of your test suite) verify features work together.
**E2E tests** cover the most critical user journeys end-to-end.

### 4.2 Testing Matrix Summary

| Layer | Tool | Scope | Speed | Flakiness | CI cost |
|---|---|---|---|---|---|
| Static | TypeScript, ESLint | Types, lint | Instant | Never | Free |
| Component | Vitest + Testing Library | Individual components | Fast (ms) | Low | Cheap |
| Integration | Playwright / Cypress | Features, page interactions | Medium (s) | Low-Med | Moderate |
| Visual regression | Percy / Chromatic | Pixel-level UI | Medium (s) | Medium | Higher |
| Accessibility | axe-core + Lighthouse | WCAG violations | Fast (ms-s) | Low | Cheap |
| E2E critical | Playwright | Full user journeys | Slow (min) | Medium | Highest |

---

## 5. Component Testing

### 5.1 Vitest + React Testing Library

**Standard setup (2025-2026):**

```javascript
// vitest.config.js
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.js',
    css: true, // process CSS imports
  },
});
```

```javascript
// src/test/setup.js
import '@testing-library/jest-dom';
import { cleanup } from '@testing-library/react';
import { afterEach } from 'vitest';

afterEach(() => { cleanup(); });
```

### 5.2 Core Query Priority

**Test as users experience the UI:**

```
1. getByRole          — Preferred for almost everything
2. getByLabelText     — Form fields
3. getByPlaceholderText — Input hints
4. getByText          — Non-interactive text
5. getByDisplayValue  — Form values
6. getByAltText       — Images
7. getByTitle         — Tooltips
8. getByTestId        — Last resort (data-testid)
```

### 5.3 Component Test Patterns

**Render + Interaction + Assert:**

```javascript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Counter } from './Counter';

it('increments count when button clicked', async () => {
  const user = userEvent.setup();
  render(<Counter />);

  await user.click(screen.getByRole('button', { name: /increment/i }));

  expect(screen.getByText('Count: 1')).toBeInTheDocument();
});
```

**Test behaviour, not implementation:**

```javascript
// Bad: testing internal state
expect(counter.state.count).toBe(1);

// Good: testing what the user sees
expect(screen.getByText('Count: 1')).toBeInTheDocument();
```

**Mock external dependencies:**

```javascript
import axios from 'axios';
vi.mock('axios');

it('displays posts after fetch', async () => {
  const posts = [{ id: 1, title: 'Hello' }];
  axios.get.mockResolvedValue({ data: posts });

  render(<PostsList />);

  await waitFor(() => {
    expect(screen.getByText('Hello')).toBeInTheDocument();
  });
});
```

**Custom hook testing:**

```javascript
import { renderHook, waitFor } from '@testing-library/react';

it('returns data from fetch', async () => {
  const { result } = renderHook(() => useFetch('/api/data'));

  await waitFor(() => expect(result.current.loading).toBe(false));

  expect(result.current.data).toEqual({ id: 1 });
});
```

### 5.4 Best Practices (Component Testing)

| Practice | Rationale |
|---|---|
| Test user-visible outcomes, not internals | Refactoring doesn't break tests |
| One assertion per test (when practical) | Clear failure messages |
| Use `userEvent`, not `fireEvent` | Realistic interaction simulation |
| Mock API calls, not modules | Tests stay fast and focused |
| Prefer `screen.` methods over destructured render | Keeps tests maintainable |
| Always clean up DOM between tests | Prevents test pollution |
| Use descriptive test names | `it('disables button while submitting')` |
| Write the test for the component's contract, not its internals | Tests validate behaviour |

---

## 6. Integration Testing

### 6.1 Playwright vs. Cypress (2025-2026)

| Dimension | Playwright | Cypress |
|---|---|---|
| **Browser support** | Chromium, Firefox, WebKit | Chromium, Firefox (limited), WebKit (beta) |
| **Language** | JS/TS, Python, Java, .NET | JS/TS only |
| **Architecture** | Browser protocol (CDP) — runs outside browser | In-browser — runs inside the browser |
| **Multi-tab/window** | Native support | Limited |
| **Network mocking** | Route interception | cy.intercept |
| **Parallel execution** | Native, sharding | Dashboard required |
| **Cross-origin iframes** | Full support | Limited |
| **Mobile emulation** | Built-in device descriptors | cy.viewport only |
| **API testing** | Same context as browser | cy.request |
| **Community** | Larger momentum (91% satisfaction in State of JS 2025) | Mature, but satisfaction declined (72%) |
| **CI integration** | Zero config | Dashboard or plugin |

**Bottom line (2026):** Playwright has become the default choice for new
projects due to broader browser support, multi-tab handling, and stronger
momentum. Cypress remains viable for teams already invested in its ecosystem.

### 6.2 Playwright Integration Test Patterns

**Page Object Model (POM) — recommended:**

```typescript
// pages/LoginPage.ts
export class LoginPage {
  constructor(private page: Page) {}

  async goto() { await this.page.goto('/login'); }
  async login(email: string, password: string) {
    await this.page.fill('[data-testid="email"]', email);
    await this.page.fill('[data-testid="password"]', password);
    await this.page.click('[data-testid="submit"]');
  }
  async getErrorMessage() {
    return this.page.textContent('[data-testid="error"]');
  }
}
```

```typescript
// tests/login.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

test('shows error on invalid credentials', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('bad@email.com', 'wrong');

  await expect(loginPage.getErrorMessage()).toContain('Invalid credentials');
});
```

**Responsive integration test with device emulation:**

```typescript
test('mobile navigation is usable', async ({ page }) => {
  // Emulate mobile viewport
  await page.setViewportSize({ width: 390, height: 844 });

  await page.goto('/');
  await page.click('[data-testid="hamburger"]');
  await expect(page.locator('[data-testid="nav-menu"]')).toBeVisible();

  // Touch targets meet minimum size (44x44 CSS pixels)
  const links = page.locator('nav a');
  const count = await links.count();
  for (let i = 0; i < count; i++) {
    const box = await links.nth(i).boundingBox();
    expect(box?.width).toBeGreaterThanOrEqual(44);
    expect(box?.height).toBeGreaterThanOrEqual(44);
  }
});
```

**API mocking in integration tests:**

```typescript
test('displays empty state when no results', async ({ page }) => {
  // Intercept API call and return empty results
  await page.route('**/api/search**', async route => {
    await route.fulfill({ json: { results: [] } });
  });

  await page.goto('/search');
  await page.fill('[name="q"]', 'nonexistent');
  await page.press('[name="q"]', 'Enter');

  await expect(page.getByText('No results found')).toBeVisible();
});
```

### 6.3 Test Organization

```
tests/
  e2e/
    login.spec.ts
    checkout.spec.ts
  integration/
    api/
      search.spec.ts
      user.spec.ts
    features/
      filters.spec.ts
      pagination.spec.ts
  visual/
    homepage.spec.ts
    product-card.spec.ts
  accessibility/
    homepage.a11y.spec.ts
    form.a11y.spec.ts
```

---

## 7. Visual Regression Testing

### 7.1 Approaches

| Approach | Tool | Pros | Cons |
|---|---|---|---|
| **Pixel-by-pixel screenshot diff** | Percy, Applitools, Chromatic | Catches every visual change | Baseline management, flakiness from animated content |
| **DOM snapshot** | Jest/Vitest snapshots | Fast, no browser needed | Fragile, doesn't catch CSS-only changes |
| **CSS-in-JS snapshot** | Storybook + Chromatic | Component-level, integrated with design system | Requires Storybook setup |
| **Layout diff** | Playwright screenshot | Full-page, device-emulated | Slower, per-environment diffs |
| **AI-assisted** | Percy AI, Applitools Eyes | Smart change detection, reduced false positives | Cost, vendor lock-in |

### 7.2 Percy (BrowserStack)

```javascript
// Cypress + Percy
cy.visit('/');
cy.percySnapshot('Homepage');

// Playwright + Percy
import percySnapshot from '@percy/playwright';
test('homepage visual', async ({ page }) => {
  await page.goto('/');
  await percySnapshot(page, 'Homepage');
});
```

### 7.3 Chromatic (Storybook)

```javascript
// .github/workflows/chromatic.yml
name: Chromatic
on: push
jobs:
  chromatic:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - run: npm ci
      - uses: chromaui/action@v11
        with:
          projectToken: ${{ secrets.CHROMATIC_PROJECT_TOKEN }}
```

### 7.4 Playwright Native Visual Testing

```typescript
import { test, expect } from '@playwright/test';

test('homepage matches snapshot', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveScreenshot('homepage.png', {
    maxDiffPixels: 100,
    fullPage: true,
  });
});
```

### 7.5 Visual Testing Best Practices

| Practice | Detail |
|---|---|
| Mock dynamic content | Replace real data with fixtures for stable screenshots |
| Freeze animations | Use `page.addStyleTag()` to disable CSS animations |
| Isolate component states | Test loading, empty, error, and edge case states |
| Set consistent viewport | Always snapshot from known viewport sizes |
| Use CI diff thresholds | Allow configurable pixel tolerance to reduce flakiness |
| Review diffs in PRs | Block merging on unapproved visual changes |
| Rebase baselines intentionally | Not on every commit — only when changes are expected |

---

## 8. Accessibility Testing

### 8.1 Automation Coverage

Automated accessibility testing catches roughly **30-40%** of WCAG violations.
This covers the "low-hanging fruit" — common, detectable issues. Manual testing
is still required for the remaining 60-70%.

**What automation catches well:**
- Missing alt text on images
- Missing form labels
- Insufficient colour contrast
- Duplicate IDs
- Missing ARIA attributes
- Invalid ARIA usage
- Missing lang attributes
- Empty links / buttons

**What requires manual testing:**
- Logical reading order
- Keyboard navigation flow
- Screen reader announcements
- Focus management
- Meaningful alt text
- Colour-only information transmission

### 8.2 axe-core Integration

**In Vitest/unit tests (jest-axe):**

```javascript
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
expect.extend(toHaveNoViolations);

it('has no accessibility violations', async () => {
  const { container } = render(<Button>Click me</Button>);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

**In Playwright E2E tests:**

```typescript
import AxeBuilder from '@axe-core/playwright';

test('homepage has no a11y violations', async ({ page }) => {
  await page.goto('/');
  const results = await new AxeBuilder({ page }).analyze();
  expect(results.violations).toEqual([]);
});

// Specific WCAG levels
test('meets WCAG AA requirements', async ({ page }) => {
  await page.goto('/');
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
    .analyze();
  expect(results.violations).toEqual([]);
});

// Targeted scan — specific element
test('navigation menu is accessible', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: 'Menu' }).click();
  const results = await new AxeBuilder({ page })
    .include('#nav-flyout')
    .analyze();
  expect(results.violations).toEqual([]);
});
```

### 8.3 Lighthouse CI

```javascript
// lighthouserc.json
{
  "ci": {
    "collect": {
      "numberOfRuns": 3,
      "staticDistDir": "./build",
      "settings": { "onlyCategories": ["accessibility"] }
    },
    "assert": {
      "assertions": {
        "categories:accessibility": ["error", { "minScore": 0.9 }]
      }
    },
    "upload": {
      "target": "temporary-public-storage"
    }
  }
}
```

### 8.4 CI/CD Integration

```yaml
# .github/workflows/accessibility.yml
name: Accessibility
on: [pull_request]
jobs:
  a11y:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - run: npm run build
      - run: npx playwright install
      - name: Run a11y tests
        run: npx playwright test --project=a11y
```

### 8.5 Accessibility Testing Maturity Model

| Level | What you do | Coverage |
|---|---|---|
| 1. None | No accessibility testing | 0% |
| 2. Manual only | Occasional Lighthouse audits | 30-40% (sporadic) |
| 3. Automated in CI | axe-core on every PR in Playwright tests | 30-40% (consistent) |
| 4. Automated + enforcement | Lighthouse CI score gates | 30-40% + regression detection |
| 5. Integrated into component tests | jest-axe on every component | 30-40% at component level |
| 6. Full pipeline | Axe + Lighthouse + manual audits + screen reader | 30-40% automated + 60-70% manual |

---

## 9. Test Data Management

### 9.1 Data Generation Strategies

| Strategy | Description | When to use |
|---|---|---|
| **Fixtures** | Static, pre-defined data in JSON/YAML files | Test data that doesn't change often |
| **Factories** | Programmatic data generation with overrides | Many tests with slight data variations |
| **Faker** | Random realistic data (names, emails, addresses) | Stress testing, large datasets |
| **Seed data** | Known, reproducible database state | E2E tests needing a consistent baseline |
| **API mocks** | Intercepted network responses | Integration/component tests without a backend |

### 9.2 Fixture Pattern

```json
// src/test/fixtures/user.json
{
  "id": 1,
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "role": "admin"
}
```

```javascript
// Using fixture in a test
import userFixture from './fixtures/user.json';

it('renders user profile', () => {
  render(<UserProfile user={userFixture} />);
  expect(screen.getByText('Alice Johnson')).toBeInTheDocument();
});
```

### 9.3 Factory Pattern

```javascript
// src/test/factories/user.js
import { faker } from '@faker-js/faker';

export function buildUser(overrides = {}) {
  return {
    id: faker.number.int({ min: 1, max: 10000 }),
    name: faker.person.fullName(),
    email: faker.internet.email(),
    role: faker.helpers.arrayElement(['user', 'admin', 'moderator']),
    avatar: faker.image.avatar(),
    createdAt: faker.date.past().toISOString(),
    ...overrides,
  };
}

// Usage
const admin = buildUser({ role: 'admin', name: 'Admin User' });
const users = Array.from({ length: 20 }, () => buildUser());
```

### 9.4 Request Mocking Patterns

```javascript
// MSW (Mock Service Worker) — recommended approach
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
  http.get('/api/users/:id', ({ params }) => {
    return HttpResponse.json({
      id: params.id,
      name: 'Mocked User',
    });
  }),
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

it('fetches and displays user', async () => {
  render(<UserDetail userId="42" />);
  await waitFor(() => {
    expect(screen.getByText('Mocked User')).toBeInTheDocument();
  });
});
```

### 9.5 Test Data Isolation

| Concern | Solution |
|---|---|
| **State leakage between tests** | `afterEach` cleanup, MSW handler reset |
| **Database state for E2E** | Database seeding before test suite, teardown after |
| **Shared state in factories** | Return new objects, not singletons |
| **Crypto-dependent IDs** | Deterministic faker seed: `faker.seed(123)` |
| **Dates / timers** | Fake timers: `vi.useFakeTimers()` |

### 9.6 Test Data Setup Patterns

```javascript
// Pattern 1: Setup in describe block
describe('UserList', () => {
  const users = Array.from({ length: 5 }, (_, i) =>
    buildUser({ id: i + 1 })
  );

  it('renders all users', () => {
    render(<UserList users={users} />);
    expect(screen.getAllByRole('listitem')).toHaveLength(5);
  });
});

// Pattern 2: Custom render
function renderWithProviders(ui, { users = [], ...options } = {}) {
  const wrapper = ({ children }) => (
    <UserProvider users={users}>
      {children}
    </UserProvider>
  );
  return render(ui, { wrapper, ...options });
}

// Pattern 3: Test factory function
function setupUserList(overrides = {}) {
  const users = overrides.users ?? [buildUser()];
  const onSelect = vi.fn();
  const utils = render(<UserList users={users} onSelect={onSelect} />);
  return { ...utils, users, onSelect };
}
```

### 9.7 Frontend Test Data Best Practices

| Practice | Detail |
|---|---|
| Use realistic data | Catch real rendering issues, not just schema validation |
| Separate data from assertions | Factories encourage readable, intention-revealing tests |
| Prefer MSW over vi.mock | MSW works at the network level, doesn't need module mocking |
| Seed deterministically | `faker.seed(123)` for reproducible failures |
| Mock at the right level | API mocking > module mocking > global mocking |
| Clean up between tests | Prevent state leakage that causes flaky tests |
| Keep fixtures small | Only include fields the test actually exercises |

---

## References & Further Reading

- **CSS Grid vs Flexbox**: blog.logrocket.com/css-flexbox-vs-css-grid
- **Container Queries Guide**: caisy.io/blog/css-container-queries
- **Beyond Media Queries (2025)**: medium.com/@orami98/beyond-media-queries
- **Modern Breakpoint Strategy**: penpot.app/blog/how-to-use-css-and-media-query-breakpoints
- **Playwright Accessibility Testing**: playwright.dev/docs/accessibility-testing
- **Vitest + Testing Library Setup**: freecodecamp.org/news/how-to-test-react-applications-with-vitest
- **Accessibility in CI/CD**: testparty.ai/blog/accessibility-testing-cicd
- **Visual Regression Guide**: desplega.ai/blog/deep-dive-7-visual-regression-testing-ui-bugs
- **Responsive Web Design Basics**: web.dev/articles/responsive-web-design-basics
- **Ten Modern Layouts in One Line of CSS**: web.dev/articles/one-line-layouts
