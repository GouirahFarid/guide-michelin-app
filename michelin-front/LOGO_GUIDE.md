# Adding the Michelin Guide Logo

## Logo Files Needed

Place these logo files in `michelin-front/public/images/`:

1. **`michelin-guide-logo.png`** - Full color logo (with background)
   - Used in: Header, Hero section
   - Recommended size: 200x200px or larger
   - Format: PNG with transparency or solid background

2. **`michelin-guide-logo-white.png`** - White version (for dark/red backgrounds)
   - Used in: Chat widget header, Button backgrounds
   - Recommended size: 100x100px or larger
   - Format: PNG with transparency

## Where to Get the Logo

1. **Official Michelin Guide Website**: https://guide.michelin.com/
2. **Michelin Press Kit**: Search for "Michelin Guide logo press kit"
3. **Vector Format**: Use SVG if available for better scaling

## Temporary Fallback

If logos are not present, the app will automatically use the "M" placeholder with Michelin red gradient.

## Adding the Logo

### Option 1: Direct Upload
```bash
# Copy your logo files to the images directory
cp michelin-guide-logo.png michelin-front/public/images/
cp michelin-guide-logo-white.png michelin-front/public/images/
```

### Option 2: Create Simple Versions
If you don't have the official logo, you can create temporary versions:

1. Use the Michelin red color: `#dc2626`
2. Use the Bibendum (Michelin Man) silhouette
3. Or use the text "MICHELIN Guide" in a serif font

## Logo Specifications

**Official Michelin Red:**
- Hex: `#DC2626` or `#B91C1C`
- RGB: `rgb(220, 38, 38)`

**Usage Guidelines:**
- Maintain aspect ratio
- Don't stretch or distort
- Use appropriate contrast for backgrounds
