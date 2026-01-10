# AI Coding Agent Instructions for devnull

## Project Overview
This is a **static documentation website** for Elder Scrolls IV: Oblivion modding guides, hosted on GitHub Pages at https://devakm.github.io/devnull/. The site preserves historical modding documentation from 2006-2015, updated for modern web standards in 2025.

**Tech Stack**: Pure static HTML/CSS - no build process, no Jekyll, no frameworks. Files in `docs/` are served directly by GitHub Pages.

## Critical Rules - NEVER VIOLATE

1. **NEVER remove ANY content from files** - This is the #1 rule. When converting or updating HTML files, preserve 100% of original content. Only update styling and broken links.

2. **Copyright Format** - Always use: `Copyright 2006, 2007, 2008, 2009, 2015, 2025 by devakm. Individual works copyright by their respective creators.`

3. **Link Modernization** - Replace dead URLs with current equivalents:
   - `cs.elderscrolls.com/constwiki/*` → `https://cs.uesp.net/wiki/*`
   - `wrye.ufrealms.net` → `https://www.nexusmods.com/site/mods/591` (Wrye Bash)
   - `tessource.net`, `tesnexus.com` → `https://www.nexusmods.com/oblivion/mods/*`
   - Remove Wayback Machine (`web.archive.org`) wrapper URLs when modernizing

## HTML Conversion Standards

### Shared CSS File
All pages should use the shared CSS file located at `css/devnull-shared.css`. This file contains:
- Dark mode color scheme with CSS variables
- Common layout and typography styles
- Navigation and footer styles
- Content boxes (warning, update, highlight, note)
- Grid layouts and responsive design
- PES Hall of Fame badge styles

**To use the shared CSS:**
```html
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Title</title>
    <link rel="stylesheet" href="css/devnull-shared.css">
</head>
```

### Dark Mode Color Scheme (available via shared CSS)
The shared CSS provides these CSS variables:
```css
:root {
    --bg-primary: #1a1a1a;
    --bg-secondary: #2d2d2d;
    --bg-tertiary: #252525;
    --text-primary: #e0e0e0;
    --text-secondary: #b0b0b0;
    --accent-red: #ff4444;
    --accent-blue: #4a9eff;
    --accent-cyan: #00d9ff;
    --accent-gold: #ffd700;
    --accent-green: #33cc00;
    --border-color: #444;
}
```

### Conversion Process
1. Convert `DOCTYPE HTML 4.01 Transitional` → `<!DOCTYPE html>`
2. Remove all Wayback Machine toolbars, scripts, and embedded content
3. Link to shared CSS file: `<link rel="stylesheet" href="css/devnull-shared.css">`
4. Add page-specific CSS only if needed (in `<style>` tag after the link)
5. Preserve ALL original content including:
   - Complete technical explanations (even if verbose)
   - Historical context and dates
   - All code examples with original formatting
   - Credits and contributor lists
   - Detailed step-by-step instructions

### Conversion Verification Checklist

**MANDATORY - Verify ALL items before completing any HTML conversion:**

#### General Page Requirements
- [ ] Used `<!DOCTYPE html>` (not HTML 4.01 Transitional)
- [ ] Linked to shared CSS: `<link rel="stylesheet" href="css/devnull-shared.css">`
- [ ] NO inline `<style>` blocks (unless page-specific styles are required)
- [ ] NO Wayback Machine scripts, toolbars, or wrapper divs
- [ ] All `<font>` tags converted to semantic HTML
- [ ] Structure uses `<div class="container">` → `<header>` → `<main>` → `<div class="footer">`
- [ ] Title tag is descriptive and accurate
- [ ] Meta charset and viewport tags present

#### Content Preservation
- [ ] 100% of original content preserved (compared against original file)
- [ ] All technical explanations intact (no summarizing)
- [ ] All code examples preserved with original formatting
- [ ] All credits and contributor names preserved
- [ ] All step-by-step instructions preserved
- [ ] All tables and structured data preserved
- [ ] Historical dates and "Last Updated" information preserved

#### Links and Navigation
- [ ] All external links have `target="_blank"`
- [ ] Dead links updated to modern equivalents (UESP, Nexusmods)
- [ ] Wayback Machine URLs unwrapped and modernized
- [ ] Internal links use relative paths (not absolute URLs)
- [ ] Footer navigation matches page type (see below)

