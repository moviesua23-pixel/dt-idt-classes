import os
import sys
import subprocess
import shutil
from PIL import Image, ImageDraw, ImageFont

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
AUDIO_DIR = os.path.join(DATA_DIR, "audio")
VIDEO_DIR = os.path.join(DATA_DIR, "video")

os.makedirs(VIDEO_DIR, exist_ok=True)

FONT_REGULAR_PATH = "C:/Windows/Fonts/segoeui.ttf"
FONT_BOLD_PATH = "C:/Windows/Fonts/segoeuib.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception as e:
        print(f"Warning: Failed to load {path}, using default font: {e}")
        return ImageFont.load_default()

F_TITLE = get_font(FONT_BOLD_PATH, 44)
F_SUB = get_font(FONT_REGULAR_PATH, 24)
F_H2 = get_font(FONT_BOLD_PATH, 32)
F_BODY = get_font(FONT_REGULAR_PATH, 24)
F_BODY_BOLD = get_font(FONT_BOLD_PATH, 24)
F_SMALL = get_font(FONT_REGULAR_PATH, 20)
F_BADGE = get_font(FONT_BOLD_PATH, 20)
F_FORMULA = get_font(FONT_BOLD_PATH, 30)

WIDTH = 1920
HEIGHT = 1080

C_BG_TOP = (11, 19, 43)
C_BG_BOT = (20, 27, 45)
C_CARD_BG = (27, 38, 59)
C_CARD_BORDER = (45, 60, 89)
C_ACCENT_BLUE = (58, 134, 255)
C_ACCENT_GOLD = (245, 158, 11)
C_ACCENT_GREEN = (16, 185, 129)
C_ACCENT_RED = (239, 68, 68)
C_TEXT_WHITE = (248, 250, 252)
C_TEXT_MUTED = (148, 163, 184)
C_TEXT_DARK = (15, 23, 42)

def draw_gradient_background(draw):
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(C_BG_TOP[0] * (1 - ratio) + C_BG_BOT[0] * ratio)
        g = int(C_BG_TOP[1] * (1 - ratio) + C_BG_BOT[1] * ratio)
        b = int(C_BG_TOP[2] * (1 - ratio) + C_BG_BOT[2] * ratio)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

def draw_card(draw, x, y, w, h, fill=C_CARD_BG, outline=C_CARD_BORDER, width=2, radius=18):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=fill, outline=outline, width=width)

def draw_header(draw, title, subtitle, doctrine_badge="§ STATUTORY DOCTRINE FLOWCHART"):
    draw.rounded_rectangle([80, 45, 540, 90], radius=10, fill=(35, 45, 70), outline=C_ACCENT_GOLD, width=2)
    draw.text((105, 54), doctrine_badge, font=F_BADGE, fill=C_ACCENT_GOLD)
    draw.text((80, 105), title, font=F_TITLE, fill=C_TEXT_WHITE)
    draw.text((80, 160), subtitle, font=F_SUB, fill=C_TEXT_MUTED)
    draw.line([(80, 205), (WIDTH - 80, 205)], fill=(45, 60, 89), width=2)

