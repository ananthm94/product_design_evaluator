# UI Component Design Patterns and Checklists

## Button Design Patterns

### Button Types and Hierarchy
- **Primary button**: Single most important action on the page. Use filled/solid style with brand color. Only one primary button per view.
- **Secondary button**: Supporting actions. Use outlined or tonal style. Can have multiple per view.
- **Tertiary button**: Low-emphasis actions like "Cancel" or "Skip". Use text-only or ghost style.
- **Destructive button**: Delete, remove, or irreversible actions. Use red/danger color. Always require confirmation for destructive actions.
- **Icon button**: Compact action with icon only. Must have tooltip and accessible label.

### Button Checklist
- Label clearly describes the action outcome ("Save Changes", not "OK")
- Minimum touch target 44x44px (iOS) or 48x48dp (Android)
- Visual states: default, hover, active/pressed, focused, disabled, loading
- Disabled buttons have reduced opacity (38-50%) and no pointer cursor
- Loading state shows spinner and disables click, optionally preserves button width
- Icons are 16-20px, placed before label (left side in LTR languages)
- Button group hierarchy is clear — primary stands out from secondary
- Destructive actions use distinct color (red) and require confirmation
- Full-width buttons on mobile for primary actions in flows
- Don't use more than one primary button per screen section

---

## Form and Input Field Patterns

### Input Field Types
- **Text input**: Single-line free text
- **Text area**: Multi-line free text with character count
- **Select / Dropdown**: Choose from predefined options
- **Date picker**: Date selection with calendar or spinners
- **File upload**: Drag-and-drop zone with browse button
- **Search input**: With magnifier icon, clear button, and suggestions

### Input Field Checklist
- Every field has a visible label (not just placeholder text)
- Labels positioned above or to the left of the field, close to it
- Placeholder text is lighter than input text — never used as the only label
- Helper text below the field for format hints or requirements
- Character count for fields with limits (bio, description)
- Appropriate keyboard type on mobile (email, number, phone, URL)
- Clear button (x) for text fields with content
- Password fields have show/hide toggle
- Autofill support for common fields (name, email, address, credit card)
- Required field indicator (asterisk or "required" label)
- Optional field indicator when most fields are required

### Form Validation
- Inline validation as the user types or on blur, not just on submit
- Error message appears next to the field, not at the top of the form
- Error state: red border, error icon, descriptive error message
- Error messages explain what's wrong AND how to fix it ("Email must include @")
- Success validation: green checkmark for confirmed fields
- Don't clear the field on error — let the user correct their input
- Validate format client-side, validate uniqueness/existence server-side
- Disable submit button only if all required fields are empty — otherwise show errors on submit

### Form Layout
- One column for most forms (especially mobile)
- Group related fields with section headers
- Logical tab order matching visual order
- Short forms: all fields visible on one screen
- Long forms: break into multi-step wizard with progress bar
- Auto-save or warn before losing unsaved changes
- Pre-fill with available data (user profile, geolocation, defaults)

---

## Navigation Patterns

