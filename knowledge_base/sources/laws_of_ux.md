# Laws of UX — Comprehensive Design Laws and Psychological Principles

## Aesthetic-Usability Effect

Users perceive aesthetically pleasing designs as more usable than less aesthetically pleasing ones, regardless of actual usability. Beautiful design creates a positive emotional response that makes users more tolerant of minor usability issues.

### Implications for Design
- Visual design matters — it directly impacts perceived usability
- Aesthetics can mask usability problems during testing
- Invest in visual polish, but don't let it substitute for actual usability testing
- First impressions are heavily influenced by visual design quality

### Common Violations
- Prioritizing functionality over visual quality, creating a "developer UI"
- Over-designing to the point where aesthetics hurt actual usability
- Assuming a beautiful design means the design is usable

---

## Choice Overload (Hick's Law Related)

Users become overwhelmed when presented with too many options simultaneously. Decision paralysis occurs and user satisfaction decreases as the number of choices increases.

### Implications for Design
- Limit the number of options visible at once (aim for 3-5 primary choices)
- Use progressive disclosure to reveal options as needed
- Provide smart defaults and recommended options
- Group related options into categories
- Consider using filters and search for large option sets

### Common Violations
- Navigation menus with 15+ top-level items
- Settings pages showing every option at once
- Product pages with too many variant selectors visible simultaneously
- Onboarding flows asking too many questions upfront

---

## Chunking

People process information more effectively when it is broken into smaller, meaningful groups rather than presented as a continuous stream. This aligns with working memory limitations.

### Implications for Design
- Break long forms into logical multi-step flows
- Group related content with clear visual separators
- Use whitespace and headings to create information clusters
- Format phone numbers, credit cards, and dates in familiar chunks (555-1234, 4242 4242 4242 4242)
- Organize navigation into grouped categories

### Common Violations
- Long, unbroken forms with 20+ fields on one page
- Walls of text without headings, bullets, or visual breaks
- Displaying long numbers without formatting (e.g., 5551234567 vs 555-123-4567)

---

## Cognitive Load

The total mental effort required to use an interface. Cognitive load consists of intrinsic load (inherent task complexity), extraneous load (poor design), and germane load (learning). Good design minimizes extraneous cognitive load.

### Implications for Design
- Remove unnecessary elements that don't serve user goals
- Use familiar patterns and conventions to reduce learning
- Provide clear visual hierarchy so users know where to look
- Avoid requiring users to remember information between steps
- Use progressive disclosure — show only what's needed now
- Minimize the number of decisions per screen

### Common Violations
- Dense interfaces with no clear hierarchy
- Requiring users to mentally translate data (e.g., timestamps without time zone labels)
- Inconsistent UI patterns that force relearning
- Excessive animations and visual noise competing for attention

---

## Doherty Threshold

Productivity increases dramatically when a system responds within 400 milliseconds. Below this threshold, users maintain flow state; above it, attention fragments and errors increase.

### Implications for Design
- Target <400ms response time for all interactions
- Use skeleton screens and shimmer loading for content that takes longer
- Provide instant visual feedback for clicks and taps (button press states)
- Use optimistic UI updates — show the expected result immediately, sync in background
- Add progress indicators for operations exceeding 1 second
- Use animations (200-300ms) to bridge gaps in responsiveness

### Common Violations
- No loading feedback during data fetches
- Blocking the entire UI during save operations
- Submit buttons with no visual press state
- Full-page reloads instead of partial updates

---

## Fitts's Law

The time required to move to a target depends on the distance to the target and the size of the target. Larger, closer targets are faster to interact with.

