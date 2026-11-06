# Credits and Assets — Zombie Runner

## 1. 3D Character Models & Animations

### Survivor / Player Character
- **Model**: "Ch05" Humanoid Character
- **Source**: Adobe Mixamo (`www.mixamo.com`)
- **Rigging & Animations**:
  - Rifle Aiming Idle
  - Rifle Run
  - Rifle Jump
  - Running Slide
  - Shoot Rifle
- **License**: Adobe Mixamo Software License Agreement (Royalty-free for commercial and non-commercial game development).
- **Secondary Model**: "X Bot" Humanoid Rigging Model (Backup / testing).

### Undead Archetypes
- **Common Runner**: "Ch10" Humanoid Zombie Model (Mixamo).
- **Fast Sprinter**: "Yaku J Ignite" Zombie Model (Mixamo).
- **Heavy Brute**: "Pumpkinhulk L Shaw" Zombie Model (Mixamo).
- **Zombie Animations**:
  - Zombie Walk, Zombie Run, Running Crawl
  - Zombie Attack, Zombie Biting, Zombie Neck Bite
  - Zombie Scream, Zombie Idle
  - Zombie Death, Zombie Dying
- **License**: Adobe Mixamo Software License Agreement.

---

## 2. Weapon Models & Props

### Tommy Gun (Submachine Gun)
- **Model**: High-detail Tommy Gun 3D model with realistic textures.
- **Location**: `Assets/ZombieRunner/Models/Weapons/TommyGun/`
- **PBR Textures**:
  - Albedo / BaseColor (Material 26 & 31)
  - Normal Maps
  - Metallic / Smoothness Maps
  - Ambient Occlusion
- **License**: Creative Commons / Royalty-Free 3D asset.

### Modular Road & Environment Props
- Abandoned Sedans and Hatchbacks
- Industrial Orange Explosive Barrels
- Concrete Highway Barriers and Roadblocks
- Subway Tunnel Modular Walls, Lamps, and Pipes
- Overhead Streetlights with flicker controllers
- Authored with custom URP Lit PBR materials (`Assets/ZombieRunner/Materials/`).

---

## 3. Audio & Music Suite

### Authored Music Tracks (`Assets/ZombieRunner/Audio/ProvidedAudio/`)
- **Main Menu Intro Music**: `main screen intro music.mp3` (Ominous cinematic title track)
- **City Ambience Loop**: `city sound.mp3` (Nocturnal urban wind and distant sirens)
- **Zombie Voice**: `zombie-voice-growl.mp3`
- **Zombie Attack**: `zombie-attack.mp3`
- **Zombie Death**: `zombie death.mp3`
- **Gunshot**: `gun shot.mp3`

### Procedural / Algorithmic Audio Stems (`Assets/ZombieRunner/Audio/Clips/`)
- **Adaptive Music System**: 4 synchronized layers dynamically mixed by `AdaptiveMusicController`:
  - Layer 1: Exploration (Eerie subterranean drone)
  - Layer 2: Tension (Heartbeat rhythm and rising strings)
  - Layer 3: Combat (Industrial percussion and aggressive synth pulses)
  - Layer 4: Critical Health (Muffled panic frequency filter)
- **Sound Effects (SFX)**:
  - Punchy Gunshots (`SFX_Gunshot_Punchy_01` to `03`)
  - Flesh / Blood Impacts (`SFX_Impact_Blood_01` to `02`)
  - Concrete & Metal Ricochets (`SFX_Impact_Concrete_01`, `SFX_Impact_Metal_01`)
  - Archetype Specific Sounds (Normal, Fast, Heavy groans, hisses, and roars)
  - UI Clicks, Hover ticks, and Game Over Horror Sting
- **License**: Generated procedural audio assets released under CC0 / Public Domain.

---

## 4. Third-Party Packages & Frameworks

| Package | Version | Publisher | License |
| :--- | :--- | :--- | :--- |
| **Universal RP** | 17.5.0 | Unity Technologies | Unity Companion License |
| **Input System** | 1.20.0 | Unity Technologies | Unity Companion License |
| **TextMeshPro (uGUI)** | 2.5.0 | Unity Technologies | Unity Companion License |
| **AI Navigation** | 2.0.14 | Unity Technologies | Unity Companion License |
| **Timeline** | 1.8.12 | Unity Technologies | Unity Companion License |
| **Visual Scripting** | 1.9.12 | Unity Technologies | Unity Companion License |