#### FCOM Page-Specific Requirements
**If converting a FCOM_*.html page, verify ALL of these:**
- [ ] Footer uses `<div class="footer">` NOT `<footer>` tag
- [ ] Footer includes PES Hall of Fame image: `<img src="images/PES_HallofFameSmall.jpg" class="nav-image">`
- [ ] Footer has `<hr class="nav-divider">` BEFORE navigation links
- [ ] Footer has `<hr class="nav-divider">` AFTER navigation links
- [ ] Footer includes ALL 7 navigation links in this order:
  1. Home
  2. Dev/Null Mods
  3. Main (FCOM_Convergence.html)
  4. Guide (FCOM_Convergence_Guide.html)
  5. Load-Order (FCOM_LoadOrder.html)
  6. Options (FCOM_Options.html)
  7. Version History (FCOM_VersionHistory.html)
- [ ] Copyright line exactly matches: `Copyright 2006, 2007, 2008, 2009, 2015, 2025 by devakm. Individual works copyright by their respective creators.`

#### Standard Page Footer Requirements
**If converting a non-FCOM page, verify:**
- [ ] Footer uses `<div class="footer">` NOT `<footer>` tag
- [ ] Footer includes standard 4-link navigation (Home | Dev/Null Mods | TOTO Main | Quest List)
- [ ] Copyright line matches standard format

#### Final Validation
- [ ] Opened file in browser to verify rendering
- [ ] All images load correctly
- [ ] No console errors in browser dev tools
- [ ] Dark mode colors display correctly
- [ ] **Link Testing (MANDATORY - Test ALL links):**
  - [ ] Clicked every external link to verify it resolves (not 404)
  - [ ] Verified internal links point to existing files
  - [ ] Checked that modernized links (UESP, Nexusmods) load correctly
  - [ ] Documented any broken links that cannot be fixed
  - [ ] Reported broken links to user before completing task

## Key Content Areas

- **FCOM: Convergence** - Major mod integration project (Francesco + WarCry + Oscuro + Martigen)
- **ArchiveInvalidation** - Critical technical documentation with detailed hash table explanations
- **Quest Mods** - Catalogs in `Big-Quest-Mods.html` and `Small-Quest-Mods.html`
- **De-Isolation Tutorial** - Technical guide for mod compatibility
- **Load Order Guides** - Critical for mod stability

## File Structure
```
docs/
  ├── index.html           # Main landing page
  ├── devakm-mods.html    # Homepage for dev/akm's work
  ├── FCOM_*.html         # FCOM documentation suite
  ├── ArchiveInvalidation.html
  ├── *-Quest-Mods.html
  └── images/
```

## Navigation Patterns

### Standard Footer Navigation
Most pages should include this standardized footer navigation:
```html
<div class="footer">
    <p>
        <a href="index.html">Home</a> |
        <a href="devakm-mods.html">Dev/Null Mods</a> |
        <a href="Oblivion-Texture-Overhaul.html">TOTO Main</a> |
        <a href="Quests.html">The Oblivion Quest List</a>
    </p>
    <p>Copyright 2006, 2007, 2008, 2009, 2015, 2025 by devakm. Individual works copyright by their respective creators.</p>
</div>
```

This navigation appears on: General documentation pages, texture guides, quest mod pages, and standalone mod pages.

### FCOM Footer Navigation
FCOM-related pages should include the extended FCOM footer navigation:
```html
<div class="footer">
    <p>
        <img src="images/PES_HallofFameSmall.jpg" title="Homage to the venerable PlanetElderScrolls Hall of Fame" class="nav-image"><br>
        <hr class="nav-divider">
        <a href="index.html">Home</a> |
        <a href="devakm-mods.html">Dev/Null Mods</a> |  
        <a href="FCOM_Convergence.html">Main</a> |
        <a href="FCOM_Convergence_Guide.html">Guide</a> |
        <a href="FCOM_LoadOrder.html">Load-Order</a> |
        <a href="FCOM_Options.html">Options</a> |
        <a href="FCOM_VersionHistory.html">Version History</a>
        <hr class="nav-divider">
    </p>
    <p>Copyright 2006, 2007, 2008, 2009, 2015, 2025 by devakm. Individual works copyright by their respective creators.</p>
</div>
```

This navigation appears on: `FCOM_Convergence.html`, `FCOM_Convergence_Guide.html`, `FCOM_LoadOrder.html`, `FCOM_LoadOrderExpanded.html`, `FCOM_Options.html`, `FCOM_VersionHistory.html`

### PES Hall of Fame Badge Decoration
Quest-related pages can include the decorative PES (Planet Elder Scrolls) Hall of Fame badge above navigation links:

**Required CSS**:
```css
.nav-image {
    height: 31px;
    vertical-align: middle;
    margin: 0 5px;
    transition: opacity 0.3s ease;
}

.nav-image:hover {
    opacity: 0.8;
}

.nav-divider {
    border: none;
    border-top: 1px solid #ffffff;
    margin: 10px auto;
    width: 50%;
    opacity: 0.3;
}
```

