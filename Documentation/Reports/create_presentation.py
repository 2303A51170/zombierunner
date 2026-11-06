import os
import sys
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def add_r(paragraph, text=""):
    r = paragraph.add_run()
    r.text = text
    return r

def build_presentation(out_pptx_path):
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette: Survival Horror Cinematic
    BG_DARK = RGBColor(14, 16, 20)         # #0E1014
    CARD_BG = RGBColor(22, 26, 33)         # #161A21
    CARD_BORDER = RGBColor(38, 45, 58)     # #262D3A
    BLOOD_RED = RGBColor(185, 30, 38)      # #B91E26
    CRIMSON = RGBColor(225, 45, 55)        # #E12D37
    TEXT_LIGHT = RGBColor(245, 247, 250)   # #F5F7FA
    TEXT_MUTED = RGBColor(165, 178, 192)   # #A5B2C0
    CYAN_ACCENT = RGBColor(56, 189, 248)   # #38BDF8

    screenshots_dir = os.path.abspath(r"E:\zombie runner\PresentationScreenshots")
    logo_path = r"C:\Users\metra\.gemini\antigravity\brain\7ea1a950-c3d7-465b-a4d2-a25115ebddc3\.user_uploaded\media_1793877402347_b6c68b90.png"

    def set_slide_background(slide, color=BG_DARK):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, tag_text, title_text):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_tag = tf.paragraphs[0]
        p_tag.space_after = Pt(2)
        r_tag = add_r(p_tag, tag_text.upper())
        r_tag.font.name = "Calibri"
        r_tag.font.size = Pt(9.5)
        r_tag.font.bold = True
        r_tag.font.color.rgb = CRIMSON

        p_title = tf.add_paragraph()
        r_title = add_r(p_title, title_text)
        r_title.font.name = "Calibri"
        r_title.font.size = Pt(21)
        r_title.font.bold = True
        r_title.font.color.rgb = TEXT_LIGHT

        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.48), Inches(11.733), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = CARD_BORDER
        line.line.fill.background()

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.2)
        return card

    # ==========================================
    # SLIDE 1 — TITLE SLIDE
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    hero_path = os.path.join(screenshots_dir, "02_Survivor_Character_Closeup.png")
    if os.path.exists(hero_path):
        s1.shapes.add_picture(hero_path, Inches(7.5), Inches(0), Inches(5.833), Inches(7.5))
        fader = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(7.48), Inches(0), Inches(0.8), Inches(7.5))
        fader.fill.solid()
        fader.fill.fore_color.rgb = BG_DARK
        fader.line.fill.background()

    c1 = add_card(s1, Inches(0.8), Inches(0.6), Inches(6.8), Inches(6.3), CARD_BG, CARD_BORDER)
    tb1 = s1.shapes.add_textbox(Inches(1.1), Inches(0.8), Inches(6.2), Inches(5.9))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_top = tf1.margin_right = tf1.margin_bottom = 0

    p = tf1.paragraphs[0]
    p.space_after = Pt(4)
    r = add_r(p, "SR UNIVERSITY | DEPARTMENT REVIEW")
    r.font.name = "Calibri"
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = CRIMSON

    p = tf1.add_paragraph()
    p.space_after = Pt(2)
    r = add_r(p, "School of Computer Science & Artificial Intelligence")
    r.font.name = "Calibri"
    r.font.size = Pt(11)
    r.font.color.rgb = TEXT_MUTED

    p = tf1.add_paragraph()
    p.space_before = Pt(12)
    p.space_after = Pt(0)
    r = add_r(p, "ZOMBIE RUNNER")
    r.font.name = "Calibri"
    r.font.size = Pt(32)
    r.font.bold = True
    r.font.color.rgb = TEXT_LIGHT

    p = tf1.add_paragraph()
    p.space_after = Pt(12)
    r = add_r(p, "A 3D Survival Horror Endless Runner Game")
    r.font.name = "Calibri"
    r.font.size = Pt(13)
    r.font.italic = True
    r.font.color.rgb = CYAN_ACCENT

    p = tf1.add_paragraph()
    p.space_before = Pt(4)
    p.space_after = Pt(2)
    r = add_r(p, "Course: ")
    r.font.bold = True
    r.font.size = Pt(10.5)
    r.font.color.rgb = TEXT_LIGHT
    r2 = add_r(p, "Game Mechanics, Design and Development (23CS201PE407)\n")
    r2.font.size = Pt(10.5)
    r2.font.color.rgb = TEXT_MUTED

    r3 = add_r(p, "Course Coordinator / Instructor: ")
    r3.font.bold = True
    r3.font.size = Pt(10.5)
    r3.font.color.rgb = TEXT_LIGHT
    r4 = add_r(p, "Dr. Vijaya Chandra Jadala\n")
    r4.font.size = Pt(10.5)
    r4.font.color.rgb = TEXT_MUTED

    p = tf1.add_paragraph()
    p.space_before = Pt(10)
    p.space_after = Pt(4)
    r = add_r(p, "Submitted by Team Members:")
    r.font.name = "Calibri"
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = CRIMSON

    team_list = [
        "1. J. Radha Krishna (Roll No: 2303A52055)",
        "2. P. Makesh Babu (Roll No: 2303A52061)",
        "3. M. Omprakash (Roll No: 2303A52057)",
        "4. V. Siddharatha (Roll No: 2303A52463)"
    ]
    for tm in team_list:
        p = tf1.add_paragraph()
        p.space_after = Pt(2)
        r = add_r(p, tm)
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.color.rgb = TEXT_LIGHT

    if os.path.exists(logo_path):
        s1.shapes.add_picture(logo_path, Inches(6.4), Inches(0.85), Inches(1.0), Inches(1.0))

    # ==========================================
    # SLIDE 2 — PROJECT OVERVIEW
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Project Overview & Genre Synthesis", "Bridging Endless Runner Velocity with Survival Horror Tension")

    overview_cards = [
        ("Hybrid Genre Innovation", "Zombie Runner evolves the traditional endless runner formula by injecting active firearm combat, ammo management, and visceral survival-horror stakes into high-speed three-lane locomotion."),
        ("Atmospheric Post-Apocalyptic Setting", "Players sprint through decaying nocturnal city ruins and subterranean subway tunnels under cool moonlight, flickering emergency sodium fixtures, trilight ambient bounce, and volumetric fog."),
        ("Core Player Objectives & Loop", "Sprint across 3 lanes, execute grounded jumps over roadblocks, slide under low overhead pipes, scavenge gold coins and ammunition, and eliminate pursuing zombies with raycast weapon fire.")
    ]
    for i, (c_title, c_desc) in enumerate(overview_cards):
        top = Inches(1.8 + i * 1.8)
        add_card(s2, Inches(0.8), top, Inches(6.0), Inches(1.6))
        tb = s2.shapes.add_textbox(Inches(1.0), top + Inches(0.12), Inches(5.6), Inches(1.35))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        r1 = add_r(p, c_title + "\n")
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = CRIMSON
        r2 = add_r(p, c_desc)
        r2.font.size = Pt(9.2)
        r2.font.color.rgb = TEXT_MUTED

    act_path = os.path.join(screenshots_dir, "07_Runner_Locomotion_Action.png")
    if os.path.exists(act_path):
        add_card(s2, Inches(7.1), Inches(1.8), Inches(5.4), Inches(5.2))
        s2.shapes.add_picture(act_path, Inches(7.2), Inches(1.9), Inches(5.2), Inches(4.5))
        tb_c = s2.shapes.add_textbox(Inches(7.2), Inches(6.5), Inches(5.2), Inches(0.4))
        p_c = tb_c.text_frame.paragraphs[0]
        p_c.alignment = PP_ALIGN.CENTER
        r_c = add_r(p_c, "Figure: Real-time gameplay showing player runner in motion along the 3-lane road")
        r_c.font.size = Pt(8.5)
        r_c.font.italic = True
        r_c.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 3 — PROBLEM STATEMENT & OBJECTIVES
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Academic Motivation & Project Scope", "Addressing Key Game Mechanics & Technical Challenges")

    # Left: Problem Statement
    add_card(s3, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.2))
    tb = s3.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.1), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.space_after = Pt(8)
    r = add_r(p, "PROBLEM STATEMENT")
    r.font.bold = True
    r.font.size = Pt(14)
    r.font.color.rgb = CRIMSON

    bullets_prob = [
        ("Passive Evasion Fatigue: ", "Traditional endless runners (Temple Run, Subway Surfers) offer only obstacle dodging. The lack of offensive combat reduces tactical engagement and player agency."),
        ("Atmospheric Disconnect: ", "Sterile, brightly saturated daytime aesthetics fail to evoke tension, fear, or narrative immersion common in horror gaming."),
        ("High-Speed Combat Desynchronization: ", "Integrating real-time shooting at high forward speeds often leads to hit registration misses, jerky camera jitter, and frame drops."),
        ("Garbage Collection Spikes: ", "Continual runtime instantiation and destruction of road chunks, projectiles, and particle bursts trigger severe GC stutter on target platforms.")
    ]
    for b_title, b_desc in bullets_prob:
        p = tf.add_paragraph()
        p.space_after = Pt(6)
        r1 = add_r(p, b_title)
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = TEXT_LIGHT
        r2 = add_r(p, b_desc)
        r2.font.size = Pt(9.0)
        r2.font.color.rgb = TEXT_MUTED

    # Right: Objectives
    add_card(s3, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.2))
    tb = s3.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.space_after = Pt(8)
    r = add_r(p, "PROJECT OBJECTIVES")
    r.font.bold = True
    r.font.size = Pt(14)
    r.font.color.rgb = CYAN_ACCENT

    bullets_obj = [
        ("Modular Unity 6 Architecture: ", "Develop a decoupled C# component architecture using ScriptableObjects, interface-based combat (IDamageable), and centralized managers."),
        ("Kinematic Locomotion Engine: ", "Implement responsive 3-lane shifts, grounded jump physics, timed slide with collision box reduction, and progressive speed scaling (8 to 16 m/s)."),
        ("Zombie AI & Raycast Combat: ", "Engineer 3 distinct zombie archetypes with Mecanim state machines, hit reactions, forward raycast shooting, visual recoil, and bullet tracers."),
        ("Procedural Environment Streaming: ", "Build a 5-segment circular object pool recycling 30m modular city ruins and subway tunnels with dynamic trilight and fog transitions."),
        ("Adaptive Horror Audio & Economy: ", "Crossfade 4-tier synchronized horror music stems across tension states; persist coins, ammo reserves, and high scores via PlayerPrefs.")
    ]
    for b_title, b_desc in bullets_obj:
        p = tf.add_paragraph()
        p.space_after = Pt(6)
        r1 = add_r(p, b_title)
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = TEXT_LIGHT
        r2 = add_r(p, b_desc)
        r2.font.size = Pt(9.0)
        r2.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 4 — TOOLS AND TECHNOLOGIES
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Technology Stack & Pipeline", "Engine, Rendering, Physics, and Audio Middleware")

    tech_boxes = [
        ("Game Engine", "Unity 6 (6000.5.9f1)", "High-performance C# runtime, unified build pipeline, robust profiler, and modern URP graphics features."),
        ("Render Pipeline", "Universal Render Pipeline (17.5.0)", "Optimized single-pass Forward+ rendering, custom Lit PBR materials, ACES tonemapping, and linear fog."),
        ("Input System", "Unity Input System (1.20.0)", "Event-driven cross-platform input supporting both keyboard/mouse and mobile touchscreen fallbacks."),
        ("Character Rigging", "Adobe Mixamo & Mecanim", "Humanoid avatar retargeting, baked in-place root motion, and multi-layer state machines."),
        ("Audio Pipeline", "Unity AudioMixer", "5-bus routing (Master, Music, SFX, Ambient, UI) with logarithmic dB attenuation and 4 adaptive stems."),
        ("Source Control", "Git & Git LFS", "Version control with Git Large File Storage tracking high-resolution 3D models (FBX), audio (WAV), and PBR textures.")
    ]
    for i, (t_title, t_tech, t_desc) in enumerate(tech_boxes):
        col = i % 3
        row = i // 3
        left = Inches(0.8 + col * 3.95)
        top = Inches(1.8 + row * 2.65)
        add_card(s4, left, top, Inches(3.75), Inches(2.4))

        tb = s4.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), Inches(3.35), Inches(2.0))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.space_after = Pt(2)
        r = add_r(p, t_title.upper())
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = CRIMSON

        p = tf.add_paragraph()
        p.space_after = Pt(4)
        r = add_r(p, t_tech)
        r.font.bold = True
        r.font.size = Pt(12)
        r.font.color.rgb = TEXT_LIGHT

        p = tf.add_paragraph()
        r = add_r(p, t_desc)
        r.font.size = Pt(8.8)
        r.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 5 — SYSTEM ARCHITECTURE
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Software Architecture & Modularity", "Decoupled Component-Based Architecture and Subsystems")

    systems = [
        ("Player Subsystem", "Locomotion & Kinematics", [
            "PlayerController: 3-lane horizontal lerp (-3, 0, +3m) at 14 m/s.",
            "Kinematic Jump: Grounded launch vy = sqrt(2gh) at g = -20 m/s².",
            "Combat Slide: CharacterController height 2.0m -> 1.05m.",
            "PlayerHealth: Invulnerability frames, shield absorption, death events."
        ]),
        ("Combat & Pooling", "Raycast & Particle VFX", [
            "ShootingController: Forward hitscan with auto-aim cone (<=12°).",
            "Weapon Recoil: Visual kickback (0.07m displacement, 3.5° climb).",
            "BulletTracer: Interpolated glowing raycast tracer lines.",
            "HitImpactManager: Pre-warmed zero-allocation blood/spark pools."
        ]),
        ("Enemy AI Subsystem", "FSM & ScriptableObjects", [
            "ZombieSpawner: Lane-aware spawner with alive limits (max 6).",
            "ZombieController: Mecanim FSM (Idle, Walk, Run, Attack, Hit, Death).",
            "ZombieConfig: Modular ScriptableObject data architecture.",
            "ZombieSoundEmitter: Logarithmic 3D spatial audio attenuation."
        ]),
        ("World & UI Systems", "Streaming & Persistence", [
            "EndlessRoadManager: Circular 5-segment pool of 30m road sections.",
            "EnvironmentThemeManager: 45m smooth trilight & fog blending.",
            "GameManager: Global finite state machine (Play, Pause, GameOver).",
            "SaveManager & ScoreManager: PlayerPrefs high score & banked coins."
        ])
    ]
    for i, (sys_title, sys_sub, sys_bullets) in enumerate(systems):
        left = Inches(0.8 + i * 2.96)
        top = Inches(1.8)
        add_card(s5, left, top, Inches(2.82), Inches(4.3))

        tb = s5.shapes.add_textbox(left + Inches(0.18), top + Inches(0.18), Inches(2.46), Inches(3.95))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.space_after = Pt(2)
        r = add_r(p, sys_title)
        r.font.bold = True
        r.font.size = Pt(11)
        r.font.color.rgb = CRIMSON

        p = tf.add_paragraph()
        p.space_after = Pt(6)
        r = add_r(p, sys_sub)
        r.font.size = Pt(8.5)
        r.font.italic = True
        r.font.color.rgb = CYAN_ACCENT

        for b in sys_bullets:
            p = tf.add_paragraph()
            p.space_after = Pt(4)
            r = add_r(p, "- " + b)
            r.font.size = Pt(8.2)
            r.font.color.rgb = TEXT_MUTED

    add_card(s5, Inches(0.8), Inches(6.25), Inches(11.733), Inches(0.85))
    tb_b = s5.shapes.add_textbox(Inches(1.0), Inches(6.3), Inches(11.333), Inches(0.75))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True
    p = tf_b.paragraphs[0]
    r1 = add_r(p, "KEY ARCHITECTURAL DECOUPLING: ")
    r1.font.bold = True
    r1.font.size = Pt(9.5)
    r1.font.color.rgb = CRIMSON
    r2 = add_r(p, "All damageable entities (Common/Fast/Heavy zombies, player health, and explosive barrels) implement the IDamageable interface. The weapon raycast system remains completely agnostic of enemy classes, ensuring clean decoupling and zero class dependencies.")
    r2.font.size = Pt(9.0)
    r2.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 6 — CORE GAMEPLAY MECHANICS
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Core Gameplay Mechanics", "Locomotion, Ballistics, Raycast Combat, and Resource Economy")

    mech_items = [
        ("Three-Lane Locomotion", "Discrete lane snapping at X = -3.0m, 0.0m, +3.0m using smooth frame-rate independent interpolation (14 m/s). Progressive speed acceleration from 8.0 m/s to 16.0 m/s."),
        ("Jump & Slide Physics", "Kinematic vertical launch vy = sqrt(2gh) (h = 1.8m, g = -20 m/s²). Timed slide (0.8s) reduces CharacterController height from 2.0m to 1.05m while preserving humanoid mesh proportions."),
        ("Raycast Combat & Recoil", "Forward hitscan with dynamic auto-aim cone (<=12°). Firing inflicts IDamageable damage, produces 0.07m visual kickback & 3.5° muzzle climb, and spawns glowing bullet tracers."),
        ("Scavenging & Economy", "Gold coins bank permanently across runs. Ammunition boxes refill +15 rounds; medical kits restore +25 HP. 4 timed power-ups: Shield, Coin Magnet, Speed Boost, Double Coins.")
    ]
    for i, (m_title, m_desc) in enumerate(mech_items):
        top = Inches(1.8 + i * 1.3)
        add_card(s6, Inches(0.8), top, Inches(6.2), Inches(1.2))
        tb = s6.shapes.add_textbox(Inches(1.0), top + Inches(0.12), Inches(5.8), Inches(0.95))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.space_after = Pt(2)
        r = add_r(p, m_title)
        r.font.bold = True
        r.font.size = Pt(11)
        r.font.color.rgb = CRIMSON
        p = tf.add_paragraph()
        r = add_r(p, m_desc)
        r.font.size = Pt(8.8)
        r.font.color.rgb = TEXT_MUTED

    ctrl_path = os.path.join(screenshots_dir, "05_Controls_Guide_Modal.png")
    if os.path.exists(ctrl_path):
        add_card(s6, Inches(7.3), Inches(1.8), Inches(5.2), Inches(5.2))
        s6.shapes.add_picture(ctrl_path, Inches(7.4), Inches(1.9), Inches(5.0), Inches(4.5))
        tb_c = s6.shapes.add_textbox(Inches(7.4), Inches(6.5), Inches(5.0), Inches(0.4))
        p_c = tb_c.text_frame.paragraphs[0]
        p_c.alignment = PP_ALIGN.CENTER
        r_c = add_r(p_c, "Figure: In-game input controls reference guide modal (Keyboard & Mouse)")
        r_c.font.size = Pt(8.5)
        r_c.font.italic = True
        r_c.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 7 — ENVIRONMENT DESIGN
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Environment & Visual Design", "Dual Biome Streaming and Calibrated Volumetric Lighting")

    add_card(s7, Inches(0.8), Inches(1.8), Inches(5.7), Inches(2.55))
    tb = s7.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(5.3), Inches(2.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.space_after = Pt(2)
    r = add_r(p, "ABANDONED CITY RUINS BIOME")
    r.font.bold = True
    r.font.size = Pt(11.5)
    r.font.color.rgb = CRIMSON

    bullets_city = [
        "Architecture: Crumbling multi-story brick facades, cracked asphalt, worn lane markings.",
        "Obstacles & Props: Concrete barricades, roadblock barriers, abandoned cars, explosive barrels.",
        "Lighting: Directional cool-blue moonlight (#C0D6FA, 1.75 intensity) and flickering sodium streetlights."
    ]
    for b in bullets_city:
        p = tf.add_paragraph()
        p.space_after = Pt(2)
        r = add_r(p, "- " + b)
        r.font.size = Pt(8.5)
        r.font.color.rgb = TEXT_MUTED

    add_card(s7, Inches(0.8), Inches(4.5), Inches(5.7), Inches(2.55))
    tb = s7.shapes.add_textbox(Inches(1.0), Inches(4.6), Inches(5.3), Inches(2.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.space_after = Pt(2)
    r = add_r(p, "SUBTERRANEAN SUBWAY TUNNEL BIOME")
    r.font.bold = True
    r.font.size = Pt(11.5)
    r.font.color.rgb = CYAN_ACCENT

    bullets_tun = [
        "Enclosure: Continuous solid 5.2m concrete side walls and 15.5m ceiling with 45° vaulted arches.",
        "Structural Ribs: Heavy portal columns spaced every 7.5m, industrial ventilation shafts, steel tracks.",
        "Luminaires: Balanced 4200K neutral ceiling luminaires & 2200K amber caged emergency bulkheads."
    ]
    for b in bullets_tun:
        p = tf.add_paragraph()
        p.space_after = Pt(2)
        r = add_r(p, "- " + b)
        r.font.size = Pt(8.5)
        r.font.color.rgb = TEXT_MUTED

    img_city = os.path.join(screenshots_dir, "03_City_Environment_Atmosphere.png")
    img_tun = os.path.join(screenshots_dir, "09_Subway_Tunnel_Materials.png")

    if os.path.exists(img_city):
        add_card(s7, Inches(6.8), Inches(1.8), Inches(5.7), Inches(2.55))
        s7.shapes.add_picture(img_city, Inches(6.9), Inches(1.9), Inches(5.5), Inches(2.05))
        tb_c = s7.shapes.add_textbox(Inches(6.9), Inches(4.0), Inches(5.5), Inches(0.3))
        p = tb_c.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = add_r(p, "Figure: Nocturnal city ruins environment with cool-blue moonlight and fog")
        r.font.size = Pt(8.0)
        r.font.italic = True
        r.font.color.rgb = TEXT_MUTED

    if os.path.exists(img_tun):
        add_card(s7, Inches(6.8), Inches(4.5), Inches(5.7), Inches(2.55))
        s7.shapes.add_picture(img_tun, Inches(6.9), Inches(4.6), Inches(5.5), Inches(2.05))
        tb_c = s7.shapes.add_textbox(Inches(6.9), Inches(6.7), Inches(5.5), Inches(0.3))
        p = tb_c.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = add_r(p, "Figure: Authored PBR texture maps for Subway Tunnel concrete, hazard plinths, and steel")
        r.font.size = Pt(8.0)
        r.font.italic = True
        r.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 8 — ZOMBIE AI AND COMBAT
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Zombie AI & Combat System", "Modular Archetypes, Mecanim State Machines, and Audio Depth")

    z_archetypes = [
        ("Common Runner Zombie", "Mixamo Ch10 (Humanoid)", "3 HP (3 shots)", "5.0 m/s", "10 DMG / 1.8m range", "100 pts", "Balanced threat spawning across lanes. Claws and lunges at player when in range."),
        ("Fast Sprinter Zombie", "Mixamo Yaku J Ignite", "2 HP (2 shots)", "7.5 m/s", "8 DMG / 1.6m range", "150 pts", "High velocity agile ambusher. Forces rapid lane evasion and quick auto-aim reflex fire."),
        ("Heavy Brute Zombie", "Mixamo Pumpkinhulk", "8 HP (8 shots)", "3.2 m/s", "25 DMG / 2.2m range", "250 pts", "Massive tank requiring sustained gunfire. Deals devastating damage on impact.")
    ]
    for i, (z_name, z_rig, z_hp, z_spd, z_dmg, z_pts, z_desc) in enumerate(z_archetypes):
        top = Inches(1.8 + i * 1.7)
        add_card(s8, Inches(0.8), top, Inches(6.0), Inches(1.55))
        tb = s8.shapes.add_textbox(Inches(1.0), top + Inches(0.1), Inches(5.6), Inches(1.35))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.space_after = Pt(2)
        r = add_r(p, z_name.upper())
        r.font.bold = True
        r.font.size = Pt(11)
        r.font.color.rgb = CRIMSON
        r2 = add_r(p, f"  |  {z_hp}  |  Speed: {z_spd}  |  Score: {z_pts}")
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = CYAN_ACCENT

        p = tf.add_paragraph()
        r = add_r(p, f"Rig: {z_rig}  *  Combat: {z_dmg}\n{z_desc}")
        r.font.size = Pt(8.5)
        r.font.color.rgb = TEXT_MUTED

    z_img = os.path.join(screenshots_dir, "08_Zombie_Archetypes_Textures.png")
    if os.path.exists(z_img):
        add_card(s8, Inches(7.1), Inches(1.8), Inches(5.4), Inches(2.6))
        s8.shapes.add_picture(z_img, Inches(7.2), Inches(1.9), Inches(5.2), Inches(2.1))
        tb_c = s8.shapes.add_textbox(Inches(7.2), Inches(4.05), Inches(5.2), Inches(0.3))
        p = tb_c.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = add_r(p, "Figure: Diffuse texture maps for Common, Fast Runner, and Heavy Brute zombies")
        r.font.size = Pt(8.0)
        r.font.italic = True
        r.font.color.rgb = TEXT_MUTED

    add_card(s8, Inches(7.1), Inches(4.55), Inches(5.4), Inches(2.45))
    tb_r = s8.shapes.add_textbox(Inches(7.3), Inches(4.65), Inches(5.0), Inches(2.25))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.space_after = Pt(4)
    r = add_r(p, "COMBAT & AI BEHAVIOR HIGHLIGHTS")
    r.font.bold = True
    r.font.size = Pt(11)
    r.font.color.rgb = CRIMSON

    bullets_ai = [
        ("Damage Metric: ", "Firearm deals exactly 1 damage point per shot. Common takes 3 hits, Fast takes 2 hits, Heavy takes 8 hits."),
        ("State Machine: ", "Transitions between Idle, Walk, Run, Attack, Hit Reaction flinch, and lethal collapse with baked in-place root motion."),
        ("3D Spatial Audio: ", "ZombieSoundEmitter provides logarithmic positional audio (2.5m to 24m) for directional threat awareness."),
        ("GC-Free Pooling: ", "HitImpactManager pre-warms blood splatters, sparks, and bullet tracers with zero heap allocations per shot.")
    ]
    for b_title, b_desc in bullets_ai:
        p = tf_r.add_paragraph()
        p.space_after = Pt(2)
        r1 = add_r(p, b_title)
        r1.font.bold = True
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = TEXT_LIGHT
        r2 = add_r(p, b_desc)
        r2.font.size = Pt(8.2)
        r2.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 9 — USER INTERFACE AND GAME FLOW
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "User Interface & Game Flow", "Main Menu Staging, HUD Feedback, and State Progression")

    add_card(s9, Inches(0.8), Inches(1.8), Inches(6.0), Inches(5.2))
    tb = s9.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.4), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.space_after = Pt(6)
    r = add_r(p, "SEAMLESS GAME STATE TRANSITIONS")
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = CRIMSON

    p = tf.add_paragraph()
    p.space_after = Pt(8)
    r = add_r(p, "Main Menu  ->  Active Gameplay  ->  Game Over  ->  Retry / Revive / Menu")
    r.font.bold = True
    r.font.size = Pt(10)
    r.font.color.rgb = CYAN_ACCENT

    bullets_ui = [
        ("3D Main Menu Staging: ", "Features an animated survivor character (Ch05) holding the Tommy Gun on a nocturnal street, accompanied by cinematic camera panning and multi-tab settings."),
        ("In-Game Survival HUD: ", "Real-time TextMeshPro meters for distance (m), score (Distance + Kills), coin inventory, ammunition reserve, segmented health bar, and power-up countdowns."),
        ("Game Over & Record Celebration: ", "Summarizes run statistics alongside persistent high scores loaded from PlayerPrefs. Surpassing the record triggers a prominent '(NEW BEST!)' celebratory banner."),
        ("One-Time Shielded Revive Loop: ", "Players can trigger a single revive per run, granting full health, +30 ammunition rounds, and a 3-second invulnerability shield before resuming traversal."),
        ("Cross-Platform Adaptation: ", "SafeAreaFitter queries Screen.safeArea, ensuring UI buttons and indicators avoid mobile camera notches and cutouts.")
    ]
    for b_title, b_desc in bullets_ui:
        p = tf.add_paragraph()
        p.space_after = Pt(5)
        r1 = add_r(p, b_title)
        r1.font.bold = True
        r1.font.size = Pt(9.2)
        r1.font.color.rgb = TEXT_LIGHT
        r2 = add_r(p, b_desc)
        r2.font.size = Pt(8.8)
        r2.font.color.rgb = TEXT_MUTED

    menu_path = os.path.join(screenshots_dir, "01_Title_Screen_Overview.png")
    if os.path.exists(menu_path):
        add_card(s9, Inches(7.1), Inches(1.8), Inches(5.4), Inches(5.2))
        s9.shapes.add_picture(menu_path, Inches(7.2), Inches(1.9), Inches(5.2), Inches(4.5))
        tb_c = s9.shapes.add_textbox(Inches(7.2), Inches(6.5), Inches(5.2), Inches(0.4))
        p_c = tb_c.text_frame.paragraphs[0]
        p_c.alignment = PP_ALIGN.CENTER
        r_c = add_r(p_c, "Figure: 3D Main Menu scene with survivor character staging, title, and buttons")
        r_c.font.size = Pt(8.5)
        r_c.font.italic = True
        r_c.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 10 — IMPLEMENTATION, TESTING & DEBUGGING
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Verification, Refactoring & Optimization", "Iterative Engineering Workflow and Documented Technical Fixes")

    add_card(s10, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.2))
    tb = s10.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.1), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.space_after = Pt(6)
    r = add_r(p, "DEVELOPMENT & VERIFICATION WORKFLOW")
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = CYAN_ACCENT

    bullets_test = [
        ("Automated Editor Audits: ", "Custom C# validation tools (ZombieCombatSystemValidator.cs, VisualAuditHelper.cs) automated hierarchy, avatar bone binding, and material audits."),
        ("Play Mode Systems Testing: ", "Validated lane-switch clamping (-3m to +3m), airborne jump locking, power-up timer refresh logic, and PlayerPrefs score persistence."),
        ("Memory & GC Profiling: ", "Profiler audits verified 0 bytes of heap allocation during active running by pooling road segments, enemies, bullet tracers, and particle VFX."),
        ("Windows Standalone Build: ", "Verified smooth 60 FPS gameplay execution with native keyboard and mouse controls on Windows PC."),
        ("Verified Android Build: ", "Completed automated Android build pipeline, producing Builds/Android/ZombieRunner.apk (42.9 MB, IL2CPP 64-bit, ARM64, minimum API 26) with zero compilation errors.")
    ]
    for b_title, b_desc in bullets_test:
        p = tf.add_paragraph()
        p.space_after = Pt(5)
        r1 = add_r(p, b_title)
        r1.font.bold = True
        r1.font.size = Pt(9.2)
        r1.font.color.rgb = TEXT_LIGHT
        r2 = add_r(p, b_desc)
        r2.font.size = Pt(8.6)
        r2.font.color.rgb = TEXT_MUTED

    add_card(s10, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.2))
    tb = s10.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.space_after = Pt(6)
    r = add_r(p, "SIX DOCUMENTED ENGINEERING FIXES")
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = CRIMSON

    fixes = [
        ("1. Slide Mesh Decoupling: ", "Decoupled CharacterController height reduction (1.05m) from humanoid visual transforms, eliminating mesh squash and ground sinking."),
        ("2. Jump Launch Cancellation: ", "Added explicit isJumping flag to eliminate premature Grounded landing cancellation on launch frames."),
        ("3. Spawner Deadlock Bug: ", "Auto-destroyed trailing zombies (> 12m behind runner) without score, preventing alive counter from capping at 6 and halting spawns."),
        ("4. Particle Lifecycle Bug: ", "Instantiated GameObjects inactive before duration assignment, resolving over 100 duration mutation console errors."),
        ("5. Subway Tunnel Enclosure: ", "Reconstructed solid 30m concrete tunnel with vaulted arches, eliminating repeating rectangular frames and open daylight leakage."),
        ("6. Audio Suite Overhaul: ", "Synthesized organic 48s Brownian noise and 4 synchronized 75 BPM adaptive stems in D minor, eliminating irritating sine whistle loops.")
    ]
    for f_title, f_desc in fixes:
        p = tf.add_paragraph()
        p.space_after = Pt(4)
        r1 = add_r(p, f_title)
        r1.font.bold = True
        r1.font.size = Pt(8.8)
        r1.font.color.rgb = TEXT_LIGHT
        r2 = add_r(p, f_desc)
        r2.font.size = Pt(8.2)
        r2.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 11 — LEARNING OUTCOMES & FUTURE WORK
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Academic Evaluation & Roadmap", "Core Competencies Mastered and Proposed Future Enhancements")

    add_card(s11, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.2))
    tb = s11.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.1), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.space_after = Pt(6)
    r = add_r(p, "LEARNING OUTCOMES ACQUIRED")
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = CYAN_ACCENT

    learn_bullets = [
        ("Real-Time 3D Game Mechanics: ", "Mastered kinematic character controllers, grounded jump physics, low-clearance sliding, and lane-based traversal in Unity 6."),
        ("Universal Render Pipeline Mastery: ", "Configured custom Lit PBR materials, ACES tonemapping, Trilight ambient lighting, and balanced volumetric fog."),
        ("Animation Retargeting & State Machines: ", "Retargeted Mixamo Humanoid rigs, baked in-place root motion, and orchestrated complex Mecanim transition graphs."),
        ("Object-Oriented Game Architecture: ", "Implemented ScriptableObject data encapsulation, interface-based messaging (IDamageable), and zero-allocation circular object pooling."),
        ("Dynamic Audio Systems: ", "Engineered 4-layer synchronized adaptive horror stems, logarithmic decibel attenuation, and 3D positional sound emitters.")
    ]
    for b_title, b_desc in learn_bullets:
        p = tf.add_paragraph()
        p.space_after = Pt(6)
        r1 = add_r(p, b_title)
        r1.font.bold = True
        r1.font.size = Pt(9.2)
        r1.font.color.rgb = TEXT_LIGHT
        r2 = add_r(p, b_desc)
        r2.font.size = Pt(8.6)
        r2.font.color.rgb = TEXT_MUTED

    add_card(s11, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.2))
    tb = s11.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.space_after = Pt(6)
    r = add_r(p, "PROPOSED FUTURE ENHANCEMENTS")
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = CRIMSON

    p = tf.add_paragraph()
    p.space_after = Pt(6)
    r = add_r(p, "(Strictly proposed future extensions beyond current verified scope)")
    r.font.size = Pt(8.2)
    r.font.italic = True
    r.font.color.rgb = TEXT_MUTED

    future_bullets = [
        ("1. Advanced Flocking & Ranged Mutant AI: ", "Flocking runner hordes and acid-spitting mutants that force players to dodge incoming parabolic projectiles while running."),
        ("2. Expanded Weapon Arsenal: ", "Collectible pump shotguns (wide-spread clearing), assault rifles, and grenade launchers with dedicated ammo economies."),
        ("3. Dynamic Subway Boss Encounters: ", "Procedural tunnel breach events featuring a pursuing Nemesis juggernaut that must be damaged over sustained running distance."),
        ("4. Global Online Leaderboards: ", "RESTful cloud database integration supporting asynchronous ghost runner replays and cross-platform high-score rankings."),
        ("5. Dynamic Atmospheric Weather VFX: ", "Screen-space rain droplets, volumetric lightning strikes dynamically casting shadows, and destructible road barricades.")
    ]
    for b_title, b_desc in future_bullets:
        p = tf.add_paragraph()
        p.space_after = Pt(6)
        r1 = add_r(p, b_title)
        r1.font.bold = True
        r1.font.size = Pt(9.0)
        r1.font.color.rgb = TEXT_LIGHT
        r2 = add_r(p, b_desc)
        r2.font.size = Pt(8.4)
        r2.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 12 — CONCLUSION AND THANK YOU
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)

    hero_path = os.path.join(screenshots_dir, "01_Title_Screen_Overview.png")
    if os.path.exists(hero_path):
        s12.shapes.add_picture(hero_path, Inches(7.5), Inches(0), Inches(5.833), Inches(7.5))
        fader = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(7.48), Inches(0), Inches(0.8), Inches(7.5))
        fader.fill.solid()
        fader.fill.fore_color.rgb = BG_DARK
        fader.line.fill.background()

    add_card(s12, Inches(0.8), Inches(0.6), Inches(6.8), Inches(6.3))
    tb12 = s12.shapes.add_textbox(Inches(1.1), Inches(0.8), Inches(6.2), Inches(5.9))
    tf12 = tb12.text_frame
    tf12.word_wrap = True
    tf12.margin_left = tf12.margin_top = tf12.margin_right = tf12.margin_bottom = 0

    p = tf12.paragraphs[0]
    p.space_after = Pt(4)
    r = add_r(p, "ACADEMIC PROJECT CONCLUSION")
    r.font.name = "Calibri"
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = CRIMSON

    p = tf12.add_paragraph()
    p.space_after = Pt(8)
    r = add_r(p, "Zombie Runner - 3D Survival Horror Endless Runner")
    r.font.name = "Calibri"
    r.font.size = Pt(20)
    r.font.bold = True
    r.font.color.rgb = TEXT_LIGHT

    p = tf12.add_paragraph()
    p.space_after = Pt(12)
    r = add_r(p, "Successfully conceived, architected, and optimized an innovative hybrid survival-horror endless runner fulfilling all rigorous academic criteria for Game Mechanics, Design and Development (23CS201PE407).")
    r.font.size = Pt(9.8)
    r.font.color.rgb = TEXT_MUTED

    p = tf12.add_paragraph()
    p.space_after = Pt(4)
    r = add_r(p, "Sincere Academic Gratitude:")
    r.font.bold = True
    r.font.size = Pt(11)
    r.font.color.rgb = CYAN_ACCENT

    p = tf12.add_paragraph()
    p.space_after = Pt(10)
    r = add_r(p, "Special thanks to our Course Coordinator & Instructor, Dr. Vijaya Chandra Jadala Sir, for his continuous guidance, technical encouragement, and pedagogical leadership.")
    r.font.size = Pt(9.5)
    r.font.color.rgb = TEXT_LIGHT

    p = tf12.add_paragraph()
    p.space_after = Pt(4)
    r = add_r(p, "Project Development Team:")
    r.font.bold = True
    r.font.size = Pt(10.5)
    r.font.color.rgb = CRIMSON

    for tm in team_list:
        p = tf12.add_paragraph()
        p.space_after = Pt(1.5)
        r = add_r(p, tm)
        r.font.size = Pt(9.0)
        r.font.color.rgb = TEXT_MUTED

    p = tf12.add_paragraph()
    p.space_before = Pt(12)
    r = add_r(p, "THANK YOU! QUESTIONS & DISCUSSION WELCOME.")
    r.font.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = CRIMSON

    if os.path.exists(logo_path):
        s12.shapes.add_picture(logo_path, Inches(6.4), Inches(0.85), Inches(1.0), Inches(1.0))

    prs.save(out_pptx_path)
    print(f"PowerPoint Presentation created successfully at: {out_pptx_path}")

if __name__ == "__main__":
    out_file = os.path.abspath(r"E:\zombie runner\Zombie_Runner_Project_Presentation.pptx")
    build_presentation(out_file)