### Top Navigation (Desktop)
- Logo on the left, links to primary sections in the center or right
- Maximum 7 top-level items (Miller's Law)
- Active page indicator (underline, background, bold text)
- Dropdown menus for sub-sections
- Search accessible from the navigation bar
- Responsive: collapses to hamburger menu on mobile
- Sticky navigation on scroll for long pages

### Bottom Tab Bar (Mobile)
- 3-5 tabs maximum
- Icon + label for each tab (no icon-only tabs)
- Active tab visually distinct (filled icon, tint color, indicator pill)
- Each tab maintains its own back stack
- Badge counts for notifications or pending items
- Most important/frequent actions at the edges (Serial Position Effect)
- Tab bar always visible (don't hide on scroll for primary navigation)

### Sidebar Navigation (Desktop/Web App)
- Used for apps with 6+ sections
- Collapsible to icon-only mode for more content space
- Section grouping with headers
- Active item highlighted with background color
- Support for nested items (expandable/collapsible)
- Fixed position or scrolls with content depending on length
- Width: 240-280px expanded, 64-80px collapsed

### Breadcrumbs
- Show the path from home to current page
- Each level is a clickable link except the current page
- Use for hierarchies 3+ levels deep
- Separator: ">" or "/" between levels
- Don't use breadcrumbs as the only navigation method
- Truncate middle levels for very deep hierarchies ("Home > ... > Category > Product")

---

## Modal and Dialog Patterns

### When to Use Modals
- Confirming destructive actions ("Delete this file?")
- Collecting focused input (login, compose message)
- Showing urgent information requiring acknowledgment
- DON'T use for routine confirmations, warnings, or information that could be inline

### Modal Checklist
- Clear, descriptive title explaining the modal's purpose
- Close mechanism: X button, click outside (for non-critical), Escape key
- Trap focus inside the modal (keyboard tab stays within)
- Restore focus to the trigger element when modal closes
- Background overlay (scrim) dims or blurs the page behind
- Responsive: full-screen on mobile, centered dialog on desktop
- Action buttons at the bottom: primary action on the right, cancel on the left
- Maximum 2-3 action buttons
- Don't stack modals (modal on top of modal)
- Prevent body scroll when modal is open
- Label the modal for screen readers (role="dialog", aria-labelledby)
- Animation: fade in + slight scale up (200-300ms)

### Confirmation Dialogs
- Title states the action: "Delete 3 items?"
- Body explains the consequence: "This action cannot be undone."
- Destructive action button is red/danger colored
- Cancel button is the default (gets focus)
- Don't use "Yes/No" — use descriptive labels ("Delete" / "Keep")

---

## Card Design Patterns

### Card Types
- **Content card**: Image + title + description (blog posts, products)
- **Interactive card**: Entire surface is clickable (navigate to detail)
- **Action card**: Contains buttons or actions within the card
- **Stat card**: Key metric with label (dashboard KPIs)

### Card Checklist
- Clear visual boundary (border, shadow, or background contrast)
- Consistent padding (16-24px inside)
- Content hierarchy: image → title → description → actions
- Clickable cards have hover state (slight elevation, border, or shadow change)
- Image aspect ratio is consistent across a grid of cards
- Truncate long text with ellipsis, don't let cards grow unbounded
- Loading state: skeleton card matching the card layout
- Empty state when no cards to display
- Responsive: grid adjusts column count by screen width
- Cards in a grid should be the same height (use CSS grid or flex with stretch)
- Avoid too many actions per card — 1-2 maximum

---

## Table and Data Display Patterns

### Table Checklist
- Column headers are visible and clearly styled (bold, background)
- Sticky header on scroll for long tables
- Sortable columns with sort indicator (arrow icon)
- Default sort order is meaningful (newest first, alphabetical)
- Row hover state for clickable rows
- Alternating row colors (zebra striping) for dense tables
- Row actions: inline buttons or overflow menu (three dots)
- Checkbox column for bulk selection with "select all" in header
- Pagination or infinite scroll for large datasets
- Show total count ("Showing 1-20 of 543 results")
- Empty state when no data matches filters
- Loading state: skeleton rows or loading overlay

### Responsive Tables
- Horizontal scroll on mobile (with scroll indicator)
- Priority columns: show most important columns, hide others
- Card view alternative: each row becomes a card on mobile
- Column resize handles for desktop power users

### Filtering and Search
- Search filters above the table
- Active filters shown as removable chips
- "Clear all filters" button when filters are active
- Filter count badge on the filter button
- Real-time filtering (filter as user types) or apply button for complex filters

---

## Toast and Notification Patterns

### Toast Notifications
- Brief, auto-dismissing messages (3-5 seconds)
- Position: top-right (desktop) or top-center/bottom-center (mobile)
- Types: success (green), error (red), warning (yellow), info (blue)
- Include icon + message text + optional action ("Undo")
- Don't stack more than 3 toasts simultaneously
- Swipe or click to dismiss manually
- Pause auto-dismiss on hover
- Don't use toasts for critical errors — use inline messages or dialogs

### Inline Notifications / Banners
- Persistent messages at the top of a section or page
- Dismissible with X button (for non-critical)
- Non-dismissible for critical system status
- Types: info, success, warning, error
- Include icon, message, and optional action link
- Full-width within their container

---

## Loading and Empty States

### Loading Patterns
- **Skeleton screens**: Gray placeholder shapes matching content layout — best for content-heavy pages
- **Spinner**: Centered circular indicator — best for small areas or overlays
- **Progress bar**: Linear indicator — best when progress can be estimated
- **Shimmer effect**: Animated gradient sweep over skeleton shapes — adds perceived speed
- Show loading immediately (within 100ms of triggering action)
- For operations >10 seconds, show estimated time remaining
- Allow cancellation for long operations

### Empty States
- Illustration or icon relevant to the content type
- Clear heading ("No messages yet")
- Brief description explaining what will appear here
- Call-to-action to get started ("Compose your first message")
- Don't show a blank page — always communicate the empty state
- Different empty states for: first-time (onboarding), no results (search), error (failed to load)

---

## Onboarding and First-Time Experience

### Onboarding Patterns
- Maximum 3-5 onboarding screens
- Skip option always available
- Progress dots showing current position
- Each screen focuses on one key feature or benefit
- Use illustrations or screenshots, not just text
- End with a clear CTA to get started
- Permission requests come in context, not upfront ("Enable notifications" when showing the notifications feature)

### Progressive Disclosure
- Show basic features first, reveal advanced features as needed
- Use expandable sections, "Advanced" toggles, or "Show more" links
- Dashboard widgets start with key metrics, expand for details
- Settings: basic settings first, "Advanced settings" section for power users
- Tooltips and info icons for features that need explanation