**Header Nav Implementation**:
```html
<nav>
    <img src="images/PES_HallofFameSmall.jpg" title="Homage to the venerable PlanetElderScrolls Hall of Fame" class="nav-image"><br>
    <hr class="nav-divider">
    <a href="index.html">Home</a> |
    <a href="devakm-mods.html">Dev/Null Mods & Guides</a> |
    <a href="Oblivion-Texture-Overhaul.html">TOTO</a>
</nav>
```

**Footer Implementation**:
```html
<footer>
    <p>
        <img src="images/PES_HallofFameSmall.jpg" title="Homage to the venerable PlanetElderScrolls Hall of Fame" class="nav-image"><br>
        <hr class="nav-divider">
        <a href="index.html">Home</a> |
        <a href="devakm-mods.html">Dev/Null Mods</a> |
        <a href="Oblivion-Texture-Overhaul.html">TOTO Main</a>
        <a href="Quests.html">The Oblivion Quest List</a>
        <hr class="nav-divider">
    </p>
    <p>Copyright 2006, 2007, 2008, 2009, 2015, 2025 by devakm. Individual works copyright by their respective creators.</p>
</footer>
```

**Note**: The badge is purely decorative (no link) since planetelderscrolls.gamespy.com no longer exists.

## Examples from Codebase

**Preserving technical detail** (from ArchiveInvalidation.html):
- Keep complete hash table explanations with underscored/strikethrough formatting
- Preserve all FilenameStringTable and DirectoryStringTable examples
- Maintain verbose "ArchiveInvalidation Explained" section (~200+ lines)

**Two-column grid layout** (from devakm-mods.html):
```css
.content-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 30px;
}
```

## Working with Original Downloads

### Verifying Content Preservation
When converting HTML files, always verify against original Wayback Machine downloads in `x:\dev-staging\temp`:

1. **Before converting**: Open the original HTML file in `x:\dev-staging\temp` to review all content sections
2. **During conversion**: Keep original file open for reference to ensure nothing is missed
3. **After conversion**: Compare paragraph by paragraph to verify 100% content preservation
4. **Critical sections**: Pay special attention to:
   - Technical explanations and code examples
   - Installation instructions and step-by-step guides
   - Credits and contributor lists
   - All links and download information
   - Tables and structured data

### Extracting Images
Original Wayback Machine downloads contain image files that need to be extracted:

1. **Locate images**: Check `*_files/` folders in `x:\dev-staging\temp` for each page
2. **Copy to repo**: Extract images to `docs/images/` folder
3. **Update paths**: Ensure HTML references use `images/filename.jpg` (not old Wayback paths)
4. **Common image types**:
   - Screenshots (`.jpg`, `.png`)
   - Thumbnails (prefixed with `th_`)
   - Diagrams and charts
   - Tool screenshots (e.g., OBMM settings)

**Example workflow**:
```powershell
# Copy images from temp to repo
Copy-Item "x:\dev-staging\temp\devnull.devakm - Page Name_files\*.jpg" "x:\dev\devnull\docs\images\" -ErrorAction SilentlyContinue
Copy-Item "x:\dev-staging\temp\devnull.devakm - Page Name_files\*.png" "x:\dev\devnull\docs\images\" -ErrorAction SilentlyContinue
```

## Testing

### Pre-Deployment Validation
Before completing any HTML conversion, perform comprehensive testing:

**Content Rendering:**
- Open converted HTML file in browser
- Verify all sections render correctly with proper formatting
- Check that dark mode colors are consistent throughout
- Confirm no missing sections or truncated content
- Verify all images load properly from `docs/images/` folder

**Link Validation (CRITICAL):**
1. **Test ALL external links:**
   - Click each external link to verify it resolves (not 404/dead)
   - Confirm modernized links (UESP, Nexusmods, UESPNET) load correctly
   - Verify target="_blank" opens in new tab
   - Document any dead links that couldn't be modernized

2. **Test ALL internal links:**
   - Click each internal link to verify file exists
   - Confirm relative paths resolve correctly
   - Check navigation footer links work properly

3. **Report Broken Links:**
   - If any links cannot be fixed or modernized, document them
   - Report to user with list of broken links and URLs attempted
   - Suggest archival alternatives or indicate "link no longer available"
   - Example: "Note: XYZ mod page no longer exists - PlanetElderScrolls is defunct"

**Browser Console Check:**
- Open browser dev tools (F12)
- Check for any JavaScript errors (there shouldn't be any - pure HTML/CSS)
- Verify no 404 errors for missing resources
- Confirm no mixed content warnings
