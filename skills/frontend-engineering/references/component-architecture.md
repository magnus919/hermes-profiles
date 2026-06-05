# Component Architecture

## Composition Patterns

| Pattern | When to use | Example |
|---------|-------------|---------|
| Atomic design | Design systems with clear hierarchy | `Button → FormField → AddressForm → CheckoutPage` |
| Compound components | Related components that share implicit state | `Select.Trigger`, `Select.Options`, `Select.Option` |
| Render props | Maximum flexibility in component behavior | Data provider that delegates rendering to consumer |
| Controlled vs uncontrolled | Form inputs, external state management | Controlled: state lives in parent. Uncontrolled: state lives in component |
| Higher-order components | Cross-cutting concerns (auth, logging) | `withAuth(Component)`, `withAnalytics(Component)` |

## Props and State Interface Design

| Aspect | Guideline |
|--------|-----------|
| Props should be minimal | Pass only what the component needs. Avoid prop drilling with context. |
| Defaults for optional props | Every optional prop has a sensible default. |
| Boolean props are named as questions | `isLoading`, `hasError`, `isDisabled`, `canSubmit` |
| Callback props describe the event | `onClick`, `onSubmit`, `onChange`, `onClose` |
| Avoid overloaded props | A prop should do one thing. `variant="primary|secondary|danger"`, not `mode="view|edit|admin"` |

## Accessibility Fundamentals

Every component must support:

- **Keyboard navigation** — All interactive elements reachable and operable via keyboard (Tab, Enter, Escape, Arrow keys)
- **Focus management** — Visible focus indicators, logical tab order, focus trapping in modals
- **Screen reader support** — ARIA labels, roles, live regions, landmarks
- **Color contrast** — Text meets WCAG AA (4.5:1 for normal text, 3:1 for large text)
- **Reduced motion** — Respect `prefers-reduced-motion` for animations and transitions
