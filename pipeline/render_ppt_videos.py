import os
import sys
import json
import subprocess
import math
from PIL import Image, ImageDraw, ImageFont

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

WIDTH = 1920
HEIGHT = 1080
FPS = 30

# Colors for Clean White PPT
BG_COLOR = (255, 255, 255)
TEXT_MAIN = (15, 23, 42)      # #0F172A deep dark slate/black
TEXT_MUTED = (71, 85, 105)    # #475569 slate muted
TEXT_SUBTLE = (148, 163, 184) # #94A3B8 light slate
CARD_BG = (248, 250, 252)     # #F8FAFC crisp off-white card
CARD_BORDER = (226, 232, 240) # #E2E8F0 subtle border
ACCENT_BLUE = (37, 99, 235)   # #2563EB electric royal blue
ACCENT_BLUE_SOFT = (239, 246, 255)
ACCENT_GOLD = (217, 119, 6)   # #D97706 warm amber
ACCENT_GREEN = (16, 185, 129) # #10B981 emerald
ACCENT_RED = (239, 68, 68)

def load_fonts():
    font_paths = [
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibrib.ttf",
        "C:/Windows/Fonts/calibri.ttf"
    ]
    def find_font(name_sub, size):
        for p in font_paths:
            if name_sub in p.lower() and os.path.exists(p):
                try:
                    return ImageFont.truetype(p, size)
                except Exception:
                    pass
        return ImageFont.load_default()

    return {
        "title": find_font("b.ttf", 46),
        "subtitle": find_font("ui.ttf", 24),
        "header_tag": find_font("b.ttf", 22),
        "card_title": find_font("b.ttf", 30),
        "card_badge": find_font("b.ttf", 20),
        "body": find_font("ui.ttf", 24),
        "body_bold": find_font("b.ttf", 24),
        "formula": find_font("b.ttf", 28),
        "footer": find_font("ui.ttf", 20)
    }

FONTS = load_fonts()

def draw_rounded_rect(draw, bbox, radius, fill, outline=None, width=1):
    x0, y0, x1, y1 = bbox
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)

