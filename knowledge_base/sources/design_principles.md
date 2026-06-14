# Core Design Principles for Digital Products

## Visual Hierarchy

Visual hierarchy controls the delivery of the experience. It refers to the arrangement of elements in a way that implies importance, guiding the user's eye through content in a deliberate order.

### Key Techniques
- **Size**: Larger elements draw attention first
- **Color and Contrast**: High-contrast elements stand out; use brand colors for primary actions
- **Spacing**: Generous whitespace around important elements isolates and elevates them
- **Typography Weight**: Bold headings vs lighter body text creates clear levels
- **Position**: Top-left to bottom-right reading flow in LTR languages; above-the-fold priority

### Common Mistakes
- Everything is bold — nothing stands out
- Equal sizing for elements of different importance
- Insufficient contrast between heading levels
- Call-to-action buttons that blend into the page

---

## Color Theory in UI Design

### Fundamentals
- **60-30-10 Rule**: 60% dominant color (background), 30% secondary color (cards/sections), 10% accent (CTAs, links)
- **Contrast Ratios**: WCAG AA requires 4.5:1 for normal text, 3:1 for large text
- **Semantic Colors**: Red for errors/destructive, green for success, yellow/amber for warnings, blue for information
- **Color Blindness**: 8% of men are red-green colorblind — never use color alone to convey meaning

### Best Practices
- Limit palette to 3-5 colors maximum
- Use consistent color meanings throughout the app
- Test designs in grayscale to verify hierarchy works without color
- Ensure sufficient contrast for accessibility
- Consider dark mode implications from the start

---

## Typography in UI

### Type Scale
A harmonious type scale creates clear hierarchy. Common ratios: 1.25 (major third), 1.333 (perfect fourth), 1.5 (perfect fifth).

### Guidelines
- **Body Text**: 16px minimum for readability on screens
- **Line Height**: 1.4-1.6x the font size for body text
- **Line Length**: 50-75 characters per line for optimal readability
- **Font Pairing**: Limit to 2 font families maximum; pair serif with sans-serif or use weight contrast within one family
- **Heading Levels**: Maintain clear size distinction between h1, h2, h3 levels

### Common Mistakes
- Font size below 14px for body text
- Too many font families creating visual chaos
- Inconsistent line height across the application
- Poor contrast between text and background
- All-caps for long passages of text

---

## Layout and Spacing

### Grid Systems
- **8px Grid**: All spacing and sizing should be multiples of 8px (8, 16, 24, 32, 40, 48...)
- **Column Grids**: 12-column grid for desktop, 4-column for mobile
- **Content Width**: Max 1200-1440px for main content on desktop
- **Gutters**: Consistent gutter width between columns (16-24px)

### Spacing Principles
- **Proximity**: Related items should be closer together than unrelated items (Gestalt principle)
- **Consistent Padding**: Use the same padding values within component categories
- **Breathing Room**: Adequate whitespace improves readability and perceived quality
- **Responsive Spacing**: Scale spacing proportionally across breakpoints

---

## Mobile-First Design

### Touch Targets
- Minimum 44x44px touch targets (Apple HIG) or 48x48dp (Material Design)
- 8px minimum spacing between touch targets
- Primary actions should be easily reachable with one thumb

### Mobile Patterns
- Bottom navigation for primary app navigation (5 items max)
- Pull-to-refresh for content updates
- Swipe gestures for secondary actions (delete, archive)
- Sheet/modal patterns for focused tasks
- Sticky headers for context during scrolling

### Common Mistakes
- Touch targets too small for comfortable tapping
- Important actions placed out of thumb reach
- Desktop patterns forced onto mobile (hover-dependent interactions)
- No consideration for one-handed use
- Fixed elements consuming too much screen real estate on mobile

---

## Accessibility (WCAG 2.1 Key Points)

### Perceivable
- All images must have alt text describing their purpose
- Color is not the only means of conveying information
- Text contrast meets minimum ratios (4.5:1 normal, 3:1 large)
- Content is readable and functional when zoomed to 200%

### Operable
- All functionality accessible via keyboard
- No content that flashes more than 3 times per second
- Users can pause, stop, or hide moving content
- Focus indicators are clearly visible

### Understandable
- Language of the page is identified in code
- Input fields have visible labels (not just placeholders)
- Error identification and suggestions are provided
- Consistent navigation across pages

### Robust
- Valid HTML/semantic markup
- ARIA roles used correctly when semantic HTML is insufficient
- Compatible with assistive technologies

---

## Interaction Design Patterns

### Feedback and Response
- **Immediate feedback**: Button press states, hover effects
- **Acknowledgment**: Success messages, toast notifications
- **Progress**: Loading indicators, progress bars, skeleton screens
- **Error states**: Inline validation, error messages

### Navigation Patterns
- **Tab bar**: 3-5 primary sections (mobile)
- **Sidebar**: Complex applications with many sections (desktop)
- **Breadcrumbs**: Deep hierarchical content
- **Search**: Large content catalogs

### Data Input
- **Smart defaults**: Pre-fill when possible
- **Inline validation**: Check as users type
- **Progressive disclosure**: Show advanced options only when needed
- **Autosave**: Prevent data loss automatically
