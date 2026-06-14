# Material Design 3 — Comprehensive Guidelines

## Design Philosophy

Material Design 3 (M3) is Google's open-source design system. It emphasizes personal, adaptive, and expressive design. M3 introduces Dynamic Color, updated typography, and refined components that adapt to user preferences and device capabilities.

### Key Principles
- **Personal**: Adapts to user preferences through Dynamic Color and theming
- **Adaptive**: Works across form factors — phone, tablet, foldable, desktop, wearable
- **Expressive**: Enables brand expression through customizable color, shape, and typography

---

## Color System

### Color Roles
M3 uses a role-based color system where colors are assigned to specific UI purposes:

- **Primary**: Key interactive elements (FABs, prominent buttons, active states)
- **On Primary**: Text and icons on primary-colored surfaces
- **Primary Container**: Standout fill color for elements needing less emphasis than primary
- **On Primary Container**: Text and icons on primary container
- **Secondary**: Less prominent interactive elements (filter chips, selection controls)
- **Secondary Container**: Fill color for secondary elements
- **Tertiary**: Contrasting accent for balancing primary and secondary colors
- **Surface**: Default background for components (cards, sheets, dialogs)
- **Surface Variant**: Alternative surface color for added contrast
- **On Surface**: Default text and icon color on surface backgrounds
- **On Surface Variant**: Lower-emphasis text and icons
- **Outline**: Borders and dividers for medium emphasis
- **Outline Variant**: Lower-emphasis borders
- **Error**: Error states and destructive actions
- **On Error**: Text on error-colored surfaces

### Tonal Palette
Each key color generates a tonal palette with 13 tonal values (0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 99, 100). Light theme uses lighter tones for surfaces and darker tones for content. Dark theme inverts this relationship.

### Dynamic Color
- Automatically derives a color scheme from the user's wallpaper (Android 12+)
- Ensures brand consistency while allowing personalization
- Fallback to a static brand palette on unsupported platforms
- Color extraction uses the Chroma algorithm to find dominant and complementary colors

### Contrast and Accessibility
- Normal text (14sp): minimum 4.5:1 contrast ratio
- Large text (18sp+ or 14sp bold): minimum 3:1 contrast ratio
- Interactive elements: minimum 3:1 against adjacent colors
- Decorative elements: no minimum requirement
- Test with increased contrast accessibility settings enabled
- Use the color system's built-in tonal relationships to ensure sufficient contrast

---

## Typography

### Type Scale
M3 defines 5 type roles, each with 3 sizes (Large, Medium, Small):

#### Display (Hero text, large numbers)
- Display Large: 57sp / Line height 64sp / Letter spacing -0.25
- Display Medium: 45sp / Line height 52sp / Letter spacing 0
- Display Small: 36sp / Line height 44sp / Letter spacing 0

#### Headline (High-emphasis text, short content)
- Headline Large: 32sp / Line height 40sp / Letter spacing 0
- Headline Medium: 28sp / Line height 36sp / Letter spacing 0
- Headline Small: 24sp / Line height 32sp / Letter spacing 0

#### Title (Medium emphasis, shorter text)
- Title Large: 22sp / Line height 28sp / Letter spacing 0
- Title Medium: 16sp / Line height 24sp / Letter spacing 0.15
- Title Small: 14sp / Line height 20sp / Letter spacing 0.1

#### Body (Longer passages of text)
- Body Large: 16sp / Line height 24sp / Letter spacing 0.5
- Body Medium: 14sp / Line height 20sp / Letter spacing 0.25
- Body Small: 12sp / Line height 16sp / Letter spacing 0.4

#### Label (Utility text, buttons, captions)
- Label Large: 14sp / Line height 20sp / Letter spacing 0.1
- Label Medium: 12sp / Line height 16sp / Letter spacing 0.5
- Label Small: 11sp / Line height 16sp / Letter spacing 0.5

### Font Recommendations
- Default: Roboto (Android system font)
- Serif alternative: Roboto Serif
- Custom brand fonts should maintain the type scale ratios
- Minimum readable text: Body Small (12sp)
- Line length: 40-60 characters for readability

