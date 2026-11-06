# Game Controls — Zombie Runner

## Default Keyboard & Mouse Controls

| Action | Primary Key | Secondary Key / Mouse | Description |
| :--- | :--- | :--- | :--- |
| **Move Left** | `A` | `Left Arrow` | Shifts the player character one lane to the left. |
| **Move Right** | `D` | `Right Arrow` | Shifts the player character one lane to the right. |
| **Jump** | `W` or `Space` | `Up Arrow` | Leaps over low obstacles (cars, roadblocks, debris). |
| **Slide** | `S` | `Down Arrow` | Duck-slides under overhead barriers and pipes. |
| **Shoot Weapon** | `F` | `Left Mouse Button` | Fires Tommy Gun towards crosshair or auto-aim target. |
| **Pause / Resume** | `Escape` | `P` | Opens pause overlay; stops in-game progression. |

## Input System Details

- **Implementation**: Powered by Unity's modern **Input System (`com.unity.inputsystem` v1.20.0)**.
- **Actions Asset**: Located at [`Assets/InputSystem_Actions.inputactions`](file:///e:/zombie%20runner/Assets/InputSystem_Actions.inputactions).
- **Lane System Configuration**:
  - Left Lane: $X = -4.0$ m
  - Middle Lane: $X = 0.0$ m
  - Right Lane: $X = +4.0$ m
  - Lateral lane shift speed is instantaneous or smoothly interpolated depending on settings in `PlayerController`.

## Auto-Aim & Target Lock

- The game features an integrated auto-aim mechanic for responsive combat while running at high speeds.
- When an undead enemy enters range within the forward vision cone, the **AutoAimTargetIndicator** displays a target lock crosshair on the enemy.
- Pressing `F` or `Left Mouse Button` directs bullet raycasts directly towards the locked target.
- If no enemy is targeted, shots travel forward along the camera center reticle.