def render_ppt_slide_frame(slide, slide_idx, total_slides, local_time, slide_dur, global_time, total_dur):
    """
    Renders a single 1080p slide frame for the clean white presentation.
    local_time is seconds into current slide.
    """
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # 1. Elegant Presentation Top Header
    draw_rounded_rect(draw, (80, 50, 430, 88), 8, ACCENT_BLUE_SOFT, ACCENT_BLUE, 1)
    draw.text((96, 58), "ICAI CA FINAL • DIRECT TAX", font=FONTS["header_tag"], fill=ACCENT_BLUE)

    badge = slide.get('section_badge', '')
    if badge:
        bbox = FONTS["header_tag"].getbbox(badge)
        bw = (bbox[2] - bbox[0]) + 30
        draw_rounded_rect(draw, (WIDTH - 80 - bw, 50, WIDTH - 80, 88), 8, (241, 245, 249), (203, 213, 225), 1)
        draw.text((WIDTH - 80 - bw + 15, 58), badge, font=FONTS["header_tag"], fill=TEXT_MUTED)

    # 2. Slide Title
    title = slide.get('slide_title', '')
    # Subtle blue bar next to title
    draw.rectangle([80, 115, 88, 175], fill=ACCENT_BLUE)
    draw.text((106, 120), title, font=FONTS["title"], fill=TEXT_MAIN)

    # 3. Slide Content Layout
    cards = slide.get('cards', [])
    formula_box = slide.get('formula_box', None)
    
    # Calculate entrance animation progress (smooth 0.5s ease out)
    enter_t = min(1.0, local_time / 0.5)
    # Ease out cubic
    ease = 1.0 - math.pow(1.0 - enter_t, 3)
    anim_offset = int((1.0 - ease) * 35) # slides up 35px

    content_top = 220 + anim_offset
    content_bottom = 960

    num_cards = len(cards)
    if num_cards > 0:
        gap = 28
        left_margin = 80
        right_margin = WIDTH - 80
        total_width = right_margin - left_margin
        
        # Grid layout: if 2 cards, side by side; if 3 cards, 3 columns; if 4 cards, 2x2 grid
        if num_cards == 2:
            card_w = (total_width - gap) // 2
            card_h = 420 if not formula_box else 320
            positions = [
                (left_margin, content_top, left_margin + card_w, content_top + card_h),
                (left_margin + card_w + gap, content_top, right_margin, content_top + card_h)
            ]
        elif num_cards == 3:
            card_w = (total_width - gap * 2) // 3
            card_h = 440 if not formula_box else 320
            positions = [
                (left_margin + i * (card_w + gap), content_top, left_margin + i * (card_w + gap) + card_w, content_top + card_h)
                for i in range(3)
            ]
        else: # 4 cards
            card_w = (total_width - gap) // 2
            card_h = 240
            positions = [
                (left_margin, content_top, left_margin + card_w, content_top + card_h),
                (left_margin + card_w + gap, content_top, right_margin, content_top + card_h),
                (left_margin, content_top + card_h + 20, left_margin + card_w, content_top + card_h * 2 + 20),
                (left_margin + card_w + gap, content_top + card_h + 20, right_margin, content_top + card_h * 2 + 20)
            ]

        for i, card in enumerate(cards[:len(positions)]):
            cx0, cy0, cx1, cy1 = positions[i]
            is_hl = card.get('is_highlight', False)
            
            # Subtle card animation: active card highlights smoothly
            c_fill = CARD_BG
            c_border = CARD_BORDER
            border_w = 2
            
            if is_hl:
                # Highlight card with gentle blue or gold border & soft tint
                c_border = ACCENT_BLUE
                c_fill = ACCENT_BLUE_SOFT
                border_w = 3

            draw_rounded_rect(draw, (cx0, cy0, cx1, cy1), 16, c_fill, c_border, border_w)

            # Card Badge (if any)
            c_badge = card.get('badge', '')
            by = cy0 + 26
            if c_badge:
                b_bbox = FONTS["card_badge"].getbbox(c_badge)
                bw = (b_bbox[2] - b_bbox[0]) + 20
                draw_rounded_rect(draw, (cx0 + 26, by, cx0 + 26 + bw, by + 34), 6, ACCENT_BLUE if is_hl else (226, 232, 240), None)
                draw.text((cx0 + 36, by + 6), c_badge, font=FONTS["card_badge"], fill=(255, 255, 255) if is_hl else TEXT_MAIN)
                by += 46

            # Card Title
            c_title = card.get('title', '')
            draw.text((cx0 + 26, by), c_title, font=FONTS["card_title"], fill=ACCENT_BLUE if is_hl else TEXT_MAIN)
            by += 48

            # Bullets
            bullets = card.get('bullets', [])
            for b in bullets:
                # Custom neat bullet circle
                draw.ellipse([cx0 + 28, by + 8, cx0 + 36, by + 16], fill=ACCENT_BLUE if is_hl else TEXT_MUTED)
                # Text wrapping or clean display
                draw.text((cx0 + 46, by), b[:75], font=FONTS["body"], fill=TEXT_MAIN)
                by += 38

    # 4. Formula Box (if applicable)
    if formula_box:
        f_top = content_top + 340 if num_cards in [2, 3] else content_top + 520
        f_w = WIDTH - 160
        f_rect = (80, f_top, 80 + f_w, f_top + 160)
        draw_rounded_rect(draw, f_rect, 14, (241, 245, 249), ACCENT_GOLD, 2)
        
        # Tag
        draw_rounded_rect(draw, (104, f_top + 18, 320, f_top + 52), 6, ACCENT_GOLD, None)
        draw.text((116, f_top + 23), "STATUTORY FORMULA", font=FONTS["card_badge"], fill=(255, 255, 255))
        
        f_text = formula_box.get('formula_text', '')
        draw.text((104, f_top + 64), f_text, font=FONTS["formula"], fill=TEXT_MAIN)
        
        f_ex = formula_box.get('example_calc', '')
        if f_ex:
            draw.text((104, f_top + 110), f_ex, font=FONTS["body"], fill=TEXT_MUTED)

    # 5. Slide Footer & Continuous Progress Bar
    draw.line([(80, 1010), (WIDTH - 80, 1010)], fill=CARD_BORDER, width=1)
    
    footer_text = f"Slide {slide_idx + 1} of {total_slides} • Tax Study Studio"
    draw.text((80, 1025), footer_text, font=FONTS["footer"], fill=TEXT_MUTED)
    
    # Progress Bar (Width 300px)
    pb_x0 = WIDTH - 380
    pb_y0 = 1032
    pb_w = 300
    pb_h = 10
    draw_rounded_rect(draw, (pb_x0, pb_y0, pb_x0 + pb_w, pb_y0 + pb_h), 5, (226, 232, 240))
    prog_ratio = min(1.0, max(0.0, global_time / max(1.0, total_dur)))
    if prog_ratio > 0:
        draw_rounded_rect(draw, (pb_x0, pb_y0, pb_x0 + int(pb_w * prog_ratio), pb_y0 + pb_h), 5, ACCENT_BLUE)

    return img

