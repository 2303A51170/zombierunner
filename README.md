# ZOMBIE RUNNER
### 3D Survival Horror Endless Runner Game

[![Unity 6](https://img.shields.io/badge/Unity-6000.5.9f1-blue.svg)](https://unity.com/releases/editor/whats-new/6000.0.5)
[![Render Pipeline](https://img.shields.io/badge/Render%20Pipeline-URP%2017.5.0-orange.svg)](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@17.0/manual/index.html)
[![Platform](https://img.shields.io/badge/Platform-Windows%20PC-success.svg)](#)
[![Language](https://img.shields.io/badge/Language-C%23-.NET%20Standard%202.1-blueviolet.svg)](#)
[![Git LFS](https://img.shields.io/badge/Git%20LFS-Enabled-purple.svg)](#git-lfs)
[![License](https://img.shields.io/badge/License-See%20Credits-lightgrey.svg)](#credits-and-third-party-asset-acknowledgements)

---

## Project Introduction

**Zombie Runner** is a 3D endless survival-horror runner game developed in Unity 6 using the Universal Render Pipeline (URP 17.5). The game immerses players in a post-apocalyptic nocturnal cityscape where they sprint through dynamically generated environments, navigate obstacles, and battle multiple zombie archetypes — all while managing ammo, health, and score.

Built as a full-featured Unity game project, Zombie Runner demonstrates a complete game-development pipeline: modular C# architecture, Mecanim animation state machines, adaptive layered audio, URP post-processing, real-time AI, and a polished main menu with settings persistence.

---

## Game Overview

The world has fallen. The streets are overrun. You are a lone survivor — armed, fast, and running.

Sprint through endless night-time city ruins and subterranean railway tunnels. Vault obstacles. Slide under barriers. Collect ammo, gold coins, and health packs. Shoot approaching zombies before they tear you apart. See how far you can run before the horde catches up.

---

## Main Features

- **Endless Procedural Environment** — Dynamically streamed 30 m modular road segments that recycle seamlessly as the player runs. Environment themes transition between city ruins and subway tunnels, each with distinct materials, lighting, and atmospheric fog.
- **Multiple Zombie Archetypes** — Three distinct zombie enemy types (Common, Fast Sprinter, Heavy Brute) with individual speed, health, attack, and reward parameters defined via ScriptableObjects.
- **Real-Time Shooting Combat** — Raycast-based shooting with visual recoil, auto-aim tracking, illuminated bullet tracers, and pooled blood and concrete impact VFX.
- **Three-Lane Runner Movement** — Instant lane switching, grounded jump physics, and low-slide clearance, all driven by Unity's new Input System.
- **Collectibles & Scoring** — Gold coins, ammo boxes, and health kits scattered through the environment. Real-time distance and kill score with persistent high-score saving via `PlayerPrefs`.
- **Health & Revive System** — Player health management with damage invulnerability frames, shield power-up protection, and a single one-time revive per run.
- **Cinematic Horror Atmosphere** — Cool-blue moonlight directional light, warm sodium emergency lamps with flicker, volumetric linear fog, ACES tonemapping, and URP post-processing (Bloom, Vignette, Color Grading).
- **Adaptive Horror Audio** — 4-layer synchronized horror soundtrack that crossfades between exploration, tension, combat, and critical-health states. 3D positional zombie audio and tactile UI sound effects.
- **Main Menu & Settings** — Polished title screen with cinematic camera pan, animated survivor character, persistent audio and graphics settings, control-reference modal, and credits panel.
- **Power-Ups** — Timed shield, coin magnet, speed boost, and double-coin multiplier power-ups.

---

## Gameplay Mechanics

### Player Movement System

| Action | Keyboard | Alternative |
|--------|----------|-------------|
| Lane Left | `A` | `Left Arrow` |
| Lane Right | `D` | `Right Arrow` |
| Jump | `W` / `Space` | `Up Arrow` |
| Slide | `S` | `Down Arrow` |
| Shoot | `F` | `Left Mouse Button` |
| Pause / Resume | `Escape` | `P` |

The player runs at a constant forward velocity that gradually increases over time. Lane transitions are instant and snapped to fixed x-positions (-4, 0, +4 units). Jumping applies an upward impulse with gravity-based fall. Sliding applies a temporary collider height reduction and animation state.

### Shooting & Combat System

- **Weapon:** Tommy Gun (Submachine Gun) with PBR metallic-roughness textures.
- **Fire Mechanism:** Raycast from the camera/weapon muzzle toward the nearest zombie or the crosshair aim point.
- **Auto-Aim:** `AutoAimTargetIndicator` locks onto the nearest zombie within range, displayed with a UI target reticle.
- **Bullet Tracers:** `BulletTracer` spawns a visual tracer line from muzzle to impact point.
- **Hit Impact:** `HitImpactManager` spawns pooled blood and concrete/metal VFX on hit, depending on what was struck.
- **Ammo System:** Player has a finite ammo count. Ammo boxes replenish ammunition.

### Zombie Enemy Types

| Type | Speed | Health | Attack Damage | Reward |
|------|-------|--------|---------------|--------|
| Common Runner | Medium | Medium | Medium | Standard |
| Fast Sprinter | High | Low | Low | High |
| Heavy Brute | Low | High | High | Bonus |

Zombie behavior is controlled by `ZombieController`: zombies detect the player within a spawn range, pursue along lane coordinates, perform melee attacks when adjacent, flinch on hit, and play a death animation before despawning. `ZombieSpawner` manages timed spawn waves with difficulty scaling.

### Environment Design

- **City Ruins** (`EnvironmentSegment_CityRuins`) — Cracked asphalt, ruined building facades, overturned cars, and orange barrel obstacles under a neon-hazard lamp atmosphere.
- **Factory District** (`EnvironmentSegment_Factory`) — Corrugated metal, industrial warning stripes, and factory-green machinery props.
- **Military Base** (`EnvironmentSegment_MilitaryBase`) — Military canvas crates, concrete barriers, and green-camo obstacle props.
- **Subway Tunnel Entrance / Exit** — Transition segments from outdoor city into the underground, with matching atmospheric lighting shifts.
- **Subway Tunnel** (`EnvironmentSegment_SubwayTunnel`) — Tiled concrete walls, industrial pipe runs, flickering emergency lamps, and deep fog creating tight claustrophobic corridors.

The `EndlessRoadManager` maintains a pool of `RoadSegment_30m` base segments, advancing and recycling them behind the player. `EnvironmentThemeManager` controls which themed prefab set is currently active, transitioning between city and tunnel biomes.

### UI & Game Progression

- **HUD** — Live distance counter, ammo count, health bar, score display, and auto-aim reticle overlay. Managed by `UIManager`.
- **Main Menu** — Animated title with survivor model, Play / Settings / Credits / Quit navigation. Managed by `MainMenuController`.
- **Settings Menu** — Master/Music/SFX volume sliders, graphics quality toggle, and control reference overlay.
- **Game Over Screen** — Score summary, high-score celebration, and Restart / Main Menu buttons. Managed by `GameOverUIController`.

---

## Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Engine | Unity | `6000.5.9f1` (Unity 6) |
| Render Pipeline | Universal Render Pipeline (URP) | `17.5.0` |
| Language | C# / .NET Standard | `2.1` |
| Input System | Unity Input System | `1.20.0` |
| Animation | Unity Mecanim — Humanoid Avatars | — |
| Audio | Unity AudioMixer + Adaptive Controller | — |
| UI | TextMeshPro + uGUI | `2.5.0` |
| AI Navigation | Unity AI Navigation | `2.0.14` |
| Version Control | Git + Git LFS | LFS `3.7.1` |

---

## Project Architecture

The project uses a **manager-based architecture** with loosely coupled systems communicating through direct references and Unity events.

```
GameManager          — Central game-state machine (Playing / Paused / GameOver)
  └─ ScoreManager    — Distance and kill score accumulation and high-score persistence
  └─ SaveManager     — PlayerPrefs wrapper for settings and score data
  └─ AudioManager    — AudioMixer routing and global volume control
  └─ UIManager       — HUD panel visibility and value updates

PlayerController     — Three-lane movement, jump, slide, speed ramping
  └─ PlayerHealth    — HP, invulnerability, revive, death event
  └─ ShootingController — Raycast fire, ammo, tracer, impact spawn
  └─ RunnerCameraFollow — Smooth camera lag follow

ZombieSpawner        — Wave-based timed spawning with difficulty curve
  └─ ZombieController — Per-zombie pursuit AI, attack, health, death
  └─ ZombieSoundEmitter — 3D positional audio per zombie instance

EndlessRoadManager   — Segment pool, advance, and recycle
  └─ EnvironmentThemeManager — Biome theme transition control
  └─ ObstacleSpawner — Random obstacle placement on new segments
  └─ CollectibleManager — Coin / ammo / health spawn distribution

AdaptiveMusicController — 4-layer horror stem crossfade based on game state
AmbientAudioController  — 3D ambient loops (city wind, streetlight hum)
```

Zombie archetypes are configured via `ZombieConfig` ScriptableObjects located in `Assets/ZombieRunner/Settings/Enemies/`, which define per-type speed, health, attack parameters, and reward values without requiring code changes.

---

## Installation Instructions

### Prerequisites

- **Unity Hub** (latest version)
- **Unity Editor `6000.5.9f1`** (Unity 6) — install via Unity Hub with the **Windows Build Support** module
- **Git** (version 2.x or later)
- **Git LFS** (version 3.x or later) — required for large binary assets (FBX models, WAV audio)

### Clone the Repository

```bash
# 1. Clone the repository
git clone https://github.com/SanskarKatkar/zombierunner.git
cd zombierunner

# 2. Pull large binary assets via Git LFS
git lfs pull
```

> **Note:** `git lfs pull` downloads all large binary assets (3D models, audio files, textures). This may take several minutes depending on your connection speed. The total asset download is approximately 1.2 GB via LFS.

### Open in Unity

1. Launch **Unity Hub**.
2. Click **Add** → **Add project from disk**.
3. Navigate to the cloned `zombierunner/` folder (the directory containing `Assets/`, `Packages/`, and `ProjectSettings/`).
4. Select Unity Editor version **`6000.5.9f1`**.
5. Click **Open**.
6. Unity will reimport assets on first open — this takes 5–15 minutes.

### Load the Game

- **Full Experience (Main Menu → Gameplay):**
  Open `Assets/ZombieRunner/Scenes/ZombieRunnerMainMenu.unity` and click **Play**.
- **Direct Gameplay Testing:**
  Open `Assets/ZombieRunner/Scenes/ZombieRunnerGameplay.unity` and click **Play**.

---

## Controls

| Action | Primary Key | Alternative |
|--------|-------------|-------------|
| Move Lane Left | `A` | `Left Arrow` |
| Move Lane Right | `D` | `Right Arrow` |
| Jump | `W` / `Space` | `Up Arrow` |
| Slide | `S` | `Down Arrow` |
| Shoot | `F` | `Left Mouse Button` |
| Pause / Resume | `Escape` | `P` |

---

## Project Folder Structure

```
zombierunner/
├── Assets/
│   ├── Resources/                      # Runtime-loaded assets (MenuAnimators, MenuWeapons)
│   ├── Scenes/                         # Template scene (SampleScene.unity)
│   ├── Settings/                       # URP pipeline and renderer assets (PC + Mobile tiers)
│   ├── TextMesh Pro/                   # TMP fonts, shaders, and essential resources
│   ├── TutorialInfo/                   # URP starter template metadata
│   └── ZombieRunner/                   # Primary authored game content
│       ├── Animations/                 # Mecanim Animator Controllers (Player, Zombie, Menu)
│       ├── Audio/
│       │   ├── Clips/                  # Procedural WAV SFX and adaptive music stems
│       │   └── ProvidedAudio/          # User-supplied MP3 music tracks
│       ├── Characters/
│       │   ├── Player/                 # Ch05 survivor model, animations, materials, textures
│       │   └── Zombie/                 # Ch10, Yaku J Ignite, Pumpkinhulk models + animations
│       ├── Editor/                     # Unity Editor custom tools and scene builders
│       ├── Materials/                  # 35+ URP Lit/Unlit materials (WR_* naming convention)
│       ├── Models/
│       │   └── Weapons/TommyGun/       # Tommy Gun FBX, PBR textures, materials
│       ├── Prefabs/
│       │   ├── Collectibles/           # Coin, AmmoBox, HealthKit, PowerUp prefabs
│       │   ├── Environment/            # Modular segment prefabs (City, Factory, Military, Tunnel)
│       │   ├── Obstacles/              # AbandonedCar, ExplosiveBarrel, Roadblock prefabs
│       │   ├── Player/                 # PlayerPlaceholder prefab
│       │   ├── UI/                     # UI prefabs
│       │   └── Zombies/                # BigZombie, CommonZombie, FastZombie, HeavyZombie, NormalZombie
│       ├── Scenes/
│       │   ├── ZombieRunnerMainMenu.unity
│       │   └── ZombieRunnerGameplay.unity
│       ├── Scripts/
│       │   ├── Audio/                  # AudioManager, AdaptiveMusicController, AmbientAudioController
│       │   ├── Collectibles/           # CollectibleManager, CollectiblePickup
│       │   ├── Core/                   # GameManager, SaveManager, ScoreManager
│       │   ├── Editor/                 # Custom editor utilities (12 tools)
│       │   ├── Enemies/                # ZombieController, ZombieConfig, ZombieSpawner, ZombieSoundEmitter
│       │   ├── Player/                 # PlayerController, PlayerHealth, RunnerCameraFollow
│       │   ├── PowerUps/               # PowerUpManager, PowerUpPickup, PowerUpType
│       │   ├── UI/                     # UIManager, MainMenuController, GameOverUIController, MenuAudioController, etc.
│       │   ├── Utilities/              # IDamageable interface
│       │   ├── Weapons/                # ShootingController, BulletTracer, HitImpactManager
│       │   └── World/                  # EndlessRoadManager, EnvironmentThemeManager, ObstacleSpawner, StreetlightFlicker, etc.
│       ├── Settings/
│       │   └── Enemies/                # ZombieConfig ScriptableObjects per archetype
│       └── Textures/
│           ├── Environment/            # PBR environment textures (asphalt, concrete, tunnel, ruins)
│           └── UI/                     # UI icon sprites (coin, crosshair, arrows, buttons)
├── Documentation/
│   ├── PROJECT_OVERVIEW.md
│   ├── GAMEPLAY_FEATURES.md
│   ├── TECHNICAL_ARCHITECTURE.md
│   ├── CONTROLS.md
│   ├── SETUP_GUIDE.md
│   ├── CREDITS_AND_ASSETS.md
│   └── DEVELOPMENT_STATUS.md
├── Screenshots/
│   ├── Audit_MainMenu_1_Overview.png
│   ├── Audit_MainMenu_2_Settings_Graphics.png
│   ├── Audit_MainMenu_3_Settings_Audio.png
│   ├── Audit_MainMenu_4_Settings_Controls.png
│   ├── Audit_MainMenu_5_Credits.png
│   └── Audit_MainMenu_6_GameplayTransition.png
├── PresentationScreenshots/            # Additional presentation visuals
├── Packages/
│   ├── manifest.json                   # Package dependency declarations
│   └── packages-lock.json              # Resolved package lock
├── ProjectSettings/                    # Unity project configuration
├── .gitattributes                      # Git LFS tracking rules
├── .gitignore                          # Unity-specific exclusion rules
├── DEVELOPMENT_STATUS.md               # Detailed engineering log
└── README.md                           # This file
```

---

## Screenshots

### Main Menu

| Overview | Settings — Graphics | Settings — Audio |
|----------|-------------------|-----------------|
| ![Main Menu Overview](Screenshots/Audit_MainMenu_1_Overview.png) | ![Settings Graphics](Screenshots/Audit_MainMenu_2_Settings_Graphics.png) | ![Settings Audio](Screenshots/Audit_MainMenu_3_Settings_Audio.png) |

| Settings — Controls | Credits | Gameplay Transition |
|--------------------|---------|--------------------|
| ![Settings Controls](Screenshots/Audit_MainMenu_4_Settings_Controls.png) | ![Credits](Screenshots/Audit_MainMenu_5_Credits.png) | ![Gameplay Transition](Screenshots/Audit_MainMenu_6_GameplayTransition.png) |

### Presentation Visuals

| Title Screen | Survivor Character | City Environment |
|-------------|-------------------|-----------------|
| ![Title Screen](Screenshots/01_Title_Screen_Overview.png) | ![Survivor](Screenshots/02_Survivor_Character_Closeup.png) | ![City](Screenshots/03_City_Environment_Atmosphere.png) |

| Gameplay Action | Zombie Archetypes | Subway Tunnel |
|----------------|------------------|--------------|
| ![Gameplay](Screenshots/06_Gameplay_Runner_Action.png) | ![Zombies](Screenshots/08_Zombie_Archetypes_Textures.png) | ![Tunnel](Screenshots/09_Subway_Tunnel_Materials.png) |

---

## Credits and Third-Party Asset Acknowledgements

### 3D Character Models & Skeletal Animations

**Mixamo (Adobe Systems)**
- Player Survivor Model: Mixamo "Ch05" textured Humanoid Character
- Player Auxiliary Model: Mixamo "X Bot" Humanoid Rigging Model
- Zombie Models: Mixamo "Ch10" (Common), "Yaku J Ignite" (Fast Runner), "Pumpkinhulk L Shaw" (Heavy Brute)
- Animation Packs: Mixamo Basic Shooter Pack (Rifle Idle, Run, Jump, Slide, Shoot) and Scary Zombie Pack (Walk, Run, Attack, Bite, Crawl, Scream, Death)
- **License:** Adobe Mixamo Software License Agreement — royalty-free for commercial and non-commercial use in games

### Weapon Models & Textures

**Tommy Gun (Submachine Gun)**
- High-detail 3D submachine gun model with PBR metallic-roughness workflow textures
- Located in `Assets/ZombieRunner/Models/Weapons/TommyGun/`
- Source archive: `tommy-gun.zip` (tracked via Git LFS)

### Audio

**User-Provided Audio Tracks** (`Assets/ZombieRunner/Audio/ProvidedAudio/`)
- Main Menu Music: `main screen intro music.mp3`
- City Ambience: `city sound.mp3`
- Zombie Growl: `zombie-voice-growl.mp3`
- Zombie Death: `zombie death.mp3`

**Procedural / Algorithmic Audio** (`Assets/ZombieRunner/Audio/Clips/`)
- 4-layer adaptive horror soundtrack stems (Exploration, Tension, Combat, Critical Health)
- Ambient loops (city wind, streetlight hum, distant rumble, metal creak)
- SFX: gunshots (punchy mix), blood impacts, concrete ricochets, item pickups, UI clicks, game-over sting
- Zombie type-specific SFX: growls, hisses, roars, attacks, deaths (Normal, Fast, Heavy archetypes)

### Engine & Packages

- **Unity Technologies:** Universal Render Pipeline 17.5, Input System 1.20, TextMeshPro (uGUI 2.5), AI Navigation 2.0.14, Timeline 1.8.12, Visual Scripting 1.9.12

---

## Developer & Author

- **Sanskar Katkar** — Solo Game Developer & Technical Artist
  - GitHub: [@SanskarKatkar](https://github.com/SanskarKatkar)
  - Repository: [Zombie Runner](https://github.com/SanskarKatkar/zombierunner)

---

## Future Improvements

- [ ] Additional zombie archetypes (crawler, exploder)
- [ ] Additional environment biomes (hospital, industrial district)
- [ ] Mobile touch-control support (swipe gestures)
- [ ] Leaderboard and online high-score integration
- [ ] Weapon variety (shotgun, pistol, grenade)
- [ ] Story mode with scripted level sequences
- [ ] Particle-based zombie ragdoll physics on death
- [ ] Localization (multi-language UI support)
- [ ] Controller / gamepad input mapping

---

## Git LFS

This repository uses **Git LFS** to store large binary assets:

```
*.fbx     — 3D character and weapon models
*.wav     — Audio clips and music stems
*.mp3     — Music tracks
*.ogg     — Compressed audio
*.zip     — Source asset archives (Mixamo packs)
*.psd     — Source art files
*.tga     — Source textures
*.blend   — Blender source files
```

After cloning, run `git lfs pull` to download all LFS-tracked assets.

---

*Zombie Runner — Unity 6 / URP 17.5 — 3D Survival Horror Endless Runner*
