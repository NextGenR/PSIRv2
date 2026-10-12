import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_psir_icon(size):
    # Create image with RGBA
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Corner radius ~22.5%
    corner_radius = int(size * 0.225)
    
    # Draw background gradient on a temporary image
    bg = Image.new("RGB", (size, size), (0, 0, 0))
    # Gradient colors: Deep royal crimson (#991b1b) to deep berry/wine (#4c0519)
    color_top = (153, 27, 27)    # #991b1b
    color_mid = (131, 24, 67)    # #831843
    color_bot = (76, 5, 25)      # #4c0519
    
    for y in range(size):
        t = y / float(size)
        if t < 0.5:
            factor = t / 0.5
            r = int(color_top[0] * (1 - factor) + color_mid[0] * factor)
            g = int(color_top[1] * (1 - factor) + color_mid[1] * factor)
            b = int(color_top[2] * (1 - factor) + color_mid[2] * factor)
        else:
            factor = (t - 0.5) / 0.5
            r = int(color_mid[0] * (1 - factor) + color_bot[0] * factor)
            g = int(color_mid[1] * (1 - factor) + color_bot[1] * factor)
            b = int(color_mid[2] * (1 - factor) + color_bot[2] * factor)
        for x in range(size):
            bg.putpixel((x, y), (r, g, b))

    # Create mask for rounded squircle
    mask = Image.new("L", (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([(0, 0), (size, size)], radius=corner_radius, fill=255)

    # Paste gradient onto RGBA using mask
    img.paste(bg, (0, 0), mask)

    # Draw border ring inside
    border_draw = ImageDraw.Draw(img)
    inset = max(2, int(size * 0.024))
    border_draw.rounded_rectangle(
        [(inset, inset), (size - inset, size - inset)],
        radius=corner_radius - inset,
        outline=(255, 255, 255, 45),
        width=max(1, int(size * 0.008))
    )

    # Text Font for PSIR in bold serif letters
    font_size = int(size * 0.31)
    font_path = r"C:\Windows\Fonts\georgiab.ttf" # Georgia Bold serif
    if not os.path.exists(font_path):
        font_path = r"C:\Windows\Fonts\arialbd.ttf"
        
    try:
        font = ImageFont.truetype(font_path, font_size)
    except:
        font = ImageFont.load_default()

    text = "PSIR"
    
    # Measure text
    bbox = border_draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    text_x = (size - text_w) // 2
    # Adjust vertical center slightly upwards to allow space for gold accent bar
    text_y = int(size * 0.30) - (bbox[1] // 2)

    # Drop shadow for text
    shadow_offset = max(2, int(size * 0.015))
    border_draw.text((text_x, text_y + shadow_offset), text, font=font, fill=(0, 0, 0, 140))
    # Crisp white text
    border_draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255, 255))

    # Gold accent line below PSIR
    bar_w = int(text_w * 0.75)
    bar_h = max(3, int(size * 0.015))
    bar_x1 = (size - bar_w) // 2
    bar_y1 = text_y + text_h + int(size * 0.05)
    border_draw.rounded_rectangle(
        [(bar_x1, bar_y1), (bar_x1 + bar_w, bar_y1 + bar_h)],
        radius=bar_h // 2,
        fill=(251, 191, 36, 240) # Amber / Gold
    )

    # Subtitle pill "PREP SUITE" or "UPSC"
    sub_font_size = int(size * 0.08)
    try:
        sub_font = ImageFont.truetype(r"C:\Windows\Fonts\georgiab.ttf", sub_font_size)
    except:
        try:
            sub_font = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", sub_font_size)
        except:
            sub_font = font

    sub_text = "EXAM SUITE"
    sub_bbox = border_draw.textbbox((0, 0), sub_text, font=sub_font)
    sub_w = sub_bbox[2] - sub_bbox[0]
    sub_h = sub_bbox[3] - sub_bbox[1]
    sub_x = (size - sub_w) // 2
    sub_y = bar_y1 + bar_h + int(size * 0.04)

    border_draw.text((sub_x, sub_y), sub_text, font=sub_font, fill=(254, 215, 170, 220))

    return img

# Generate all required icon sizes
print("Generating 512x512 app icon...")
icon512 = create_psir_icon(512)
icon512.save("icon-512.png", "PNG")

print("Generating 192x192 app icon...")
icon192 = create_psir_icon(192)
icon192.save("icon-192.png", "PNG")

print("Generating 180x180 apple touch icon...")
icon180 = create_psir_icon(180)
icon180.save("apple-touch-icon.png", "PNG")

print("Generating 48x48 favicon...")
icon48 = create_psir_icon(48)
icon48.save("favicon.png", "PNG")

# Generate SVG Favicon with bold PSIR
svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#991b1b"/>
      <stop offset="50%" stop-color="#831843"/>
      <stop offset="100%" stop-color="#4c0519"/>
    </linearGradient>
    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#f59e0b"/>
      <stop offset="50%" stop-color="#fbbf24"/>
      <stop offset="100%" stop-color="#f59e0b"/>
    </linearGradient>
    <filter id="textGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#000000" flood-opacity="0.45"/>
    </filter>
  </defs>
  <!-- App Icon Background -->
  <rect width="512" height="512" rx="115" fill="url(#bgGrad)"/>
  <rect x="12" y="12" width="488" height="488" rx="103" fill="none" stroke="rgba(255,255,255,0.22)" stroke-width="4"/>
  <!-- Bold PSIR Typography -->
  <text x="256" y="275" font-family="'Roboto Serif', Georgia, serif" font-weight="900" font-size="160" fill="#ffffff" text-anchor="middle" letter-spacing="4" filter="url(#textGlow)">PSIR</text>
  <!-- Gold Accent Divider -->
  <rect x="166" y="318" width="180" height="8" rx="4" fill="url(#goldGrad)"/>
  <!-- Sub-label -->
  <text x="256" y="375" font-family="'Roboto Serif', Georgia, serif" font-weight="800" font-size="38" fill="#fed7aa" text-anchor="middle" letter-spacing="6">EXAM SUITE</text>
</svg>'''

with open("favicon.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)

print("[OK] All PSIR bold app icons generated successfully!")