def draw_arrow_right(draw, x_start, x_end, y, color=C_ACCENT_BLUE, width=4, text=None):
    draw.line([(x_start, y), (x_end, y)], fill=color, width=width)
    draw.polygon([(x_end - 12, y - 8), (x_end - 12, y + 8), (x_end, y)], fill=color)
    if text:
        draw.text(((x_start + x_end) // 2 - 20, y - 26), text, font=F_SMALL, fill=color)

def draw_progress(draw, cur_sec, total_sec):
    draw.line([(0, HEIGHT - 8), (WIDTH, HEIGHT - 8)], fill=(30, 41, 59), width=8)
    progress_w = int(WIDTH * min(1.0, max(0.0, cur_sec / total_sec)))
    if progress_w > 0:
        draw.line([(0, HEIGHT - 8), (progress_w, HEIGHT - 8)], fill=C_ACCENT_GOLD, width=8)

# ----------------- Q9: Domestic Companies Flowchart Video ----------------- #
def render_q9_frame(t, total_dur):
    im = Image.new("RGB", (WIDTH, HEIGHT))
    d = ImageDraw.Draw(im)
    draw_gradient_background(d)
    draw_header(d, "Domestic Companies: Surcharge & Marginal Relief Flowchart",
                "Section 4 · Annual Finance Act · Spoken Malayalam Audio Explainer")

    draw_card(d, 80, 235, 500, 380, fill=(30, 41, 65), outline=C_ACCENT_BLUE, width=3)
    d.text((105, 255), "1. Domestic Base Tax", font=F_H2, fill=C_ACCENT_BLUE)
    d.text((105, 320), "Turnover <= Rs 400 Cr", font=F_BODY, fill=C_TEXT_WHITE)
    d.rounded_rectangle([400, 310, 520, 360], radius=8, fill=C_ACCENT_BLUE)
    d.text((435, 318), "25%", font=F_BODY_BOLD, fill=C_TEXT_WHITE)
    
    d.text((105, 400), "Turnover > Rs 400 Cr", font=F_BODY, fill=C_TEXT_WHITE)
    d.rounded_rectangle([400, 390, 520, 440], radius=8, fill=(71, 85, 105))
    d.text((435, 398), "30%", font=F_BODY_BOLD, fill=C_TEXT_WHITE)

    draw_arrow_right(d, 590, 610, 355, color=C_ACCENT_BLUE)

    b1_active = (t >= 4.5 and t < 8.5)
    b1_bg = (30, 58, 80) if b1_active else (25, 35, 55)
    b1_out = C_ACCENT_GOLD if b1_active else C_CARD_BORDER
    draw_card(d, 615, 235, 620, 115, fill=b1_bg, outline=b1_out, width=4 if b1_active else 2)
    d.text((640, 255), "Up to Rs 1 Crore Total Income", font=F_H2, fill=C_TEXT_WHITE)
    d.text((640, 300), "Surcharge Applicable:", font=F_BODY, fill=C_TEXT_MUTED)
    d.rounded_rectangle([1100, 255, 1215, 325], radius=10, fill=C_ACCENT_GREEN if b1_active else (30, 60, 50))
    d.text((1125, 270), "NIL", font=F_H2, fill=C_TEXT_WHITE)

    b2_active = (t >= 8.5 and t < 12.5) or (t >= 14.5)
    b2_bg = (50, 40, 20) if b2_active else (25, 35, 55)
    b2_out = C_ACCENT_GOLD if b2_active else C_CARD_BORDER
    draw_card(d, 615, 365, 620, 115, fill=b2_bg, outline=b2_out, width=4 if b2_active else 2)
    d.text((640, 385), "> Rs 1 Cr up to Rs 10 Crore", font=F_H2, fill=C_TEXT_WHITE)
    d.text((640, 430), "Surcharge Applicable:", font=F_BODY, fill=C_TEXT_MUTED)
    d.rounded_rectangle([1100, 385, 1215, 455], radius=10, fill=C_ACCENT_GOLD if b2_active else (70, 50, 20))
    d.text((1135, 400), "7%", font=F_H2, fill=C_TEXT_DARK if b2_active else C_TEXT_WHITE)

    b3_active = (t >= 11.5 and t < 15.0)
    b3_bg = (50, 40, 20) if b3_active else (25, 35, 55)
    b3_out = C_ACCENT_GOLD if b3_active else C_CARD_BORDER
    draw_card(d, 615, 495, 620, 115, fill=b3_bg, outline=b3_out, width=4 if b3_active else 2)
    d.text((640, 515), "Income Exceeding Rs 10 Crore", font=F_H2, fill=C_TEXT_WHITE)
    d.text((640, 560), "Surcharge Applicable:", font=F_BODY, fill=C_TEXT_MUTED)
    d.rounded_rectangle([1100, 515, 1215, 585], radius=10, fill=C_ACCENT_GOLD if b3_active else (70, 50, 20))
    d.text((1120, 530), "12%", font=F_H2, fill=C_TEXT_DARK if b3_active else C_TEXT_WHITE)

    draw_card(d, 1260, 235, 580, 375, fill=(20, 30, 50), outline=C_CARD_BORDER, width=2)
    d.text((1290, 255), "Computation Sequence (AY 2026-27)", font=F_H2, fill=C_TEXT_WHITE)
    
    steps = [
        ("Step 1", "Compute Base Tax @ 25% or 30%", C_ACCENT_BLUE),
        ("Step 2", "Add Surcharge @ 7% (or 12%)", C_ACCENT_GOLD),
        ("Step 3", "Deduct Marginal Relief (if income > Rs 1 Cr)", C_ACCENT_GREEN),
        ("Step 4", "Add Health & Education Cess @ 4%", C_ACCENT_BLUE)
    ]
    for idx, (st_name, st_desc, col) in enumerate(steps):
        sy = 320 + idx * 65
        d.rounded_rectangle([1290, sy, 1375, sy + 40], radius=6, fill=col)
        d.text((1305, sy + 8), st_name, font=F_BADGE, fill=C_TEXT_DARK if col == C_ACCENT_GOLD else C_TEXT_WHITE)
        d.text((1395, sy + 8), st_desc, font=F_BODY, fill=C_TEXT_WHITE)

    mr_active = (t >= 14.0)
    mr_bg = (35, 30, 15) if mr_active else (20, 28, 45)
    mr_out = C_ACCENT_GOLD if mr_active else C_CARD_BORDER
    draw_card(d, 80, 640, 1760, 380, fill=mr_bg, outline=mr_out, width=4 if mr_active else 2)

    d.rounded_rectangle([120, 670, 520, 715], radius=8, fill=C_ACCENT_GOLD if mr_active else (40, 50, 70), outline=C_ACCENT_GOLD, width=2)
    d.text((140, 680), "SEC 4 · STATUTORY MARGINAL RELIEF", font=F_BADGE, fill=C_TEXT_DARK if mr_active else C_ACCENT_GOLD)

    d.text((120, 735), "Rule of Law: Incremental tax & surcharge cannot exceed incremental income over Rs 1 Crore!",
           font=F_H2, fill=C_TEXT_WHITE if mr_active else C_TEXT_MUTED)

    draw_card(d, 120, 790, 830, 190, fill=(20, 25, 40), outline=C_ACCENT_BLUE, width=2)
    d.text((150, 810), "Maximum Tax Payable (Statutory Ceiling):", font=F_BODY_BOLD, fill=C_ACCENT_BLUE)
    d.text((150, 865), "Tax on Rs 1 Crore  +  (Total Income  -  Rs 1,00,00,000)", font=F_FORMULA, fill=C_TEXT_WHITE)
    d.text((150, 925), "Assessee's total tax + surcharge is capped strictly at this amount", font=F_SMALL, fill=C_TEXT_MUTED)

    draw_card(d, 980, 790, 820, 190, fill=(20, 25, 40), outline=C_ACCENT_GREEN, width=2)
    d.text((1010, 810), "Marginal Relief Quantum (Direct Deduction):", font=F_BODY_BOLD, fill=C_ACCENT_GREEN)
    d.text((1010, 865), "(Tax + Surcharge)  -  [Maximum Tax Payable]", font=F_FORMULA, fill=C_ACCENT_GOLD)
    d.text((1010, 925), "Deducted before applying 4% Health & Education Cess", font=F_SMALL, fill=C_TEXT_MUTED)

    draw_progress(d, t, total_dur)
    return im

def build_q9_video():
    audio_path = os.path.join(AUDIO_DIR, "q9.mp3")
    out_video = os.path.join(VIDEO_DIR, "q9.mp4")
    total_dur = 29.5
    fps = 2
    total_frames = int(total_dur * fps)
    
    tmp_dir = os.path.join(DATA_DIR, "_tmp_q9_frames")
    os.makedirs(tmp_dir, exist_ok=True)
    
    print(f"Generating {total_frames} frames for Q9 flowchart video...")
    for i in range(total_frames):
        t = i / fps
        frame = render_q9_frame(t, total_dur)
        frame.save(os.path.join(tmp_dir, f"frame_{i:04d}.png"))

    print("Encoding video with ffmpeg...")
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-i", os.path.join(tmp_dir, "frame_%04d.png"),
        "-i", audio_path,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        out_video
    ]
    subprocess.run(cmd, check=True)
    shutil.rmtree(tmp_dir, ignore_errors=True)
    print(f"Successfully generated: {out_video} ({os.path.getsize(out_video)} bytes)")

# ----------------- Q1: Diversion vs Application Flowchart Video ----------------- #
def render_q1_frame(t, total_dur):
    im = Image.new("RGB", (WIDTH, HEIGHT))
    d = ImageDraw.Draw(im)
    draw_gradient_background(d)
    draw_header(d, "Diversion of Income by Overriding Title vs. Application of Income",
                "Section 4 · Section 28 · Supreme Court Landmark Tests (Sitaldas Tirathdas)")

    # Top Central Origin Node
    draw_card(d, 660, 240, 600, 100, fill=(30, 45, 75), outline=C_ACCENT_BLUE, width=3)
    d.text((690, 260), "Source of Income / Earning Activity", font=F_H2, fill=C_TEXT_WHITE)
    d.text((690, 300), "Professional Fees, Firm Profits, Business Assets", font=F_SMALL, fill=C_TEXT_MUTED)

    # Branch Left: Diversion by Overriding Title (Active 11.5s - 25s)
    div_active = (t >= 11.5 and t < 25.0) or (t >= 38.0)
    div_bg = (35, 45, 30) if div_active else (22, 32, 48)
    div_out = C_ACCENT_GREEN if div_active else C_CARD_BORDER
    draw_card(d, 80, 420, 840, 400, fill=div_bg, outline=div_out, width=4 if div_active else 2)
    d.rounded_rectangle([110, 445, 460, 485], radius=8, fill=C_ACCENT_GREEN if div_active else (40, 60, 45))
    d.text((125, 453), "DOCTRINE: DIVERSION OF INCOME", font=F_BADGE, fill=C_TEXT_DARK if div_active else C_TEXT_WHITE)
    
    d.text((110, 510), "* Nature: Enforceable pre-existing legal obligation", font=F_BODY, fill=C_TEXT_WHITE)
    d.text((110, 560), "* Point of Transfer: Diverted at source BEFORE reaching assessee", font=F_BODY, fill=C_TEXT_WHITE)
    d.text((110, 610), "* Beneficial Title: Assessee NEVER acquires title or ownership", font=F_BODY, fill=C_TEXT_WHITE)
    
    # Outcome Card Left
    draw_card(d, 110, 675, 780, 115, fill=(15, 35, 25), outline=C_ACCENT_GREEN, width=3)
    d.text((130, 695), "TAX CONSEQUENCE (TOTAL INCOME):", font=F_BODY_BOLD, fill=C_ACCENT_GREEN)
    d.text((130, 735), "EXCLUDED from Total Income · NOT TAXABLE!", font=F_FORMULA, fill=C_ACCENT_GREEN)

    # Branch Right: Application of Income (Active 25s - 38s)
    app_active = (t >= 25.0 and t < 38.0) or (t >= 38.0)
    app_bg = (45, 30, 30) if app_active else (22, 32, 48)
    app_out = C_ACCENT_RED if app_active else C_CARD_BORDER
    draw_card(d, 1000, 420, 840, 400, fill=app_bg, outline=app_out, width=4 if app_active else 2)
    d.rounded_rectangle([1030, 445, 1370, 485], radius=8, fill=C_ACCENT_RED if app_active else (70, 35, 35))
    d.text((1045, 453), "DOCTRINE: APPLICATION OF INCOME", font=F_BADGE, fill=C_TEXT_WHITE)
    
    d.text((1030, 510), "* Nature: Voluntary condition or self-imposed desire", font=F_BODY, fill=C_TEXT_WHITE)
    d.text((1030, 560), "* Point of Transfer: Spent / applied AFTER reaching assessee", font=F_BODY, fill=C_TEXT_WHITE)
    d.text((1030, 610), "* Beneficial Title: Assessee acquires full beneficial title first", font=F_BODY, fill=C_TEXT_WHITE)

    # Outcome Card Right
    draw_card(d, 1030, 675, 780, 115, fill=(35, 15, 20), outline=C_ACCENT_RED, width=3)
    d.text((1050, 695), "TAX CONSEQUENCE (TOTAL INCOME):", font=F_BODY_BOLD, fill=C_ACCENT_RED)
    d.text((1050, 735), "INCLUDED in Total Income · FULLY TAXABLE u/s 28!", font=F_FORMULA, fill=C_ACCENT_RED)

    # Bottom Benchmark Rulings Card
    draw_card(d, 80, 850, 1760, 180, fill=(20, 30, 50), outline=C_ACCENT_GOLD, width=3)
    d.text((110, 875), "Landmark Supreme Court Benchmark (CIT v. Sitaldas Tirathdas):", font=F_H2, fill=C_ACCENT_GOLD)
    d.text((110, 925), "Test: Does money reach assessee as his own income before application? Or does an overriding charge divert it at source?", font=F_BODY, fill=C_TEXT_WHITE)
    d.text((110, 970), "Thakar Das Bhargava: Advocate voluntarily creating charitable trust on fees = Pure Application of Income (Taxable).", font=F_SMALL, fill=C_TEXT_MUTED)

    draw_progress(d, t, total_dur)
    return im

def build_q1_video():
    audio_path = os.path.join(AUDIO_DIR, "q1.mp3")
    out_video = os.path.join(VIDEO_DIR, "q1.mp4")
    total_dur = 48.5
    fps = 2
    total_frames = int(total_dur * fps)
    
    tmp_dir = os.path.join(DATA_DIR, "_tmp_q1_frames")
    os.makedirs(tmp_dir, exist_ok=True)
    
    print(f"Generating {total_frames} frames for Q1 flowchart video...")
    for i in range(total_frames):
        t = i / fps
        frame = render_q1_frame(t, total_dur)
        frame.save(os.path.join(tmp_dir, f"frame_{i:04d}.png"))

    print("Encoding video with ffmpeg...")
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-i", os.path.join(tmp_dir, "frame_%04d.png"),
        "-i", audio_path,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        out_video
    ]
    subprocess.run(cmd, check=True)
    shutil.rmtree(tmp_dir, ignore_errors=True)
    print(f"Successfully generated: {out_video} ({os.path.getsize(out_video)} bytes)")

