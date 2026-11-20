from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]

# Exact colors from the first HTML slide deck
DARK_BG = RGBColor(15, 23, 42)       # #0f172a
LIGHT_BG = RGBColor(248, 250, 252)   # #f8fafc
WHITE = RGBColor(255, 255, 255)
BORDER_GRAY = RGBColor(226, 232, 240)# #e2e8f0
DIVIDER_GRAY = RGBColor(203, 213, 225)# #cbd5e1
BLUE = RGBColor(2, 132, 199)         # #0284c7
ROSE = RGBColor(225, 29, 72)         # #e11d48
TEXT_DARK = RGBColor(15, 23, 42)     # #0f172a
TEXT_BODY = RGBColor(71, 85, 105)    # #475569
TEXT_MUTED = RGBColor(148, 163, 184) # #94a3b8
TEXT_LIST = RGBColor(51, 65, 85)     # #334155

FONT_NAME = "Arial"

def set_bg(slide, color):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_text(slide, left, top, width, height, text, size, color, bold=False, align=PP_ALIGN.LEFT):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = align
    p.text = text
    p.font.name = FONT_NAME
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    return tf

def add_rect(slide, left, top, width, height, fill_color, border_color=None, rounded=False):
    shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE
    sh = slide.shapes.add_shape(shape_type, left, top, width, height)
    if rounded:
        sh.adjustments[0] = 0.05
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill_color
    if border_color:
        sh.line.color.rgb = border_color
        sh.line.width = Pt(1)
    else:
        sh.line.fill.background()
    return sh

# Slide 1: Title Slide
s1 = prs.slides.add_slide(blank)
set_bg(s1, DARK_BG)
add_text(s1, Inches(0.85), Inches(1.85), Inches(9.5), Inches(0.35),
         "CYBER SECURITY PROJECT PRESENTATION", 12, BLUE, bold=True)
add_text(s1, Inches(0.85), Inches(2.3), Inches(9.5), Inches(1.8),
         "NetSentinel: Real-Time Network Traffic Analyzer", 46, LIGHT_BG, bold=True)
add_text(s1, Inches(0.85), Inches(4.25), Inches(8.5), Inches(0.6),
         "Live Packet Inspection, Protocol Telemetry & Anomaly Alerting", 18, TEXT_MUTED)
add_rect(s1, Inches(0.85), Inches(5.05), Inches(0.75), Inches(0.05), ROSE)

# Slide 2: Core Objectives & Tech Stack
s2 = prs.slides.add_slide(blank)
set_bg(s2, LIGHT_BG)
add_text(s2, Inches(0.75), Inches(0.6), Inches(6), Inches(0.3), "PROJECT SCOPE", 11, BLUE, bold=True)
add_text(s2, Inches(0.75), Inches(0.92), Inches(10), Inches(0.6), "Core Objectives & Tech Stack", 28, TEXT_DARK, bold=True)

cards_s2 = [
    ("Live Packet Capture", "Zero-storage Scapy sniffing across interfaces.", BLUE),
    ("Anomaly Detection", "Real-time ARP spoofing and SYN alerts.", ROSE),
    ("Flask & Chart.js UI", "1.5-second live JSON dashboard polling.", BLUE)
]
for i, (heading, desc, accent) in enumerate(cards_s2):
    left = Inches(0.75 + i * 4.05)
    top = Inches(2.55)
    add_rect(s2, left, top, Inches(3.75), Inches(2.5), WHITE, border_color=BORDER_GRAY, rounded=True)
    add_rect(s2, left + Inches(0.32), top + Inches(0.38), Inches(0.35), Inches(0.08), accent)
    add_text(s2, left + Inches(0.32), top + Inches(0.65), Inches(3.1), Inches(0.45), heading, 18, TEXT_DARK, bold=True)
    add_text(s2, left + Inches(0.32), top + Inches(1.15), Inches(3.1), Inches(0.9), desc, 14.5, TEXT_BODY)