### Implications for Design
- Make primary action buttons large and prominent
- Place frequently used actions near the user's current focus
- Touch targets should be minimum 44x44px (iOS) or 48x48dp (Android)
- Put destructive actions away from primary actions to prevent accidental clicks
- Consider thumb zones for mobile — bottom of screen is easiest to reach
- Edge and corner positions are effectively infinite in size (Fitts's Law advantage)

### Common Violations
- Small clickable text links as primary actions
- Touch targets smaller than 44px
- Important actions positioned far from content they relate to
- Close-together buttons for opposing actions (Save next to Delete)

---

## Goal-Gradient Effect

Users accelerate their behavior as they approach a goal. Motivation increases with perceived proximity to completion.

### Implications for Design
- Show progress bars during multi-step processes
- Pre-fill progress indicators slightly (start at 10-20%, not 0%)
- Break large tasks into smaller milestones with visible completion
- Use checklists that show completed items
- Gamification elements: progress bars, achievement counts, completion percentages
- Loyalty programs benefit from showing partial progress

### Common Violations
- Multi-step forms with no progress indicator
- No visual feedback on how far along a user is in a process
- Starting progress at 0% instead of giving "artificial advancement"

---

## Jakob's Law

Users spend most of their time on other websites and apps. They expect your interface to work the same way as the ones they already know. Familiarity reduces learning curve.

### Implications for Design
- Follow platform conventions (iOS patterns on iOS, Material on Android)
- Use standard icon meanings (hamburger = menu, gear = settings, magnifier = search)
- Place navigation where users expect it (top or bottom)
- Use standard e-commerce patterns (cart icon, product grid, filters sidebar)
- When innovating, do so incrementally — don't redesign everything at once
- Study competitor UX patterns in your category

### Common Violations
- Custom navigation patterns when standard ones exist
- Non-standard icon usage (using a star for settings)
- Checkout flows that differ significantly from major e-commerce sites
- Placing search in unusual locations
- Custom gesture interactions without onboarding

---

## Law of Common Region

Elements that share a clearly defined visual boundary are perceived as belonging to the same group. Cards, boxes, backgrounds, and borders create logical groupings.

### Implications for Design
- Use cards to group related content
- Apply subtle background colors to create visual regions
- Use borders and dividers to separate distinct sections
- Ensure form field groups share a common visual container
- Dashboard widgets should have clear boundaries

### Common Violations
- Related information scattered across the page without visual grouping
- No visual distinction between separate functional areas
- Form fields that aren't visually grouped by topic

---

## Law of Proximity

Objects that are close to each other are perceived as related. Spatial distance implies conceptual distance.

### Implications for Design
- Place labels directly adjacent to their fields (top or left-aligned, close)
- Group related buttons together with tight spacing
- Use more whitespace between unrelated sections than between related items
- In navigation, space primary groups apart from secondary groups
- Error messages should appear next to the field they relate to

### Common Violations
- Labels far from their input fields
- Equal spacing between all elements regardless of relationship
- Error messages at the top of the form instead of inline
- Action buttons placed far from the content they act on

---

## Law of Prägnanz (Law of Simplicity)

People interpret complex or ambiguous visual information in the simplest way possible. The brain prefers patterns that are regular, simple, and orderly.

### Implications for Design
- Simplify complex interfaces into clean, recognizable shapes
- Use consistent, regular grid layouts
- Reduce visual noise — every element should earn its place
- Icons should be simple and immediately recognizable
- Avoid decorative elements that add visual complexity without function

### Common Violations
- Overly detailed icons that are hard to parse at small sizes
- Irregular layouts that break visual pattern expectations
- Competing visual styles within one interface

---

## Law of Similarity

Elements that look similar are perceived as belonging to the same group or having the same function. Visual consistency creates functional expectations.

### Implications for Design
- All clickable elements should share visual traits (color, underline, cursor)
- Similar functions should have similar visual treatment
- Differentiate distinct element types clearly (buttons vs. links vs. tags)
- Use consistent color coding across the interface
- Icon style should be uniform (don't mix filled and outlined icons)

### Common Violations
- Non-clickable elements that look like links or buttons
- Different visual styles for the same type of element across pages
- Mixing icon styles (outlined, filled, colored) inconsistently

---

## Law of Uniform Connectedness

Elements that are visually connected by lines, colors, frames, or other visual properties are perceived as more related than unconnected elements.

### Implications for Design
- Use connecting lines in step indicators and timelines
- Apply consistent color to related elements (same-color badges)
- Use visual connectors in flowcharts and process diagrams
- Group related navigation items under a shared visual treatment

---

## Miller's Law

The average person can hold 7 (plus or minus 2) items in working memory. Design should respect this cognitive limitation.

### Implications for Design
- Navigation menus should have 5-7 top-level items maximum
- Phone numbers chunked into 3-4 digit groups
- Limit steps in wizards and processes to under 7
- Don't require users to remember information from previous screens
- Use recognition (showing options) over recall (requiring typing)

### Common Violations
- Navigation with 12+ top-level items
- Requiring users to remember a code from one screen to enter on another
- Displaying too many data points without filtering or grouping

---

## Occam's Razor

The simplest solution that solves the problem is usually the best. Avoid adding unnecessary complexity, features, or elements.

### Implications for Design
- Start with the minimum viable interface and add only what's proven necessary
- Remove features that usage data shows aren't valuable
- When two designs solve the same problem, choose the simpler one
- Question every element: does removing this hurt the experience?

---

## Pareto Principle (80/20 Rule)

80% of effects come from 20% of causes. In UX, 80% of users use only 20% of features. Focus design effort on the critical 20%.

### Implications for Design
- Identify and optimize the most-used features first
- Don't give equal visual weight to rarely-used features
- Use analytics to find the 20% of features driving 80% of value
- Progressive disclosure: surface the vital 20%, tuck the rest away
- Prioritize fixing issues in high-traffic flows

### Common Violations
- Equal visual prominence for all features regardless of usage
- Spending design effort on edge-case features while core flows suffer
- Feature-stuffed interfaces where everything competes for attention

---

## Peak-End Rule

People judge an experience based on how they felt at the most intense moment (the peak) and at the end, not based on the average of every moment.

### Implications for Design
- Design memorable, delightful moments at key milestones (the "peak")
- End experiences positively — success screens, confirmation messages, thank-you pages
- Error recovery should end with a clear resolution, not just "try again"
- Onboarding should end with a quick win
- Checkout should end with clear confirmation and next steps

### Common Violations
- Generic, bland confirmation pages after purchase
- Error flows that end with confusion rather than resolution
- No celebration or acknowledgment at task completion

---

## Postel's Law (Robustness Principle)

Be liberal in what you accept from users, and conservative in what you output. Accept flexible input, deliver consistent output.

### Implications for Design
- Accept multiple input formats (dates, phone numbers, addresses)
- Auto-format user input to a standard format
- Don't reject input for minor formatting differences
- Search should handle typos and synonyms gracefully
- Output should be consistently formatted regardless of input variation

### Common Violations
- Rejecting phone numbers because of dashes, spaces, or parentheses
- Requiring exact date format (MM/DD/YYYY) without alternatives
- Search that returns zero results for slight misspellings

---

## Serial Position Effect

Users best remember the first (primacy) and last (recency) items in a series. Middle items are forgotten most easily.

### Implications for Design
- Place the most important navigation items first and last
- In bottom tab bars, put key actions at the edges
- Lists should put critical information at the top and bottom
- Feature tours should front-load and end with key takeaways

### Common Violations
- Burying the most important navigation item in the middle
- Placing primary actions in the middle of a toolbar

---

## Tesler's Law (Conservation of Complexity)

Every system has an inherent amount of complexity that cannot be eliminated — only shifted between the user and the system. Good design absorbs complexity so the user doesn't have to.

### Implications for Design
- Automate complex calculations and data transformations
- Use smart defaults instead of requiring configuration
- Handle edge cases in code rather than exposing them to users
- Pre-fill forms with available data
- Absorb complexity in the backend — don't pass it to the UI

### Common Violations
- Exposing raw system data (database IDs, timestamps in UTC)
- Requiring users to configure settings that could be auto-detected
- Making users format data that the system could format automatically

---

## Von Restorff Effect (Isolation Effect)

When multiple similar items are present, the one that differs from the rest is most likely to be remembered. Distinctiveness drives attention and recall.

### Implications for Design
- Make primary CTAs visually distinct from secondary actions
- Use color, size, or shape to highlight the most important element
- Pricing tables should visually emphasize the recommended plan
- Important notifications should stand out from regular content
- Use visual contrast strategically — if everything stands out, nothing does

### Common Violations
- All buttons having the same visual weight
- No visual emphasis on the recommended or most common option
- Notifications that blend into regular content

---

## Zeigarnik Effect

People remember incomplete tasks better than completed ones. The tension of an unfinished task creates mental engagement that persists until resolution.

### Implications for Design
- Use progress indicators to create awareness of incomplete tasks
- Show partially completed profiles or setups to motivate completion
- LinkedIn-style "profile strength" bars encourage continued engagement
- Streak counters and incomplete checklists maintain engagement
- Save partial progress so users can return to complete tasks

### Common Violations
- Losing user progress when they navigate away
- No indication of incomplete onboarding steps
- No "continue where you left off" for abandoned flows
