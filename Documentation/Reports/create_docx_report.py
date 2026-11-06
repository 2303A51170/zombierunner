import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="B0C4DE", sz="6", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:left w:val="none"/>
            <w:right w:val="none"/>
            <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideV w:val="none"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

def add_page_number_to_run(run):
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = "PAGE"
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')
    fldChar3 = OxmlElement('w:fldChar')
    fldChar3.set(qn('w:fldCharType'), 'end')
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)

def create_docx(output_path):
    doc = docx.Document()
    
    # Page setup - 0.75 in margins for academic density
    for sec in doc.sections:
        sec.top_margin = Inches(0.75)
        sec.bottom_margin = Inches(0.75)
        sec.left_margin = Inches(0.75)
        sec.right_margin = Inches(0.75)
        sec.different_first_page_header_footer = True
        
        # Configure Header
        header = sec.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("Zombie Runner: 3D Survival Horror Endless Runner | SR University")
        hrun.font.name = "Calibri"
        hrun.font.size = Pt(8.5)
        hrun.font.italic = True
        hrun.font.color.rgb = RGBColor(120, 140, 160)
        
        # Configure Footer
        footer = sec.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        frun1 = fp.add_run("School of Computer Science & Artificial Intelligence          Page ")
        frun1.font.name = "Calibri"
        frun1.font.size = Pt(8.5)
        frun1.font.color.rgb = RGBColor(120, 140, 160)
        add_page_number_to_run(fp.add_run())
        for r in fp.runs[-1:]:
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            r.font.color.rgb = RGBColor(120, 140, 160)
    
    # Styles Setup
    COLOR_PRIMARY = RGBColor(11, 59, 96)     # SRU Navy Blue
    COLOR_SECONDARY = RGBColor(31, 78, 121)  # Slate Blue
    COLOR_DARK = RGBColor(40, 40, 40)        # Dark Charcoal
    COLOR_MUTED = RGBColor(90, 105, 120)     # Muted Blue-Grey
    
    # Helper to add Headings
    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = "Calibri"
        run.font.size = Pt(14)
        run.font.color.rgb = COLOR_PRIMARY
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = "Calibri"
        run.font.size = Pt(11.5)
        run.font.color.rgb = COLOR_SECONDARY
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = "Calibri"
        run.font.size = Pt(10.5)
        run.font.color.rgb = COLOR_DARK
        return p

    def add_body(text, bold_prefix=None):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4.5)
        p.paragraph_format.line_spacing = 1.15
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if bold_prefix:
            br = p.add_run(bold_prefix)
            br.bold = True
            br.font.name = "Calibri"
            br.font.size = Pt(10)
            br.font.color.rgb = COLOR_DARK
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(10)
        run.font.color.rgb = COLOR_DARK
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2.5)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            br = p.add_run(bold_prefix)
            br.bold = True
            br.font.name = "Calibri"
            br.font.size = Pt(9.5)
            br.font.color.rgb = COLOR_DARK
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(9.5)
        run.font.color.rgb = COLOR_DARK
        return p

    def add_callout(text, bold_title="Key Technical Architecture Note:"):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        set_cell_background(cell, "F0F4F8")
        set_cell_margins(cell, top=100, bottom=100, left=180, right=150)
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(f'''
            <w:tcBorders {nsdecls("w")}>
                <w:left w:val="single" w:sz="24" w:space="0" w:color="0B3B60"/>
                <w:top w:val="none"/>
                <w:bottom w:val="none"/>
                <w:right w:val="none"/>
            </w:tcBorders>
        ''')
        tcPr.append(borders)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        br = p.add_run(bold_title + " ")
        br.bold = True
        br.font.name = "Calibri"
        br.font.size = Pt(9.5)
        br.font.color.rgb = COLOR_PRIMARY
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.color.rgb = COLOR_DARK
        # spacer after table
        sp = doc.add_paragraph()
        sp.paragraph_format.space_before = Pt(2)
        sp.paragraph_format.space_after = Pt(2)

    def add_figure(img_path, caption):
        if os.path.exists(img_path):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run()
            run.add_picture(img_path, width=Inches(5.0))
            
            cp = doc.add_paragraph()
            cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cp.paragraph_format.space_before = Pt(0)
            cp.paragraph_format.space_after = Pt(6)
            crun = cp.add_run(caption)
            crun.font.name = "Calibri"
            crun.font.size = Pt(8.5)
            crun.font.italic = True
            crun.font.color.rgb = COLOR_MUTED

    print("Document structure ready. Adding Cover Page...")

    # ==========================================
    # 1. COVER PAGE (Matching Course Plan Reference Layout)
    # ==========================================
    p_head = doc.add_paragraph()
    p_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_head.paragraph_format.space_before = Pt(12)
    p_head.paragraph_format.space_after = Pt(2)
    r1 = p_head.add_run("PROJECT REPORT\n")
    r1.bold = True
    r1.font.name = "Calibri"
    r1.font.size = Pt(17)
    r1.font.color.rgb = COLOR_PRIMARY
    
    r2 = p_head.add_run("For\n")
    r2.font.name = "Calibri"
    r2.font.size = Pt(12)
    r2.font.italic = True
    r2.font.color.rgb = COLOR_DARK
    
    r3 = p_head.add_run("GAME MECHANICS, DESIGN AND DEVELOPMENT\n")
    r3.bold = True
    r3.font.name = "Calibri"
    r3.font.size = Pt(14)
    r3.font.color.rgb = COLOR_PRIMARY
    
    r4 = p_head.add_run("(COURSE CODE: 23CS201PE407)\n\n")
    r4.bold = True
    r4.font.name = "Calibri"
    r4.font.size = Pt(12.5)
    r4.font.color.rgb = COLOR_DARK

    # Project Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(4)
    p_title.paragraph_format.space_after = Pt(16)
    rt = p_title.add_run("PROJECT TITLE:\nZOMBIE RUNNER – 3D SURVIVAL HORROR ENDLESS RUNNER")
    rt.bold = True
    rt.font.name = "Calibri"
    rt.font.size = Pt(14.5)
    rt.font.color.rgb = COLOR_SECONDARY

    # Metadata Table (Colon-aligned, matching Course Plan screenshot)
    meta_table = doc.add_table(rows=9, cols=3)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    col_widths = [Inches(2.2), Inches(0.3), Inches(3.8)]
    for row in meta_table.rows:
        for i, w in enumerate(col_widths):
            row.cells[i].width = w

    meta_data = [
        ("Course Coordinator", ":", "Dr. Vijaya Chandra Jadala"),
        ("Course Instructors", ":", "Dr. Vijaya Chandra Jadala"),
        ("Course Type", ":", "Program Elective 1 (PE1)"),
        ("Semester and Year", ":", "IV Year, 1st Semester"),
        ("L-T-P", ":", "2-0-2"),
        ("Credits", ":", "3"),
        ("School", ":", "School of Computer Science and Artificial Intelligence"),
        ("Department", ":", "Department of Computer Science and Artificial Intelligence"),
        ("Course Level", ":", "Undergraduate (UG)")
    ]

    for idx, (label, sep, val) in enumerate(meta_data):
        row = meta_table.rows[idx]
        
        # Label cell
        p0 = row.cells[0].paragraphs[0]
        p0.paragraph_format.space_after = Pt(2)
        r = p0.add_run(label)
        r.font.name = "Calibri"
        r.font.size = Pt(10)
        r.bold = True
        r.font.color.rgb = COLOR_DARK
        
        # Separator cell
        p1 = row.cells[1].paragraphs[0]
        p1.paragraph_format.space_after = Pt(2)
        r = p1.add_run(sep)
        r.font.name = "Calibri"
        r.font.size = Pt(10)
        r.font.color.rgb = COLOR_DARK
        
        # Value cell
        p2 = row.cells[2].paragraphs[0]
        p2.paragraph_format.space_after = Pt(2)
        r = p2.add_run(val)
        r.font.name = "Calibri"
        r.font.size = Pt(10)
        r.font.color.rgb = COLOR_DARK

    # Team Members Block
    p_team_h = doc.add_paragraph()
    p_team_h.paragraph_format.space_before = Pt(14)
    p_team_h.paragraph_format.space_after = Pt(3)
    rth = p_team_h.add_run("Submitted by Team Members:")
    rth.bold = True
    rth.font.name = "Calibri"
    rth.font.size = Pt(10.5)
    rth.font.color.rgb = COLOR_PRIMARY

    team_table = doc.add_table(rows=4, cols=3)
    team_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_widths = [Inches(0.6), Inches(3.2), Inches(2.5)]
    for row in team_table.rows:
        for i, w in enumerate(t_widths):
            row.cells[i].width = w

    members = [
        ("1.", "J. Radha Krishna", "Roll No: 2303A52055"),
        ("2.", "P. Makesh Babu", "Roll No: 2303A52061"),
        ("3.", "M. Omprakash", "Roll No: 2303A52057"),
        ("4.", "V. Siddharatha", "Roll No: 2303A52463")
    ]
    for idx, (num, name, rno) in enumerate(members):
        row = team_table.rows[idx]
        for c_idx, text in enumerate([num, name, rno]):
            p = row.cells[c_idx].paragraphs[0]
            p.paragraph_format.space_after = Pt(1.5)
            r = p.add_run(text)
            r.font.name = "Calibri"
            r.font.size = Pt(10)
            if c_idx == 1:
                r.bold = True
            r.font.color.rgb = COLOR_DARK

    # Bottom Cover Elements
    p_bottom = doc.add_paragraph()
    p_bottom.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_bottom.paragraph_format.space_before = Pt(18)
    p_bottom.paragraph_format.space_after = Pt(4)
    rb1 = p_bottom.add_run("School of Computer Science and Artificial Intelligence\n")
    rb1.bold = True
    rb1.font.name = "Calibri"
    rb1.font.size = Pt(12)
    rb1.font.color.rgb = COLOR_PRIMARY

    # SRU Logo
    logo_path = r"C:\Users\metra\.gemini\antigravity\brain\7ea1a950-c3d7-465b-a4d2-a25115ebddc3\.user_uploaded\media_1793877402347_b6c68b90.png"
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(2)
        p_logo.paragraph_format.space_after = Pt(4)
        run_logo = p_logo.add_run()
        run_logo.add_picture(logo_path, width=Inches(1.55))

    p_univ = doc.add_paragraph()
    p_univ.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_univ.paragraph_format.space_before = Pt(2)
    p_univ.paragraph_format.space_after = Pt(2)
    ru = p_univ.add_run("SR University\n")
    ru.bold = True
    ru.font.name = "Calibri"
    ru.font.size = Pt(13.5)
    ru.font.color.rgb = COLOR_PRIMARY
    
    ru2 = p_univ.add_run("Ananthasagar, Hasanparthy, Warangal, Telangana – 506371\nAcademic Year: 2026–2027 | Date of Submission: November 2026")
    ru2.font.name = "Calibri"
    ru2.font.size = Pt(9.5)
    ru2.font.color.rgb = COLOR_MUTED

    doc.add_page_break()

    # ==========================================
    # 2. ACKNOWLEDGEMENT
    # ==========================================
    add_h1("2. Acknowledgement")
    add_body("We express our deepest and most sincere gratitude to our esteemed Course Coordinator and Instructor, Dr. Vijaya Chandra Jadala, for his invaluable guidance, technical insight, continuous academic encouragement, and constructive critique throughout the conception, architectural design, implementation, and rigorous testing of the project \"Zombie Runner – 3D Survival Horror Endless Runner\". His pedagogical emphasis on rigorous software architecture, real-time computational performance, and immersive mechanical design in the course Game Mechanics, Design and Development (23CS201PE407) was fundamental in elevating this work from a prototype into an optimized, robust game.")
    add_body("We also extend our grateful appreciation to the leadership and faculty of the School of Computer Science and Artificial Intelligence at SR University for providing state-of-the-art computational infrastructure, modern gaming laboratories, and an inspiring academic environment conducive to advanced interactive media engineering.")
    add_body("Finally, we thank our peers and academic colleagues who participated in usability trials, playtesting audits, and gameplay balancing sessions. Their critical feedback on controls, combat responsiveness, and horror audio-visual immersion provided invaluable qualitative data that refined the game's mechanics and user experience.")

    # ==========================================
    # 3. ABSTRACT
    # ==========================================
    add_h1("3. Abstract")
    add_body("This project report documents the design, architectural implementation, optimization, and evaluation of \"Zombie Runner\", an advanced 3D endless survival horror runner game engineered in Unity 6 (6000.5.9f1) utilizing the Universal Render Pipeline (URP 17.5.0) and C# (.NET Standard 2.1). Moving beyond conventional endless runners that rely exclusively on passive obstacle dodging, Zombie Runner introduces an active survival horror combat loop. The player navigates an apocalyptic landscape spanning crumbling urban ruins and subterranean subway tunnels across three discrete lanes, executing grounded jumps, low-clearance combat slides, and forward raycast shooting against dynamic undead threats.")
    add_body("The game architecture features: (1) an endless modular procedural environment streaming system with 30-meter road and subway tunnel segments recycling dynamically in a 5-segment circular object pool; (2) a modular enemy AI system utilizing ScriptableObjects to configure distinct zombie archetypes—Common Runner, Fast Sprinter, and Heavy Brute—governed by Mecanim finite state machines and 3D spatialized logarithmic audio emitters; (3) a responsive combat engine with forward raycasting, auto-aim target tracking, weapon recoil kinematics, illuminated bullet tracers, and pre-allocated, zero-allocation particle impact pooling; (4) a 4-tier adaptive horror music system that seamlessly crossfades between exploration, tension, active combat, and critical health states; and (5) a persistent player economy tracking gold coins, ammunition reserves, medical supplies, high scores, and a single shielded revive loop.")
    add_body("Performance profiling confirms stable 60 frames per second (FPS) execution with minimal memory allocations, eliminating Garbage Collection stutter. The complete codebase, assets, and Android build configurations are integrated cleanly, fulfilling the rigorous learning objectives of modern game development.")
    add_body("Game Mechanics, 3D Endless Runner, Survival Horror, Unity 6, Universal Render Pipeline (URP), Finite State Machine, Zombie AI, Raycast Combat, Object Pooling, Adaptive Audio.", bold_prefix="Keywords: ")

    doc.add_page_break()

    # ==========================================
    # 4. TABLE OF CONTENTS & LIST OF FIGURES/TABLES
    # ==========================================
    add_h1("4. Table of Contents")
    
    toc_table = doc.add_table(rows=20, cols=2)
    toc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    toc_widths = [Inches(5.7), Inches(0.8)]
    for row in toc_table.rows:
        for i, w in enumerate(toc_widths):
            row.cells[i].width = w

    toc_items = [
        ("1. Cover Page", "1"),
        ("2. Acknowledgement", "2"),
        ("3. Abstract", "2"),
        ("4. Table of Contents & Lists of Visual Assets", "3"),
        ("5. Introduction", "4"),
        ("6. Problem Statement", "4"),
        ("7. Objectives and Scope", "4"),
        ("8. Tools and Technologies", "5"),
        ("9. System Design and Architecture", "5"),
        ("10. Gameplay Mechanics and Controls", "6"),
        ("11. Environment and Visual Design", "7"),
        ("12. Zombie AI and Combat System", "8"),
        ("13. User Interface and Game Flow", "9"),
        ("14. Implementation Overview", "9"),
        ("15. Testing and Debugging", "10"),
        ("16. Challenges and Solutions", "10"),
        ("17. Learning Outcomes", "11"),
        ("18. Future Enhancements", "11"),
        ("19. Conclusion", "11"),
        ("20. References and Asset Credits", "11")
    ]
    for idx, (title, page) in enumerate(toc_items):
        row = toc_table.rows[idx]
        p0 = row.cells[0].paragraphs[0]
        p0.paragraph_format.space_after = Pt(1.5)
        r0 = p0.add_run(title)
        r0.font.name = "Calibri"
        r0.font.size = Pt(9.5)
        if title.split(".")[0].strip() in ["1", "5", "8", "9", "10", "11", "12", "13", "14", "15", "16", "19"]:
            r0.bold = True
        
        p1 = row.cells[1].paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p1.paragraph_format.space_after = Pt(1.5)
        r1 = p1.add_run(page)
        r1.font.name = "Calibri"
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = COLOR_MUTED

    add_h2("List of Figures")
    fig_items = [
        ("Figure 1", "Title Screen and 3D Survivor Character Staging (Audit_MainMenu_1_Overview)", "6"),
        ("Figure 2", "Main Menu Settings: Audio Mixer Bus Controls and Volume Persistence", "7"),
        ("Figure 3", "Keyboard and Mouse Input Configuration Reference Guide", "8"),
        ("Figure 4", "In-Game Nocturnal Environment and Atmospheric Lighting Transition", "9")
    ]
    for fig_id, fig_desc, fig_page in fig_items:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(1.5)
        r = p.add_run(f"{fig_id}: {fig_desc}")
        r.font.name = "Calibri"
        r.font.size = Pt(9)
        r.font.color.rgb = COLOR_DARK
        r_p = p.add_run(f"  ................................................................................  Page {fig_page}")
        r_p.font.name = "Calibri"
        r_p.font.size = Pt(8.5)
        r_p.font.color.rgb = COLOR_MUTED

    add_h2("List of Tables")
    tbl_items = [
        ("Table 1", "Primary Technology Stack and Engine Specifications", "5"),
        ("Table 2", "Core System Architecture and Manager Responsibilities", "5"),
        ("Table 3", "Player Locomotion, Kinematics, and Input Controls Reference", "6"),
        ("Table 4", "Zombie Enemy Archetypes and Behavioral Specifications", "8"),
        ("Table 5", "Collectibles, Economy, and Power-Up Specifications", "8"),
        ("Table 6", "Key Implementation Scripts and Software Module Directory", "9")
    ]
    for tbl_id, tbl_desc, tbl_page in tbl_items:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(1.5)
        r = p.add_run(f"{tbl_id}: {tbl_desc}")
        r.font.name = "Calibri"
        r.font.size = Pt(9)
        r.font.color.rgb = COLOR_DARK
        r_p = p.add_run(f"  ................................................................................  Page {tbl_page}")
        r_p.font.name = "Calibri"
        r_p.font.size = Pt(8.5)
        r_p.font.color.rgb = COLOR_MUTED

    doc.add_page_break()

    # ==========================================
    # 5. INTRODUCTION
    # ==========================================
    add_h1("5. Introduction")
    add_h2("5.1 Context and Evolution of the Genre")
    add_body("The endless runner genre represents one of the most commercially resilient and mechanically focused archetypes in contemporary video game design. Originally popularized by mobile pioneers such as Canabalt (2009), Temple Run (2011), and Subway Surfers (2012), the genre traditionally challenges players with reflex-driven avoidance of obstacles across a continuously generating, non-terminating path. However, despite high initial engagement, classic endless runners frequently suffer from mechanical fatigue: player actions are constrained strictly to evasion (jumping, ducking, shifting lanes), with virtually no proactive interaction, combat strategy, or resource management. Consequently, modern game design has trended toward hybrid genres that fuse high-speed traversal with secondary core loops such as tactical shooting, resource scavenging, and atmospheric storytelling.")

    add_h2("5.2 Project Overview and Design Philosophy")
    add_body("\"Zombie Runner\" was conceived to bridge the gap between fast-paced arcade endless runners and high-stakes survival horror games. Developed as a 3D endless survival horror runner in Unity 6, the game places the player in the role of an armed survivor navigating a post-apocalyptic cityscape and subterranean subway railway network overrun by reanimated undead. Unlike traditional runners, players cannot merely outrun every obstacle; aggressive zombie archetypes dynamically spawn in the player's path, actively lunging and pursuing across lanes. Survival necessitates a dynamic synthesis of agile spatial maneuvers (lane shifts, jumps over barricades, sliding beneath low obstacles) and decisive firearm combat (conserving ammunition, landing raycast headshots, and eliminating explosive hazards).")

    add_h2("5.3 Academic Motivation")
    add_body("Developed for the course Game Mechanics, Design and Development (23CS201PE407) in the School of Computer Science and Artificial Intelligence at SR University, this project serves as a comprehensive academic synthesis of fundamental game engineering principles. The implementation incorporates real-time physics simulation, procedural object pooling, finite state machine (FSM) AI design, Universal Render Pipeline (URP) shader customization, and dynamic spatial audio engineering. Through rigorous software engineering, the project addresses real-world game development challenges including Garbage Collection mitigation, frame-rate consistency, and cross-platform UI adaptability.")

    # ==========================================
    # 6. PROBLEM STATEMENT
    # ==========================================
    add_h1("6. Problem Statement")
    add_h2("6.1 Limitations in Traditional Endless Runners")
    add_body("A critical analysis of existing endless runner games reveals three primary mechanical and architectural limitations:")
    add_bullet("Mono-Dimensional Evasion Loop: Gameplay relies entirely on passive dodging. The absence of defensive or offensive counter-mechanisms renders encounters predictable and reduces tactical decision-making.", bold_prefix="1. ")
    add_bullet("Predictable Environmental Staging: Typical runners employ static daytime lighting, brightly saturated cartoon palettes, and repetitive static tile sets that fail to evoke emotional tension or atmospheric immersion.", bold_prefix="2. ")
    add_bullet("Mechanical Disconnect in Combat Prototypes: Prior attempts to integrate shooting into endless runners often resulted in awkward targeting, imprecise hit registration, or significant computational stutter caused by continuous instantiation of projectiles and particle systems.", bold_prefix="3. ")

    add_h2("6.2 Technical and Engineering Challenges")
    add_body("To overcome these limitations, Zombie Runner addresses four specific technical hurdles:")
    add_bullet("Real-Time Hitscan Combat at High Forward Velocities: Harmonizing forward player translation (8 to 16 m/s) with raycast weapon aiming, visual recoil, and projectile tracer rendering without visual desynchronization.", bold_prefix="A. ")
    add_bullet("Object Lifecycle and Garbage Collection Overhead: Managing hundreds of streamed 30m modular city/tunnel segments, obstacles, collectibles, bullet tracers, and particle bursts without runtime GC memory allocation.", bold_prefix="B. ")
    add_bullet("Atmospheric Horror Lighting vs. Gameplay Readability: Creating a dark, foggy survival horror atmosphere (cool moonlight, flickering streetlamps, trilight ambient bounce) while ensuring obstacles and enemy silhouettes remain identifiable at high speeds.", bold_prefix="C. ")
    add_bullet("AI Spawner Deadlock Prevention: Ensuring enemy spawners and obstacle pools recycle cleanly without memory leaks or capping concurrent alive limits when actors pass behind the runner.", bold_prefix="D. ")

    # ==========================================
    # 7. OBJECTIVES AND SCOPE
    # ==========================================
    add_h1("7. Objectives and Scope")
    add_h2("7.1 Primary Objectives")
    add_bullet("Modular Game Architecture: Develop a decoupled, component-based Unity 6 architecture in C# adhering to object-oriented principles, ScriptableObject data separation, and interface-driven combat (IDamageable).", bold_prefix="1. ")
    add_bullet("Responsive Player Kinematics: Implement a CharacterController runner supporting instant 3-lane shifts, grounded jump physics, low-profile sliding with collision box adjustment, and progressive difficulty acceleration.", bold_prefix="2. ")
    add_bullet("Tactical Zombie AI & Combat Engine: Engineer three distinct zombie archetypes (Common Runner, Fast Sprinter, Heavy Brute) governed by Mecanim FSMs, accompanied by hitscan raycast shooting, dynamic auto-aim, and pooling.", bold_prefix="3. ")
    add_bullet("Endless Modular Environment Streaming: Construct a circular pooling system seamlessly recycling 30m modular Abandoned City and Subterranean Subway Tunnel segments with dynamic lighting and fog transitions.", bold_prefix="4. ")
    add_bullet("Layered Adaptive Horror Audio: Implement a 4-tier dynamic audio system in Unity AudioMixer crossfading across exploration, tension, combat, and critical health states, coupled with 3D spatialized positional zombie audio.", bold_prefix="5. ")
    add_bullet("Comprehensive UI and Persistence: Design a complete UI flow (Main Menu, HUD, Settings, Game Over) with PlayerPrefs high-score caching and a single shielded revive loop per run.", bold_prefix="6. ")

    add_h2("7.2 Project Scope & Boundaries")
    add_body("The primary implementation target is Windows PC Standalone with full keyboard and mouse input. In addition, the codebase has been structured and verified for mobile compilation readiness, including portrait layout orientation, safe-area screen fitting, touch/swipe input handling, and successful Android APK compilation (Builds/Android/ZombieRunner.apk, 42.9 MB). Explicitly outside the current project scope and designated as future enhancements are online multiplayer leaderboards, networked co-op, procedural branching road mazes, and in-app microtransactions.")

    doc.add_page_break()

    # ==========================================
    # 8. TOOLS AND TECHNOLOGIES
    # ==========================================
    add_h1("8. Tools and Technologies")
    add_body("The development of Zombie Runner utilized industry-standard software tools, modern rendering pipelines, and modular programming frameworks. Table 1 summarizes the core technology stack.")
    
    # Table 1: Tech Stack
    t1 = doc.add_table(rows=7, cols=3)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t1)
    w_t1 = [Inches(1.8), Inches(2.2), Inches(2.7)]
    for row in t1.rows:
        for i, w in enumerate(w_t1):
            row.cells[i].width = w

    t1_headers = ["Domain / Component", "Technology / Version", "Academic & Technical Rationale"]
    for i, h in enumerate(t1_headers):
        cell = t1.rows[0].cells[i]
        set_cell_background(cell, "0B3B60")
        set_cell_margins(cell, 120, 120, 150, 150)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    t1_rows = [
        ("Game Engine", "Unity 6 (6000.5.9f1)", "High-performance C# runtime, unified build pipeline, robust profiler, and modern URP graphics features."),
        ("Render Pipeline", "Universal Render Pipeline (17.5.0)", "Optimized single-pass Forward+ rendering, custom Lit PBR materials, ACES tonemapping, and volumetric fog."),
        ("Programming Language", "C# (.NET Standard 2.1)", "Object-oriented, type-safe architecture, garbage-collection control, and efficient memory layouts."),
        ("Input Framework", "Unity Input System (1.20.0)", "Event-driven cross-platform input supporting both keyboard/mouse and mobile touchscreen fallbacks."),
        ("UI System", "TextMeshPro / uGUI (2.5.0)", "SDF font rendering for crisp text at all resolutions, safe-area anchoring, and 9-sliced procedural sprites."),
        ("Character Animation", "Adobe Mixamo & Mecanim", "Humanoid avatar retargeting, baked in-place root motion, and multi-layer state machines.")
    ]
    for idx, (c1, c2, c3) in enumerate(t1_rows):
        row = t1.rows[idx + 1]
        bg = "F7FAFC" if idx % 2 == 1 else "FFFFFF"
        for c_i, val in enumerate([c1, c2, c3]):
            cell = row.cells[c_i]
            set_cell_background(cell, bg)
            set_cell_margins(cell, 80, 80, 120, 120)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.1
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(9)
            if c_i == 0:
                r.bold = True
            r.font.color.rgb = COLOR_DARK

    add_body("Version control was maintained via Git with Git Large File Storage (LFS) configured for tracking high-resolution 3D models (FBX), 16-bit uncompressed audio (WAV), and PBR textures (PNG). Custom editor automation scripts were authored under Assets/ZombieRunner/Scripts/Editor/ to ensure idempotent project configuration and automated scene verification.", bold_prefix="\nBuild & Repository Management: ")

    # ==========================================
    # 9. SYSTEM DESIGN AND ARCHITECTURE
    # ==========================================
    add_h1("9. System Design and Architecture")
    add_h2("9.1 High-Level Architecture Overview")
    add_body("Zombie Runner is structured around a decoupled, component-based architecture following Unity's Entity-Component model. Rather than tightly coupling systems through direct monolithic references, components communicate using C# events, interfaces (e.g., IDamageable for combat targets), and centralized singleton managers for core game loops. This ensures high modularity, testability, and isolated failure domains.")

    add_h2("9.2 Core Managers and Responsibilities")
    add_body("The software architecture is partitioned into distinct functional subsystems coordinated by dedicated managers, as outlined in Table 2.")

    # Table 2: Architecture Managers
    t2 = doc.add_table(rows=6, cols=3)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t2)
    w_t2 = [Inches(1.8), Inches(2.2), Inches(2.7)]
    for row in t2.rows:
        for i, w in enumerate(w_t2):
            row.cells[i].width = w

    t2_headers = ["Subsystem Manager", "Namespace / Script", "Architectural Role & Key Methods"]
    for i, h in enumerate(t2_headers):
        cell = t2.rows[0].cells[i]
        set_cell_background(cell, "0B3B60")
        set_cell_margins(cell, 120, 120, 150, 150)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    t2_rows = [
        ("Game Lifecycle", "GameManager.cs\n(ZombieRunner.Core)", "Coordinates global game states (Play, Pause, GameOver), timeScale manipulation, mobile frame rates, and the 1-time revive token."),
        ("Score & Economy", "ScoreManager.cs / SaveManager.cs\n(ZombieRunner.Core)", "Tracks distance and kill points, commits high scores and banked coins to PlayerPrefs, and triggers high-score record alerts."),
        ("World Streaming", "EndlessRoadManager.cs /\nEnvironmentThemeManager.cs", "Maintains circular pools of 30m road and subway segments; interpolates trilight lighting, fog, and point lights across biomes."),
        ("Combat & VFX Pooling", "ShootingController.cs /\nHitImpactManager.cs", "Executes forward raycast hitscan checks, auto-aim math, recoil kickback, bullet tracers, and pre-allocated blood/spark particle pools."),
        ("Audio & Ambience", "AudioManager.cs /\nAdaptiveMusicController.cs", "Controls master AudioMixer buses (Master, Music, Ambient, SFX, UI) with logarithmic dB curves and crossfades 4 adaptive horror stems.")
    ]
    for idx, (c1, c2, c3) in enumerate(t2_rows):
        row = t2.rows[idx + 1]
        bg = "F7FAFC" if idx % 2 == 1 else "FFFFFF"
        for c_i, val in enumerate([c1, c2, c3]):
            cell = row.cells[c_i]
            set_cell_background(cell, bg)
            set_cell_margins(cell, 80, 80, 120, 120)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.1
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            if c_i == 0:
                r.bold = True
            r.font.color.rgb = COLOR_DARK

    add_callout("All damageable entities—including all zombie archetypes, player health, and explosive barrels—implement the IDamageable interface (TakeDamage(int amount, Vector3 hitPoint, Vector3 hitNormal)). This abstraction allows the weapon raycast system to remain completely agnostic of the specific target entity type, eliminating tight coupling and hard class dependencies.")

    doc.add_page_break()

    # ==========================================
    # 10. GAMEPLAY MECHANICS AND CONTROLS
    # ==========================================
    add_h1("10. Gameplay Mechanics and Controls")
    add_h2("10.1 Player Locomotion and Three-Lane Navigation")
    add_body("Player movement is governed by PlayerController.cs utilizing Unity's CharacterController component. The player navigates across three discrete lanes positioned at X = -3.0m (Left), X = 0.0m (Center), and X = +3.0m (Right). Horizontal lane switching utilizes smooth frame-rate independent interpolation (Mathf.MoveTowards or Vector3.Lerp) at a configurable lane-switch speed of 14 m/s, providing crisp, responsive lane snapping without jerky camera jitter.")
    add_body("To establish an escalating tension curve, the runner incorporates progressive forward acceleration: starting from an initial velocity of 8.0 m/s, forward speed scales continuously at a rate of 0.005 m/s² up to a maximum terminal velocity of 16.0 m/s. This ensures early accessibility for new players while challenging experienced players with extreme reaction demands at extended distances.")

    add_h2("10.2 Jump Kinematics and Timed Combat Slide Physics")
    add_body("Vertical locomotion and low obstacle evasion are implemented with strict physical ballistics:")
    add_bullet("Jump Ballistics: Jump launch velocity is derived kinematically via v_y = sqrt(2 * |g| * h), where gravity g = -20.0 m/s² and jump height h = 1.8m. Jumping is strictly grounded; an airborne state flag (isJumping) locks premature double jumps and prevents landing transition flickers.", bold_prefix="• ")
    add_bullet("Combat Slide Mechanics: Triggering a slide initiates a 0.8-second low-profile slide. The CharacterController's collision height is dynamically reduced from 2.0m to 1.05m and its center Y-offset adjusted from 1.0m to 0.525m, enabling the survivor to slip under overhead pipes, subway tunnel beams, and barrier blockades. Crucially, visual scaling is isolated from the humanoid skeletal rig, ensuring the character model does not squash unnaturally or penetrate the asphalt surface.", bold_prefix="• ")

    add_h2("10.3 Raycast Weapon Mechanics and Visual Recoil")
    add_body("Combat is managed by ShootingController.cs. When the player triggers fire, the system casts an instantaneous forward raycast along the weapon trajectory. An auto-aim cone calculation (angle <= 12°, range <= 32m) dynamically identifies the nearest IDamageable zombie in the forward corridor. Upon hit registration, the target takes damage, a glowing bullet tracer (BulletTracer.cs) interpolates from the muzzle socket to the impact point, and a blood or spark particle effect is triggered from the object pool. Firing produces procedural visual weapon kickback (0.07m rearward translation, 3.5° muzzle climb) and triggers a momentary point light flash, imparting heavy tactile feedback.")

    add_h2("10.4 Collectibles, Economy, and Power-Up Dynamics")
    add_body("Scattered along the road and tunnel corridors are interactive collectibles managed by CollectibleManager.cs and PowerUpManager.cs. Gold coins increase run currency and bank permanently into PlayerPrefs upon run completion. Ammunition boxes refill +15 rounds, while medical kits restore +25 HP. Additionally, four timed power-ups provide game-altering buffs: (1) Energy Shield (absorbs one lethal collision/attack); (2) Coin Magnet (draws coins within 8m radius); (3) Speed Boost (+50% forward velocity with temporary invulnerability); and (4) Double Coins (2x multiplier on coin rewards).")

    # Table 3: Controls Reference
    t3 = doc.add_table(rows=6, cols=3)
    t3.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t3)
    w_t3 = [Inches(1.8), Inches(2.2), Inches(2.7)]
    for row in t3.rows:
        for i, w in enumerate(w_t3):
            row.cells[i].width = w

    t3_headers = ["Action", "Primary Keyboard Key", "Secondary / Mouse / Touch"]
    for i, h in enumerate(t3_headers):
        cell = t3.rows[0].cells[i]
        set_cell_background(cell, "0B3B60")
        set_cell_margins(cell, 120, 120, 150, 150)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    t3_rows = [
        ("Move Left / Right", "A / D", "Left Arrow / Right Arrow / Touch Swipe"),
        ("Jump (Clear Hurdles)", "W / Space", "Up Arrow / Swipe Up"),
        ("Slide (Under Barriers)", "S", "Down Arrow / Swipe Down"),
        ("Shoot Firearm", "F", "Left Mouse Button / On-Screen Fire Button"),
        ("Pause / Resume", "Escape", "P / UI Pause Button")
    ]
    for idx, (c1, c2, c3) in enumerate(t3_rows):
        row = t3.rows[idx + 1]
        bg = "F7FAFC" if idx % 2 == 1 else "FFFFFF"
        for c_i, val in enumerate([c1, c2, c3]):
            cell = row.cells[c_i]
            set_cell_background(cell, bg)
            set_cell_margins(cell, 80, 80, 120, 120)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(9)
            if c_i == 0:
                r.bold = True
            r.font.color.rgb = COLOR_DARK

    # Screenshot 1: Overview
    ss_overview = r"E:\zombie runner\Screenshots\Audit_MainMenu_1_Overview.png"
    add_figure(ss_overview, "Figure 1: Title Screen and 3D Survivor Character Staging (Audit_MainMenu_1_Overview)")

    doc.add_page_break()

    # ==========================================
    # 11. ENVIRONMENT AND VISUAL DESIGN
    # ==========================================
    add_h1("11. Environment and Visual Design")
    add_h2("11.1 Modular Streaming Architecture and Endless Road Pooling")
    add_body("To maintain infinite gameplay without unbounded memory consumption, EndlessRoadManager.cs and EnvironmentThemeManager.cs maintain circular pools of five 30-meter environment segments (totaling 150 meters of actively rendered world). When a segment trails the player by more than 35 meters along the Z-axis, it is deactivated, translated forward to the head of the queue (Z_new = Z_lead + 30m), and reactivated with freshly populated obstacle and collectible distributions. This circular recycling operates with zero runtime memory allocations.")

    add_h2("11.2 Biome Aesthetics: Abandoned City Ruins and Subterranean Subway Tunnel")
    add_body("The game dynamically streams across distinct visual biomes every 300 meters, creating continuous atmospheric variety:")
    add_bullet("Abandoned City Ruins: Decaying multi-story brick facades, cracked asphalt with worn yellow road striping, concrete rubble, rusted barriers, and flickering sodium-vapor streetlights evoke an authentic nocturnal apocalypse.", bold_prefix="1. ")
    add_bullet("Subterranean Subway Tunnel: Engineered as a continuous 30m modular enclosure featuring solid 5.2m reinforced concrete side-walls, a 15.5m wide ceiling with 45-degree vaulted arches, heavy portal rib columns every 7.5m, industrial overhead ventilation shafts, dual high-voltage cable trays, steel railway tracks, and embedded concrete sleepers. Overhead neutral luminaires (4200K) and caged amber emergency bulkheads (2200K) cast deep shadows, creating claustrophobic survival horror tension.", bold_prefix="2. ")

    add_h2("11.3 Cinematic Horror Lighting, Trilight Ambient Bounce, and Volumetric Fog")
    add_body("Lighting design in Zombie Runner strictly balances survival horror gloom with competitive runner visibility:")
    add_bullet("Cool-Blue Directional Moonlight: A key directional light (hex #C0D6FA, intensity 1.75) establishes a chilling nocturnal baseline.", bold_prefix="• ")
    add_bullet("Trilight Ambient Bounce Lighting: Configured across all theme profiles (Sky #576785, Equator #47546B, Ground #384052) to eliminate pure black pitch shadows and preserve texture definition on character clothing and road surfaces.", bold_prefix="• ")
    add_bullet("Calibrated Linear Atmospheric Fog: Fog is configured with a 42-meter start distance and 165-meter end distance. This critical calibration ensures the immediate 42-meter gameplay corridor remains crystal-clear for rapid obstacle detection and zombie targeting, while the background dissolves into deep, atmospheric dread.", bold_prefix="• ")
    add_bullet("Player Tactical Flashlight: Mounted to the weapon muzzle is a dual-beam spotlight setup (a high-intensity 48m narrow beam and a 40m wide fill beam) that sweeps dynamically with auto-aim tracking, piercing dark subway tunnels.", bold_prefix="• ")

    # Screenshot 2: Settings Audio
    ss_audio = r"E:\zombie runner\Screenshots\Audit_MainMenu_3_Settings_Audio.png"
    add_figure(ss_audio, "Figure 2: Main Menu Settings: Audio Mixer Bus Controls and Volume Persistence")

    doc.add_page_break()

    # ==========================================
    # 12. ZOMBIE AI AND COMBAT SYSTEM
    # ==========================================
    add_h1("12. Zombie AI and Combat System")
    add_h2("12.1 ScriptableObject Architecture and Archetype Design")
    add_body("Enemy parameters in Zombie Runner are strictly decoupled from executable code using Unity ScriptableObjects (ZombieConfig.cs). Designers can author, tune, and test new enemy variants in the Inspector without recompiling scripts. Table 4 specifies the operational attributes of the three implemented zombie archetypes.")

    # Table 4: Zombie Archetypes
    t4 = doc.add_table(rows=4, cols=6)
    t4.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t4)
    w_t4 = [Inches(1.2), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.1)]
    for row in t4.rows:
        for i, w in enumerate(w_t4):
            row.cells[i].width = w

    t4_headers = ["Archetype", "3D Model / Rig", "Health", "Speed", "Damage / Range", "Points"]
    for i, h in enumerate(t4_headers):
        cell = t4.rows[0].cells[i]
        set_cell_background(cell, "0B3B60")
        set_cell_margins(cell, 100, 100, 120, 120)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(255, 255, 255)

    t4_rows = [
        ("Common Runner", "Mixamo Ch10 (Humanoid)", "3 HP (3 shots)", "5.0 m/s", "10 DMG / 1.8m", "100 pts"),
        ("Fast Sprinter", "Yaku J Ignite (Humanoid)", "2 HP (2 shots)", "7.5 m/s", "8 DMG / 1.6m", "150 pts"),
        ("Heavy Brute", "Pumpkinhulk (Humanoid)", "8 HP (8 shots)", "3.2 m/s", "25 DMG / 2.2m", "250 pts")
    ]
    for idx, row_data in enumerate(t4_rows):
        row = t4.rows[idx + 1]
        bg = "F7FAFC" if idx % 2 == 1 else "FFFFFF"
        for c_i, val in enumerate(row_data):
            cell = row.cells[c_i]
            set_cell_background(cell, bg)
            set_cell_margins(cell, 80, 80, 100, 100)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            if c_i == 0:
                r.bold = True
            r.font.color.rgb = COLOR_DARK

    add_h2("12.2 AI State Machine and Animation Retargeting")
    add_body("Zombie behavior is orchestrated via ZombieController.cs driving a Mecanim Animator Controller. The state machine transitions across Idle, Walk, Run, Attack, Hit Reaction, and Death states. All locomotion animations (extracted from Mixamo's Scary Zombie Pack) have their translation baked into root motion pose curves, allowing C# translation to handle actual forward lane velocity without desynchronizing footfalls. When hit, zombies play an upper-body flinch before resuming pursuit; upon lethal damage, they collapse backward or forward and disable collisions instantly.")

    add_h2("12.3 Positional 3D Audio and Spatial Attenuation")
    add_body("Every zombie prefab incorporates ZombieSoundEmitter.cs, which routes groans, guttural snarls, and attack lunges through custom 3D AudioSource components. Logarithmic spatial attenuation (minDistance = 2.5m, maxDistance = 24m) provides auditory depth perception, allowing players wearing headphones to pinpoint approaching undead by directional audio cues before they emerge from the distant fog.")

    add_h2("12.4 Combat Feedback and GC-Free Particle Pooling")
    add_body("Combat impacts utilize HitImpactManager.cs, an object pooling manager pre-warming pools of blood splatter VFX, metal ricochet sparks, and concrete impact dust. When high-speed automatic weapon fire strikes enemies or walls, pooled particles are repositioned and activated rather than instantiated dynamically, guaranteeing 0 bytes of heap allocation per shot and preventing GC frame spikes.")

    # Screenshot 3: Controls
    ss_ctrl = r"E:\zombie runner\Screenshots\Audit_MainMenu_4_Settings_Controls.png"
    add_figure(ss_ctrl, "Figure 3: Keyboard and Mouse Input Configuration Reference Guide")

    doc.add_page_break()

    # ==========================================
    # 13. USER INTERFACE AND GAME FLOW
    # ==========================================
    add_h1("13. User Interface and Game Flow")
    add_h2("13.1 Main Menu Experience and Survivor Staging")
    add_body("The title screen (ZombieRunnerMainMenu.unity) establishes an immersive presentation. Rather than static 2D buttons over a flat image, the scene features a fully lit 3D survivor character (Mixamo Ch05) equipped with the Tommy Gun, framed by a cinematic panning camera and subtle atmospheric ash particles. Players can navigate to Play, open multi-tabbed Settings (Graphics quality toggles, AudioMixer decibel sliders for Master/Music/SFX, and Input Control guides), or inspect team Credits.")

    add_h2("13.2 Heads-Up Display (HUD) and Real-Time State Tracking")
    add_body("The in-game HUD (UIManager.cs) provides essential survival metrics using TextMeshPro: (1) real-time distance traversed in meters; (2) current run score (Score = Distance + Kills); (3) coin counter; (4) remaining ammunition with low-ammo warnings; (5) a color-coded segmented health bar; and (6) active power-up countdown icons. The HUD incorporates SafeAreaFitter.cs, which queries Screen.safeArea to guarantee that UI elements remain fully visible and unobstructed on modern mobile screens with notches or camera cutouts.")

    add_h2("13.3 Game Over, High Score Celebration, and Revive Flow")
    add_body("When player health drops to zero, the game transitions to the Game Over state. Run statistics are displayed alongside persistent high scores loaded from PlayerPrefs. If the current run surpasses the record, the UI highlights a prominent `(NEW BEST!)` celebratory banner. Players have access to Retry, Return to Menu, and a one-time Shielded Revive button. Choosing Revive grants the player full health, 30 ammunition rounds, and a 3-second invulnerability shield, resuming the run seamlessly.")

    # ==========================================
    # 14. IMPLEMENTATION OVERVIEW
    # ==========================================
    add_h1("14. Implementation Overview")
    add_body("The project codebase consists of 25 modular C# gameplay and system scripts organized under Assets/ZombieRunner/Scripts/, complemented by 11 custom editor utilities. Table 6 provides an architectural directory breakdown.")

    # Table 6: Scripts Directory
    t6 = doc.add_table(rows=7, cols=3)
    t6.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t6)
    w_t6 = [Inches(1.5), Inches(2.3), Inches(2.9)]
    for row in t6.rows:
        for i, w in enumerate(w_t6):
            row.cells[i].width = w

    t6_headers = ["Module Directory", "Primary C# Scripts", "System Responsibility"]
    for i, h in enumerate(t6_headers):
        cell = t6.rows[0].cells[i]
        set_cell_background(cell, "0B3B60")
        set_cell_margins(cell, 100, 100, 120, 120)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(255, 255, 255)

    t6_rows = [
        ("Core", "GameManager.cs, SaveManager.cs, ScoreManager.cs", "State coordination, PlayerPrefs high score & banked coin persistence."),
        ("Player", "PlayerController.cs, PlayerHealth.cs, RunnerCameraFollow.cs", "Three-lane locomotion, jump/slide mechanics, health events, follow camera."),
        ("Enemies", "ZombieController.cs, ZombieSpawner.cs, ZombieSoundEmitter.cs, ZombieConfig.cs", "FSM enemy behavior, ScriptableObject stats, lane-aware spawner, 3D audio."),
        ("Weapons", "ShootingController.cs, BulletTracer.cs, HitImpactManager.cs", "Raycast combat, auto-aim math, recoil kickback, tracer & impact pooling."),
        ("World", "EndlessRoadManager.cs, EnvironmentThemeManager.cs, StreetlightFlicker.cs", "Circular segment pooling, theme blending, trilight lighting, lamp flicker."),
        ("Audio", "AudioManager.cs, AdaptiveMusicController.cs, AmbientAudioController.cs", "AudioMixer bus routing, 4-tier synchronized adaptive horror stems, ambient stingers.")
    ]
    for idx, (c1, c2, c3) in enumerate(t6_rows):
        row = t6.rows[idx + 1]
        bg = "F7FAFC" if idx % 2 == 1 else "FFFFFF"
        for c_i, val in enumerate([c1, c2, c3]):
            cell = row.cells[c_i]
            set_cell_background(cell, bg)
            set_cell_margins(cell, 80, 80, 100, 100)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            if c_i == 0:
                r.bold = True
            r.font.color.rgb = COLOR_DARK

    # Screenshot 4: Gameplay Transition
    ss_gameplay = r"E:\zombie runner\Screenshots\Audit_MainMenu_6_GameplayTransition.png"
    add_figure(ss_gameplay, "Figure 4: In-Game Nocturnal Environment and Atmospheric Lighting Transition")

    doc.add_page_break()

    # ==========================================
    # 15. TESTING AND DEBUGGING
    # ==========================================
    add_h1("15. Testing and Debugging")
    add_h2("15.1 Verification Workflow and Custom Editor Tools")
    add_body("Testing in Zombie Runner combined continuous Unity Editor Play Mode audits with custom diagnostic tools authored in C#. Utilities such as ZombieCombatSystemValidator.cs, VisualAuditHelper.cs, and ProjectPolisher.cs were developed to automatically validate scene hierarchy references, verify that all SkinnedMeshRenderers have valid URP Lit materials, confirm that Humanoid Avatars are bound without missing bone mappings, and audit AudioMixer group assignments.")

    add_h2("15.2 Gameplay Systems Verification")
    add_body("Rigorous verification scenarios were executed across all core mechanics:")
    add_bullet("Locomotion Bounds: Verified that rapid directional inputs clamp strictly between X = -3.0m and X = +3.0m without overshooting or getting stuck on road curbs.", bold_prefix="• ")
    add_bullet("Jump & Slide Isolation: Confirmed that triggering Jump while airborne is rejected, and that triggering Slide while jumping is locked until the CharacterController confirms grounded status.", bold_prefix="• ")
    add_bullet("Combat Hit Registration: Verified that raycast shots correctly decrement zombie health (Normal: 3 shots, Fast: 2 shots, Heavy: 8 shots) and that zero-health triggers lethal collapse and collider deactivation immediately.", bold_prefix="• ")
    add_bullet("Power-Up Timers: Verified that re-collecting an active power-up refreshes its countdown duration rather than stacking speed or multiplier values multiplicatively.", bold_prefix="• ")

    add_h2("15.3 Performance Profiling and GC Suppression")
    add_body("Memory profiling was conducted using Unity Profiler. By implementing object pooling for road segments, subway tunnels, obstacles, collectibles, bullet tracers, and particle bursts, runtime memory allocations were reduced to virtually zero bytes during continuous running, eliminating GC spikes and sustaining solid 60 FPS performance on target hardware.")

    add_h2("15.4 Build Verification")
    add_body("The project was verified as a standalone Windows PC executable and prepared for Android deployment. The Android build configuration (Tools > Zombie Runner > Prepare Android Build) was executed, configuring IL2CPP 64-bit compilation, ARM64 target architecture, minimum Android API 26 (Android 8.0 Oreo), and the Mobile URP quality tier. The build completed successfully, outputting Builds/Android/ZombieRunner.apk (42,953,718 bytes) with zero compilation errors.")

    # ==========================================
    # 16. CHALLENGES AND SOLUTIONS
    # ==========================================
    add_h1("16. Challenges and Solutions")
    add_body("During the engineering lifecycle of Zombie Runner, six major technical challenges emerged and were resolved:")
    
    add_body("Challenge: Modifying CharacterController height to 1.05m during a slide caused placeholder capsule meshes to squash, but when humanoid Mixamo character models (Ch05) were integrated, applying visual scaling distorted the skeletal proportions and pushed character feet below the road surface (Y < -1.0m).\nSolution: Decoupled collision box scaling from visual transform hierarchy in PlayerController.cs. Visual squash scaling is restricted exclusively to unrigged placeholder meshes (if (visualRoot != null && animator == null)), while rigged humanoid characters play the authentic Mixamo Running Slide animation at 1.95x synchronized playback speed, preserving anatomic proportions and perfect ground contact.", bold_prefix="1. Humanoid Mesh Distortion During Combat Slide: ")

    add_body("Challenge: CharacterController.isGrounded evaluated to true on the very first frame of a jump before upward velocity cleared the physical collision skin width, causing the Animator Controller transition (Jump -> Run with condition Grounded == true) to cancel the jump animation instantly on frame 1.\nSolution: Implemented an explicit isJumping boolean flag in PlayerController.cs. Upon jump launch, isJumping is set to true, resetting the jump trigger and forcing Grounded to false. The flag remains true while verticalSpeed > 0, clearing only when descending (verticalSpeed <= 0) and physically touching ground, ensuring complete jump arc animation playback.", bold_prefix="2. Launch-Frame Premature Jump Cancellation: ")

    add_body("Challenge: In rapid playtests, zombie spawns completely stopped after 30-40 seconds of running.\nSolution: Audit revealed that zombies passed by the runner remained alive behind the camera, causing the concurrent alive counter to reach maximumAlive (6) and permanently halting subsequent spawns. Added automated distance cleanup in ZombieSpawner.cs that checks if active zombies trail the player by > 12 meters, silently destroying them and resetting spawn slots without awarding unearned score.", bold_prefix="3. Enemy Spawner Deadlock Bug: ")

    add_body("Challenge: Over 100 console errors appeared stating: \"Setting the duration while system is still playing is not supported.\"\nSolution: In HitImpactManager.cs, AddComponent<ParticleSystem>() was called on an active GameObject, triggering immediate playback on Awake before custom duration properties were modified. Resolved by instantiating the GameObject in an inactive state (go.SetActive(false)), calling ps.Stop(true, ParticleSystemStopBehavior.StopEmittingAndClear), setting duration safely, and re-activating on demand.", bold_prefix="4. Particle System Lifecycle Mutation Error: ")

    add_body("Challenge: The initial Subway Tunnel segment rendered as disconnected open rectangular frames with strong artificial cyan wash, allowing players to see daylight and creating repetitive visual artifacts.\nSolution: Completely reconstructed EnvironmentSegment_SubwayTunnel.prefab with continuous solid 5.2m concrete side walls, 15.5m ceiling with vaulted arches, heavy portal columns every 7.5m, overhead ventilation ducts, high-voltage cable trays, steel tracks, and neutral 4200K luminaires balanced with 2200K emergency caged lamps, eliminating daylight leakage and establishing deep horror atmosphere.", bold_prefix="5. Subterranean Repeating Blue Rectangular Frame Artifacts: ")

    add_body("Challenge: Early builds featured an irritating 6.0-second repeating wind loop with a harsh 480Hz-550Hz sine whistle and sharp 8-bit arcade UI beeps that destroyed horror immersion.\nSolution: Audited and overhauled audio architecture in Stage 26. Synthesized an organic 48.0s continuous Brownian wind bed and engineered a 4-layer synchronized 75 BPM adaptive horror music suite in D minor with an engineered 1.2kHz-4.2kHz frequency notch to keep gunshots and zombie growls punchy and intelligible.", bold_prefix="6. Harsh Audio Whistle Loop & Arcade Beeper Disconnect: ")

    doc.add_page_break()

    # ==========================================
    # 17. LEARNING OUTCOMES
    # ==========================================
    add_h1("17. Learning Outcomes")
    add_body("The development of Zombie Runner provided extensive practical experience in modern real-time graphics, physics, and gameplay programming:")
    add_bullet("Universal Render Pipeline Mastery: Gained deep expertise in configuring URP Lit materials, configuring ACES tonemapping, optimizing Trilight ambient lighting, and balancing volumetric fog for competitive visibility.", bold_prefix="• ")
    add_bullet("Character Animation Engineering: Mastered Mecanim Humanoid Avatar retargeting, bone mapping synchronization, in-place root motion baking, and multi-parameter state machine transitions.", bold_prefix="• ")
    add_bullet("Real-Time Combat Math: Implemented raycast hitscan math, dynamic auto-aim cone angle calculations, visual weapon kickback kinematics, and bullet tracer line rendering.", bold_prefix="• ")
    add_bullet("Decoupled Systems Architecture: Applied object-oriented design patterns including ScriptableObject data encapsulation, interface-based messaging (IDamageable), and pre-allocated circular object pooling.", bold_prefix="• ")
    add_bullet("Dynamic Adaptive Audio: Engineered layered audio crossfading, logarithmic decibel volume conversion, and 3D spatialized sound attenuation curves.", bold_prefix="• ")

    # ==========================================
    # 18. FUTURE ENHANCEMENTS
    # ==========================================
    add_h1("18. Future Enhancements")
    add_body("While the current implementation fulfills all core project specifications, several high-value features have been architected as prospective future enhancements:")
    add_bullet("Advanced AI Behaviors: Implementing flocking behaviors and ranged acid-spitting mutants that force players to dodge incoming projectile arcs while running.", bold_prefix="1. ")
    add_bullet("Expanded Weapon Arsenal: Integrating collectible shotguns (wide-spread clearing), automatic assault rifles, and grenade launchers with distinct ammo economies.", bold_prefix="2. ")
    add_bullet("Dynamic Boss Encounters: Procedural subway tunnel breach events featuring a massive pursuing Nemesis brute that must be damaged over sustained running distance.", bold_prefix="3. ")
    add_bullet("Online Leaderboards & Ghost Racing: RESTful cloud database integration allowing asynchronous ghost runner playback and global competitive ranking.", bold_prefix="4. ")
    add_bullet("Dynamic Weather System: Screen-space rain droplets, volumetric lightning strikes that dynamically cast long shadows, and destructible road barricades.", bold_prefix="5. ")

    # ==========================================
    # 19. CONCLUSION
    # ==========================================
    add_h1("19. Conclusion")
    add_body("Zombie Runner successfully demonstrates that the high-speed kinetic appeal of the 3D endless runner genre can be synergistically fused with the tactical resource management and psychological tension of survival horror. Through disciplined software engineering in Unity 6 and URP, the project realized responsive three-lane navigation, physics-based jumping, low-clearance combat sliding, and visceral raycast shooting. The implementation of circular modular environment streaming, ScriptableObject-driven enemy archetypes, layered adaptive audio, and GC-suppressed particle pooling guarantees a polished, high-framerate gameplay experience.")
    add_body("Academic evaluation under the curriculum of Game Mechanics, Design and Development (23CS201PE407) confirms that all learning outcomes and technical milestones were rigorously accomplished, establishing a robust foundation for future commercial or academic game engineering endeavors.")

    # ==========================================
    # 20. REFERENCES AND ASSET CREDITS
    # ==========================================
    add_h1("20. References and Asset Credits")
    add_h2("20.1 Academic Literature and Technical References")
    add_bullet("Unity Technologies. (2025). Unity 6 User Manual and Universal Render Pipeline (URP 17.5) Documentation. San Francisco, CA.", bold_prefix="[1] ")
    add_bullet("Millington, I., & Funge, J. (2018). Artificial Intelligence for Games (3rd ed.). CRC Press / Taylor & Francis Group.", bold_prefix="[2] ")
    add_bullet("Schell, J. (2019). The Art of Game Design: A Book of Lenses (3rd ed.). A K Peters / CRC Press.", bold_prefix="[3] ")
    add_bullet("Rogers, S. (2014). Level Up! The Guide to Great Video Game Design (2nd ed.). John Wiley & Sons.", bold_prefix="[4] ")
    add_bullet("Gregory, J. (2018). Game Engine Architecture (3rd ed.). CRC Press.", bold_prefix="[5] ")

    add_h2("20.2 Asset Credits and Licenses")
    add_bullet("Mixamo (Adobe Systems): Survivor Humanoid Model (Ch05, X Bot), Zombie Archetypes (Ch10 Common, Yaku J Ignite Fast Runner, Pumpkinhulk L Shaw Heavy Brute), and animation clips from Shooter Pack and Scary Zombie Pack. Licensed under Adobe Mixamo Software License (Royalty-free for commercial and non-commercial game development).", bold_prefix="• ")
    add_bullet("Weapon 3D Assets: High-detail Tommy Gun submachine gun model with PBR metallic-roughness workflow textures located at Assets/ZombieRunner/Models/Weapons/TommyGun/.", bold_prefix="• ")
    add_bullet("Audio Assets: Algorithmic horror soundscape stems and procedural audio generator released under CC0 / Public Domain. Full breakdown in Assets/ZombieRunner/Audio/AUDIO_CREDITS.md.", bold_prefix="• ")
    add_bullet("Academic Institution: Course structure and academic guidelines provided by the School of Computer Science and Artificial Intelligence, SR University, Warangal, Telangana.", bold_prefix="• ")

    doc.save(output_path)
    print(f"DOCX created successfully at: {output_path}")

if __name__ == "__main__":
    out = os.path.abspath(r"E:\zombie runner\Zombie_Runner_Project_Report.docx")
    create_docx(out)