# ----------------- Q4: Old Tax Regime Slabs ----------------- #
def render_q4_frame(t, total_dur):
    im = Image.new("RGB", (WIDTH, HEIGHT))
    d = ImageDraw.Draw(im)
    draw_gradient_background(d)
    draw_header(d, "Optional (Old) Tax Regime: Age-Based Slabs Flowchart",
                "Section 4 · Section 115BAC(6) · Progressive Slabs for Individuals")

    # 3 Category Columns
    # Col 1: < 60 Years (Active 0s - 11s)
    c1_act = (t < 11.0)
    draw_card(d, 80, 240, 560, 480, fill=(35, 45, 65) if c1_act else C_CARD_BG, outline=C_ACCENT_BLUE if c1_act else C_CARD_BORDER, width=3 if c1_act else 2)
    d.rounded_rectangle([110, 265, 380, 305], radius=6, fill=C_ACCENT_BLUE if c1_act else (50, 70, 100))
    d.text((125, 273), "Resident < 60 Years", font=F_BADGE, fill=C_TEXT_WHITE)
    d.text((110, 330), "Up to Rs 2,50,000  ->  NIL (Basic Exemption)", font=F_BODY_BOLD, fill=C_ACCENT_GREEN if c1_act else C_TEXT_WHITE)
    d.text((110, 390), "Rs 2,50,001 - Rs 5,00,000  ->  5%", font=F_BODY, fill=C_TEXT_WHITE)
    d.text((110, 450), "Rs 5,00,001 - Rs 10,00,000 -> 20%", font=F_BODY, fill=C_TEXT_WHITE)
    d.text((110, 510), "Above Rs 10,00,000         -> 30%", font=F_BODY, fill=C_TEXT_WHITE)
    d.text((110, 580), "Exemption Limit: Rs 2,50,000", font=F_H2, fill=C_ACCENT_GOLD if c1_act else C_TEXT_MUTED)

    # Col 2: Senior Citizen 60 - 80 (Active 11s - 18s)
    c2_act = (t >= 11.0 and t < 18.0)
    draw_card(d, 680, 240, 560, 480, fill=(45, 40, 25) if c2_act else C_CARD_BG, outline=C_ACCENT_GOLD if c2_act else C_CARD_BORDER, width=3 if c2_act else 2)
    d.rounded_rectangle([710, 265, 1010, 305], radius=6, fill=C_ACCENT_GOLD if c2_act else (80, 60, 20))
    d.text((725, 273), "Senior Citizen (60 - < 80)", font=F_BADGE, fill=C_TEXT_DARK if c2_act else C_TEXT_WHITE)
    d.text((710, 330), "Up to Rs 3,00,000  ->  NIL (Enhanced)", font=F_BODY_BOLD, fill=C_ACCENT_GREEN if c2_act else C_TEXT_WHITE)
    d.text((710, 390), "Rs 3,00,001 - Rs 5,00,000  ->  5%", font=F_BODY, fill=C_TEXT_WHITE)
    d.text((710, 450), "Rs 5,00,001 - Rs 10,00,000 -> 20%", font=F_BODY, fill=C_TEXT_WHITE)
    d.text((710, 510), "Above Rs 10,00,000         -> 30%", font=F_BODY, fill=C_TEXT_WHITE)
    d.text((710, 580), "Exemption Limit: Rs 3,00,000", font=F_H2, fill=C_ACCENT_GOLD if c2_act else C_TEXT_MUTED)

    # Col 3: Super Senior 80+ (Active 18s - 26s)
    c3_act = (t >= 18.0 and t < 26.0)
    draw_card(d, 1280, 240, 560, 480, fill=(35, 45, 35) if c3_act else C_CARD_BG, outline=C_ACCENT_GREEN if c3_act else C_CARD_BORDER, width=3 if c3_act else 2)
    d.rounded_rectangle([1310, 265, 1630, 305], radius=6, fill=C_ACCENT_GREEN if c3_act else (30, 60, 40))
    d.text((1325, 273), "Super Senior Citizen (80+)", font=F_BADGE, fill=C_TEXT_DARK if c3_act else C_TEXT_WHITE)
    d.text((1310, 330), "Up to Rs 5,00,000  ->  NIL (Max Exempt)", font=F_BODY_BOLD, fill=C_ACCENT_GREEN)
    d.text((1310, 390), "Rs 2.5L to Rs 5L Bracket   ->  NIL (0%)", font=F_BODY, fill=C_TEXT_MUTED)
    d.text((1310, 450), "Rs 5,00,001 - Rs 10,00,000 -> 20%", font=F_BODY, fill=C_TEXT_WHITE)
    d.text((1310, 510), "Above Rs 10,00,000         -> 30%", font=F_BODY, fill=C_TEXT_WHITE)
    d.text((1310, 580), "Exemption Limit: Rs 5,00,000", font=F_H2, fill=C_ACCENT_GREEN if c3_act else C_TEXT_MUTED)

    # Bottom Statutory Levies Card (Active 26s+)
    levy_act = (t >= 26.0)
    draw_card(d, 80, 750, 1760, 270, fill=(30, 35, 55) if levy_act else C_CARD_BG, outline=C_ACCENT_GOLD if levy_act else C_CARD_BORDER, width=3 if levy_act else 2)
    d.text((110, 775), "Additional Levies & Statutory Reliefs (Mandatory Steps):", font=F_H2, fill=C_ACCENT_GOLD)
    d.text((110, 830), "1. Health & Education Cess: Mandatory 4% added to aggregate income-tax (after surcharge & rebate).", font=F_BODY, fill=C_TEXT_WHITE)
    d.text((110, 875), "2. Section 87A Rebate: Up to Rs 12,500 available for resident individuals having Total Income <= Rs 5,00,000.", font=F_BODY, fill=C_TEXT_WHITE)
    d.text((110, 920), "3. Surcharge: Applicable only if Total Income exceeds Rs 50 Lakhs (10%, 15%, 25%, 37%).", font=F_BODY, fill=C_TEXT_MUTED)

    draw_progress(d, t, total_dur)
    return im

