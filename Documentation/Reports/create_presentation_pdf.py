import os
import sys
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT

class LandscapeBackgroundCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(LandscapeBackgroundCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_slide_background()
            super(LandscapeBackgroundCanvas, self).showPage()
        super(LandscapeBackgroundCanvas, self).save()

    def draw_slide_background(self):
        # Draw dark charcoal background
        self.saveState()
        self.setFillColor(colors.HexColor("#0E1014"))
        self.rect(0, 0, 13.333 * inch, 7.5 * inch, fill=1, stroke=0)

        # Draw slide number in footer
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#8C9BAC"))
        self.drawRightString(13.333 * inch - 36, 18, f"Slide {self._pageNumber} of 12  |  Zombie Runner Academic Presentation")
        self.drawString(36, 18, "SR University  *  School of Computer Science & Artificial Intelligence  *  23CS201PE407")
        self.restoreState()

def create_presentation_pdf(out_pdf_path):
    doc = SimpleDocTemplate(
        out_pdf_path,
        pagesize=(13.333 * inch, 7.5 * inch),
        leftMargin=36,
        rightMargin=36,
        topMargin=28,
        bottomMargin=28
    )

    PRIMARY_RED = colors.HexColor("#B91E26")
    CRIMSON = colors.HexColor("#E12D37")
    TEXT_LIGHT = colors.HexColor("#F5F7FA")
    TEXT_MUTED = colors.HexColor("#A5B2C0")
    CYAN = colors.HexColor("#38BDF8")
    CARD_BG = colors.HexColor("#161A21")
    BORDER_COLOR = colors.HexColor("#262D3A")

    # Typography Styles
    style_tag = ParagraphStyle('SlideTag', fontName='Helvetica-Bold', fontSize=8.5, leading=10, textColor=CRIMSON, spaceAfter=2)
    style_title = ParagraphStyle('SlideTitle', fontName='Helvetica-Bold', fontSize=17, leading=20, textColor=TEXT_LIGHT, spaceAfter=4)
    style_card_title = ParagraphStyle('CardTitle', fontName='Helvetica-Bold', fontSize=10.5, leading=13, textColor=CRIMSON, spaceAfter=2)
    style_card_title_cyan = ParagraphStyle('CardTitleCyan', fontName='Helvetica-Bold', fontSize=10.5, leading=13, textColor=CYAN, spaceAfter=2)
    style_body = ParagraphStyle('SlideBody', fontName='Helvetica', fontSize=7.6, leading=9.8, textColor=TEXT_MUTED)
    style_body_light = ParagraphStyle('SlideBodyLight', fontName='Helvetica', fontSize=7.6, leading=9.8, textColor=TEXT_LIGHT)
    style_caption = ParagraphStyle('SlideCap', fontName='Helvetica-Oblique', fontSize=7.0, leading=8.5, textColor=TEXT_MUTED, alignment=TA_CENTER)

    screenshots_dir = os.path.abspath(r"E:\zombie runner\PresentationScreenshots")
    logo_path = r"C:\Users\metra\.gemini\antigravity\brain\7ea1a950-c3d7-465b-a4d2-a25115ebddc3\.user_uploaded\media_1793877402347_b6c68b90.png"

    story = []

    def make_header_table(tag, title):
        h_data = [
            [Paragraph(tag.upper(), style_tag)],
            [Paragraph(title, style_title)]
        ]
        t = Table(h_data, colWidths=[888])
        t.setStyle(TableStyle([
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('LINEBELOW', (0,1), (-1,1), 0.8, BORDER_COLOR),
        ]))
        return t

    # ==========================================
    # SLIDE 1 — TITLE SLIDE
    # ==========================================
    s1_left = [
        Paragraph("SR UNIVERSITY | DEPARTMENT REVIEW", style_tag),
        Paragraph("School of Computer Science & Artificial Intelligence", style_body),
        Spacer(1, 8),
        Paragraph("<b>ZOMBIE RUNNER</b>", ParagraphStyle('S1Title', fontName='Helvetica-Bold', fontSize=26, leading=29, textColor=TEXT_LIGHT)),
        Paragraph("<i>A 3D Survival Horror Endless Runner Game</i>", ParagraphStyle('S1Sub', fontName='Helvetica-Oblique', fontSize=11, leading=14, textColor=CYAN)),
        Spacer(1, 8),
        Paragraph("<b>Course:</b> Game Mechanics, Design and Development (23CS201PE407)<br/><b>Course Coordinator / Instructor:</b> Dr. Vijaya Chandra Jadala", style_body_light),
        Spacer(1, 8),
        Paragraph("<b>Submitted by Team Members:</b>", ParagraphStyle('S1TeamH', fontName='Helvetica-Bold', fontSize=9.5, leading=12, textColor=CRIMSON)),
        Paragraph("1. J. Radha Krishna (Roll No: 2303A52055)<br/>2. P. Makesh Babu (Roll No: 2303A52061)<br/>3. M. Omprakash (Roll No: 2303A52057)<br/>4. V. Siddharatha (Roll No: 2303A52463)", style_body_light),
    ]

    img_hero = os.path.join(screenshots_dir, "02_Survivor_Character_Closeup.png")
    hero_elem = Image(img_hero, width=5.0*inch, height=5.5*inch) if os.path.exists(img_hero) else Paragraph("Hero Image", style_body)

    s1_data = [[s1_left, hero_elem]]
    t_s1 = Table(s1_data, colWidths=[490, 398])
    t_s1.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (0,0), CARD_BG),
        ('BOX', (0,0), (0,0), 1.0, BORDER_COLOR),
        ('LEFTPADDING', (0,0), (0,0), 20),
        ('RIGHTPADDING', (0,0), (0,0), 20),
        ('TOPPADDING', (0,0), (0,0), 18),
        ('BOTTOMPADDING', (0,0), (0,0), 18),
    ]))
    story.append(t_s1)
    story.append(PageBreak())

    # ==========================================
    # SLIDE 2 — PROJECT OVERVIEW
    # ==========================================
    story.append(make_header_table("Project Overview & Genre Synthesis", "Bridging Endless Runner Velocity with Survival Horror Tension"))
    story.append(Spacer(1, 10))

    s2_left = [
        Paragraph("Hybrid Genre Innovation", style_card_title),
        Paragraph("Zombie Runner evolves the traditional endless runner formula by injecting active firearm combat, ammo management, and visceral survival-horror stakes into high-speed three-lane locomotion.", style_body),
        Spacer(1, 8),
        Paragraph("Atmospheric Post-Apocalyptic Setting", style_card_title),
        Paragraph("Players sprint through decaying nocturnal city ruins and subterranean subway tunnels under cool moonlight, flickering emergency sodium fixtures, trilight ambient bounce, and volumetric fog.", style_body),
        Spacer(1, 8),
        Paragraph("Core Player Objectives & Loop", style_card_title),
        Paragraph("Sprint across 3 lanes, execute grounded jumps over roadblocks, slide under low overhead pipes, scavenge gold coins and ammunition, and eliminate pursuing zombies with raycast weapon fire.", style_body),
    ]
    img_act = os.path.join(screenshots_dir, "07_Runner_Locomotion_Action.png")
    s2_right = [
        Image(img_act, width=5.3*inch, height=4.2*inch) if os.path.exists(img_act) else Paragraph("Gameplay Action", style_body),
        Spacer(1, 4),
        Paragraph("Figure: Real-time gameplay showing player runner in motion along the 3-lane road", style_caption)
    ]
    t_s2 = Table([[s2_left, s2_right]], colWidths=[450, 438])
    t_s2.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (0,0), CARD_BG),
        ('BOX', (0,0), (0,0), 1.0, BORDER_COLOR),
        ('LEFTPADDING', (0,0), (0,0), 16),
        ('RIGHTPADDING', (0,0), (0,0), 16),
        ('TOPPADDING', (0,0), (0,0), 14),
        ('BOTTOMPADDING', (0,0), (0,0), 14),
    ]))
    story.append(t_s2)
    story.append(PageBreak())

    # ==========================================
    # SLIDE 3 — PROBLEM STATEMENT & OBJECTIVES
    # ==========================================
    story.append(make_header_table("Academic Motivation & Project Scope", "Addressing Key Game Mechanics & Technical Challenges"))
    story.append(Spacer(1, 10))

    s3_left = [
        Paragraph("PROBLEM STATEMENT", style_card_title),
        Spacer(1, 4),
        Paragraph("<b>Passive Evasion Fatigue:</b> Traditional endless runners (Temple Run, Subway Surfers) offer only obstacle dodging. The lack of offensive combat reduces tactical engagement and player agency.", style_body),
        Spacer(1, 5),
        Paragraph("<b>Atmospheric Disconnect:</b> Sterile, brightly saturated daytime aesthetics fail to evoke tension, fear, or narrative immersion common in horror gaming.", style_body),
        Spacer(1, 5),
        Paragraph("<b>High-Speed Combat Desynchronization:</b> Integrating real-time shooting at high forward speeds often leads to hit registration misses, jerky camera jitter, and frame drops.", style_body),
        Spacer(1, 5),
        Paragraph("<b>Garbage Collection Spikes:</b> Continual runtime instantiation and destruction of road chunks, projectiles, and particle bursts trigger severe GC stutter on target platforms.", style_body),
    ]
    s3_right = [
        Paragraph("PROJECT OBJECTIVES", style_card_title_cyan),
        Spacer(1, 4),
        Paragraph("<b>Modular Unity 6 Architecture:</b> Develop a decoupled C# component architecture using ScriptableObjects, interface-based combat (IDamageable), and centralized managers.", style_body),
        Spacer(1, 5),
        Paragraph("<b>Kinematic Locomotion Engine:</b> Implement responsive 3-lane shifts, grounded jump physics, timed slide with collision box reduction, and progressive speed scaling (8 to 16 m/s).", style_body),
        Spacer(1, 5),
        Paragraph("<b>Zombie AI & Raycast Combat:</b> Engineer 3 distinct zombie archetypes with Mecanim state machines, hit reactions, forward raycast shooting, visual recoil, and bullet tracers.", style_body),
        Spacer(1, 5),
        Paragraph("<b>Procedural Environment Streaming:</b> Build a 5-segment circular object pool recycling 30m modular city ruins and subway tunnels with dynamic trilight and fog transitions.", style_body),
        Spacer(1, 5),
        Paragraph("<b>Adaptive Horror Audio & Economy:</b> Crossfade 4-tier synchronized horror music stems across tension states; persist coins, ammo reserves, and high scores via PlayerPrefs.", style_body),
    ]
    t_s3 = Table([[s3_left, s3_right]], colWidths=[436, 436])
    t_s3.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (0,0), CARD_BG),
        ('BACKGROUND', (1,0), (1,0), CARD_BG),
        ('BOX', (0,0), (0,0), 1.0, BORDER_COLOR),
        ('BOX', (1,0), (1,0), 1.0, BORDER_COLOR),
        ('LEFTPADDING', (0,0), (-1,-1), 16),
        ('RIGHTPADDING', (0,0), (-1,-1), 16),
        ('TOPPADDING', (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
    ]))
    story.append(t_s3)
    story.append(PageBreak())

    # ==========================================
    # SLIDE 4 — TOOLS AND TECHNOLOGIES
    # ==========================================
    story.append(make_header_table("Technology Stack & Pipeline", "Engine, Rendering, Physics, and Audio Middleware"))
    story.append(Spacer(1, 10))

    t_box_data = [
        [
            [Paragraph("GAME ENGINE", style_card_title), Paragraph("<b>Unity 6 (6000.5.9f1)</b><br/>High-performance C# runtime, unified build pipeline, robust profiler, and modern URP graphics features.", style_body)],
            [Paragraph("RENDER PIPELINE", style_card_title), Paragraph("<b>URP (17.5.0)</b><br/>Optimized single-pass Forward+ rendering, custom Lit PBR materials, ACES tonemapping, and linear fog.", style_body)],
            [Paragraph("INPUT FRAMEWORK", style_card_title), Paragraph("<b>Unity Input System (1.20.0)</b><br/>Event-driven cross-platform input supporting both keyboard/mouse and mobile touchscreen fallbacks.", style_body)]
        ],
        [
            [Paragraph("CHARACTER RIGGING", style_card_title), Paragraph("<b>Mixamo & Mecanim</b><br/>Humanoid avatar retargeting, baked in-place root motion, and multi-layer state machines.", style_body)],
            [Paragraph("AUDIO PIPELINE", style_card_title), Paragraph("<b>Unity AudioMixer</b><br/>5-bus routing (Master, Music, SFX, Ambient, UI) with logarithmic dB attenuation and 4 adaptive stems.", style_body)],
            [Paragraph("SOURCE CONTROL", style_card_title), Paragraph("<b>Git & Git LFS</b><br/>Tracking high-resolution 3D models (FBX), audio (WAV), and PBR textures with automated C# editor tools.", style_body)]
        ]
    ]
    t_s4 = Table(t_box_data, colWidths=[290, 290, 290])
    t_s4.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
        ('BOX', (0,0), (-1,-1), 1.0, BORDER_COLOR),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_s4)
    story.append(PageBreak())

    # ==========================================
    # SLIDE 5 — SYSTEM ARCHITECTURE
    # ==========================================
    story.append(make_header_table("Software Architecture & Modularity", "Decoupled Component-Based Architecture and Subsystems"))
    story.append(Spacer(1, 10))

    s5_boxes = [
        [
            [Paragraph("Player Subsystem", style_card_title), Paragraph("• <b>PlayerController:</b> 3-lane horizontal lerp (-3, 0, +3m) at 14 m/s.<br/>• <b>Kinematic Jump:</b> Launch vy = sqrt(2gh) at g = -20 m/s².<br/>• <b>Combat Slide:</b> CharacterController height 2.0m -> 1.05m.<br/>• <b>PlayerHealth:</b> Invulnerability frames, shield absorption, death.", style_body)],
            [Paragraph("Combat & Pooling", style_card_title), Paragraph("• <b>ShootingController:</b> Forward hitscan with auto-aim cone (<=12°).<br/>• <b>Weapon Recoil:</b> Visual kickback (0.07m displacement, 3.5° climb).<br/>• <b>BulletTracer:</b> Interpolated glowing raycast tracer lines.<br/>• <b>HitImpactManager:</b> Pre-warmed zero-allocation blood/spark pools.", style_body)],
            [Paragraph("Enemy AI Subsystem", style_card_title), Paragraph("• <b>ZombieSpawner:</b> Lane-aware spawner with alive limits (max 6).<br/>• <b>ZombieController:</b> Mecanim FSM (Idle, Walk, Run, Attack, Hit, Death).<br/>• <b>ZombieConfig:</b> Modular ScriptableObject data architecture.<br/>• <b>ZombieSoundEmitter:</b> Logarithmic 3D spatial audio attenuation.", style_body)],
            [Paragraph("World & UI Systems", style_card_title), Paragraph("• <b>EndlessRoadManager:</b> Circular 5-segment pool of 30m road sections.<br/>• <b>ThemeManager:</b> 45m smooth trilight & fog blending.<br/>• <b>GameManager:</b> Global finite state machine (Play, Pause, GameOver).<br/>• <b>SaveManager:</b> PlayerPrefs high score & banked coin persistence.", style_body)],
        ]
    ]
    t_s5 = Table(s5_boxes, colWidths=[218, 218, 218, 218])
    t_s5.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
        ('BOX', (0,0), (-1,-1), 1.0, BORDER_COLOR),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_s5)
    story.append(Spacer(1, 8))

    callout_p = Paragraph("<b>KEY ARCHITECTURAL DECOUPLING:</b> All damageable entities (Common/Fast/Heavy zombies, player health, and explosive barrels) implement the <code>IDamageable</code> interface. The weapon raycast system remains completely agnostic of enemy classes, ensuring clean decoupling and zero class dependencies.", style_body_light)
    t_s5_b = Table([[callout_p]], colWidths=[888])
    t_s5_b.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#1A202C")),
        ('BOX', (0,0), (-1,-1), 1.0, CRIMSON),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_s5_b)
    story.append(PageBreak())

    # ==========================================
    # SLIDE 6 — CORE GAMEPLAY MECHANICS
    # ==========================================
    story.append(make_header_table("Core Gameplay Mechanics", "Locomotion, Ballistics, Raycast Combat, and Resource Economy"))
    story.append(Spacer(1, 10))

    s6_left = [
        Paragraph("Three-Lane Locomotion", style_card_title),
        Paragraph("Discrete lane snapping at X = -3.0m, 0.0m, +3.0m using smooth frame-rate independent interpolation (14 m/s). Progressive speed acceleration from 8.0 m/s to 16.0 m/s.", style_body),
        Spacer(1, 6),
        Paragraph("Jump & Slide Physics", style_card_title),
        Paragraph("Kinematic vertical launch vy = sqrt(2gh) (h = 1.8m, g = -20 m/s²). Timed slide (0.8s) reduces CharacterController height from 2.0m to 1.05m while preserving humanoid mesh proportions.", style_body),
        Spacer(1, 6),
        Paragraph("Raycast Combat & Recoil", style_card_title),
        Paragraph("Forward hitscan with dynamic auto-aim cone (<=12°). Firing inflicts IDamageable damage, produces 0.07m visual kickback & 3.5° muzzle climb, and spawns glowing bullet tracers.", style_body),
        Spacer(1, 6),
        Paragraph("Scavenging & Economy", style_card_title),
        Paragraph("Gold coins bank permanently across runs. Ammunition boxes refill +15 rounds; medical kits restore +25 HP. 4 timed power-ups: Shield, Coin Magnet, Speed Boost, Double Coins.", style_body),
    ]
    img_ctrl = os.path.join(screenshots_dir, "05_Controls_Guide_Modal.png")
    s6_right = [
        Image(img_ctrl, width=5.2*inch, height=4.2*inch) if os.path.exists(img_ctrl) else Paragraph("Controls Modal", style_body),
        Spacer(1, 4),
        Paragraph("Figure: In-game input controls reference guide modal (Keyboard & Mouse)", style_caption)
    ]
    t_s6 = Table([[s6_left, s6_right]], colWidths=[450, 438])
    t_s6.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (0,0), CARD_BG),
        ('BOX', (0,0), (0,0), 1.0, BORDER_COLOR),
        ('LEFTPADDING', (0,0), (0,0), 14),
        ('RIGHTPADDING', (0,0), (0,0), 14),
        ('TOPPADDING', (0,0), (0,0), 12),
        ('BOTTOMPADDING', (0,0), (0,0), 12),
    ]))
    story.append(t_s6)
    story.append(PageBreak())

    # ==========================================
    # SLIDE 7 — ENVIRONMENT DESIGN
    # ==========================================
    story.append(make_header_table("Environment & Visual Design", "Dual Biome Streaming and Calibrated Volumetric Lighting"))
    story.append(Spacer(1, 10))

    s7_left = [
        Paragraph("ABANDONED CITY RUINS BIOME", style_card_title),
        Paragraph("• <b>Architecture:</b> Crumbling multi-story brick facades, cracked asphalt, worn lane markings.<br/>• <b>Obstacles & Props:</b> Concrete barricades, roadblock barriers, abandoned cars, explosive barrels.<br/>• <b>Lighting:</b> Cool-blue moonlight (#C0D6FA, 1.75 intensity) and flickering sodium streetlights.", style_body),
        Spacer(1, 10),
        Paragraph("SUBTERRANEAN SUBWAY TUNNEL BIOME", style_card_title_cyan),
        Paragraph("• <b>Enclosure:</b> Continuous solid 5.2m concrete side walls and 15.5m ceiling with 45° vaulted arches.<br/>• <b>Structural Ribs:</b> Heavy portal columns every 7.5m, industrial ventilation shafts, steel tracks.<br/>• <b>Luminaires:</b> Balanced 4200K neutral ceiling luminaires & 2200K amber caged emergency bulkheads.", style_body),
    ]
    img_city = os.path.join(screenshots_dir, "03_City_Environment_Atmosphere.png")
    img_tun = os.path.join(screenshots_dir, "09_Subway_Tunnel_Materials.png")
    s7_right = [
        Image(img_city, width=5.2*inch, height=2.0*inch) if os.path.exists(img_city) else Paragraph("City Ruins", style_body),
        Paragraph("Figure: Nocturnal city ruins environment with cool-blue moonlight and fog", style_caption),
        Spacer(1, 4),
        Image(img_tun, width=5.2*inch, height=2.0*inch) if os.path.exists(img_tun) else Paragraph("Tunnel PBR", style_body),
        Paragraph("Figure: Authored PBR texture maps for Subway Tunnel concrete, hazard plinths, and steel", style_caption)
    ]
    t_s7 = Table([[s7_left, s7_right]], colWidths=[440, 448])
    t_s7.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (0,0), CARD_BG),
        ('BOX', (0,0), (0,0), 1.0, BORDER_COLOR),
        ('LEFTPADDING', (0,0), (0,0), 14),
        ('RIGHTPADDING', (0,0), (0,0), 14),
        ('TOPPADDING', (0,0), (0,0), 12),
        ('BOTTOMPADDING', (0,0), (0,0), 12),
    ]))
    story.append(t_s7)
    story.append(PageBreak())

    # ==========================================
    # SLIDE 8 — ZOMBIE AI AND COMBAT
    # ==========================================
    story.append(make_header_table("Zombie AI & Combat System", "Modular Archetypes, Mecanim State Machines, and Audio Depth"))
    story.append(Spacer(1, 10))

    s8_left = [
        Paragraph("COMMON RUNNER ZOMBIE (Mixamo Ch10)", style_card_title),
        Paragraph("<b>3 HP (3 shots)</b>  |  Speed: 5.0 m/s  |  Damage: 10 / 1.8m range  |  Score: 100 pts<br/>Balanced threat spawning across lanes. Claws and lunges at player when in range.", style_body),
        Spacer(1, 6),
        Paragraph("FAST SPRINTER ZOMBIE (Mixamo Yaku J Ignite)", style_card_title),
        Paragraph("<b>2 HP (2 shots)</b>  |  Speed: 7.5 m/s  |  Damage: 8 / 1.6m range  |  Score: 150 pts<br/>High velocity agile ambusher. Forces rapid lane evasion and quick auto-aim reflex fire.", style_body),
        Spacer(1, 6),
        Paragraph("HEAVY BRUTE ZOMBIE (Mixamo Pumpkinhulk)", style_card_title),
        Paragraph("<b>8 HP (8 shots)</b>  |  Speed: 3.2 m/s  |  Damage: 25 / 2.2m range  |  Score: 250 pts<br/>Massive tank requiring sustained gunfire. Deals devastating damage on impact.", style_body),
    ]
    img_z = os.path.join(screenshots_dir, "08_Zombie_Archetypes_Textures.png")
    s8_right = [
        Image(img_z, width=5.2*inch, height=2.1*inch) if os.path.exists(img_z) else Paragraph("Zombie Textures", style_body),
        Paragraph("Figure: Diffuse texture maps for Common, Fast Runner, and Heavy Brute zombies", style_caption),
        Spacer(1, 4),
        Paragraph("<b>Combat & AI Behavior Highlights:</b>", style_card_title_cyan),
        Paragraph("• <b>Damage Metric:</b> Firearm deals exactly 1 damage point per shot.<br/>• <b>State Machine:</b> Transitions between Idle, Walk, Run, Attack, Hit, and Death collapse.<br/>• <b>3D Spatial Audio:</b> Logarithmic attenuation (2.5m to 24m) for positional hearing.<br/>• <b>GC-Free Pooling:</b> HitImpactManager pre-warms blood splatters, sparks, and bullet tracers.", style_body)
    ]
    t_s8 = Table([[s8_left, s8_right]], colWidths=[440, 448])
    t_s8.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (0,0), CARD_BG),
        ('BOX', (0,0), (0,0), 1.0, BORDER_COLOR),
        ('LEFTPADDING', (0,0), (0,0), 14),
        ('RIGHTPADDING', (0,0), (0,0), 14),
        ('TOPPADDING', (0,0), (0,0), 12),
        ('BOTTOMPADDING', (0,0), (0,0), 12),
    ]))
    story.append(t_s8)
    story.append(PageBreak())

    # ==========================================
    # SLIDE 9 — USER INTERFACE AND GAME FLOW
    # ==========================================
    story.append(make_header_table("User Interface & Game Flow", "Main Menu Staging, HUD Feedback, and State Progression"))
    story.append(Spacer(1, 10))

    s9_left = [
        Paragraph("SEAMLESS GAME STATE TRANSITIONS", style_card_title),
        Paragraph("<b>Main Menu  ->  Active Gameplay  ->  Game Over  ->  Retry / Revive / Menu</b>", style_body_light),
        Spacer(1, 6),
        Paragraph("<b>3D Main Menu Staging:</b> Features an animated survivor character (Ch05) holding the Tommy Gun on a nocturnal street, accompanied by cinematic camera panning and multi-tab settings.", style_body),
        Spacer(1, 5),
        Paragraph("<b>In-Game Survival HUD:</b> Real-time TextMeshPro meters for distance (m), score (Distance + Kills), coin inventory, ammunition reserve, segmented health bar, and power-up countdowns.", style_body),
        Spacer(1, 5),
        Paragraph("<b>Game Over & Record Celebration:</b> Summarizes run statistics alongside persistent high scores loaded from PlayerPrefs. Surpassing the record triggers a prominent '(NEW BEST!)' celebratory banner.", style_body),
        Spacer(1, 5),
        Paragraph("<b>One-Time Shielded Revive Loop:</b> Players can trigger a single revive per run, granting full health, +30 ammunition rounds, and a 3-second invulnerability shield before resuming traversal.", style_body),
        Spacer(1, 5),
        Paragraph("<b>Cross-Platform Adaptation:</b> SafeAreaFitter queries Screen.safeArea, ensuring UI buttons and indicators avoid mobile camera notches and cutouts.", style_body),
    ]
    img_menu = os.path.join(screenshots_dir, "01_Title_Screen_Overview.png")
    s9_right = [
        Image(img_menu, width=5.2*inch, height=4.2*inch) if os.path.exists(img_menu) else Paragraph("Main Menu", style_body),
        Spacer(1, 4),
        Paragraph("Figure: 3D Main Menu scene with survivor character staging, title, and buttons", style_caption)
    ]
    t_s9 = Table([[s9_left, s9_right]], colWidths=[450, 438])
    t_s9.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (0,0), CARD_BG),
        ('BOX', (0,0), (0,0), 1.0, BORDER_COLOR),
        ('LEFTPADDING', (0,0), (0,0), 14),
        ('RIGHTPADDING', (0,0), (0,0), 14),
        ('TOPPADDING', (0,0), (0,0), 12),
        ('BOTTOMPADDING', (0,0), (0,0), 12),
    ]))
    story.append(t_s9)
    story.append(PageBreak())

    # ==========================================
    # SLIDE 10 — IMPLEMENTATION, TESTING & DEBUGGING
    # ==========================================
    story.append(make_header_table("Verification, Refactoring & Optimization", "Iterative Engineering Workflow and Documented Technical Fixes"))
    story.append(Spacer(1, 10))

    s10_left = [
        Paragraph("DEVELOPMENT & VERIFICATION WORKFLOW", style_card_title_cyan),
        Spacer(1, 4),
        Paragraph("<b>Automated Editor Audits:</b> Custom C# validation tools (ZombieCombatSystemValidator.cs, VisualAuditHelper.cs) automated hierarchy, avatar bone binding, and material audits.", style_body),
        Spacer(1, 5),
        Paragraph("<b>Play Mode Systems Testing:</b> Validated lane-switch clamping (-3m to +3m), airborne jump locking, power-up timer refresh logic, and PlayerPrefs score persistence.", style_body),
        Spacer(1, 5),
        Paragraph("<b>Memory & GC Profiling:</b> Profiler audits verified 0 bytes of heap allocation during active running by pooling road segments, enemies, bullet tracers, and particle VFX.", style_body),
        Spacer(1, 5),
        Paragraph("<b>Windows Standalone Build:</b> Verified smooth 60 FPS gameplay execution with native keyboard and mouse controls on Windows PC.", style_body),
        Spacer(1, 5),
        Paragraph("<b>Verified Android Build:</b> Completed automated Android build pipeline, producing Builds/Android/ZombieRunner.apk (42.9 MB, IL2CPP 64-bit, ARM64, minimum API 26) with zero compilation errors.", style_body),
    ]
    s10_right = [
        Paragraph("SIX DOCUMENTED ENGINEERING FIXES", style_card_title),
        Spacer(1, 4),
        Paragraph("<b>1. Slide Mesh Decoupling:</b> Decoupled CharacterController height reduction (1.05m) from humanoid visual transforms, eliminating mesh squash and ground sinking.", style_body),
        Spacer(1, 4),
        Paragraph("<b>2. Jump Launch Cancellation:</b> Added explicit isJumping flag to eliminate premature Grounded landing cancellation on launch frames.", style_body),
        Spacer(1, 4),
        Paragraph("<b>3. Spawner Deadlock Bug:</b> Auto-destroyed trailing zombies (> 12m behind runner) without score, preventing alive counter from capping at 6 and halting spawns.", style_body),
        Spacer(1, 4),
        Paragraph("<b>4. Particle Lifecycle Bug:</b> Instantiated GameObjects inactive before duration assignment, resolving over 100 duration mutation console errors.", style_body),
        Spacer(1, 4),
        Paragraph("<b>5. Subway Tunnel Enclosure:</b> Reconstructed solid 30m concrete tunnel with vaulted arches, eliminating repeating rectangular frames and open daylight leakage.", style_body),
        Spacer(1, 4),
        Paragraph("<b>6. Audio Suite Overhaul:</b> Synthesized organic 48s Brownian noise and 4 synchronized 75 BPM adaptive stems in D minor, eliminating irritating sine whistle loops.", style_body),
    ]
    t_s10 = Table([[s10_left, s10_right]], colWidths=[436, 436])
    t_s10.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (0,0), CARD_BG),
        ('BACKGROUND', (1,0), (1,0), CARD_BG),
        ('BOX', (0,0), (0,0), 1.0, BORDER_COLOR),
        ('BOX', (1,0), (1,0), 1.0, BORDER_COLOR),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_s10)
    story.append(PageBreak())

    # ==========================================
    # SLIDE 11 — LEARNING OUTCOMES & FUTURE WORK
    # ==========================================
    story.append(make_header_table("Academic Evaluation & Roadmap", "Core Competencies Mastered and Proposed Future Enhancements"))
    story.append(Spacer(1, 10))

    s11_left = [
        Paragraph("LEARNING OUTCOMES ACQUIRED", style_card_title_cyan),
        Spacer(1, 4),
        Paragraph("<b>Real-Time 3D Game Mechanics:</b> Mastered kinematic character controllers, grounded jump physics, low-clearance sliding, and lane-based traversal in Unity 6.", style_body),
        Spacer(1, 5),
        Paragraph("<b>Universal Render Pipeline Mastery:</b> Configured custom Lit PBR materials, ACES tonemapping, Trilight ambient lighting, and balanced volumetric fog.", style_body),
        Spacer(1, 5),
        Paragraph("<b>Animation Retargeting & State Machines:</b> Retargeted Mixamo Humanoid rigs, baked in-place root motion, and orchestrated complex Mecanim transition graphs.", style_body),
        Spacer(1, 5),
        Paragraph("<b>Object-Oriented Game Architecture:</b> Implemented ScriptableObject data encapsulation, interface-based messaging (IDamageable), and zero-allocation circular object pooling.", style_body),
        Spacer(1, 5),
        Paragraph("<b>Dynamic Audio Systems:</b> Engineered 4-layer synchronized adaptive horror stems, logarithmic decibel attenuation, and 3D positional sound emitters.", style_body),
    ]
    s11_right = [
        Paragraph("PROPOSED FUTURE ENHANCEMENTS", style_card_title),
        Paragraph("<i>(Strictly proposed future extensions beyond current verified scope)</i>", style_caption),
        Spacer(1, 4),
        Paragraph("<b>1. Advanced Flocking & Ranged Mutant AI:</b> Flocking runner hordes and acid-spitting mutants that force players to dodge incoming parabolic projectiles while running.", style_body),
        Spacer(1, 5),
        Paragraph("<b>2. Expanded Weapon Arsenal:</b> Collectible pump shotguns (wide-spread clearing), assault rifles, and grenade launchers with dedicated ammo economies.", style_body),
        Spacer(1, 5),
        Paragraph("<b>3. Dynamic Subway Boss Encounters:</b> Procedural tunnel breach events featuring a pursuing Nemesis juggernaut that must be damaged over sustained running distance.", style_body),
        Spacer(1, 5),
        Paragraph("<b>4. Global Online Leaderboards:</b> RESTful cloud database integration supporting asynchronous ghost runner replays and cross-platform high-score rankings.", style_body),
        Spacer(1, 5),
        Paragraph("<b>5. Dynamic Atmospheric Weather VFX:</b> Screen-space rain droplets, volumetric lightning strikes dynamically casting shadows, and destructible road barricades.", style_body),
    ]
    t_s11 = Table([[s11_left, s11_right]], colWidths=[436, 436])
    t_s11.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (0,0), CARD_BG),
        ('BACKGROUND', (1,0), (1,0), CARD_BG),
        ('BOX', (0,0), (0,0), 1.0, BORDER_COLOR),
        ('BOX', (1,0), (1,0), 1.0, BORDER_COLOR),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_s11)
    story.append(PageBreak())

    # ==========================================
    # SLIDE 12 — CONCLUSION AND THANK YOU
    # ==========================================
    s12_left = [
        Paragraph("ACADEMIC PROJECT CONCLUSION", style_tag),
        Spacer(1, 4),
        Paragraph("<b>Zombie Runner – 3D Survival Horror Endless Runner</b>", style_title),
        Paragraph("Successfully conceived, architected, and optimized an innovative hybrid survival-horror endless runner fulfilling all rigorous academic criteria for Game Mechanics, Design and Development (23CS201PE407).", style_body),
        Spacer(1, 8),
        Paragraph("Sincere Academic Gratitude:", style_card_title_cyan),
        Paragraph("Special thanks to our Course Coordinator & Instructor, <b>Dr. Vijaya Chandra Jadala Sir</b>, for his continuous guidance, technical encouragement, and pedagogical leadership.", style_body_light),
        Spacer(1, 8),
        Paragraph("Project Development Team:", style_card_title),
        Paragraph("1. J. Radha Krishna (Roll No: 2303A52055)<br/>2. P. Makesh Babu (Roll No: 2303A52061)<br/>3. M. Omprakash (Roll No: 2303A52057)<br/>4. V. Siddharatha (Roll No: 2303A52463)", style_body_light),
        Spacer(1, 10),
        Paragraph("<b>THANK YOU! QUESTIONS & DISCUSSION WELCOME.</b>", ParagraphStyle('S12Thx', fontName='Helvetica-Bold', fontSize=12, leading=15, textColor=CRIMSON)),
    ]
    img_menu = os.path.join(screenshots_dir, "01_Title_Screen_Overview.png")
    s12_right = [
        Image(img_menu, width=5.0*inch, height=5.5*inch) if os.path.exists(img_menu) else Paragraph("Final Overview", style_body)
    ]
    t_s12 = Table([[s12_left, s12_right]], colWidths=[490, 398])
    t_s12.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (0,0), CARD_BG),
        ('BOX', (0,0), (0,0), 1.0, BORDER_COLOR),
        ('LEFTPADDING', (0,0), (0,0), 20),
        ('RIGHTPADDING', (0,0), (0,0), 20),
        ('TOPPADDING', (0,0), (0,0), 18),
        ('BOTTOMPADDING', (0,0), (0,0), 18),
    ]))
    story.append(t_s12)

    doc.build(story, canvasmaker=LandscapeBackgroundCanvas)
    print(f"Presentation PDF created successfully at: {out_pdf_path}")

if __name__ == "__main__":
    out_pdf = os.path.abspath(r"E:\zombie runner\Zombie_Runner_Project_Presentation.pdf")
    create_presentation_pdf(out_pdf)