def render_ppt_video_for_topic(key, topic_data):
    """
    Renders the complete 1080p MP4 video for key by piping frames directly into FFmpeg.
    """
    audio_path = os.path.join(PROJECT_ROOT, 'data', 'audio', f"{key}.mp3")
    output_video = os.path.join(PROJECT_ROOT, 'data', 'video', f"{key}.mp4")
    os.makedirs(os.path.dirname(output_video), exist_ok=True)
    
    slides = topic_data.get('slides', [])
    total_dur = topic_data.get('total_duration', 30.0)
    
    if not os.path.exists(audio_path):
        print(f"Error: audio file {audio_path} does not exist.")
        return False
        
    print(f"\n--- Rendering 1080p PPT Video for {key} (Duration: {total_dur}s, {len(slides)} slides) ---")
    
    total_frames = int(total_dur * FPS)
    
    # Launch FFmpeg process piping raw RGB24 frames
    cmd = [
        'ffmpeg', '-y',
        '-f', 'rawvideo',
        '-vcodec', 'rawvideo',
        '-s', f"{WIDTH}x{HEIGHT}",
        '-pix_fmt', 'rgb24',
        '-r', str(FPS),
        '-i', '-',
        '-i', audio_path,
        '-c:v', 'libx264',
        '-preset', 'veryfast',
        '-crf', '20',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-pix_fmt', 'yuv420p',
        '-shortest',
        output_video
    ]
    
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    for frame_idx in range(total_frames):
        t = frame_idx / FPS
        
        # Find which slide is active at time t
        active_slide = slides[0]
        active_idx = 0
        for s_idx, s in enumerate(slides):
            if s.get('t0', 0) <= t <= s.get('t1', total_dur):
                active_slide = s
                active_idx = s_idx
                break
            elif t > s.get('t1', 0):
                active_slide = s
                active_idx = s_idx

        s_t0 = active_slide.get('t0', 0)
        s_dur = active_slide.get('duration', 10.0)
        local_t = t - s_t0
        
        # Morph transition between slides (smoothstep cross-dissolve during first 0.5s)
        if active_idx > 0 and local_t < 0.5:
            alpha = max(0.0, min(1.0, local_t / 0.5))
            ease_alpha = alpha * alpha * (3.0 - 2.0 * alpha)
            prev_slide = slides[active_idx - 1]
            prev_dur = prev_slide.get('duration', 10.0)
            img_prev = render_ppt_slide_frame(prev_slide, active_idx - 1, len(slides), prev_dur, prev_dur, t, total_dur)
            img_curr = render_ppt_slide_frame(active_slide, active_idx, len(slides), local_t, s_dur, t, total_dur)
            frame_img = Image.blend(img_prev, img_curr, ease_alpha)
        else:
            frame_img = render_ppt_slide_frame(
                active_slide,
                active_idx,
                len(slides),
                local_t,
                s_dur,
                t,
                total_dur
            )
        
        proc.stdin.write(frame_img.tobytes())
        
        if frame_idx % (FPS * 5) == 0:
            print(f"  Rendered {frame_idx}/{total_frames} frames ({int(t)}s / {int(total_dur)}s)")
            
    proc.stdin.close()
    proc.wait()
    print(f"-> Video successfully rendered to {output_video}")
    return True

def main():
    specific_key = next((arg for arg in sys.argv[1:] if not arg.startswith('--')), None)
    sb_file = os.path.join(PROJECT_ROOT, 'data', 'ppt_storyboards.json')
    if not os.path.exists(sb_file):
        print("No storyboards file found.")
        return

    with open(sb_file, 'r', encoding='utf-8') as f:
        storyboards = json.load(f)

    for key, topic_data in storyboards.items():
        if specific_key and key != specific_key:
            continue
        render_ppt_video_for_topic(key, topic_data)

if __name__ == '__main__':
    main()
