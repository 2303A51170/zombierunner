# Technical Architecture — Zombie Runner

## Overview

Zombie Runner is developed with a modular, decoupled architecture in C# for Unity 6 (URP 17.5). Systems interact primarily via direct manager references, standard Unity events, and interfaces such as `IDamageable`.

## System Architecture Diagram

```
[ GameManager ] ──────────────────────────────────────────┐
  │                                                       │
  ├──► [ ScoreManager ] ──► [ SaveManager (PlayerPrefs) ] │
  ├──► [ AudioManager ] ──► [ AudioMixer & Stems ]        │
  └──► [ UIManager ] ─────► [ HUD & Screen Overlays ]     │
                                                          │ (Game State Events)
[ PlayerController ] ◄────────────────────────────────────┘
  ├──► [ CharacterController / Physics ]
  ├──► [ PlayerHealth ] (Invulnerability, Revive, Death)
  ├──► [ ShootingController ] ──► [ BulletTracer ] & [ HitImpactManager ]
  └──► [ RunnerCameraFollow ] (Smooth positional lag)

[ EndlessRoadManager ]
  ├──► [ EnvironmentThemeManager ] (City Ruins, Factory, Military, Subway Tunnel)
  ├──► [ RoadSegment_30m Pooling ]
  ├──► [ ObstacleSpawner ] (Cars, Barrels, Roadblocks)
  └──► [ CollectibleManager ] (Coins, Ammo, Health, PowerUps)

[ ZombieSpawner ]
  └──► [ ZombieController ] (AI Locomotion, Damage, Attack)
         ├──► [ ZombieConfig (ScriptableObject) ]
         ├──► [ ZombieSoundEmitter (3D Positional Audio) ]
         └──► Implements [ IDamageable ]

[ Audio Architecture ]
  ├──► [ AudioManager ] (Master, Music, SFX volume & routing)
  ├──► [ AdaptiveMusicController ] (4-layer dynamic tension stems)
  └──► [ AmbientAudioController ] (City wind, subway hum loops)
```

## Core Script Subsystems

### 1. Core & Game Loop
- **`GameManager.cs`**: Controls high-level game states (Menu, Playing, Paused, GameOver). Coordinates restart, revive, and scene transitions.
- **`ScoreManager.cs`**: Tracks real-time forward running distance, zombie kill counts, coin counts, and calculates score. Manages persistent high scores.
- **`SaveManager.cs`**: Encapsulates `PlayerPrefs` read/write operations for high scores, graphics settings, audio volume sliders, and controls preferences.

### 2. Player Subsystem
- **`PlayerController.cs`**: Implements 3-lane horizontal movement (-4, 0, +4 units), forward speed acceleration over time, grounded jump impulse, and timed sliding with collider height reduction.
- **`PlayerHealth.cs`**: Maintains player HP (default 3 hits), invulnerability frames (i-frames) on hit, damage screen flash, one-time revive token handling, and death events.
- **`RunnerCameraFollow.cs`**: Third-person perspective camera follower maintaining offset and smooth positional damping behind the runner.

### 3. Combat & Weapons
- **`ShootingController.cs`**: Manages raycast firing from muzzle point, ammo deduction, weapon recoil animation, rate of fire, and target validation.
- **`AutoAimTargetIndicator.cs`**: Scans for nearest active zombie within target cone and range, provides auto-aim angle compensation, and projects a screen-space UI lock-on crosshair.
- **`BulletTracer.cs`**: Spawns and animates high-velocity laser-like bullet tracers using `LineRenderer` with fast alpha falloff.
- **`HitImpactManager.cs`**: Object-pooled particle effects triggering blood splatters on organic targets or sparks/dust on concrete and metal.
- **`IDamageable.cs`**: Standard interface (`void TakeDamage(int amount)`) implemented by all enemy types and destructibles.

### 4. Enemies & AI
- **`ZombieController.cs`**: Implements lane-aware approach, player proximity detection, attack lunges, damage flinch animations, and death sequencing.
- **`ZombieSpawner.cs`**: Dynamic wave spawner placing zombies ahead of the runner on available lanes with progressive difficulty scaling.
- **`ZombieConfig.cs`**: `ScriptableObject` defining speed, health, attack damage, and point value per archetype (Normal, Fast, Heavy).
- **`ZombieSoundEmitter.cs`**: Attaches to zombie instances to emit 3D spatialized groans, attack shouts, and death screams.

### 5. World & Environment Generation
- **`EndlessRoadManager.cs`**: Object pool managing 30m modular road segments, recycling trailing segments forward seamlessly.
- **`EnvironmentThemeManager.cs`**: Controls theme transitions between City Ruins and Subway Tunnel biomes, modulating fog parameters, skybox, and directional light colors.
- **`ObstacleSpawner.cs`**: Procedurally places obstacles (Abandoned Cars, Explosive Barrels, Roadblocks) with guaranteed solvable lane pathways.
- **`StreetlightFlicker.cs`**: Procedural lighting flicker simulating damaged electrical grid.
- **`AtmosphericLightningFlash.cs`**: Periodic skybox illumination bursts for nocturnal horror atmosphere.

### 6. Power-Ups & Collectibles
- **`CollectibleManager.cs`**: Spawns coins in patterns (lines, arcs) and distributes ammo boxes / health kits.
- **`CollectiblePickup.cs`**: Trigger collider handler awarding coins, ammo, or health.
- **`PowerUpManager.cs`**: Manages active timers for Shield, Magnet, Speed Boost, and Double Coins.
- **`PowerUpPickup.cs`**: Activates power-up states and triggers HUD notification.

### 7. Audio Architecture
- **`AudioManager.cs`**: Central access point for UI clicks, one-shot SFX, and global AudioMixer channel control.
- **`AdaptiveMusicController.cs`**: Evaluates player danger state, health percentage, and enemy density to crossfade between 4 synchronized horror music stems (Exploration, Tension, Combat, Critical Health).
- **`AmbientAudioController.cs`**: Spatially blends urban night wind and subterranean hums.

### 8. User Interface (UI)
- **`UIManager.cs`**: Real-time HUD updates (health icons, ammo counter, distance, current score, active power-up timers).
- **`MainMenuController.cs`**: Main menu navigation, camera panning, settings panel, controls guide, and credits.
- **`GameOverUIController.cs`**: Displays final run statistics, high-score banner, restart prompt, and return to title.
- **`MenuAudioController.cs`**: Dedicated UI sound synthesis for clicks, hover events, and slider adjustments.
