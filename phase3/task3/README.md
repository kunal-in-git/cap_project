# Task C — Figma-to-React: Pricing Card

## No Figma file was available
No sample design was provided and no Figma access exists in this environment (no MCP connection, no browser). Rather than fabricate a Figma source, the "design" here is a written brief standing in for one — a standard SaaS pricing card, the kind found in most free Figma community UI kits: a bordered card with a plan name, large price + billing period, a checklist of features, a CTA button, and a visually distinct "featured" variant with a badge. Everything downstream (the AI-first-pass code, the review, the fixes) is real; only the design source itself is a written substitute for an actual Figma file.

## The component
`PricingCard` — accepts `planName`, `price`, `features` (all required), plus optional `billingPeriod`, `highlighted`, and `onSelect`. Fully interactive: clicking "Choose Plan" calls `onSelect(planName)` and flips the card into a real "Selected ✓" state (via `useState`), not a static mockup.

## Files
- `src/components/PricingCard.jsx` — the component
- `src/components/PricingCard.test.jsx` — 5 vitest/RTL tests
- `src/App.jsx` — demo rendering 3 plans (one highlighted), wiring `onSelect` to visible state
- Tailwind + Vite + Vitest, fully configured

## Running it
```bash
npm install
npm run dev      # demo at http://localhost:5173
npm test         # 5 tests
npm run build    # production bundle
```

## What the AI got right, wrong, and how it was fixed

**Prompt used:** *"Generate a React pricing card component from this design: a bordered card with a plan name, a large price with a '/mo' suffix, a bullet list of features, and a 'Choose Plan' button."*

**What the AI got right on the first pass:** the overall layout and Tailwind class choices (padding, rounded corners, shadow, font sizing/weight hierarchy for price vs. plan name) needed no changes — that part of the design translated correctly on the first try.

**What it got wrong:**
- **Generic component name.** It exported `Card`, not `PricingCard` — mismatched with the file and unhelpful for anyone importing it.
- **No prop validation.** `props.title` and `props.price` were read directly with no `PropTypes`/defaults — passing the wrong shape would silently render `undefined` instead of failing loudly.
- **Placeholder text.** The feature list was hardcoded as `"Feature 1"`, `"Feature 2"`, `"Feature 3"` — not driven by data at all, which fails the task's explicit "no placeholder text" requirement.
- **Not actually interactive.** The "Choose Plan" button had no `onClick` — it was a static-looking button with zero behavior behind it.
- **Mixed styling.** It combined an inline `style` object with Tailwind classes on the same element — inconsistent, and exactly the kind of thing that rots in a real codebase.
- **No "featured" variant**, despite that being a standard part of this design pattern (most pricing cards highlight one plan).

**How it was fixed (manually, by reviewing the diff):**
- Renamed `Card` → `PricingCard`, matching the file and export.
- Added `PropTypes` for every prop, with `planName`/`price`/`features` required.
- Replaced the hardcoded feature strings with a `features.map(...)`, driven entirely by the `features` prop.
- Added real interactivity: a `useState` flag flips the button into a disabled "Selected ✓" state and calls the `onSelect` callback prop with the plan name.
- Removed the inline `style` object; every visual property now comes from Tailwind classes.
- Added the `highlighted` prop, which switches the border to a colored ring and renders a "Most Popular" badge.
- **Found only after running the actual tests, not just eyeballing the code:** React logged `Warning: PricingCard: Support for defaultProps will be removed from function components in a future major release.` — the first fix had used `PricingCard.defaultProps = {...}` (correct for older React idioms, but deprecated for function components). Fixed by moving the defaults into the destructured parameter list (`billingPeriod = "month"`, `highlighted = false`) and deleting the `defaultProps` assignment. This is exactly the kind of thing that only surfaces by actually running the code, not by reading it.

All 5 tests (rendering from props, custom `billingPeriod`, the highlighted badge, the `onSelect`/selected-state interaction, and graceful behavior when `onSelect` is omitted) pass, and `npm run build` completes cleanly.
