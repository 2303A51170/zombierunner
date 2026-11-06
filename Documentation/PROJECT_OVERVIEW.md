# Project Overview — Zombie Runner

## Concept

**Zombie Runner** is a 3D endless survival-horror runner game built in Unity 6 (URP 17.5). The game blends the momentum-driven lane-runner genre with real-time third-person shooting combat and atmospheric horror design.

The core loop is: **Run → Dodge → Shoot → Survive → Score**.

## Game Premise

The world has collapsed. City streets are overrun by the undead. The player controls a sole survivor equipped with a Tommy Gun, sprinting through an apocalyptic nocturnal city that never ends. The city transitions into claustrophobic subway tunnels before resurging into more ruins — an infinite gauntlet that grows faster and more dangerous over time.

## Target Platform

- **Primary:** Windows PC (Keyboard + Mouse)
- **Engine:** Unity 6 (`6000.5.9f1`) with URP 17.5

## Objectives

### Player Objectives
- Run as far as possible without dying.
- Shoot zombies to earn kill score and prevent being attacked.
- Collect gold coins, ammo boxes, and health packs scattered throughout the environment.
- Beat your personal high score (saved persistently across sessions).

### Design Objectives
- Demonstrate a complete, feature-rich Unity game architecture suitable for a development portfolio.
- Implement industry-standard patterns: manager singletons, ScriptableObject-based data, component composition, object pooling, and event-driven UI.
- Achieve a cinematic, polished horror atmosphere using URP lighting, post-processing, and adaptive audio.

## Scope

### Implemented
- Endless procedural environment with 6 modular prefab segment types
- Three zombie archetypes with AI, animations, and audio
- Complete player movement (lane switching, jump, slide)
- Raycast shooting with auto-aim, tracer, and VFX
- Collectibles (coins, ammo, health, power-ups)
- Adaptive 4-layer horror music system
- Polished main menu with settings persistence
- Game Over flow with score and high-score display

### Not Implemented (Planned)
- Mobile touch input
- Leaderboards
- Additional weapon types
- Additional biomes beyond City and Subway

## Key Creative Decisions

| Decision | Rationale |
|----------|-----------|
| Three lanes instead of continuous movement | Keeps gameplay readable and allows precise obstacle/zombie placement |
| Auto-aim system | Reduces frustration on fast-moving targets; keeps pace high |
| Adaptive layered audio | Dynamically reflects game state without jarring music cuts |
| Modular environment segments | Enables infinite reuse with visual variety through material/prop swaps |
| ScriptableObject-based zombie configs | Allows balance tuning without code recompilation |