# Slide 3: Packet-to-Dashboard Data Flow
s3 = prs.slides.add_slide(blank)
set_bg(s3, LIGHT_BG)
add_text(s3, Inches(0.75), Inches(0.6), Inches(6), Inches(0.3), "SYSTEM ARCHITECTURE", 11, BLUE, bold=True)
add_text(s3, Inches(0.75), Inches(0.92), Inches(10), Inches(0.6), "Packet-to-Dashboard Data Flow", 28, TEXT_DARK, bold=True)

steps_s3 = [
    ("1", "NIC Capture", "Sniffs lo and active interface threads.", BLUE),
    ("2", "Layer Decoding", "Parses ARP, IP, TCP, UDP, DNS.", BLUE),
    ("3", "Threat Heuristics", "Flags MAC shifts and SYN bursts.", ROSE),
    ("4", "Flask Telemetry", "Thread-safe JSON served via /api/stats.", BLUE)
]
for i, (num, title, desc, color) in enumerate(steps_s3):
    left = Inches(0.75 + i * 3.05)
    top = Inches(2.85)
    circle = s3.shapes.add_shape(MSO_SHAPE.OVAL, left, top, Inches(0.55), Inches(0.55))
    circle.fill.solid()
    circle.fill.fore_color.rgb = color
    circle.line.fill.background()
    cp = circle.text_frame.paragraphs[0]
    cp.alignment = PP_ALIGN.CENTER
    cp.text = num
    cp.font.name = FONT_NAME
    cp.font.size = Pt(16)
    cp.font.bold = True
    cp.font.color.rgb = WHITE

    if i < 3:
        add_rect(s3, left + Inches(0.75), top + Inches(0.26), Inches(2.05), Inches(0.03), DIVIDER_GRAY)

    add_text(s3, left, top + Inches(0.8), Inches(2.7), Inches(0.4), title, 16.5, TEXT_DARK, bold=True)
    add_text(s3, left, top + Inches(1.25), Inches(2.7), Inches(0.9), desc, 14.5, TEXT_BODY)

# Slide 4: Built-In Threat Detection Rules
s4 = prs.slides.add_slide(blank)
set_bg(s4, LIGHT_BG)
add_text(s4, Inches(0.75), Inches(0.6), Inches(6), Inches(0.3), "INTRUSION LOGIC", 11, ROSE, bold=True)
add_text(s4, Inches(0.75), Inches(0.92), Inches(10), Inches(0.6), "Built-In Threat Detection Rules", 28, TEXT_DARK, bold=True)

