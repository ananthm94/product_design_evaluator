# Web Content Accessibility Guidelines (WCAG 2.1) — Detailed Reference

## Perceivable — Information must be presentable in ways users can perceive

### 1.1 Text Alternatives
- All non-decorative images must have descriptive alt text
- Decorative images use empty alt="" to hide from screen readers
- Complex images (charts, diagrams) need long descriptions
- Icons that convey meaning need accessible labels
- Image alt text should describe the purpose, not just "image of..."
- Form image buttons need alt text describing the action

### 1.2 Time-Based Media
- Video must have captions (synchronized text for audio content)
- Audio-only content needs text transcripts
- Pre-recorded video needs audio descriptions for visual-only information
- Live audio content should have real-time captions when possible

### 1.3 Adaptable Content
- Use semantic HTML (headings h1-h6 in order, lists, tables, landmarks)
- Reading order in code matches visual presentation order
- Don't rely on sensory characteristics alone ("click the round button", "the red text")
- Orientation: content works in both portrait and landscape
- Form fields have programmatically associated labels
- Table data cells are associated with table headers

### 1.4 Distinguishable

#### Color Contrast Requirements
- **Normal text** (under 18pt or under 14pt bold): 4.5:1 contrast ratio minimum
- **Large text** (18pt+ or 14pt+ bold): 3:1 contrast ratio minimum
- **UI components and graphics**: 3:1 contrast ratio against adjacent colors
- **Focus indicators**: 3:1 contrast ratio
- **Placeholder text**: must meet contrast requirements (often fails — common violation)

#### Color Independence
- Don't use color as the only way to convey information
- Error states need icon or text in addition to red color
- Required fields need asterisk or text, not just red border
- Links in body text need underline or other non-color indicator
- Chart data series need patterns or labels in addition to colors
- Status indicators need icon or text alongside color (green checkmark, red X)

#### Text Presentation
- Text can be resized to 200% without loss of content or function
- No horizontal scrolling at 320px viewport width (reflow)
- Line height at least 1.5x the font size for body text
- Paragraph spacing at least 2x the font size
- Letter spacing at least 0.12x the font size
- Word spacing at least 0.16x the font size
- Text is not presented as an image (use real text)

#### Visual Presentation
- Content doesn't flash more than 3 times per second (seizure risk)
- Users can pause, stop, or hide moving, blinking, or auto-updating content
- Background audio can be paused, and volume controlled independently
- No content changes triggered solely by hover or focus without user control

---

## Operable — Users must be able to operate the interface

### 2.1 Keyboard Accessible
- All functionality available via keyboard (no mouse-only interactions)
- No keyboard traps — users can always navigate away using standard keys
- Standard keyboard shortcuts: Tab (next), Shift+Tab (previous), Enter/Space (activate), Escape (close/cancel), Arrow keys (within components)
- Custom keyboard shortcuts should not conflict with browser or screen reader shortcuts
- Skip navigation link at the top of the page ("Skip to main content")

### 2.2 Enough Time
- Adjustable time limits — users can turn off, adjust, or extend
- Moving, blinking, or scrolling content (like carousels) can be paused or stopped
- Auto-updating content can be paused (live feeds, stock tickers)
- No time limits on essential tasks unless absolutely required
- Warn users before timeout and allow extension

### 2.3 Seizures and Physical Reactions
- No content flashes more than 3 times per second
- Motion animation can be disabled (respect prefers-reduced-motion)
- Parallax effects have an alternative or can be turned off

### 2.4 Navigable
- Pages have descriptive, unique titles
- Focus order is logical and follows visual reading order
- Link text describes the destination or purpose (not "click here" or "read more")
- Multiple ways to reach any page (navigation, search, sitemap)
- Headings and labels describe the topic or purpose
- Focus is visible — all interactive elements show a clear focus indicator
- Section headings organize content logically

### 2.5 Input Modalities
- Touch target minimum: 44x44 CSS pixels
- Functionality available through single pointer (click/tap) — no complex gestures required
- Multi-point or path-based gestures have single-pointer alternatives
- Drag-and-drop operations have alternative keyboard/button methods
- Device motion (shake, tilt) can be disabled and has alternatives

---

## Understandable — Information and UI operation must be understandable

### 3.1 Readable
- Page language is set in HTML (lang attribute)
- Passages in a different language are marked (lang attribute on the element)
- Unusual words are defined or a glossary is provided
- Abbreviations are expanded on first use

### 3.2 Predictable
- Focus doesn't trigger unexpected context changes (no auto-submit on focus)
- Input doesn't trigger unexpected changes (no auto-navigate on select)
- Navigation is consistent across all pages
- Components with the same function are labeled consistently

### 3.3 Input Assistance
- Errors are identified and described in text (not just color)
- Labels or instructions are provided for user input
- Error suggestions offer specific correction advice
- Submissions are reversible, checked, or confirmed
- Context-sensitive help is available for complex inputs
- Successful submission is clearly confirmed

---

## Robust — Content must be robust enough for assistive technologies

### 4.1 Compatible
- Valid HTML — no duplicate IDs, proper nesting
- Name, role, and value are programmatically determinable for all UI components
- Custom components expose correct ARIA roles, states, and properties
- Status messages can be determined by assistive technologies without receiving focus (use aria-live regions)

---

## ARIA Best Practices

### When to Use ARIA
- First choice: use native HTML elements (button, input, nav, dialog)
- Only use ARIA when native HTML doesn't provide the needed semantics
- Don't change native semantics (don't put role="button" on an anchor link — use a button element)

### Common ARIA Patterns
- **aria-label**: Text label for elements without visible text
- **aria-labelledby**: Points to the ID of the labeling element
- **aria-describedby**: Points to the ID of a description element
- **aria-expanded**: true/false for expandable elements (accordions, menus)
- **aria-hidden="true"**: Hides decorative elements from screen readers
- **aria-live="polite"**: Announces dynamic content changes (toast notifications, status updates)
- **aria-live="assertive"**: Immediately announces critical updates (errors)
- **role="alert"**: Urgent, time-sensitive notifications
- **role="dialog"**: Modal dialogs (with aria-labelledby)
- **role="tablist"/"tab"/"tabpanel"**: Tab interfaces

### Common Accessibility Mistakes
- Missing alt text on informative images
- Form fields without labels (using placeholder as label)
- Low color contrast (especially gray text on white background)
- No visible focus indicator (outline: none without replacement)
- Mouse-only interactions (hover menus without keyboard access)
- Auto-playing media without pause controls
- PDF documents without proper tagging
- Timeout without warning or extension option
- Dynamic content changes not announced to screen readers
- Modals that don't trap focus or manage focus on close
- Links that say "click here" or "read more" without context
- Missing heading structure or skipped heading levels
- Tables without proper header markup
- Touch targets smaller than 44px

---

## Accessibility Testing Checklist

### Automated Testing
- Run aXe, WAVE, or Lighthouse accessibility audit
- Check color contrast with a contrast checker tool
- Validate HTML for structural issues
- Test with CSS disabled to verify content order

### Manual Testing
- Navigate the entire site using keyboard only (Tab, Enter, Escape, Arrow keys)
- Test with a screen reader (VoiceOver on Mac/iOS, NVDA or JAWS on Windows, TalkBack on Android)
- Zoom to 200% and verify no content is lost or overlapping
- Test with high contrast mode enabled
- Test with reduced motion preference enabled
- Verify all images have appropriate alt text
- Check that all forms can be completed without a mouse
- Verify error messages are announced by screen readers
- Test color-dependent information with a color blindness simulator
