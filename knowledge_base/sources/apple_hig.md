# Apple Human Interface Guidelines — Key Principles and Patterns

## Core Design Themes

### Clarity
Text is legible at every size, icons are precise and lucid, adornments are subtle and appropriate, and a sharpened focus on functionality motivates the design. Negative space, color, fonts, graphics, and interface elements subtly highlight important content and convey interactivity.

### Deference
Fluid motion and a crisp, beautiful interface help people understand and interact with content while never competing with it. Content typically fills the entire screen, while translucency and blurring often hint at more. Minimal use of bezels, gradients, and drop shadows keep the interface light and airy, while ensuring that content is paramount.

### Depth
Distinct visual layers and realistic motion convey hierarchy, impart vitality, and facilitate understanding. Touch and discoverability heighten delight and enable access to functionality and additional content without losing context. Transitions provide a sense of depth as you navigate through content.

---

## iOS Platform Considerations

### Screen Sizes and Safe Areas
- Design for multiple screen sizes (iPhone SE through iPhone Pro Max)
- Respect safe areas — avoid placing interactive elements under the notch, Dynamic Island, or home indicator
- Use Auto Layout and size classes for responsive design
- Support both portrait and landscape where appropriate
- Test on the smallest supported device to ensure usability

### Navigation Patterns

#### Tab Bar (Bottom Navigation)
- Use for 3-5 top-level sections of equal importance
- Always visible, providing one-tap access to major areas
- Each tab maintains its own navigation stack
- Use filled icons for selected state, outlined for unselected
- Badge tabs to indicate new content or required attention

#### Navigation Bar (Top Bar)
- Shows current location with a title
- Back button in top-left for hierarchical navigation
- Action buttons in top-right (Edit, Done, Share, etc.)
- Large titles for top-level views, standard titles for deeper views
- Supports search bar integration

#### Modal Presentation
- Use sheets for self-contained tasks
- Full-screen modals for immersive content (photos, videos)
- Always provide a clear dismiss action (Done, Cancel, X, or swipe down)
- Prevent accidental dismissal for forms with unsaved data

### Gestures
- Swipe back from left edge for navigation
- Pull-to-refresh for content updates
- Swipe-to-delete on list items
- Long press for context menus
- Pinch to zoom on images and maps
- Don't override standard system gestures
- Provide alternative ways to perform gesture-based actions

---

## Typography (San Francisco Font System)

### SF Pro
- System font for iOS, macOS, and tvOS
- Automatically adjusts tracking at different sizes
- Supports Dynamic Type for user-controlled text sizing

### Type Styles
- Large Title: 34pt, used for top-level view titles
- Title 1: 28pt, section headers
- Title 2: 22pt, subsection headers
- Title 3: 20pt, smaller headers
- Headline: 17pt semibold, list item titles
- Body: 17pt, primary content
- Callout: 16pt, secondary content
- Subhead: 15pt, metadata
- Footnote: 13pt, tertiary information
- Caption 1: 12pt, annotations
- Caption 2: 11pt, smallest readable text

### Dynamic Type
- Support all Dynamic Type sizes (xSmall through AX5)
- Test with the largest accessibility sizes
- Ensure text truncation is handled gracefully
- Use system text styles, not fixed point sizes
- Minimum body text size: 17pt at default setting

---

## Color Guidelines

### System Colors
- Blue: Default tint color, interactive elements, links
- Green: Success states, positive indicators
- Red: Destructive actions, errors, alerts
- Orange: Warnings, attention-needed states
- Yellow: Caution, non-critical warnings
- Purple: Creative, premium features
- Pink: Playful, social features
- Gray: Secondary text, disabled states, dividers

### Color Principles
- Support both Light and Dark Mode with appropriate color values
- Use semantic colors (label, secondaryLabel, systemBackground) not fixed values
- Maintain WCAG AA contrast ratios (4.5:1 for body text, 3:1 for large text)
- Don't rely on color alone to convey information
- Test with color blindness simulators (8% of men are red-green colorblind)
- Use vibrant colors sparingly for emphasis; muted tones for backgrounds
- Ensure colors work on both white and black backgrounds

### Dark Mode
- Use elevated background colors to convey depth (not just inverting light mode)
- System provides four background levels: systemBackground, secondarySystemBackground, tertiarySystemBackground, systemGroupedBackground
- Reduce vibrancy and saturation of accent colors in dark mode
- Materials (blur effects) automatically adapt to dark mode
- Test all custom colors in both modes

---

## Icons and Images

### SF Symbols
- 5,000+ built-in symbols designed for San Francisco font
- Nine weights matching text weights (ultralight through black)
- Four scales: small, medium (default), large
- Four rendering modes: monochrome, hierarchical, palette, multicolor
- Automatically align with text baselines
- Use SF Symbols over custom icons when a matching symbol exists

