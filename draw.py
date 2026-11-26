import os
from PIL import Image, ImageDraw, ImageFont

def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
                current_line = [word]
            else:
                lines.append(word)
    if current_line:
        lines.append(" ".join(current_line))
    return lines

def draw_illustration(draw, panel_type, box):
    # box is (x0, y0, x1, y1)
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    w = x1 - x0
    h = y1 - y0

    # Background for illustration box
    draw.rectangle([x0, y0, x1, y1], fill="#f5f2eb", outline="#d0c8b8", width=1)

    if panel_type == "hormuz":
        # Ocean waves
        draw.rectangle([x0+5, y1-25, x1-5, y1-5], fill="#204060")
        for i in range(x0+10, x1-10, 20):
            draw.arc([i, y1-30, i+15, y1-20], start=0, end=180, fill="#4070a0", width=2)
        # Tanker hull
        hull_x0, hull_y0 = cx - 45, cy - 5
        hull_x1, hull_y1 = cx + 45, cy + 25
        draw.polygon([
            (hull_x0 + 10, hull_y0),
            (hull_x1 - 10, hull_y0),
            (hull_x1, hull_y1),
            (hull_x0, hull_y1)
        ], fill="#333333")
        # Superstructure
        draw.rectangle([cx - 20, hull_y0 - 15, cx + 15, hull_y0], fill="#555555")
        # Fire & smoke
        draw.ellipse([cx - 15, hull_y0 - 30, cx + 5, hull_y0 - 5], fill="#ff4500")
        draw.ellipse([cx - 5, hull_y0 - 45, cx + 20, hull_y0 - 20], fill="#ff8c00")
        draw.ellipse([cx, hull_y0 - 60, cx + 30, hull_y0 - 35], fill="#888888")

    elif panel_type == "refineries":
        # Ground
        draw.rectangle([x0+5, y1-15, x1-5, y1-5], fill="#555555")
        # Refinery towers
        towers = [cx - 60, cx - 20, cx + 25]
        for tx in towers:
            draw.rectangle([tx, cy - 10, tx + 18, y1 - 15], fill="#777777")
            # Pipes
            draw.line([(tx+9, cy - 10), (tx+9, y1 - 15)], fill="#444444", width=2)
            # Explosion / fire at left tower (Syzran)
            if tx == cx - 60:
                draw.ellipse([tx - 15, cy - 35, tx + 25, cy - 5], fill="#ff3300")
                draw.ellipse([tx - 10, cy - 50, tx + 20, cy - 20], fill="#ffaa00")
        # Drone trajectory lines
        draw.line([(x0 + 10, y0 + 15), (cx - 60, cy - 20)], fill="#cc0000", width=2)
        draw.polygon([(cx - 60, cy - 20), (cx - 50, cy - 25), (cx - 55, cy - 15)], fill="#cc0000")

    elif panel_type == "markets":
        # Grid lines
        for y_line in range(y0 + 10, y1 - 10, 20):
            draw.line([(x0 + 10, y_line), (x1 - 10, y_line)], fill="#e0dcd0", width=1)
        # Red plunge bar chart
        bars = [
            ("KOSPI\n-6.2%", 30, "#cc0000"),
            ("N Nikkei\n-2.8%", 70, "#dd3333"),
            ("Taiex\n~-5%", 110, "#cc0000"),
            ("Nvidia\nFall", 150, "#990000")
        ]
        bw = 32
        start_x = x0 + 18
        for label, val_y, col in bars:
            bx = start_x
            draw.rectangle([bx, cy - 15, bx + bw, y1 - 18], fill=col)
            start_x += 45
        # Trend line connecting drops
        draw.line([(x0 + 34, cy), (x0 + 79, cy + 15), (x0 + 124, cy + 5), (x0 + 169, cy + 25)], fill="#ffffff", width=2)

    elif panel_type == "huawei":
        # Courthouse columns
        col_w = 12
        col_y0 = y0 + 15
        col_y1 = y1 - 15
        for cx_pos in [cx - 45, cx - 15, cx + 15, cx + 45]:
            draw.rectangle([cx_pos, col_y0 + 10, cx_pos + col_w, col_y1], fill="#888888", outline="#444444")
        # Pediment
        draw.polygon([
            (cx - 60, col_y0 + 10),
            (cx + 60, col_y0 + 10),
            (cx, col_y0 - 15)
        ], fill="#666666")
        # Verdict stamp banner
        draw.rectangle([cx - 55, cy - 10, cx + 55, cy + 15], fill="#b30000")

    elif panel_type == "space":
        # Space background (stars)
        for sx, sy in [(x0+20, y0+20), (x1-30, y0+30), (x0+50, y1-30), (x1-40, y1-40), (cx, y0+15)]:
            draw.ellipse([sx, sy, sx+3, sy+3], fill="#ffffff")
        # Tiangong station module
        draw.rectangle([cx - 40, cy - 12, cx + 10, cy + 12], fill="#cccccc", outline="#ffffff", width=1)
        # Solar panels
        draw.rectangle([cx - 70, cy - 6, cx - 40, cy + 6], fill="#113355", outline="#6699cc", width=1)
        draw.rectangle([cx + 10, cy - 6, cx + 40, cy + 6], fill="#113355", outline="#6699cc", width=1)
        # Shenzhou spacecraft approaching
        draw.polygon([
            (cx + 35, cy),
            (cx + 55, cy - 6),
            (cx + 55, cy + 6)
        ], fill="#ffffff")

    elif panel_type == "cairo":
        # Roadway perspective
        draw.polygon([
            (cx, cy + 10),
            (x0 + 20, y1 - 10),
            (x1 - 20, y1 - 10)
        ], fill="#333333")
        # Dashed center line
        draw.line([(cx, cy + 10), (cx, y1 - 10)], fill="#ffcc00", width=2)
        # Tanker truck & fire
        draw.rectangle([cx - 25, cy - 5, cx + 15, cy + 15], fill="#444444")
        draw.ellipse([cx - 20, cy - 35, cx + 25, cy + 5], fill="#ff4500")
        draw.ellipse([cx - 10, cy - 50, cx + 20, cy - 20], fill="#ffaa00")

