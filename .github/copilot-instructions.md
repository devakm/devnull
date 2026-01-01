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

### Dark Mode Color Scheme (required for all pages)
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
3. Apply standardized dark mode CSS (see existing files like `devakm-mods.html`)
4. Preserve ALL original content including:
   - Complete technical explanations (even if verbose)
   - Historical context and dates
   - All code examples with original formatting
   - Credits and contributor lists
   - Detailed step-by-step instructions

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
        <a href="FCOM_FAQ.html">FAQ</a> |
        <a href="FCOM_Support.html">Support</a> |
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
Open converted HTML files in browser to verify:
- All content renders correctly
- Links work (especially updated UESP/Nexus links)
- Dark mode colors are consistent
- No missing sections or truncated content
- All images load properly from `docs/images/` folder
