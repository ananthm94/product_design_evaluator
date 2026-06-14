# Nielsen's 10 Usability Heuristics for User Interface Design

## H1: Visibility of System Status

The design should always keep users informed about what is going on, through appropriate feedback within a reasonable amount of time.

When users know the current system status, they learn the outcome of their prior interactions and determine next steps. Predictable interactions create trust in the product as well as the brand.

### Examples of Good Implementation
- Progress bars during file uploads or long operations
- Loading spinners with estimated time remaining
- Highlighted active navigation items showing current location
- Real-time form validation showing field status
- "Saving..." and "Saved" indicators in document editors

### Common Violations
- No loading indicator during data fetching
- Form submissions with no feedback on success or failure
- Navigation without highlighting the current page
- Background processes running without user awareness
- Search with no indication that results are loading

---

## H2: Match Between System and the Real World

The design should speak the users' language. Use words, phrases, and concepts familiar to the user, rather than internal jargon. Follow real-world conventions, making information appear in a natural and logical order.

### Examples of Good Implementation
- Shopping cart icon and terminology in e-commerce
- Calendar interfaces that mirror physical calendars
- File and folder metaphors in file management systems
- "Trash" or "Recycle Bin" for deleted items
- Natural date formats matching user locale

### Common Violations
- Technical error codes shown to end users (Error 500, NullPointerException)
- Internal database field names as form labels
- Developer terminology in user-facing interfaces
- Counter-intuitive icon choices that don't match real-world meaning
- Date formats that don't match user expectations (MM/DD vs DD/MM)

---

## H3: User Control and Freedom

Users often perform actions by mistake. They need a clearly marked "emergency exit" to leave the unwanted action without having to go through an extended process.

### Examples of Good Implementation
- Undo/redo functionality in editors
- "Cancel" buttons on dialogs and forms
- Back navigation that preserves state
- "Discard changes" option when leaving edited forms
- Gmail's "Undo Send" feature

### Common Violations
- No way to cancel a multi-step process
- Destructive actions without confirmation
- No undo after deleting items
- Modal dialogs with no close button or escape key support
- Forced completion of forms before allowing navigation away

---

## H4: Consistency and Standards

Users should not have to wonder whether different words, situations, or actions mean the same thing. Follow platform and industry conventions.

### Examples of Good Implementation
- Consistent button styles throughout the application
- Standard icons (hamburger menu, settings gear, search magnifier)
- Uniform color coding (red for errors, green for success)
- Consistent placement of navigation and action buttons
- Following platform guidelines (iOS HIG, Material Design)

### Common Violations
- Multiple visual styles for the same type of button
- Inconsistent terminology (save vs submit vs confirm for the same action)
- Different navigation patterns on different pages
- Mixing design systems within one application
- Non-standard gestures or interactions

---

## H5: Error Prevention

Good error messages are important, but the best designs carefully prevent problems from occurring in the first place. Either eliminate error-prone conditions, or check for them and present users with a confirmation option before they commit to the action.

### Examples of Good Implementation
- Greying out unavailable options rather than allowing selection
- Inline validation as users type
- Confirmation dialogs for destructive actions ("Delete 5 items?")
- Autocomplete and suggestions for text input
- Constraints on input fields (date pickers instead of text fields)

### Common Violations
- Free text fields for structured data (dates, phone numbers)
- Allowing form submission with invalid data
- No confirmation before permanent deletion
- Enabling buttons that lead to errors
- No input validation until form submission

---

## H6: Recognition Rather Than Recall

Minimize the user's memory load by making elements, actions, and options visible. The user should not have to remember information from one part of the interface to another. Information required to use the design should be visible or easily retrievable.

### Examples of Good Implementation
- Dropdown menus showing all options instead of requiring typed input
- Recent items and search history
- Breadcrumb navigation showing the path taken
- Tooltips explaining icon meanings on hover
- Previews and thumbnails for file selection

### Common Violations
- Requiring users to remember codes or IDs from previous screens
- Unlabeled icons with no tooltips
- Complex keyboard shortcuts as the only way to access features
- Hidden features with no visual indication
- Forms that require information from other pages without providing it

---

## H7: Flexibility and Efficiency of Use

Shortcuts — hidden from novice users — can speed up the interaction for the expert user so that the design can cater to both inexperienced and experienced users. Allow users to tailor frequent actions.

### Examples of Good Implementation
- Keyboard shortcuts alongside menu options
- Customizable dashboards and toolbars
- Advanced search filters alongside simple search
- Batch operations for managing multiple items
- Templates and presets for common configurations

### Common Violations
- No keyboard shortcuts for common actions
- One-size-fits-all interface with no customization
- Forcing expert users through the same wizard every time
- No bulk operations when managing lists
- Missing search functionality in long lists

---

## H8: Aesthetic and Minimalist Design

Interfaces should not contain information that is irrelevant or rarely needed. Every extra unit of information in an interface competes with the relevant units of information and diminishes their relative visibility.

### Examples of Good Implementation
- Clean layouts with adequate whitespace
- Progressive disclosure hiding advanced options
- Clear visual hierarchy guiding the eye to important elements
- Concise copy that communicates essential information
- Focused pages with a single primary action

### Common Violations
- Cluttered layouts with too many elements competing for attention
- Walls of text without visual hierarchy
- Unnecessary decorative elements that don't serve function
- Information overload on single screens
- Multiple competing calls-to-action

---

## H9: Help Users Recognize, Diagnose, and Recover from Errors

Error messages should be expressed in plain language (no error codes), precisely indicate the problem, and constructively suggest a solution.

### Examples of Good Implementation
- "Email address format is invalid. Example: name@domain.com"
- Inline error messages next to the relevant field
- Suggested corrections for typos in search
- Clear instructions for resolving the error
- Visual emphasis (color, icon) on error messages

### Common Violations
- Generic "Something went wrong" messages
- Technical error codes without explanation
- Error messages far from the field that caused them
- No guidance on how to fix the error
- Error messages that blame the user

---

## H10: Help and Documentation

It's best if the system can be used without documentation. However, it may be necessary to provide help and documentation. Such information should be easy to search, focused on the user's task, list concrete steps, and not be too large.

### Examples of Good Implementation
- Contextual help tooltips near complex features
- Searchable help center or knowledge base
- Onboarding tours for new users
- FAQ sections for common questions
- In-app chat support or help widgets

### Common Violations
- No help documentation at all
- Help content that requires searching through lengthy manuals
- Outdated documentation that doesn't match current UI
- Help that describes features rather than user tasks
- No contextual help near complex interface elements