---

## Shape System

### Corner Radius Tokens
M3 uses a shape scale for consistent corner rounding:

- **None**: 0dp — square corners (full-bleed images, bottom sheets at full height)
- **Extra Small**: 4dp — small chips, small cards
- **Small**: 8dp — buttons, text fields, small cards
- **Medium**: 12dp — cards, dialogs
- **Large**: 16dp — large cards, navigation drawers
- **Extra Large**: 28dp — FABs, large sheets
- **Full**: 50% — circular elements (icon buttons, avatars)

### Shape Principles
- Rounded corners feel friendlier and more approachable
- Sharper corners feel more precise and professional
- Consistent shape usage across similar component types
- Interactive elements should have rounded corners to invite interaction
- Container shapes should match or exceed the radius of their contents

---

## Elevation and Shadows

### Elevation Levels
- Level 0 (0dp): Flat surfaces, backgrounds
- Level 1 (1dp): Cards, app bars, navigation rail
- Level 2 (3dp): Buttons, elevated cards
- Level 3 (6dp): FABs, navigation drawers, bottom sheets
- Level 4 (8dp): Menus, dialogs, side sheets
- Level 5 (12dp): Modal bottom sheets, navigation drawers (modal)

### M3 Tonal Elevation (Replaces Drop Shadows)
- Instead of shadow-based elevation, M3 uses tonal surface color shifts
- Higher elevation = surface color shifts toward primary color
- This creates a subtle color overlay that indicates elevation
- In dark theme, higher surfaces appear lighter
- In light theme, higher surfaces show a slight primary color tint
- Shadows are still used for some components (FABs, menus) for clarity

---

## Component Guidelines

### Buttons

#### Types (by prominence)
1. **Filled Button**: Highest emphasis, primary actions. Solid primary color background.
2. **Filled Tonal Button**: Medium-high emphasis, secondary actions. Primary container background.
3. **Elevated Button**: Medium emphasis, with shadow. Surface color with elevation.
4. **Outlined Button**: Medium emphasis, no fill. Border with transparent background.
5. **Text Button**: Lowest emphasis, tertiary actions. No border, no fill.

#### Button Specifications
- Minimum width: 64dp
- Height: 40dp
- Horizontal padding: 24dp (16dp for icon buttons)
- Corner radius: 20dp (Full round)
- Label text: Label Large (14sp)
- Icon size: 18dp, 8dp spacing from label
- Touch target: minimum 48dp

#### States
- Enabled: Default appearance
- Hovered: State layer (8% opacity of content color)
- Focused: State layer (12% opacity) + focus ring
- Pressed: State layer (12% opacity)
- Disabled: 38% opacity container, 38% opacity content
- Loading: Replace label with circular progress indicator

### Cards

#### Types
1. **Filled Card**: Default surface color, no elevation
2. **Elevated Card**: Shadow elevation, surface-tint overlay
3. **Outlined Card**: Border, no elevation or fill change

#### Card Specifications
- Corner radius: 12dp (Medium)
- Padding: 16dp internal
- No minimum size; adapts to content
- Support drag interaction for reordering
- Action area: entire card surface for primary action
- Supplemental actions: buttons in a bottom action area

### Navigation

#### Bottom Navigation Bar
- 3-5 destinations maximum
- Icon + label for each destination
- Active state: filled icon in a pill-shaped indicator
- Inactive state: outlined icon, no indicator
- Height: 80dp
- Icon size: 24dp
- Label: Label Medium (12sp)
- Badge support for notification counts

#### Navigation Rail (Tablet/Desktop)
- Side rail with 3-7 destinations
- Width: 80dp
- Can include FAB at top
- Same icon/label treatment as bottom navigation
- Used for regular width layouts (tablets, desktop)

#### Navigation Drawer
- Full list of destinations with labels and optional icons
- Standard drawer: persistent, side-by-side with content
- Modal drawer: overlays content with scrim
- Width: 360dp maximum
- Section headers for grouping destinations

