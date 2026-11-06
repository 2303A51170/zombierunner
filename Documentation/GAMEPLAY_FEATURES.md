# Gameplay Features — Zombie Runner

## Player Movement

### Lane System
- Three horizontal lanes at X positions: **-4, 0, +4** world units.
- Lane switching is instant (no interpolation delay) — controlled by `PlayerController`.
- Input via Unity Input System: `A`/`Left Arrow` (move left), `D`/`Right Arrow` (move right).

### Running
- The player runs forward automatically at a constant Z velocity.
- Run speed increases gradually over time (difficulty scaling).
- Base speed is set in `PlayerController` and ramped by a time-based multiplier.

### Jumping
- Pressing `W`, `Space`, or `Up Arrow` applies an upward impulse via `Rigidbody.AddForce`.
- Jump height and gravity are tuned in `PlayerController`.
- Jumping prevents sliding and vice versa (mutually exclusive states).

### Sliding
- Pressing `S` or `Down Arrow` triggers the slide animation and temporarily shrinks the collider height.
- Slide duration is fixed (configurable in `PlayerController`).
- Sliding allows passing under low obstacles.

## Shooting & Combat

### Weapon
- **Tommy Gun** — submachine gun with PBR metallic-roughness textures.
- Displayed in the player's hands via animation rigging.

### Fire Mechanics
- **Input:** `F` key or Left Mouse Button.
- **Detection:** Raycast from weapon muzzle point in the camera forward direction (or auto-aimed direction).
- **Hit:** If the ray hits an `IDamageable` (zombie), `TakeDamage()` is called.
- **Ammo:** Each shot costs one ammo unit. Shooting with zero ammo produces a click sound and no tracer.

### Auto-Aim (`AutoAimTargetIndicator`)
- Finds the nearest zombie within a configurable range.
- Soft-locks the aim direction toward the target.
- Displays a UI reticle overlay on the locked target.

### Bullet Tracer (`BulletTracer`)
- A short `LineRenderer`-based visual tracer is spawned from muzzle to impact point.
- Fades out over approximately 0.1 seconds.

### Hit Impact (`HitImpactManager`)
- On zombie hit: spawns pooled blood splatter VFX at impact position.
- On environment hit: spawns pooled concrete or metal ricochet VFX depending on surface tag.

### Recoil
- `ShootingController` applies a brief visual kickback animation offset on each shot.

## Zombies

### Archetypes

| Type Prefab | Speed | Health | Attack Damage | Kill Reward |
|-------------|-------|--------|---------------|-------------|
| `CommonZombie` / `NormalZombie` | Medium | Medium | Medium | Standard |
| `FastZombie` | High | Low | Low | High |
| `HeavyZombie` / `BigZombie` | Low | High | High | Bonus |

Configured via `ZombieConfig` ScriptableObjects in `Assets/ZombieRunner/Settings/Enemies/`.

### Zombie AI (`ZombieController`)
1. **Spawn** — Zombies spawn ahead of the player via `ZombieSpawner` at a fixed forward offset.
2. **Pursue** — The zombie moves toward the player's current lane X position.
3. **Attack** — When within melee range, plays attack animation and calls `PlayerHealth.TakeDamage()`.
4. **Flinch** — On receiving damage, plays a brief flinch animation.
5. **Death** — On reaching 0 HP, plays death animation, despawns after delay, awards score.

### Zombie Spawning (`ZombieSpawner`)
- Spawns zombies at fixed intervals (reducing over time for difficulty scaling).
- Randomly assigns a zombie type weighted by difficulty stage.
- Spawns on a random lane.

### Zombie Audio (`ZombieSoundEmitter`)
- Each zombie has a 3D audio source for type-specific growls, hisses, roars, attacks, and deaths.
- Audio emitter position tracks the zombie GameObject in world space.

## Collectibles

### Gold Coins (`GoldCoin`)
- Scattered on road segments by `CollectibleManager`.
- Collected on trigger enter.
- Awards score points.

### Ammo Boxes (`AmmoBox`)
- Replenishes ammo count on pickup.
- Displayed with orange warning-stripe material.

### Health Kits (`HealthKit`)
- Restores a fixed HP amount on pickup (up to max HP).

## Health & Revive System

### Player Health (`PlayerHealth`)
- Max HP: configurable (default 3 hit points).
- On taking damage: HP decrements, invulnerability frames begin (brief window to prevent multi-hit), damage flash UI feedback.
- At 0 HP with revive available: prompts the revive screen, restores 1 HP, removes revive token.
- At 0 HP with no revive: triggers Game Over event consumed by `GameManager`.

### Shield Power-Up
- When active, absorbs a fixed number of zombie hits before deactivating.
- Visual aura indicator on player.

## Power-Ups (`PowerUpManager`)

| Power-Up | Effect | Duration |
|----------|--------|----------|
| Shield | Absorbs incoming damage | 10 s |
| Coin Magnet | Auto-collects nearby coins | 10 s |
| Speed Boost | Increases run speed | 8 s |
| Double Coins | Multiplies coin value × 2 | 15 s |

Power-ups are spawned by `CollectibleManager` on road segments. `PowerUpPickup` triggers activation. `PowerUpManager` tracks active timers.

## Score System (`ScoreManager`)

- **Distance Score:** Accumulates continuously while running (1 point per unit of distance).
- **Kill Score:** Each zombie kill awards type-specific bonus points.
- **Coin Score:** Each coin collected awards fixed points.
- **High Score:** Stored in `PlayerPrefs` and loaded on game start. Displays a celebration banner if beaten.

## Game Over Flow

1. `PlayerHealth` fires a death event.
2. `GameManager` transitions to `GameOver` state.
3. `GameOverUIController` displays the Game Over panel with:
   - Final distance and score.
   - High score (updated if beaten).
   - **Restart** button — reloads the gameplay scene.
   - **Main Menu** button — loads `ZombieRunnerMainMenu`.

## Main Menu

Managed by `MainMenuController` in `ZombieRunnerMainMenu.unity`:

- **Title panel** — Logo, survivor character with idle animation, background city environment, animated camera pan (`MenuCameraPan`).
- **Play button** — Loads `ZombieRunnerGameplay.unity` with a fade transition.
- **Settings panel** — Master/Music/SFX sliders (saved to `PlayerPrefs`), graphics quality toggle.
- **Controls panel** — Keyboard reference overlay.
- **Credits panel** — Asset credits.
- **Quit button** — `Application.Quit()`.

UI audio feedback (button hover / click SFX) managed by `MenuButtonEffects` and `MenuAudioController`.