add_text(s4, Inches(0.75), Inches(2.35), Inches(5.3), Inches(0.35), "HIGH SEVERITY", 12, ROSE, bold=True)
add_text(s4, Inches(0.75), Inches(2.7), Inches(5.3), Inches(0.5), "ARP Spoofing Detection", 22, TEXT_DARK, bold=True)
arp_bullets = [
    ("Inspects Replies: ", "Monitors ARP is-at packets (op == 2)."),
    ("MAC Tracking: ", "Maps source IP to hardware MAC."),
    ("Instant Alert: ", "Triggers when existing IP changes MAC.")
]
for j, (b_head, b_text) in enumerate(arp_bullets):
    tb = s4.shapes.add_textbox(Inches(0.75), Inches(3.45 + j * 0.65), Inches(5.4), Inches(0.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r1 = p.add_run()
    r1.text = b_head
    r1.font.name = FONT_NAME
    r1.font.size = Pt(15)
    r1.font.bold = True
    r1.font.color.rgb = TEXT_LIST
    r2 = p.add_run()
    r2.text = b_text
    r2.font.name = FONT_NAME
    r2.font.size = Pt(15)
    r2.font.color.rgb = TEXT_LIST

add_rect(s4, Inches(6.65), Inches(2.35), Inches(0.025), Inches(3.2), DIVIDER_GRAY)

add_text(s4, Inches(7.15), Inches(2.35), Inches(5.3), Inches(0.35), "MEDIUM SEVERITY", 12, BLUE, bold=True)
add_text(s4, Inches(7.15), Inches(2.7), Inches(5.3), Inches(0.5), "TCP SYN Port Scan Detection", 22, TEXT_DARK, bold=True)
syn_bullets = [
    ("SYN Filtering: ", "Tracks TCP packets with SYN flag."),
    ("Rolling Window: ", "Counts unique ports over 10 seconds."),
    ("Threshold Alert: ", "Flags sources probing >15 ports.")
]
for j, (b_head, b_text) in enumerate(syn_bullets):
    tb = s4.shapes.add_textbox(Inches(7.15), Inches(3.45 + j * 0.65), Inches(5.4), Inches(0.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r1 = p.add_run()
    r1.text = b_head
    r1.font.name = FONT_NAME
    r1.font.size = Pt(15)
    r1.font.bold = True
    r1.font.color.rgb = TEXT_LIST
    r2 = p.add_run()
    r2.text = b_text
    r2.font.name = FONT_NAME
    r2.font.size = Pt(15)
    r2.font.color.rgb = TEXT_LIST

# Slide 5: Ubuntu Test Results & Limitations
s5 = prs.slides.add_slide(blank)
set_bg(s5, LIGHT_BG)
add_text(s5, Inches(0.75), Inches(0.6), Inches(6), Inches(0.3), "LIVE BENCHMARK & EVALUATION", 11, BLUE, bold=True)
add_text(s5, Inches(0.75), Inches(0.92), Inches(10), Inches(0.6), "Ubuntu Test Results & Limitations", 28, TEXT_DARK, bold=True)

metrics = [
    ("1.04M+", "Packets captured live", BLUE),
    ("255 pps", "Sustained throughput rate", TEXT_DARK),
    ("14 Alerts", "Anomalies logged on LAN", ROSE)
]
for i, (val, label, col) in enumerate(metrics):
    left = Inches(0.75 + i * 4.05)
    add_text(s5, left, Inches(2.45), Inches(3.7), Inches(0.85), val, 42, col, bold=True)
    add_text(s5, left, Inches(3.35), Inches(3.7), Inches(0.45), label, 15, TEXT_BODY)

add_rect(s5, Inches(0.75), Inches(4.25), Inches(11.8), Inches(0.02), DIVIDER_GRAY)

lims = [
    ("Volatile Memory: ", "Stats reset upon server restart."),
    ("Root Coupling: ", "Sniffer and Flask share sudo privileges."),
    ("LAN Noise: ", "Dynamic DHCP MAC shifts trigger ARP alerts.")
]
for i, (l_head, l_text) in enumerate(lims):
    left = Inches(0.75 + i * 4.05)
    tb = s5.shapes.add_textbox(left, Inches(4.65), Inches(3.75), Inches(1.1))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r1 = p.add_run()
    r1.text = l_head
    r1.font.name = FONT_NAME
    r1.font.size = Pt(14.5)
    r1.font.bold = True
    r1.font.color.rgb = TEXT_LIST
    r2 = p.add_run()
    r2.text = l_text
    r2.font.name = FONT_NAME
    r2.font.size = Pt(14.5)
    r2.font.color.rgb = TEXT_LIST

# Slide 6: Use Cases & Conclusion
s6 = prs.slides.add_slide(blank)
set_bg(s6, DARK_BG)
add_text(s6, Inches(1.5), Inches(2.0), Inches(10.333), Inches(0.35),
         "USE CASES & CONCLUSION", 12, BLUE, bold=True, align=PP_ALIGN.CENTER)
add_text(s6, Inches(1.8), Inches(2.5), Inches(9.733), Inches(1.3),
         "Real-Time Visibility for Labs & Local Networks", 38, LIGHT_BG, bold=True, align=PP_ALIGN.CENTER)
add_text(s6, Inches(2.5), Inches(4.0), Inches(8.333), Inches(0.9),
         "Ideal for security demos, bandwidth diagnostics, and baseline intrusion alerting—ready for SQLite persistence and rule tuning.",
         16.5, TEXT_MUTED, align=PP_ALIGN.CENTER)
add_rect(s6, Inches(6.29), Inches(5.2), Inches(0.75), Inches(0.05), ROSE)

prs.save("NetSentinel_First_Deck.pptx")
print("Generated NetSentinel_First_Deck.pptx successfully!")