### App Icons
- 1024x1024px master size, system generates all smaller sizes
- No transparency — use solid backgrounds
- Simple, recognizable silhouette that works at 29px
- Avoid text in icons (localization issues, readability at small sizes)
- Use a single focal point
- Consider how the icon looks alongside others on the Home Screen
- Rounded rectangle mask is applied automatically — don't include it in artwork

### Custom Icons
- Match SF Symbol weight and optical sizes
- Use consistent stroke widths across all custom icons
- Design on a pixel grid for crisp rendering
- Provide @1x, @2x, and @3x versions
- Test at all displayed sizes

---

## Layout and Spacing

### Margins and Padding
- Standard horizontal margin: 16pt (compact width), 20pt (regular width)
- Use consistent spacing increments (typically multiples of 4 or 8 points)
- List rows: 44pt minimum height for comfortable tapping
- Navigation bar height: 44pt
- Tab bar height: 49pt
- Toolbar height: 44pt

### Content Hierarchy
- Use visual weight to establish hierarchy (size, color, font weight)
- Most important content appears at the top
- Group related items using proximity and common region
- Use dividers sparingly — whitespace often provides sufficient separation
- Left-align text for readability (except centered titles)

### Adaptivity
- Use trait collections (horizontal/vertical size class) for layout adaptation
- Compact width: single-column layouts (iPhone portrait)
- Regular width: multi-column, split views (iPad, iPhone landscape)
- Support Slide Over and Split View on iPad
- Design for the smallest size first, then expand

---

## Controls and Interactions

### Buttons
- System buttons: text-only or with icon, tinted with the app's accent color
- Filled buttons: for primary actions, strong visual prominence
- Gray buttons: for secondary actions
- Bordered/outlined buttons: medium prominence
- Destructive buttons: use red tint for delete, remove, cancel subscription
- Minimum touch target: 44x44pt
- Button text should describe the action ("Save Photo", not "OK")

### Text Fields
- Use appropriate keyboard type (email, numeric, URL, phone)
- Show clear button (x) for quick content deletion
- Use secure text entry for passwords
- Place labels above or to the left of fields
- Use placeholder text for formatting hints, never as a label substitute
- Support autofill for common fields (name, email, password, credit card)

### Switches and Toggles
- Use for binary on/off states only
- The effect should be immediate (no save button needed)
- Green = on (system default), don't change the color semantics
- Label the switch with what the on state means
- Don't use switches for actions — use buttons instead

### Lists and Tables
- Standard row height: 44pt minimum
- Use disclosure indicators (chevrons) for drill-down navigation
- Support swipe actions (delete, archive, pin)
- Use section headers to group related rows
- Support pull-to-refresh for dynamic content
- Include empty states for lists with no content

---

## Feedback and Status

### Alerts
- Use sparingly — alerts interrupt the user's flow
- Title should be a short, clear question or statement
- Provide 2-3 action buttons maximum
- Destructive actions should be on the left (cancel on the right)
- Don't use alerts for routine confirmations — use inline feedback

### Action Sheets
- Use when there are multiple choices related to an action
- Present from the bottom of the screen on iPhone
- Include a Cancel button
- Destructive options should be red and positioned at the top

### Haptic Feedback
- Use Taptic Engine feedback for important interactions
- Light impact: UI element selection
- Medium impact: successful action completion
- Heavy impact: significant event (error, warning)
- Don't overuse — haptics should feel meaningful, not constant

### Loading States
- Show activity indicators for indeterminate waits
- Use progress bars when duration can be estimated
- Skeleton screens for content-heavy views
- Never show a blank screen during loading
- Allow interaction with already-loaded content while more loads

---

## Accessibility

### VoiceOver Support
- All interactive elements must have accessibility labels
- Images need descriptive alt text
- Group related elements for efficient screen reader navigation
- Test complete user flows with VoiceOver enabled
- Custom controls must implement proper accessibility traits

### Dynamic Type
- All text must respond to Dynamic Type settings
- Test at the largest accessibility sizes
- Ensure layouts don't break with very large text
- Use scalable metrics for icon sizes alongside text

### Reduce Motion
- Provide alternatives when Reduce Motion is enabled
- Replace animations with fade transitions
- Disable parallax effects, bouncing, and sliding transitions
- Auto-playing media should respect this setting

### Other Considerations
- Support Bold Text setting
- Provide sufficient color contrast (minimum 4.5:1)
- Don't rely solely on color to convey meaning
- Support Switch Control and Voice Control
- Test with Smart Invert (Dark Mode alternative)
