# State Management

## State Classification

| State type | Where it lives | How to manage | Example |
|-----------|----------------|---------------|---------|
| Local UI state | Component | `useState`, `useReducer` | Form input values, toggle open/closed |
| Shared UI state | Context or store | `useContext`, Zustand, Redux | Theme preference, sidebar collapsed state |
| Server state | Cache layer | React Query, SWR, Apollo | User profile, product list, search results |
| URL state | Browser URL | `useRouter`, search params | Current page, sort order, active filters |
| Form state | Form library | React Hook Form, Formik | Form values, validation errors, submission status |

## Data Fetching Patterns

| Pattern | When to use | Loading | Error | Empty |
|---------|-------------|---------|-------|-------|
| Fetch on render | Data needed immediately on page load | Skeleton/spinner | Error toast or inline error | Empty state message |
| Fetch on interaction | Data needed after user action | Button loading state | Inline error next to trigger | Handle in response |
| Prefetch | Next likely interaction | Background fetch, no loading UI | Silent failure, retry on explicit action | Handle on navigation |
| Infinite scroll | Paginated lists | Loading indicator at bottom | Inline error with retry | "No more results" |
| Optimistic update | Actions with predictable success | Instant UI update, rollback on error | Revert optimistic update, show error toast | N/A |

## Caching Strategy

| Aspect | Approach |
|--------|----------|
| Cache duration | Configurable per query type (stale-while-revalidate) |
| Invalidation | On mutation success, optimistic update, or manual refetch |
| Deduplication | Identical in-flight queries share a single request |
| Garbage collection | Unused cache entries evicted after configurable TTL |