def main():
    img_size = 1024
    img = Image.new("RGB", (img_size, img_size), "#fdfbf7")
    draw = ImageDraw.Draw(img)

    # Load fonts
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 40)
        font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
        font_panel_tag = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 11)
        font_headline = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 13)
        font_caption = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_panel_tag = ImageFont.load_default()
        font_headline = ImageFont.load_default()
        font_caption = ImageFont.load_default()

    # --- Masthead ---
    # Top rule
    draw.line([(20, 20), (1004, 20)], fill="#1a1a1a", width=3)
    draw.line([(20, 26), (1004, 26)], fill="#1a1a1a", width=1)

    # Title text
    title_text = "THE GLOBAL CHRONICLE"
    t_bbox = draw.textbbox((0, 0), title_text, font=font_title)
    t_w = t_bbox[2] - t_bbox[0]
    draw.text(((img_size - t_w) // 2, 35), title_text, fill="#1a1a1a", font=font_title)

    # Subhead / Date bar
    sub_text = "WEDNESDAY, 25 NOVEMBER 2026  •  WORLD EDITION  •  ISSUE NO. 4,189"
    s_bbox = draw.textbbox((0, 0), sub_text, font=font_sub)
    s_w = s_bbox[2] - s_bbox[0]
    draw.text(((img_size - s_w) // 2, 85), sub_text, fill="#444444", font=font_sub)

    # Bottom masthead rule
    draw.line([(20, 108), (1004, 108)], fill="#1a1a1a", width=2)
    draw.line([(20, 112), (1004, 112)], fill="#1a1a1a", width=1)

    # --- Six Panels Layout (3 cols x 2 rows) ---
    cols = 3
    rows = 2
    margin_x = 20
    margin_y = 125
    gap_x = 16
    gap_y = 16

    total_w = img_size - (margin_x * 2) - (gap_x * (cols - 1))
    col_w = total_w // cols

    total_h = img_size - margin_y - 20 - (gap_y * (rows - 1))
    row_h = total_h // rows

    stories = [
        {
            "type": "hormuz",
            "tag": "MIDDLE EAST",
            "headline": "Hormuz Tankers Hit Mines & Burn; Houthis Claim Ras Tanura Attack",
            "caption": "Crude tankers burn in the Strait of Hormuz after coordinated mine blasts; Houthis claim strike on Saudi Ras Tanura refinery."
        },
        {
            "type": "refineries",
            "tag": "CONFLICT",
            "headline": "Ukrainian Drones Strike Russian Refineries; Odesa & Kyiv Hit",
            "caption": "Long-range Ukrainian drones target Russian refineries at Syzran and Kuibyshev; heavy Russian missile strikes hit Odesa and Kyiv."
        },
        {
            "type": "markets",
            "tag": "FINANCE",
            "headline": "Asian Markets Plunge & Nvidia Falls After Prior Surge",
            "caption": "KOSPI drops 6.16%, Nikkei falls 2.78%, Taiex tumbles ~5% amid regional sell-off; Nvidia retreats following prior tech surge."
        },
        {
            "type": "huawei",
            "tag": "LEGAL",
            "headline": "Huawei Convicted in U.S. Criminal Trial on Fraud & Trade Secrets",
            "caption": "Federal jury finds Huawei guilty in U.S. criminal court on multiple felony counts of wire fraud, conspiracy, and theft of trade secrets."
        },
        {
            "type": "space",
            "tag": "SPACE",
            "headline": "Shenzhou-24 Docks at Tiangong With Pakistan Astronaut Aboard",
            "caption": "Historic docking carries Muhammad Zeeshan Ali of Pakistan, marking the first foreign astronaut on a Chinese crewed space mission."
        },
        {
            "type": "cairo",
            "tag": "ACCIDENT",
            "headline": "Fuel Tanker Crash & Massive Fire Near Cairo Kills At Least 31",
            "caption": "Devastating highway collision involving a fuel tanker triggers massive fires on the outskirts of Cairo, resulting in at least 31 fatalities."
        }
    ]

    idx = 0
    for r in range(rows):
        for c in range(cols):
            if idx >= len(stories):
                break
            story = stories[idx]
            idx += 1

            x0 = margin_x + c * (col_w + gap_x)
            y0 = margin_y + r * (row_h + gap_y)
            x1 = x0 + col_w
            y1 = y0 + row_h

            # Panel background & border
            draw.rectangle([x0, y0, x1, y1], fill="#ffffff", outline="#333333", width=2)
            # Inner padding box
            px0, py0 = x0 + 10, y0 + 10
            px1, py1 = x1 - 10, y1 - 10
            max_w = px1 - px0

            # 1. Tag
            tag_text = story["tag"]
            draw.text((px0, py0), tag_text, fill="#b30000", font=font_panel_tag)
            py_cursor = py0 + 16

            # 2. Headline (wrapped, max 2-3 lines)
            headline_lines = wrap_text(draw, story["headline"], font_headline, max_w)
            for line in headline_lines[:3]:
                draw.text((px0, py_cursor), line, fill="#1a1a1a", font=font_headline)
                bbox = draw.textbbox((px0, py_cursor), line, font=font_headline)
                py_cursor += (bbox[3] - bbox[1]) + 3
            # Headline underline rule
            draw.line([(px0, py_cursor + 1), (px1, py_cursor + 1)], fill="#d0c8b8", width=1)
            py_cursor += 6

            # 3. Procedural Illustration box
            ill_h = 150
            ill_box = [px0, py_cursor, px1, py_cursor + ill_h]
            draw_illustration(draw, story["type"], ill_box)
            py_cursor += ill_h + 8

            # 4. Caption (wrapped, max 2-3 lines)
            caption_lines = wrap_text(draw, story["caption"], font_caption, max_w)
            for line in caption_lines[:3]:
                draw.text((px0, py_cursor), line, fill="#444444", font=font_caption)
                bbox = draw.textbbox((px0, py_cursor), line, font=font_caption)
                py_cursor += (bbox[3] - bbox[1]) + 2

            # Verify every label stays inside its panel (py_cursor <= py1)
            if py_cursor > py1:
                print(f"WARNING: Panel {story['tag']} content overflow by {py_cursor - py1}px!")
            else:
                print(f"Panel {story['tag']} verified: bottom y {py_cursor} within panel limit {py1}")

    # Save output
    out_path = "entry.png"
    img.save(out_path, "PNG")
    file_size = os.path.getsize(out_path)
    print(f"Successfully generated {out_path}: size={file_size} bytes, dimensions={img.size}")

if __name__ == "__main__":
    main()
