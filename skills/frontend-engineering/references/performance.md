# Client-Side Performance

## Core Web Vitals Targets

| Metric | Good | Needs improvement | Poor |
|--------|------|-------------------|------|
| LCP (Largest Contentful Paint) | ≤ 2.5s | 2.5s - 4.0s | > 4.0s |
| FID (First Input Delay) / INP | ≤ 100ms | 100ms - 300ms | > 300ms |
| CLS (Cumulative Layout Shift) | ≤ 0.1 | 0.1 - 0.25 | > 0.25 |

## Bundle Optimization

| Technique | Impact | Effort |
|-----------|--------|--------|
| Code splitting by route | High | Low (built-in with most frameworks) |
| Dynamic imports for heavy components | Medium | Low |
| Tree shaking unused exports | Medium | Low (enabled by default in bundlers) |
| Import cost awareness | Medium | Medium (lint rules, CI checks) |
| Image optimization (format, sizing, lazy loading) | High | Medium |
| Dependency audit (remove unused, find lighter alternatives) | Medium | High |

## Render Optimization

| Pattern | When to use | Mechanism |
|---------|-------------|-----------|
| Memoization | Pure components that re-render often | `React.memo`, `useMemo`, `useCallback` |
| Virtualization | Long lists (1000+ items) | `react-window`, `react-virtuoso` |
| Debouncing | High-frequency events (search input, scroll) | Debounce by 300-500ms |
| Throttling | Rate-limited updates (resize, scroll position) | Throttle by 100-200ms |
| Progressive hydration | Heavy interactive content below the fold | Lazy hydrate on visibility |
