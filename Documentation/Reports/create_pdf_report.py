import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            # Suppress header and footer on the cover page
            return

        self.saveState()
        self.setFont("Helvetica-Oblique", 8)
        self.setFillColor(colors.HexColor("#788CA0"))

        # Running Header
        header_text = "Zombie Runner: 3D Survival Horror Endless Runner | SR University"
        self.drawRightString(letter[0] - 54, letter[1] - 34, header_text)
        self.setStrokeColor(colors.HexColor("#D0DCE5"))
        self.setLineWidth(0.5)
        self.line(54, letter[1] - 38, letter[0] - 54, letter[1] - 38)

        # Running Footer
        footer_left = "School of Computer Science & Artificial Intelligence"
        footer_right = f"Page {self._pageNumber} of {page_count}"
        self.drawString(54, 30, footer_left)
        self.drawRightString(letter[0] - 54, 30, footer_right)
        self.line(54, 40, letter[0] - 54, 40)

        self.restoreState()

def create_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()
    
    PRIMARY = colors.HexColor("#0B3B60")
    SECONDARY = colors.HexColor("#1F4E79")
    DARK = colors.HexColor("#282828")
    MUTED = colors.HexColor("#5A6978")

    # Custom Paragraph Styles
    style_cover_super = ParagraphStyle('CoverSuper', fontName='Helvetica-Bold', fontSize=15, leading=18, textColor=PRIMARY, alignment=TA_CENTER)
    style_cover_for = ParagraphStyle('CoverFor', fontName='Helvetica-Oblique', fontSize=11, leading=14, textColor=DARK, alignment=TA_CENTER)
    style_cover_course = ParagraphStyle('CoverCourse', fontName='Helvetica-Bold', fontSize=12.5, leading=15.5, textColor=PRIMARY, alignment=TA_CENTER)
    style_cover_code = ParagraphStyle('CoverCode', fontName='Helvetica-Bold', fontSize=11.5, leading=14, textColor=DARK, alignment=TA_CENTER)
    style_cover_title = ParagraphStyle('CoverTitle', fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=SECONDARY, alignment=TA_CENTER)
    
    style_h1 = ParagraphStyle('AcademicH1', fontName='Helvetica-Bold', fontSize=12, leading=14.5, textColor=PRIMARY, spaceBefore=7, spaceAfter=2.5, keepWithNext=True)
    style_h2 = ParagraphStyle('AcademicH2', fontName='Helvetica-Bold', fontSize=9.8, leading=12, textColor=SECONDARY, spaceBefore=4.5, spaceAfter=2, keepWithNext=True)
    style_body = ParagraphStyle('AcademicBody', fontName='Helvetica', fontSize=8.2, leading=10.4, textColor=DARK, alignment=TA_JUSTIFY, spaceAfter=2.5)
    style_bullet = ParagraphStyle('AcademicBullet', fontName='Helvetica', fontSize=8.0, leading=10.0, textColor=DARK, alignment=TA_JUSTIFY, leftIndent=12, spaceAfter=1.5)
    
    style_th = ParagraphStyle('TableH', fontName='Helvetica-Bold', fontSize=7.6, leading=9.2, textColor=colors.white, alignment=TA_CENTER)
    style_td = ParagraphStyle('TableD', fontName='Helvetica', fontSize=7.4, leading=9.0, textColor=DARK)
    style_td_bold = ParagraphStyle('TableDBold', fontName='Helvetica-Bold', fontSize=7.4, leading=9.0, textColor=DARK)
    style_td_center = ParagraphStyle('TableDCenter', fontName='Helvetica', fontSize=7.4, leading=9.0, textColor=DARK, alignment=TA_CENTER)
    
    style_caption = ParagraphStyle('FigureCap', fontName='Helvetica-Oblique', fontSize=7.2, leading=8.5, textColor=MUTED, alignment=TA_CENTER, spaceBefore=1.5, spaceAfter=3)
    style_callout = ParagraphStyle('Callout', fontName='Helvetica', fontSize=7.6, leading=9.5, textColor=DARK, alignment=TA_JUSTIFY)

    story = []

    # ==========================================
    # 1. COVER PAGE (Matching Course Plan Reference Layout)
    # ==========================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("PROJECT REPORT", style_cover_super))
    story.append(Spacer(1, 4))
    story.append(Paragraph("For", style_cover_for))
    story.append(Spacer(1, 4))
    story.append(Paragraph("GAME MECHANICS, DESIGN AND DEVELOPMENT", style_cover_course))
    story.append(Paragraph("(COURSE CODE: 23CS201PE407)", style_cover_code))
    story.append(Spacer(1, 8))
    story.append(Paragraph("PROJECT TITLE:<br/>ZOMBIE RUNNER – 3D SURVIVAL HORROR ENDLESS RUNNER", style_cover_title))
    story.append(Spacer(1, 10))

    # Colon-aligned Course Details Table
    meta_rows = [
        [Paragraph("<b>Course Coordinator</b>", style_td), Paragraph(":", style_td_center), Paragraph("Dr. Vijaya Chandra Jadala", style_td)],
        [Paragraph("<b>Course Instructors</b>", style_td), Paragraph(":", style_td_center), Paragraph("Dr. Vijaya Chandra Jadala", style_td)],
        [Paragraph("<b>Course Type</b>", style_td), Paragraph(":", style_td_center), Paragraph("Program Elective 1 (PE1)", style_td)],
        [Paragraph("<b>Semester and Year</b>", style_td), Paragraph(":", style_td_center), Paragraph("IV Year, 1<sup>st</sup> Semester", style_td)],
        [Paragraph("<b>L-T-P</b>", style_td), Paragraph(":", style_td_center), Paragraph("2-0-2", style_td)],
        [Paragraph("<b>Credits</b>", style_td), Paragraph(":", style_td_center), Paragraph("3", style_td)],
        [Paragraph("<b>School</b>", style_td), Paragraph(":", style_td_center), Paragraph("School of Computer Science and Artificial Intelligence", style_td)],
        [Paragraph("<b>Department</b>", style_td), Paragraph(":", style_td_center), Paragraph("Department of Computer Science and Artificial Intelligence", style_td)],
        [Paragraph("<b>Course Level</b>", style_td), Paragraph(":", style_td_center), Paragraph("Undergraduate (UG)", style_td)]
    ]
    t_meta = Table(meta_rows, colWidths=[150, 15, 339])
    t_meta.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 10))

    # Team Members Block
    story.append(Paragraph("<b>Submitted by Team Members:</b>", ParagraphStyle('TeamH', fontName='Helvetica-Bold', fontSize=9.5, leading=12, textColor=PRIMARY)))
    story.append(Spacer(1, 3))
    team_rows = [
        [Paragraph("1.", style_td_bold), Paragraph("J. Radha Krishna", style_td_bold), Paragraph("Roll No: 2303A52055", style_td)],
        [Paragraph("2.", style_td_bold), Paragraph("P. Makesh Babu", style_td_bold), Paragraph("Roll No: 2303A52061", style_td)],
        [Paragraph("3.", style_td_bold), Paragraph("M. Omprakash", style_td_bold), Paragraph("Roll No: 2303A52057", style_td)],
        [Paragraph("4.", style_td_bold), Paragraph("V. Siddharatha", style_td_bold), Paragraph("Roll No: 2303A52463", style_td)]
    ]
    t_team = Table(team_rows, colWidths=[25, 230, 249])
    t_team.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_team)
    story.append(Spacer(1, 12))

    # Bottom Department, Logo, and University
    story.append(Paragraph("<b>School of Computer Science and Artificial Intelligence</b>", ParagraphStyle('SchoolH', fontName='Helvetica-Bold', fontSize=10.5, leading=13, textColor=PRIMARY, alignment=TA_CENTER)))
    story.append(Spacer(1, 6))

    logo_path = r"C:\Users\metra\.gemini\antigravity\brain\7ea1a950-c3d7-465b-a4d2-a25115ebddc3\.user_uploaded\media_1793877402347_b6c68b90.png"
    if os.path.exists(logo_path):
        img_logo = Image(logo_path, width=1.35*inch, height=1.35*inch)
        img_logo.hAlign = 'CENTER'
        story.append(img_logo)
        story.append(Spacer(1, 6))

    story.append(Paragraph("<b>SR University</b>", ParagraphStyle('UnivH', fontName='Helvetica-Bold', fontSize=12, leading=14.5, textColor=PRIMARY, alignment=TA_CENTER)))
    story.append(Paragraph("Ananthasagar, Hasanparthy, Warangal, Telangana – 506371<br/>Academic Year: 2026–2027 | Date of Submission: November 2026", ParagraphStyle('UnivSub', fontName='Helvetica', fontSize=8.2, leading=10.5, textColor=MUTED, alignment=TA_CENTER)))

    story.append(PageBreak())

    # ==========================================
    # 2. ACKNOWLEDGEMENT & 3. ABSTRACT
    # ==========================================
    story.append(Paragraph("2. Acknowledgement", style_h1))
    story.append(Paragraph("We express our deepest and most sincere gratitude to our esteemed Course Coordinator and Instructor, <b>Dr. Vijaya Chandra Jadala</b>, for his invaluable guidance, technical insight, continuous academic encouragement, and constructive critique throughout the conception, architectural design, implementation, and testing of <i>Zombie Runner – 3D Survival Horror Endless Runner</i>. His pedagogical emphasis on rigorous software architecture, real-time computational performance, and mechanical design in <b>Game Mechanics, Design and Development (23CS201PE407)</b> was fundamental in elevating this work from a prototype into an optimized, robust game.", style_body))
    story.append(Paragraph("We also extend our grateful appreciation to the leadership and faculty of the School of Computer Science and Artificial Intelligence at SR University for providing state-of-the-art computational infrastructure, modern gaming laboratories, and an inspiring academic environment conducive to advanced interactive media engineering.", style_body))
    story.append(Paragraph("Finally, we thank our peers and academic colleagues who participated in usability trials, playtesting audits, and gameplay balancing sessions. Their critical feedback on controls, combat responsiveness, and horror audio-visual immersion provided invaluable qualitative data that refined the game's mechanics and user experience.", style_body))

    story.append(Spacer(1, 4))
    story.append(Paragraph("3. Abstract", style_h1))
    story.append(Paragraph("This project report documents the design, architectural implementation, optimization, and evaluation of <b>Zombie Runner</b>, an advanced 3D endless survival horror runner game engineered in <b>Unity 6 (6000.5.9f1)</b> utilizing the <b>Universal Render Pipeline (URP 17.5.0)</b> and <b>C# (.NET Standard 2.1)</b>. Moving beyond conventional endless runners that rely exclusively on passive obstacle dodging, Zombie Runner introduces an active survival horror combat loop. The player navigates an apocalyptic landscape spanning crumbling urban ruins and subterranean subway tunnels across three discrete lanes, executing grounded jumps, low-clearance combat slides, and forward raycast shooting against dynamic undead threats.", style_body))
    story.append(Paragraph("The game architecture features: (1) an endless modular procedural environment streaming system with 30-meter road and subway tunnel segments recycling dynamically in a 5-segment circular object pool; (2) a modular enemy AI system utilizing ScriptableObjects to configure distinct zombie archetypes—Common Runner, Fast Sprinter, and Heavy Brute—governed by Mecanim finite state machines and 3D spatialized logarithmic audio emitters; (3) a responsive combat engine with forward raycasting, auto-aim target tracking, weapon recoil kinematics, illuminated bullet tracers, and pre-allocated, zero-allocation particle impact pooling; (4) a 4-tier adaptive horror music system that seamlessly crossfades between exploration, tension, active combat, and critical health states; and (5) a persistent player economy tracking gold coins, ammunition reserves, medical supplies, high scores, and a single shielded revive loop.", style_body))
    story.append(Paragraph("Performance profiling confirms stable 60 frames per second (FPS) execution with minimal memory allocations, eliminating Garbage Collection stutter. The complete codebase, assets, and Android build configurations are integrated cleanly, fulfilling the rigorous learning objectives of modern game development.", style_body))
    story.append(Paragraph("<b>Keywords:</b> Game Mechanics, 3D Endless Runner, Survival Horror, Unity 6, Universal Render Pipeline (URP), Finite State Machine, Zombie AI, Raycast Combat, Object Pooling, Adaptive Audio.", style_body))

    story.append(PageBreak())

    # ==========================================
    # 4. TABLE OF CONTENTS & LIST OF FIGURES/TABLES
    # ==========================================
    story.append(Paragraph("4. Table of Contents", style_h1))
    
    toc_data = [
        [Paragraph("<b>1. Cover Page</b>", style_td), Paragraph("<b>1</b>", style_td_center), Paragraph("<b>11. Environment and Visual Design</b>", style_td), Paragraph("<b>7</b>", style_td_center)],
        [Paragraph("<b>2. Acknowledgement</b>", style_td), Paragraph("<b>2</b>", style_td_center), Paragraph("<b>12. Zombie AI and Combat System</b>", style_td), Paragraph("<b>8</b>", style_td_center)],
        [Paragraph("<b>3. Abstract</b>", style_td), Paragraph("<b>2</b>", style_td_center), Paragraph("<b>13. User Interface and Game Flow</b>", style_td), Paragraph("<b>9</b>", style_td_center)],
        [Paragraph("<b>4. Table of Contents & Lists of Visual Assets</b>", style_td), Paragraph("<b>3</b>", style_td_center), Paragraph("<b>14. Implementation Overview</b>", style_td), Paragraph("<b>9</b>", style_td_center)],
        [Paragraph("<b>5. Introduction</b>", style_td), Paragraph("<b>4</b>", style_td_center), Paragraph("<b>15. Testing and Debugging</b>", style_td), Paragraph("<b>10</b>", style_td_center)],
        [Paragraph("<b>6. Problem Statement</b>", style_td), Paragraph("<b>4</b>", style_td_center), Paragraph("<b>16. Challenges and Solutions</b>", style_td), Paragraph("<b>10</b>", style_td_center)],
        [Paragraph("<b>7. Objectives and Scope</b>", style_td), Paragraph("<b>4</b>", style_td_center), Paragraph("<b>17. Learning Outcomes</b>", style_td), Paragraph("<b>11</b>", style_td_center)],
        [Paragraph("<b>8. Tools and Technologies</b>", style_td), Paragraph("<b>5</b>", style_td_center), Paragraph("<b>18. Future Enhancements</b>", style_td), Paragraph("<b>11</b>", style_td_center)],
        [Paragraph("<b>9. System Design and Architecture</b>", style_td), Paragraph("<b>5</b>", style_td_center), Paragraph("<b>19. Conclusion</b>", style_td), Paragraph("<b>11</b>", style_td_center)],
        [Paragraph("<b>10. Gameplay Mechanics and Controls</b>", style_td), Paragraph("<b>6</b>", style_td_center), Paragraph("<b>20. References and Asset Credits</b>", style_td), Paragraph("<b>11</b>", style_td_center)],
    ]
    t_toc = Table(toc_data, colWidths=[210, 35, 224, 35])
    t_toc.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LINEBELOW', (0,0), (-1,-1), 0.3, colors.HexColor("#E2E8F0")),
    ]))
    story.append(t_toc)
    story.append(Spacer(1, 6))

    story.append(Paragraph("List of Figures", style_h2))
    figs = [
        ("Figure 1", "Title Screen and 3D Survivor Character Staging (Audit_MainMenu_1_Overview)", "Page 6"),
        ("Figure 2", "Main Menu Settings: Audio Mixer Bus Controls and Volume Persistence", "Page 7"),
        ("Figure 3", "Keyboard and Mouse Input Configuration Reference Guide", "Page 8"),
        ("Figure 4", "In-Game Nocturnal Environment and Atmospheric Lighting Transition", "Page 9")
    ]
    for fid, fdesc, fp in figs:
        story.append(Paragraph(f"<b>{fid}:</b> {fdesc} <font color='#5A6978'>........................................................................... {fp}</font>", style_bullet))

    story.append(Spacer(1, 4))
    story.append(Paragraph("List of Tables", style_h2))
    tbls = [
        ("Table 1", "Primary Technology Stack and Engine Specifications", "Page 5"),
        ("Table 2", "Core System Architecture and Manager Responsibilities", "Page 5"),
        ("Table 3", "Player Locomotion, Kinematics, and Input Controls Reference", "Page 6"),
        ("Table 4", "Zombie Enemy Archetypes and Behavioral Specifications", "Page 8"),
        ("Table 5", "Collectibles, Economy, and Power-Up Specifications", "Page 8"),
        ("Table 6", "Key Implementation Scripts and Software Module Directory", "Page 9")
    ]
    for tid, tdesc, tp in tbls:
        story.append(Paragraph(f"<b>{tid}:</b> {tdesc} <font color='#5A6978'>........................................................................... {tp}</font>", style_bullet))

    story.append(PageBreak())

    # ==========================================
    # 5. INTRODUCTION, 6. PROBLEM STATEMENT, 7. OBJECTIVES
    # ==========================================
    story.append(Paragraph("5. Introduction", style_h1))
    story.append(Paragraph("<b>5.1 Context and Evolution of the Genre:</b> The endless runner genre represents one of the most commercially resilient and mechanically focused archetypes in video game design. Originally popularized by mobile pioneers such as Canabalt, Temple Run, and Subway Surfers, the genre traditionally challenges players with reflex-driven avoidance of obstacles across an endless path. However, classic runners frequently suffer from mechanical fatigue: player actions are constrained strictly to passive evasion (jumping, ducking, shifting lanes), with no offensive capability or resource management. Consequently, modern game design trends toward hybrid genres that fuse high-speed traversal with real-time shooting and atmospheric horror.", style_body))
    story.append(Paragraph("<b>5.2 Project Overview and Design Philosophy:</b> <i>Zombie Runner</i> was engineered to bridge fast-paced arcade runner mechanics with high-stakes survival horror. Developed in Unity 6, the game casts the player as an armed survivor navigating a post-apocalyptic cityscape and subterranean subway railway network overrun by reanimated undead. Survival demands an active synthesis of spatial agility (lane shifts, vaulting hurdles, sliding beneath barricades) and decisive firearm combat (conserving ammunition, auto-aim tracking, and neutralizing approaching zombies).", style_body))
    story.append(Paragraph("<b>5.3 Academic Motivation:</b> Authored for Game Mechanics, Design and Development (23CS201PE407) at SR University, this project synthesizes core disciplines: real-time physics simulation, procedural object pooling, finite state machine AI, Universal Render Pipeline (URP) shader customization, and dynamic spatial audio engineering.", style_body))

    story.append(Spacer(1, 3))
    story.append(Paragraph("6. Problem Statement", style_h1))
    story.append(Paragraph("Traditional endless runners present significant mechanical and architectural constraints: (1) <i>Mono-Dimensional Evasion Loop:</i> Gameplay relies entirely on passive dodging, reducing tactical depth; (2) <i>Predictable Staging:</i> Static daytime lighting and repetitive textures fail to evoke emotional immersion; (3) <i>Technical Bottlenecks in Combat Prototypes:</i> Continuous instantiation and destruction of projectiles and enemies generate heavy Garbage Collection (GC) pressure, causing visual stutter during rapid gameplay.", style_body))
    story.append(Paragraph("Zombie Runner solves these challenges through: (a) harmonizing forward player velocity (8 to 16 m/s) with real-time raycast combat; (b) implementing pre-allocated circular object pools for road sections, enemies, tracers, and VFX; (c) calibrating horror lighting with linear fog (42m-165m) and trilight ambient bounce to ensure rapid obstacle identification; and (d) engineering automated distance recycling to eliminate spawner deadlocks.", style_body))

    story.append(Spacer(1, 3))
    story.append(Paragraph("7. Objectives and Scope", style_h1))
    story.append(Paragraph("<b>7.1 Primary Objectives:</b>", style_h2))
    story.append(Paragraph("1. <b>Modular Architecture:</b> Engineer a decoupled Unity 6 C# architecture utilizing ScriptableObjects and interface-driven combat (<code>IDamageable</code>).", style_bullet))
    story.append(Paragraph("2. <b>Kinematic Locomotion:</b> Build a 3-lane CharacterController runner with grounded jump physics, low slide clearance, and progressive speed scaling.", style_bullet))
    story.append(Paragraph("3. <b>Zombie AI & Raycast Combat:</b> Implement three zombie archetypes (Common, Fast, Heavy) governed by Mecanim FSMs, paired with hitscan shooting, visual recoil, and bullet tracers.", style_bullet))
    story.append(Paragraph("4. <b>Modular World Streaming:</b> Construct a 5-segment circular pool recycling 30m Abandoned City and Subway Tunnel segments with seamless theme transitions.", style_bullet))
    story.append(Paragraph("5. <b>Adaptive Horror Audio:</b> Create a 4-tier dynamic audio system crossfading across exploration, tension, combat, and critical health states with 3D spatialized zombie sound.", style_bullet))
    story.append(Paragraph("6. <b>UI & Economy Persistence:</b> Design a responsive UI flow (Menu, HUD, Pause, GameOver) with PlayerPrefs persistence and a single shielded revive loop.", style_bullet))
    story.append(Paragraph("<b>7.2 Project Scope:</b> Target platform is Windows PC Standalone with keyboard/mouse controls. The architecture is verified for mobile compilation readiness (portrait orientation, safe-area UI, Android APK build). Explicitly reserved for future work are online multiplayer leaderboards, networked co-op, branching procedural mazes, and in-app storefronts.", style_body))

    story.append(PageBreak())

    # ==========================================
    # 8. TOOLS AND TECHNOLOGIES & 9. SYSTEM ARCHITECTURE
    # ==========================================
    story.append(Paragraph("8. Tools and Technologies", style_h1))
    story.append(Paragraph("Zombie Runner utilizes industry-standard software tools and modern rendering pipelines, summarized in Table 1.", style_body))

    t1_data = [
        [Paragraph("<b>Domain / Component</b>", style_th), Paragraph("<b>Technology / Version</b>", style_th), Paragraph("<b>Academic & Technical Rationale</b>", style_th)],
        [Paragraph("<b>Game Engine</b>", style_td_bold), Paragraph("Unity 6 (6000.5.9f1)", style_td), Paragraph("High-performance C# runtime, unified build pipeline, robust profiler, and modern URP graphics features.", style_td)],
        [Paragraph("<b>Render Pipeline</b>", style_td_bold), Paragraph("Universal Render Pipeline (17.5.0)", style_td), Paragraph("Optimized single-pass Forward+ rendering, custom Lit PBR materials, ACES tonemapping, and volumetric fog.", style_td)],
        [Paragraph("<b>Programming Language</b>", style_td_bold), Paragraph("C# (.NET Standard 2.1)", style_td), Paragraph("Object-oriented, type-safe architecture, garbage-collection control, and efficient memory layouts.", style_td)],
        [Paragraph("<b>Input Framework</b>", style_td_bold), Paragraph("Unity Input System (1.20.0)", style_td), Paragraph("Event-driven cross-platform input supporting both keyboard/mouse and mobile touchscreen fallbacks.", style_td)],
        [Paragraph("<b>UI System</b>", style_td_bold), Paragraph("TextMeshPro / uGUI (2.5.0)", style_td), Paragraph("SDF font rendering for crisp text at all resolutions, safe-area anchoring, and 9-sliced procedural sprites.", style_td)],
        [Paragraph("<b>Character Animation</b>", style_td_bold), Paragraph("Adobe Mixamo & Mecanim", style_td), Paragraph("Humanoid avatar retargeting, baked in-place root motion, and multi-layer state machines.", style_td)]
    ]
    t1_table = Table(t1_data, colWidths=[110, 150, 244])
    t1_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor("#CBD5E1")),
    ]))
    story.append(t1_table)
    story.append(Spacer(1, 4))

    story.append(Paragraph("9. System Design and Architecture", style_h1))
    story.append(Paragraph("Zombie Runner follows a decoupled, component-based architecture following Unity's Entity-Component paradigm. Components communicate via C# events, interfaces (<code>IDamageable</code>), and centralized managers as specified in Table 2.", style_body))

    t2_data = [
        [Paragraph("<b>Subsystem Manager</b>", style_th), Paragraph("<b>Namespace / Script</b>", style_th), Paragraph("<b>Architectural Role & Key Methods</b>", style_th)],
        [Paragraph("<b>Game Lifecycle</b>", style_td_bold), Paragraph("GameManager.cs (ZombieRunner.Core)", style_td), Paragraph("Coordinates global game states (Play, Pause, GameOver), timeScale manipulation, mobile frame rates, and 1-time revive token.", style_td)],
        [Paragraph("<b>Score & Economy</b>", style_td_bold), Paragraph("ScoreManager.cs / SaveManager.cs", style_td), Paragraph("Tracks distance and kill points, commits high scores and banked coins to PlayerPrefs, and triggers high-score record alerts.", style_td)],
        [Paragraph("<b>World Streaming</b>", style_td_bold), Paragraph("EndlessRoadManager.cs / ThemeManager", style_td), Paragraph("Maintains circular pools of 30m road and subway segments; interpolates trilight lighting, fog, and point lights across biomes.", style_td)],
        [Paragraph("<b>Combat & Pooling</b>", style_td_bold), Paragraph("ShootingController.cs / HitImpactManager", style_td), Paragraph("Executes forward raycast hitscan checks, auto-aim math, recoil kickback, bullet tracers, and pre-allocated blood/spark particle pools.", style_td)],
        [Paragraph("<b>Audio Routing</b>", style_td_bold), Paragraph("AudioManager.cs / AdaptiveMusic", style_td), Paragraph("Controls master AudioMixer buses (Master, Music, Ambient, SFX, UI) with logarithmic dB curves and crossfades 4 adaptive horror stems.", style_td)]
    ]
    t2_table = Table(t2_data, colWidths=[110, 150, 244])
    t2_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor("#CBD5E1")),
    ]))
    story.append(t2_table)
    story.append(Spacer(1, 4))

    # Architecture Callout
    callout_data = [[Paragraph("<b>Key Architectural Insight:</b> All damageable entities (Common/Fast/Heavy zombies, player health, and explosive barrels) implement the <code>IDamageable</code> interface (<code>TakeDamage(int amount, Vector3 hitPoint, Vector3 hitNormal)</code>). The raycast combat controller remains fully decoupled from specific enemy classes, preventing tight class dependencies.", style_callout)]]
    t_callout = Table(callout_data, colWidths=[504])
    t_callout.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0F4F8")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LINELEFT', (0,0), (-1,-1), 3.0, PRIMARY),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#D0DCE5")),
    ]))
    story.append(t_callout)

    story.append(PageBreak())

    # ==========================================
    # 10. GAMEPLAY MECHANICS AND CONTROLS
    # ==========================================
    story.append(Paragraph("10. Gameplay Mechanics and Controls", style_h1))
    story.append(Paragraph("<b>10.1 Player Locomotion and Three-Lane Navigation:</b> Player movement is governed by <code>PlayerController.cs</code> using a CharacterController component. The player navigates across three discrete lanes at X = -3.0m (Left), X = 0.0m (Center), and X = +3.0m (Right). Horizontal switching uses smooth frame-rate independent interpolation (lane switch speed: 14 m/s). Forward speed incorporates progressive acceleration: starting at 8.0 m/s, forward speed scales continuously at 0.005 m/s² up to a maximum terminal velocity of 16.0 m/s.", style_body))
    story.append(Paragraph("<b>10.2 Jump Kinematics and Timed Combat Slide Physics:</b> Vertical locomotion is governed kinematically via v<sub>y</sub> = sqrt(2 * |g| * h), where gravity g = -20.0 m/s² and jump height h = 1.8m. Jumping is strictly grounded; an airborne state flag (<code>isJumping</code>) prevents landing transition flickers. Triggering a slide initiates a 0.8s low-profile slide: CharacterController collision height drops from 2.0m to 1.05m and center Y-offset adjusts from 1.0m to 0.525m to slip beneath low barriers without deforming the humanoid skeletal mesh.", style_body))
    story.append(Paragraph("<b>10.3 Raycast Weapon Mechanics and Visual Recoil:</b> Combat is managed by <code>ShootingController.cs</code>. When fire is triggered, an auto-aim cone calculation (angle <= 12°, range <= 32m) selects the nearest zombie. A forward raycast inflicts damage on <code>IDamageable</code> targets, an illuminated bullet tracer interpolates to the hit point, and pre-allocated blood/spark particle bursts trigger from the object pool. Firing produces procedural visual recoil (0.07m kickback, 3.5° muzzle climb) and a momentary muzzle-flash point light.", style_body))
    story.append(Paragraph("<b>10.4 Collectibles, Economy, and Power-Up Dynamics:</b> Interactive pickups include Gold Coins (banked currency), Ammo Boxes (+15 rounds), and Medical Kits (+25 HP). Four timed power-ups provide gameplay modifiers: (1) Energy Shield (absorbs one lethal hit); (2) Coin Magnet (draws coins within 8m); (3) Speed Boost (+50% forward velocity with invulnerability); and (4) Double Coins (2x coin multiplier).", style_body))

    # Table 3: Controls Reference
    t3_data = [
        [Paragraph("<b>Action</b>", style_th), Paragraph("<b>Primary Keyboard Key</b>", style_th), Paragraph("<b>Secondary / Mouse / Touch</b>", style_th)],
        [Paragraph("<b>Move Left / Right</b>", style_td_bold), Paragraph("A / D", style_td), Paragraph("Left Arrow / Right Arrow / Touch Swipe", style_td)],
        [Paragraph("<b>Jump (Clear Hurdles)</b>", style_td_bold), Paragraph("W / Space", style_td), Paragraph("Up Arrow / Swipe Up", style_td)],
        [Paragraph("<b>Slide (Under Barriers)</b>", style_td_bold), Paragraph("S", style_td), Paragraph("Down Arrow / Swipe Down", style_td)],
        [Paragraph("<b>Shoot Firearm</b>", style_td_bold), Paragraph("F", style_td), Paragraph("Left Mouse Button / On-Screen Fire Button", style_td)],
        [Paragraph("<b>Pause / Resume</b>", style_td_bold), Paragraph("Escape", style_td), Paragraph("P / UI Pause Button", style_td)]
    ]
    t3_table = Table(t3_data, colWidths=[130, 150, 224])
    t3_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.0),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor("#CBD5E1")),
    ]))
    story.append(t3_table)
    story.append(Spacer(1, 3))

    # Figure 1
    ss_overview = r"E:\zombie runner\Screenshots\Audit_MainMenu_1_Overview.png"
    if os.path.exists(ss_overview):
        img_fig1 = Image(ss_overview, width=4.1*inch, height=2.3*inch)
        img_fig1.hAlign = 'CENTER'
        story.append(img_fig1)
        story.append(Paragraph("Figure 1: Title Screen and 3D Survivor Character Staging (Audit_MainMenu_1_Overview)", style_caption))

    story.append(PageBreak())

    # ==========================================
    # 11. ENVIRONMENT AND VISUAL DESIGN
    # ==========================================
    story.append(Paragraph("11. Environment and Visual Design", style_h1))
    story.append(Paragraph("<b>11.1 Modular Streaming Architecture and Endless Road Pooling:</b> To support infinite traversal without unbounded memory allocation, <code>EndlessRoadManager.cs</code> and <code>EnvironmentThemeManager.cs</code> maintain circular pools of five 30-meter environment segments (totaling 150m of active world). When a segment trails the player by > 35m, it is deactivated, translated forward (Z<sub>new</sub> = Z<sub>lead</sub> + 30m), and reactivated with freshly randomized obstacles and pickups with zero heap allocations.", style_body))
    story.append(Paragraph("<b>11.2 Biome Aesthetics: Abandoned City Ruins and Subterranean Subway Tunnel:</b> The game alternates visual themes every 300 meters:", style_body))
    story.append(Paragraph("• <b>Abandoned City Ruins:</b> Multi-story brick facades, cracked asphalt with worn yellow road striping, rubble barricades, and flickering sodium-vapor streetlights establish a nocturnal survival atmosphere.", style_bullet))
    story.append(Paragraph("• <b>Subterranean Subway Tunnel:</b> A continuous 30m modular enclosure featuring solid 5.2m reinforced concrete side-walls, a 15.5m ceiling with 45-degree vaulted arches, heavy portal rib columns every 7.5m, industrial overhead ventilation shafts, dual high-voltage cable trays, steel railway tracks, and embedded concrete sleepers. Overhead neutral luminaires (4200K) and caged amber emergency bulkheads (2200K) cast deep shadows, creating claustrophobic survival horror tension.", style_bullet))
    story.append(Paragraph("<b>11.3 Cinematic Horror Lighting, Trilight Ambient Bounce, and Volumetric Fog:</b> Lighting design balances atmospheric dread with high-speed competitive clarity:", style_body))
    story.append(Paragraph("• <i>Cool-Blue Directional Moonlight:</i> Key directional light (#C0D6FA, intensity 1.75) establishes a chilling nocturnal baseline.", style_bullet))
    story.append(Paragraph("• <i>Trilight Ambient Bounce Lighting:</i> Calibrated across all theme profiles (Sky #576785, Equator #47546B, Ground #384052) to eliminate pure black pitch shadows and preserve texture definition on character clothing and road surfaces.", style_bullet))
    story.append(Paragraph("• <i>Calibrated Linear Atmospheric Fog:</i> Fog is configured with a 42-meter start distance and 165-meter end distance. This critical calibration ensures the immediate 42-meter gameplay corridor remains crystal-clear for rapid obstacle detection and zombie targeting, while the background dissolves into deep, atmospheric dread.", style_bullet))
    story.append(Paragraph("• <i>Player Tactical Flashlight:</i> Weapon-mounted dual-beam spotlight (high-intensity 48m narrow beam and 40m wide fill beam) sweeps dynamically with auto-aim tracking, piercing dark subway tunnels.", style_bullet))

    story.append(Spacer(1, 3))
    # Figure 2
    ss_audio = r"E:\zombie runner\Screenshots\Audit_MainMenu_3_Settings_Audio.png"
    if os.path.exists(ss_audio):
        img_fig2 = Image(ss_audio, width=4.1*inch, height=2.3*inch)
        img_fig2.hAlign = 'CENTER'
        story.append(img_fig2)
        story.append(Paragraph("Figure 2: Main Menu Settings: Audio Mixer Bus Controls and Volume Persistence", style_caption))

    story.append(PageBreak())

    # ==========================================
    # 12. ZOMBIE AI AND COMBAT SYSTEM
    # ==========================================
    story.append(Paragraph("12. Zombie AI and Combat System", style_h1))
    story.append(Paragraph("<b>12.1 ScriptableObject Architecture and Archetype Design:</b> Enemy parameters are strictly decoupled from executable code using Unity ScriptableObjects (<code>ZombieConfig.cs</code>). Designers can author, tune, and balance enemy variants in the Inspector without recompilation. Table 4 outlines the specifications of the three implemented archetypes.", style_body))

    t4_data = [
        [Paragraph("<b>Archetype</b>", style_th), Paragraph("<b>3D Model / Rig</b>", style_th), Paragraph("<b>Health</b>", style_th), Paragraph("<b>Speed</b>", style_th), Paragraph("<b>Damage / Range</b>", style_th), Paragraph("<b>Points</b>", style_th)],
        [Paragraph("<b>Common Runner</b>", style_td_bold), Paragraph("Mixamo Ch10 (Humanoid)", style_td), Paragraph("3 HP (3 shots)", style_td_center), Paragraph("5.0 m/s", style_td_center), Paragraph("10 DMG / 1.8m", style_td), Paragraph("100 pts", style_td_center)],
        [Paragraph("<b>Fast Sprinter</b>", style_td_bold), Paragraph("Yaku J Ignite (Humanoid)", style_td), Paragraph("2 HP (2 shots)", style_td_center), Paragraph("7.5 m/s", style_td_center), Paragraph("8 DMG / 1.6m", style_td), Paragraph("150 pts", style_td_center)],
        [Paragraph("<b>Heavy Brute</b>", style_td_bold), Paragraph("Pumpkinhulk (Humanoid)", style_td), Paragraph("8 HP (8 shots)", style_td_center), Paragraph("3.2 m/s", style_td_center), Paragraph("25 DMG / 2.2m", style_td), Paragraph("250 pts", style_td_center)]
    ]
    t4_table = Table(t4_data, colWidths=[85, 120, 75, 55, 95, 74])
    t4_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.0),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor("#CBD5E1")),
    ]))
    story.append(t4_table)
    story.append(Spacer(1, 3))

    story.append(Paragraph("<b>12.2 AI State Machine and Animation Retargeting:</b> Zombie behavior is governed by <code>ZombieController.cs</code> driving a Mecanim Animator Controller. The FSM manages transitions between Idle, Walk, Run, Attack, Hit Reaction, and Death states. Locomotion animations (Mixamo Scary Zombie Pack) have displacement baked into root motion pose curves, letting C# velocity control forward translation without foot sliding. Non-lethal hits trigger an upper-body flinch before resuming pursuit; lethal damage initiates backward/forward collapse with immediate collider disabling.", style_body))
    story.append(Paragraph("<b>12.3 Positional 3D Audio and Spatial Attenuation:</b> All zombie prefabs include <code>ZombieSoundEmitter.cs</code>, which routes groans, snarling breaths, and attack lunges through custom 3D AudioSource components. Logarithmic spatial attenuation (minDistance = 2.5m, maxDistance = 24m) provides auditory depth perception, enabling players to detect approaching threats directionally through headphones prior to visual contact.", style_body))
    story.append(Paragraph("<b>12.4 Combat Feedback and GC-Free Particle Pooling:</b> Combat impacts utilize <code>HitImpactManager.cs</code>, which maintains pre-warmed pools of blood splatter VFX, metal ricochet sparks, and concrete impact dust. Impact effects are recycled without heap allocation, eliminating GC pauses during rapid combat.", style_body))

    story.append(Spacer(1, 3))
    # Figure 3
    ss_ctrl = r"E:\zombie runner\Screenshots\Audit_MainMenu_4_Settings_Controls.png"
    if os.path.exists(ss_ctrl):
        img_fig3 = Image(ss_ctrl, width=4.1*inch, height=2.3*inch)
        img_fig3.hAlign = 'CENTER'
        story.append(img_fig3)
        story.append(Paragraph("Figure 3: Keyboard and Mouse Input Configuration Reference Guide", style_caption))

    story.append(PageBreak())

    # ==========================================
    # 13. USER INTERFACE & 14. IMPLEMENTATION OVERVIEW
    # ==========================================
    story.append(Paragraph("13. User Interface and Game Flow", style_h1))
    story.append(Paragraph("<b>13.1 Main Menu Experience and Survivor Staging:</b> The title screen (<code>ZombieRunnerMainMenu.unity</code>) features a fully lit 3D survivor model (Mixamo Ch05) equipped with the Tommy Gun, framed by a cinematic panning camera and subtle atmospheric ash particles. Players can navigate to Play, open multi-tabbed Settings (Graphics toggles, AudioMixer decibel sliders for Master/Music/SFX, and Input Control guides), or inspect team Credits.", style_body))
    story.append(Paragraph("<b>13.2 Heads-Up Display (HUD) and Real-Time State Tracking:</b> The in-game HUD (<code>UIManager.cs</code>) renders real-time survival data using TextMeshPro: (1) distance traversed in meters; (2) current run score (Score = Distance + Kills); (3) coin counter; (4) remaining ammunition with low-ammo warnings; (5) a color-coded segmented health bar; and (6) active power-up countdown icons. <code>SafeAreaFitter.cs</code> queries Screen.safeArea to guarantee that UI elements remain fully visible on notched screens.", style_body))
    story.append(Paragraph("<b>13.3 Game Over, High Score Celebration, and Revive Flow:</b> Upon player death, the Game Over screen displays run statistics alongside persistent high scores loaded from PlayerPrefs. Surpassing the record triggers a prominent `(NEW BEST!)` celebratory banner. Players can select Retry, Return to Menu, or a one-time Shielded Revive button that restores full health, 30 ammunition rounds, and a 3-second invulnerability shield.", style_body))

    story.append(Spacer(1, 3))
    story.append(Paragraph("14. Implementation Overview", style_h1))
    story.append(Paragraph("The codebase comprises 25 modular C# gameplay scripts under <code>Assets/ZombieRunner/Scripts/</code>, complemented by 11 custom editor utilities. Table 6 provides an architectural directory breakdown.", style_body))

    t6_data = [
        [Paragraph("<b>Module Directory</b>", style_th), Paragraph("<b>Primary C# Scripts</b>", style_th), Paragraph("<b>System Responsibility</b>", style_th)],
        [Paragraph("<b>Core</b>", style_td_bold), Paragraph("GameManager.cs, SaveManager.cs, ScoreManager.cs", style_td), Paragraph("State coordination, PlayerPrefs high score & banked coin persistence.", style_td)],
        [Paragraph("<b>Player</b>", style_td_bold), Paragraph("PlayerController.cs, PlayerHealth.cs, RunnerCameraFollow.cs", style_td), Paragraph("Three-lane locomotion, jump/slide mechanics, health events, follow camera.", style_td)],
        [Paragraph("<b>Enemies</b>", style_td_bold), Paragraph("ZombieController.cs, ZombieSpawner.cs, ZombieSoundEmitter.cs, ZombieConfig.cs", style_td), Paragraph("FSM enemy behavior, ScriptableObject stats, lane-aware spawner, 3D audio.", style_td)],
        [Paragraph("<b>Weapons</b>", style_td_bold), Paragraph("ShootingController.cs, BulletTracer.cs, HitImpactManager.cs", style_td), Paragraph("Raycast combat, auto-aim math, recoil kickback, tracer & impact pooling.", style_td)],
        [Paragraph("<b>World</b>", style_td_bold), Paragraph("EndlessRoadManager.cs, EnvironmentThemeManager.cs, StreetlightFlicker.cs", style_td), Paragraph("Circular segment pooling, theme blending, trilight lighting, lamp flicker.", style_td)],
        [Paragraph("<b>Audio</b>", style_td_bold), Paragraph("AudioManager.cs, AdaptiveMusicController.cs, AmbientAudioController.cs", style_td), Paragraph("AudioMixer bus routing, 4-tier synchronized adaptive horror stems, ambient stingers.", style_td)]
    ]
    t6_table = Table(t6_data, colWidths=[95, 175, 234])
    t6_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.0),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor("#CBD5E1")),
    ]))
    story.append(t6_table)
    story.append(Spacer(1, 3))

    # Figure 4
    ss_gameplay = r"E:\zombie runner\Screenshots\Audit_MainMenu_6_GameplayTransition.png"
    if os.path.exists(ss_gameplay):
        img_fig4 = Image(ss_gameplay, width=4.1*inch, height=2.3*inch)
        img_fig4.hAlign = 'CENTER'
        story.append(img_fig4)
        story.append(Paragraph("Figure 4: In-Game Nocturnal Environment and Atmospheric Lighting Transition", style_caption))

    story.append(PageBreak())

    # ==========================================
    # 15. TESTING & DEBUGGING & 16. CHALLENGES AND SOLUTIONS
    # ==========================================
    story.append(Paragraph("15. Testing and Debugging", style_h1))
    story.append(Paragraph("<b>15.1 Verification Workflow and Custom Editor Tools:</b> Testing combined continuous Play Mode audits with custom C# diagnostic tools. Utilities including <code>ZombieCombatSystemValidator.cs</code>, <code>VisualAuditHelper.cs</code>, and <code>ProjectPolisher.cs</code> automatically verified scene hierarchy bindings, SkinnedMeshRenderer URP material assignments, Humanoid Avatar bone maps, and AudioMixer routing.", style_body))
    story.append(Paragraph("<b>15.2 Gameplay Systems Verification:</b> Rigorous verification covered: (1) Locomotion bounds: verified lane positions clamp strictly to X = -3.0m, 0.0m, +3.0m without curb clipping; (2) Jump/Slide isolation: confirmed airborne slides and mid-air double jumps are rejected; (3) Hit registration: verified raycast damage decrements zombie health and triggers death states; (4) Power-up refresh: confirmed re-collecting active power-ups refreshes duration without stacking.", style_body))
    story.append(Paragraph("<b>15.3 Performance Profiling & Build Verification:</b> Profiling via Unity Profiler confirmed zero runtime GC allocations during running. Standalone Windows PC testing confirmed 60 FPS execution. Mobile readiness was validated by executing the automated Android build pipeline, producing <code>Builds/Android/ZombieRunner.apk</code> (42,953,718 bytes, IL2CPP 64-bit, ARM64, minimum API 26) with zero compilation errors.", style_body))

    story.append(Spacer(1, 4))
    story.append(Paragraph("16. Challenges and Solutions", style_h1))
    story.append(Paragraph("During development, six major technical challenges were diagnosed and resolved:", style_body))
    
    challenges = [
        ("1. Humanoid Mesh Distortion During Combat Slide:", "Modifying CharacterController height to 1.05m squashed placeholder capsules, but distorted rigged Mixamo models (Ch05) and pushed feet below the road. <i>Solution:</i> Decoupled collision box scaling from visual transforms; visual scaling was restricted exclusively to unrigged meshes, while rigged models execute the authentic Mixamo Running Slide clip at 1.95x speed."),
        ("2. Launch-Frame Premature Jump Cancellation:", "CharacterController.isGrounded evaluated true on the launch frame before clearing skin width, causing the Jump->Run transition to cancel jump animation instantly. <i>Solution:</i> Added an explicit <code>isJumping</code> flag that sets true on launch, forces Grounded false, and clears only when descending (v<sub>y</sub> <= 0) and physically grounded."),
        ("3. Enemy Spawner Deadlock Bug:", "Zombies trailing behind the runner remained alive, causing concurrent alive count to cap at maximumAlive (6) and permanently halting spawns. <i>Solution:</i> Implemented automated cleanup in <code>ZombieSpawner.cs</code> destroying zombies > 12m behind the runner without unearned score."),
        ("4. Particle System Lifecycle Mutation Error:", "Over 100 console errors stated: 'Setting duration while system is playing is not supported'. <i>Solution:</i> Instantiated GameObjects inactive (<code>go.SetActive(false)</code>), invoked <code>ps.Stop(true, StopEmittingAndClear)</code>, safely assigned custom module duration, and activated on demand."),
        ("5. Subterranean Repeating Blue Rectangular Frame Artifacts:", "Subway tunnel rendered as disconnected open rectangular frames with strong artificial cyan ambient wash, exposing the open skybox. <i>Solution:</i> Reconstructed <code>EnvironmentSegment_SubwayTunnel.prefab</code> with continuous 5.2m concrete side walls, 15.5m vaulted ceiling, portal columns every 7.5m, overhead utilities, and balanced 4200K neutral luminaires with 2200K emergency caged lamps."),
        ("6. Harsh Audio Whistle Loop & Arcade Beeper Disconnect:", "Early builds featured a repeating 6.0s wind loop with a harsh 480-550Hz whistle and sharp 8-bit UI beeps. <i>Solution:</i> Synthesized an organic 48.0s continuous Brownian wind soundscape and engineered a 4-tier synchronized 75 BPM adaptive horror music suite in D minor with a 1.2kHz-4.2kHz frequency notch for clear gunfire acoustics.")
    ]
    for c_title, c_desc in challenges:
        story.append(Paragraph(f"<b>{c_title}</b> {c_desc}", style_bullet))

    story.append(PageBreak())

    # ==========================================
    # 17. LEARNING OUTCOMES, 18. FUTURE WORK, 19. CONCLUSION, 20. REFERENCES
    # ==========================================
    story.append(Paragraph("17. Learning Outcomes", style_h1))
    story.append(Paragraph("The engineering of Zombie Runner provided deep practical competence across game programming disciplines: (1) <i>URP Pipeline Expertise:</i> Calibrating custom Lit materials, ACES tonemapping, Trilight ambient lighting, and volumetric fog; (2) <i>Animation Retargeting:</i> Configuring Mecanim Humanoid Avatars, in-place root motion baking, and multi-parameter state machines; (3) <i>Combat Kinematics:</i> Authoring hitscan raycast math, auto-aim cone calculations, visual weapon kickback, and bullet tracer line rendering; (4) <i>Architectural Decoupling:</i> Implementing ScriptableObject data encapsulation, interface messaging (<code>IDamageable</code>), and circular object pooling; (5) <i>Adaptive Audio Engineering:</i> Constructing multi-tier stem crossfades, logarithmic dB conversion, and 3D spatial attenuation curves.", style_body))

    story.append(Spacer(1, 3))
    story.append(Paragraph("18. Future Enhancements", style_h1))
    story.append(Paragraph("High-value features architected for future development cycles include:", style_body))
    story.append(Paragraph("1. <b>Advanced Flocking & Ranged Mutant AI:</b> Flocking runner hordes and ranged acid-spitting mutants requiring dynamic evasion.", style_bullet))
    story.append(Paragraph("2. <b>Expanded Weapon Arsenal:</b> Collectible shotguns (wide-spread clearing), assault rifles, and grenade launchers with distinct ammo pools.", style_bullet))
    story.append(Paragraph("3. <b>Dynamic Subway Boss Encounters:</b> Procedural tunnel breach events featuring a pursuing Nemesis brute damaged over distance.", style_bullet))
    story.append(Paragraph("4. <b>Global Online Leaderboards:</b> RESTful cloud database integration supporting asynchronous ghost runner replays and ranking.", style_bullet))
    story.append(Paragraph("5. <b>Dynamic Weather Effects:</b> Screen-space rain droplets, volumetric lightning strikes casting dynamic shadows, and destructible barricades.", style_bullet))

    story.append(Spacer(1, 3))
    story.append(Paragraph("19. Conclusion", style_h1))
    story.append(Paragraph("Zombie Runner demonstrates that the kinetic momentum of the 3D endless runner genre can be synergistically elevated through tactical survival horror combat and atmospheric audiovisual immersion. Engineered in Unity 6 with URP, the project realized responsive 3-lane navigation, physics-based jumping, low combat sliding, and visceral raycast shooting. The integration of circular modular world streaming, ScriptableObject-driven zombie archetypes, layered adaptive audio, and GC-suppressed particle pooling guarantees a polished, high-framerate gameplay experience. Evaluation under Game Mechanics, Design and Development (23CS201PE407) confirms that all academic objectives and engineering milestones were rigorously fulfilled.", style_body))

    story.append(Spacer(1, 3))
    story.append(Paragraph("20. References and Asset Credits", style_h1))
    story.append(Paragraph("<b>20.1 Academic Literature and Technical References:</b>", style_h2))
    story.append(Paragraph("<b>[1]</b> Unity Technologies. (2025). Unity 6 User Manual and Universal Render Pipeline (URP 17.5) Documentation. San Francisco, CA.", style_bullet))
    story.append(Paragraph("<b>[2]</b> Millington, I., & Funge, J. (2018). Artificial Intelligence for Games (3rd ed.). CRC Press / Taylor & Francis Group.", style_bullet))
    story.append(Paragraph("<b>[3]</b> Schell, J. (2019). The Art of Game Design: A Book of Lenses (3rd ed.). A K Peters / CRC Press.", style_bullet))
    story.append(Paragraph("<b>[4]</b> Rogers, S. (2014). Level Up! The Guide to Great Video Game Design (2nd ed.). John Wiley & Sons.", style_bullet))
    story.append(Paragraph("<b>[5]</b> Gregory, J. (2018). Game Engine Architecture (3rd ed.). CRC Press.", style_bullet))

    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>20.2 Asset Credits and Licenses:</b>", style_h2))
    story.append(Paragraph("• <b>Mixamo (Adobe Systems):</b> Survivor Models (Ch05, X Bot), Zombie Archetypes (Ch10 Common, Yaku J Ignite Fast, Pumpkinhulk Heavy), and locomotion/combat clips from Shooter Pack and Scary Zombie Pack. Licensed under Adobe Mixamo Royalty-Free License.", style_bullet))
    story.append(Paragraph("• <b>Weapon 3D Assets:</b> High-detail Tommy Gun submachine gun model with PBR metallic-roughness textures under <code>Assets/ZombieRunner/Models/Weapons/TommyGun/</code>.", style_bullet))
    story.append(Paragraph("• <b>Audio Suite:</b> Algorithmic horror soundscape stems and procedural audio generator released under CC0 / Public Domain. Full credit manifest in <code>Assets/ZombieRunner/Audio/AUDIO_CREDITS.md</code>.", style_bullet))
    story.append(Paragraph("• <b>Academic Institution:</b> Course curriculum and evaluation criteria provided by the School of Computer Science and Artificial Intelligence, SR University, Warangal, Telangana.", style_bullet))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF created successfully at: {output_path}")

if __name__ == "__main__":
    out_pdf = os.path.abspath(r"E:\zombie runner\Zombie_Runner_Project_Report.pdf")
    create_pdf(out_pdf)