### Dialogs
- Use for urgent information requiring acknowledgment
- Title: Headline Small (24sp)
- Body: Body Medium (14sp)
- Action buttons: right-aligned, text buttons
- Maximum 3 action buttons
- Corner radius: 28dp (Extra Large)
- Minimum width: 280dp, Maximum width: 560dp
- Scrim overlay: surface color at 32% opacity

### Text Fields

#### Types
1. **Filled Text Field**: Solid container with bottom border
2. **Outlined Text Field**: Border around entire field

#### Specifications
- Height: 56dp
- Label text: Body Small (12sp) when focused/filled, Body Large (16sp) when empty
- Supporting text: Body Small (12sp), below the field
- Leading icon: 24dp, optional
- Trailing icon: 24dp, for actions (clear, toggle visibility, dropdown)
- Error state: Error color on border, label, and supporting text
- Character counter: right-aligned below field

### Chips
- Assist Chip: Represents a smart suggestion (icon + label)
- Filter Chip: For filtering content (selectable, supports multiple selection)
- Input Chip: Represents user input (removable, like email recipients)
- Suggestion Chip: Dynamically generated suggestions
- Height: 32dp
- Corner radius: 8dp (Small)

---

## Spacing and Layout

### Grid System
- 4-column grid for compact screens (phones)
- 8-column grid for medium screens (tablets)
- 12-column grid for expanded screens (desktop)
- Margins: 16dp (compact), 24dp (medium), 24dp (expanded)
- Gutters: 8dp between columns

### Spacing Scale
- 4dp: Minimal spacing (between related inline elements)
- 8dp: Tight spacing (between related items in a group)
- 12dp: Default spacing (between items in a list)
- 16dp: Standard spacing (padding within components)
- 24dp: Comfortable spacing (between sections)
- 32dp: Generous spacing (between major sections)
- 48dp: Spacious (page-level section breaks)

### Responsive Breakpoints
- Compact: 0-599dp (phone portrait)
- Medium: 600-839dp (phone landscape, small tablet)
- Expanded: 840dp+ (tablet, desktop)
- Use adaptive layouts that reflow content at breakpoints
- Navigation pattern changes at breakpoints (bottom bar → rail → drawer)

---

## Motion and Animation

### Duration Tokens
- Short 1: 50ms (micro-interactions, ripple)
- Short 2: 100ms (simple state changes)
- Short 3: 150ms (icon transitions)
- Short 4: 200ms (small component transitions)
- Medium 1: 250ms (component enter)
- Medium 2: 300ms (component exit, standard transitions)
- Medium 3: 350ms (page transitions)
- Medium 4: 400ms (complex transitions)
- Long 1: 450ms (full-screen transitions)
- Long 2: 500ms (elaborate animations)

### Easing
- Emphasized: For primary transitions that draw attention
- Emphasized Decelerate: Elements entering the screen
- Emphasized Accelerate: Elements leaving the screen
- Standard: For utility animations that shouldn't draw attention
- Standard Decelerate: Entering
- Standard Accelerate: Exiting

### Motion Principles
- Motion should feel natural and responsive
- Enter animations should be longer than exit animations
- Shared element transitions connect related screens
- Stagger animations for lists and grids (50ms offset per item)
- Reduce motion for users who prefer it (prefers-reduced-motion)

---

## Accessibility in Material Design 3

### Touch Targets
- Minimum touch target: 48x48dp
- Minimum spacing between targets: 8dp
- Visual size can be smaller than touch target
- Use touch target padding to meet minimums

### Screen Readers
- All interactive elements need content descriptions
- Decorative images should be hidden from screen readers
- Group related elements with semantic containers
- Announce state changes (expanded/collapsed, selected/unselected)
- Custom components need proper role announcements

### Color and Contrast
- Test all color combinations with contrast checker
- Provide non-color indicators (icons, text, patterns)
- Support high-contrast theme
- Dynamic Color maintains contrast requirements automatically

### Focus and Navigation
- Visible focus indicators on all interactive elements
- Logical tab order matching visual order
- Skip navigation links for keyboard users
- Focus management during page transitions and modal opening