def build_q4_video():
    audio_path = os.path.join(AUDIO_DIR, "q4.mp3")
    out_video = os.path.join(VIDEO_DIR, "q4.mp4")
    total_dur = 35.5
    fps = 2
    total_frames = int(total_dur * fps)
    tmp_dir = os.path.join(DATA_DIR, "_tmp_q4_frames")
    os.makedirs(tmp_dir, exist_ok=True)
    for i in range(total_frames):
        render_q4_frame(i / fps, total_dur).save(os.path.join(tmp_dir, f"frame_{i:04d}.png"))
    subprocess.run(["ffmpeg", "-y", "-framerate", str(fps), "-i", os.path.join(tmp_dir, "frame_%04d.png"),
                    "-i", audio_path, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", out_video], check=True)
    shutil.rmtree(tmp_dir, ignore_errors=True)
    print(f"Generated: {out_video}")

# ----------------- Q5: Section 87A Rebate ----------------- #
def render_q5_frame(t, total_dur):
    im = Image.new("RGB", (WIDTH, HEIGHT))
    d = ImageDraw.Draw(im)
    draw_gradient_background(d)
    draw_header(d, "Rebate under Section 87A Flowchart (Normal Provisions)",
                "Section 87A · Relief for Resident Individuals having Income <= Rs 5,00,000")

    # Step 1: Eligibility check
    draw_card(d, 80, 240, 520, 240, fill=(25, 40, 60), outline=C_ACCENT_BLUE, width=3)
    d.text((110, 265), "Step 1: Assessee Status Check", font=F_H2, fill=C_ACCENT_BLUE)
    d.text((110, 320), "Assessee must be a Resident Individual.", font=F_BODY, fill=C_TEXT_WHITE)
    d.text((110, 365), "HUF, BOI, AOP, Firms & Companies are", font=F_BODY, fill=C_TEXT_MUTED)
    d.text((110, 405), "NOT eligible for Section 87A rebate.", font=F_BODY_BOLD, fill=C_ACCENT_RED)

    draw_arrow_right(d, 600, 680, 360, color=C_ACCENT_BLUE, text="Eligible")

    # Step 2: Income threshold
    draw_card(d, 680, 240, 560, 240, fill=(25, 45, 40) if t >= 15.0 else C_CARD_BG, outline=C_ACCENT_GREEN if t >= 15.0 else C_CARD_BORDER, width=3)
    d.text((710, 265), "Step 2: Total Income Threshold", font=F_H2, fill=C_ACCENT_GREEN)
    d.text((710, 320), "Total Income (after Ch VI-A deductions):", font=F_BODY, fill=C_TEXT_WHITE)
    d.rounded_rectangle([710, 365, 1100, 425], radius=10, fill=C_ACCENT_GREEN if t >= 15.0 else (30, 60, 50))
    d.text((735, 378), "Total Income <= Rs 5,00,000", font=F_H2, fill=C_TEXT_DARK if t >= 15.0 else C_TEXT_WHITE)

    draw_arrow_right(d, 1240, 1320, 360, color=C_ACCENT_GREEN, text="Threshold Met")

    # Step 3: Rebate Quantum Box
    draw_card(d, 1320, 240, 520, 240, fill=(45, 35, 20) if t >= 20.0 else C_CARD_BG, outline=C_ACCENT_GOLD if t >= 20.0 else C_CARD_BORDER, width=3)
    d.text((1350, 265), "Step 3: Maximum Rebate", font=F_H2, fill=C_ACCENT_GOLD)
    d.text((1350, 320), "Statutory Rebate Ceiling:", font=F_BODY, fill=C_TEXT_WHITE)
    d.text((1350, 365), "Rs 12,500 (100% Tax Payable)", font=F_FORMULA, fill=C_ACCENT_GOLD)
    d.text((1350, 415), "Lower of: Tax on Income or Rs 12,500", font=F_SMALL, fill=C_TEXT_MUTED)

    # Bottom Hero Card: Result & Zero Tax
    draw_card(d, 80, 520, 1760, 500, fill=(20, 30, 48), outline=C_ACCENT_GOLD, width=3)
    d.text((110, 550), "Statutory Example & Net Tax Liability:", font=F_H2, fill=C_ACCENT_GOLD)
    
    d.text((110, 610), "On Total Income of Rs 5,00,000:", font=F_BODY_BOLD, fill=C_TEXT_WHITE)
    d.text((110, 660), "* Up to Rs 2,50,000: Tax = NIL", font=F_BODY, fill=C_TEXT_WHITE)
    d.text((110, 710), "* Rs 2,50,001 to Rs 5,00,000 @ 5%: Tax = Rs 12,500", font=F_BODY, fill=C_TEXT_WHITE)
    d.text((110, 760), "* Less: Rebate u/s 87A (Lower of Rs 12,500 or Tax): (-) Rs 12,500", font=F_BODY_BOLD, fill=C_ACCENT_GREEN)
    
    draw_card(d, 110, 830, 1700, 140, fill=(15, 35, 25), outline=C_ACCENT_GREEN, width=3)
    d.text((140, 850), "FINAL NET TAX PAYABLE (BEFORE CESS):", font=F_BODY_BOLD, fill=C_ACCENT_GREEN)
    d.text((140, 895), "Rs 0 (NIL TAX) · Zero tax for any resident earning up to Rs 5 Lakhs!", font=F_FORMULA, fill=C_ACCENT_GREEN)

    draw_progress(d, t, total_dur)
    return im

def build_q5_video():
    audio_path = os.path.join(AUDIO_DIR, "q5.mp3")
    out_video = os.path.join(VIDEO_DIR, "q5.mp4")
    total_dur = 33.0
    fps = 2
    total_frames = int(total_dur * fps)
    tmp_dir = os.path.join(DATA_DIR, "_tmp_q5_frames")
    os.makedirs(tmp_dir, exist_ok=True)
    for i in range(total_frames):
        render_q5_frame(i / fps, total_dur).save(os.path.join(tmp_dir, f"frame_{i:04d}.png"))
    subprocess.run(["ffmpeg", "-y", "-framerate", str(fps), "-i", os.path.join(tmp_dir, "frame_%04d.png"),
                    "-i", audio_path, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", out_video], check=True)
    shutil.rmtree(tmp_dir, ignore_errors=True)
    print(f"Generated: {out_video}")

# ----------------- Q6: Section 115BAC Slabs ----------------- #
def render_q6_frame(t, total_dur):
    im = Image.new("RGB", (WIDTH, HEIGHT))
    d = ImageDraw.Draw(im)
    draw_gradient_background(d)
    draw_header(d, "Default Concessional Tax Regime: Section 115BAC(1A)",
                "Applicable for Individuals, HUF, AOP, BOI & AJP · AY 2025-26 & AY 2026-27")

    # Step slabs table rendered as a modern progression card
    draw_card(d, 80, 240, 1140, 520, fill=(20, 30, 50), outline=C_ACCENT_BLUE, width=3)
    d.text((110, 265), "Section 115BAC(1A) Progressive Slabs", font=F_H2, fill=C_ACCENT_BLUE)

    slabs = [
        ("Up to Rs 4,00,000", "NIL", C_ACCENT_GREEN, t >= 4.5),
        ("Rs 4,00,001 - Rs 8,00,000", "5%", C_ACCENT_GOLD, t >= 11.0),
        ("Rs 8,00,001 - Rs 12,00,000", "10%", C_ACCENT_GOLD, t >= 14.0),
        ("Rs 12,00,001 - Rs 16,00,000", "15%", C_ACCENT_GOLD, t >= 17.0),
        ("Rs 16,00,001 - Rs 20,00,000", "20%", C_ACCENT_GOLD, t >= 20.0),
        ("Rs 20,00,001 - Rs 24,00,000", "25%", C_ACCENT_GOLD, t >= 23.0),
        ("Above Rs 24,00,000", "30%", C_ACCENT_RED, t >= 26.0)
    ]
    for i, (slab_range, rate, col, act) in enumerate(slabs):
        sy = 325 + i * 55
        bg_col = (45, 50, 70) if act else (25, 35, 55)
        d.rounded_rectangle([110, sy, 1090, sy + 45], radius=8, fill=bg_col, outline=col if act else C_CARD_BORDER, width=2 if act else 1)
        d.text((130, sy + 10), slab_range, font=F_BODY_BOLD, fill=C_TEXT_WHITE)
        d.text((950, sy + 10), rate, font=F_H2, fill=col if act else C_TEXT_MUTED)

    # Right Hero Panel: Critical Statutory Notes
    draw_card(d, 1260, 240, 580, 520, fill=(35, 40, 25) if t >= 28.0 else C_CARD_BG, outline=C_ACCENT_GOLD if t >= 28.0 else C_CARD_BORDER, width=3)
    d.text((1290, 265), "Key Statutory Provisions", font=F_H2, fill=C_ACCENT_GOLD)
    
    d.text((1290, 330), "1. Uniform Exemption Limit:", font=F_BODY_BOLD, fill=C_TEXT_WHITE)
    d.text((1290, 370), "Rs 4,00,000 applies universally across all age categories.", font=F_BODY, fill=C_TEXT_MUTED)
    d.text((1290, 410), "NO enhanced limit for Senior or Super Senior citizens!", font=F_BODY_BOLD, fill=C_ACCENT_RED)
    
    d.text((1290, 480), "2. Health & Education Cess:", font=F_BODY_BOLD, fill=C_TEXT_WHITE)
    d.text((1290, 520), "Mandatory 4% on aggregate income-tax.", font=F_BODY, fill=C_TEXT_MUTED)

    d.text((1290, 590), "3. Default Regime Applicability:", font=F_BODY_BOLD, fill=C_TEXT_WHITE)
    d.text((1290, 630), "Assessee must formally opt out u/s 115BAC(6)", font=F_BODY, fill=C_TEXT_MUTED)
    d.text((1290, 670), "to be taxed under optional normal regime.", font=F_BODY, fill=C_TEXT_MUTED)

    # Bottom Banner
    draw_card(d, 80, 800, 1760, 220, fill=(20, 25, 40), outline=C_ACCENT_GREEN, width=3)
    d.text((110, 830), "Statutory Comparison (Old Regime vs. Section 115BAC):", font=F_H2, fill=C_ACCENT_GREEN)
    d.text((110, 885), "* Old Regime: Basic Exemption Rs 2.5L / 3L / 5L depending on age + Deductions allowed.", font=F_BODY, fill=C_TEXT_WHITE)
    d.text((110, 935), "* Default Regime: Basic Exemption Rs 4L for ALL + Lower slab rates + Most deductions forgone.", font=F_BODY, fill=C_TEXT_WHITE)

    draw_progress(d, t, total_dur)
    return im

def build_q6_video():
    audio_path = os.path.join(AUDIO_DIR, "q6.mp3")
    out_video = os.path.join(VIDEO_DIR, "q6.mp4")
    total_dur = 36.0
    fps = 2
    total_frames = int(total_dur * fps)
    tmp_dir = os.path.join(DATA_DIR, "_tmp_q6_frames")
    os.makedirs(tmp_dir, exist_ok=True)
    for i in range(total_frames):
        render_q6_frame(i / fps, total_dur).save(os.path.join(tmp_dir, f"frame_{i:04d}.png"))
    subprocess.run(["ffmpeg", "-y", "-framerate", str(fps), "-i", os.path.join(tmp_dir, "frame_%04d.png"),
                    "-i", audio_path, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", out_video], check=True)
    shutil.rmtree(tmp_dir, ignore_errors=True)
    print(f"Generated: {out_video}")

# ----------------- Q7: Section 87A under Section 115BAC ----------------- #
def render_q7_frame(t, total_dur):
    im = Image.new("RGB", (WIDTH, HEIGHT))
    d = ImageDraw.Draw(im)
    draw_gradient_background(d)
    draw_header(d, "Enhanced Section 87A Rebate under Default Tax Regime",
                "Section 115BAC · Full Tax Exemption up to Rs 12 Lakhs Total Income")

    # Left: Threshold Node
    draw_card(d, 80, 240, 840, 480, fill=(25, 45, 40) if t >= 3.5 else C_CARD_BG, outline=C_ACCENT_GREEN if t >= 3.5 else C_CARD_BORDER, width=3)
    d.text((110, 265), "Eligibility & Threshold Check (Section 115BAC)", font=F_H2, fill=C_ACCENT_GREEN)
    d.text((110, 330), "Resident Individual Total Income Threshold:", font=F_BODY, fill=C_TEXT_WHITE)
    
    draw_card(d, 110, 380, 780, 140, fill=(15, 35, 25), outline=C_ACCENT_GREEN, width=3)
    d.text((140, 405), "TOTAL INCOME THRESHOLD:", font=F_BODY_BOLD, fill=C_ACCENT_GREEN)
    d.text((140, 450), "Total Income <= Rs 12,00,000", font=F_FORMULA, fill=C_TEXT_WHITE)

    d.text((110, 550), "* Rebate Quantum: Lower of Tax Payable or Rs 60,000", font=F_BODY_BOLD, fill=C_ACCENT_GOLD)
    d.text((110, 600), "* On Rs 12,00,000 income, slab tax is exactly Rs 60,000.", font=F_BODY, fill=C_TEXT_MUTED)
    d.text((110, 645), "* Entire Rs 60,000 is absorbed by Section 87A rebate!", font=F_BODY_BOLD, fill=C_ACCENT_GREEN)

    # Right: Outcome Card
    draw_card(d, 960, 240, 880, 480, fill=(35, 30, 20) if t >= 8.0 else C_CARD_BG, outline=C_ACCENT_GOLD if t >= 8.0 else C_CARD_BORDER, width=3)
    d.text((990, 265), "Statutory Tax Payable (AY 2026-27)", font=F_H2, fill=C_ACCENT_GOLD)
    
    steps = [
        ("Income Up to Rs 4 Lakhs", "Nil (0%)"),
        ("Rs 4L to Rs 8L @ 5%", "Rs 20,000"),
        ("Rs 8L to Rs 12L @ 10%", "Rs 40,000"),
        ("Aggregate Tax Payable", "Rs 60,000"),
        ("Less: Rebate u/s 87A", "(-) Rs 60,000"),
        ("Net Tax Liability", "Rs 0 (NIL!)")
    ]
    for idx, (label, val) in enumerate(steps):
        sy = 330 + idx * 55
        is_tot = (idx == 5)
        d.rounded_rectangle([990, sy, 1800, sy + 45], radius=6, fill=(20, 50, 30) if is_tot else (30, 40, 60))
        d.text((1010, sy + 10), label, font=F_BODY_BOLD if is_tot else F_BODY, fill=C_ACCENT_GREEN if is_tot else C_TEXT_WHITE)
        d.text((1650, sy + 10), val, font=F_BODY_BOLD if is_tot else F_BODY, fill=C_ACCENT_GREEN if is_tot else C_ACCENT_GOLD)

    # Bottom Summary
    draw_card(d, 80, 760, 1760, 260, fill=(20, 25, 45), outline=C_ACCENT_BLUE, width=3)
    d.text((110, 790), "Conclusion for Students:", font=F_H2, fill=C_ACCENT_BLUE)
    d.text((110, 845), "Under the default regime, any resident earning up to Rs 12,00,000 has ZERO tax liability.", font=F_BODY_BOLD, fill=C_TEXT_WHITE)
    d.text((110, 895), "Tax liability starts only when Total Income crosses Rs 12,00,000.", font=F_BODY, fill=C_TEXT_MUTED)
    d.text((110, 940), "If income crosses Rs 12,00,000 marginally, Marginal Relief applies to protect the taxpayer.", font=F_BODY, fill=C_ACCENT_GOLD)

    draw_progress(d, t, total_dur)
    return im

def build_q7_video():
    audio_path = os.path.join(AUDIO_DIR, "q7.mp3")
    out_video = os.path.join(VIDEO_DIR, "q7.mp4")
    total_dur = 24.5
    fps = 2
    total_frames = int(total_dur * fps)
    tmp_dir = os.path.join(DATA_DIR, "_tmp_q7_frames")
    os.makedirs(tmp_dir, exist_ok=True)
    for i in range(total_frames):
        render_q7_frame(i / fps, total_dur).save(os.path.join(tmp_dir, f"frame_{i:04d}.png"))
    subprocess.run(["ffmpeg", "-y", "-framerate", str(fps), "-i", os.path.join(tmp_dir, "frame_%04d.png"),
                    "-i", audio_path, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", out_video], check=True)
    shutil.rmtree(tmp_dir, ignore_errors=True)
    print(f"Generated: {out_video}")

# ----------------- Q8: Marginal Relief u/s 87A ----------------- #
def render_q8_frame(t, total_dur):
    im = Image.new("RGB", (WIDTH, HEIGHT))
    d = ImageDraw.Draw(im)
    draw_gradient_background(d)
    draw_header(d, "Marginal Relief under Section 87A in Default Tax Regime",
                "Section 87A Proviso · Protection when Income Marginally Exceeds Rs 12 Lakhs")

    draw_card(d, 80, 240, 1760, 440, fill=(30, 25, 45) if t >= 10.0 else C_CARD_BG, outline=C_ACCENT_GOLD if t >= 10.0 else C_CARD_BORDER, width=3)
    d.text((110, 265), "The Problem & The Statutory Protection", font=F_H2, fill=C_ACCENT_GOLD)
    d.text((110, 325), "If a taxpayer earns Rs 12,05,000 (just Rs 5,000 above the threshold),", font=F_BODY, fill=C_TEXT_WHITE)
    d.text((110, 365), "without marginal relief, the entire rebate of Rs 60,000 would be lost and tax would be Rs 60,750!", font=F_BODY_BOLD, fill=C_ACCENT_RED)
    d.text((110, 415), "That means Rs 5,000 extra income causes Rs 60,750 extra tax! This absurdity is cured by Marginal Relief.", font=F_BODY, fill=C_TEXT_WHITE)

    # Formula Card
    draw_card(d, 110, 480, 1700, 170, fill=(20, 35, 30), outline=C_ACCENT_GREEN, width=3)
    d.text((140, 500), "STATUTORY MARGINAL RELIEF FORMULA (Section 87A Proviso):", font=F_BODY_BOLD, fill=C_ACCENT_GREEN)
    d.text((140, 550), "Rebate u/s 87A = Tax on Total Income  -  (Total Income  -  Rs 12,00,000)", font=F_FORMULA, fill=C_TEXT_WHITE)
    d.text((140, 605), "Final Tax Payable is restricted strictly to: (Income exceeding Rs 12,00,000) + 4% Cess", font=F_BODY_BOLD, fill=C_ACCENT_GOLD)

    # Bottom Numerical Example
    draw_card(d, 80, 710, 1760, 310, fill=(20, 25, 45), outline=C_ACCENT_BLUE, width=3)
    d.text((110, 735), "Working Example (Income = Rs 12,10,000):", font=F_H2, fill=C_ACCENT_BLUE)
    d.text((110, 790), "1. Slab Tax on Rs 12,10,000 = Rs 61,500", font=F_BODY, fill=C_TEXT_WHITE)
    d.text((110, 835), "2. Excess income over Rs 12 Lakhs = Rs 10,000", font=F_BODY, fill=C_TEXT_WHITE)
    d.text((110, 880), "3. Marginal Relief = Rs 61,500 - Rs 10,000 = Rs 51,500", font=F_BODY_BOLD, fill=C_ACCENT_GOLD)
    d.text((110, 925), "4. Net Tax = Rs 10,000 + 4% Cess (Rs 400) = Rs 10,400 (Tax cannot exceed extra income!)", font=F_BODY_BOLD, fill=C_ACCENT_GREEN)

    draw_progress(d, t, total_dur)
    return im

def build_q8_video():
    audio_path = os.path.join(AUDIO_DIR, "q8.mp3")
    out_video = os.path.join(VIDEO_DIR, "q8.mp4")
    total_dur = 27.5
    fps = 2
    total_frames = int(total_dur * fps)
    tmp_dir = os.path.join(DATA_DIR, "_tmp_q8_frames")
    os.makedirs(tmp_dir, exist_ok=True)
    for i in range(total_frames):
        render_q8_frame(i / fps, total_dur).save(os.path.join(tmp_dir, f"frame_{i:04d}.png"))
    subprocess.run(["ffmpeg", "-y", "-framerate", str(fps), "-i", os.path.join(tmp_dir, "frame_%04d.png"),
                    "-i", audio_path, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", out_video], check=True)
    shutil.rmtree(tmp_dir, ignore_errors=True)
    print(f"Generated: {out_video}")

def build_all():
    print("Building all 7 statutory flowchart videos...")
    build_q9_video()
    build_q1_video()
    build_q4_video()
    build_q5_video()
    build_q6_video()
    build_q7_video()
    build_q8_video()
    print("ALL VIDEOS BUILT SUCCESSFULLY!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1].lower()
        if target in globals() and callable(globals()[target]):
            globals()[target]()
    else:
        build_all()
