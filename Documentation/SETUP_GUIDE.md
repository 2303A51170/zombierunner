# Setup & Installation Guide — Zombie Runner

## System Requirements

- **Operating System**: Windows 10 / 11 (64-bit)
- **Unity Editor**: Version **`6000.5.9f1` (Unity 6)**
- **Render Pipeline**: Universal Render Pipeline (URP `17.5.0`)
- **Version Control Tools**:
  - Git 2.30+
  - Git LFS (Large File Storage) 3.0+
- **Hardware Requirements**:
  - GPU: DirectX 11 / 12 compatible graphics card (NVIDIA GTX 1050 / AMD RX 560 or better)
  - RAM: 8 GB minimum (16 GB recommended)
  - Disk Space: ~6 GB free space (project files + Library cache)

---

## 1. Cloning the Repository

Because Zombie Runner uses Git LFS to track 3D meshes (.fbx), high-resolution textures, and uncompressed audio (.wav), make sure Git LFS is installed and initialized before cloning:

```bash
# Verify Git LFS installation
git lfs install

# Clone the repository
git clone https://github.com/SanskarKatkar/zombierunner.git
cd zombierunner

# Pull all large binary assets
git lfs pull
```

---

## 2. Adding the Project to Unity Hub

1. Launch **Unity Hub**.
2. Click the **Add** button (top-right) and select **Add project from disk**.
3. Browse to the root of the cloned directory (where `Assets/`, `Packages/`, and `ProjectSettings/` reside).
4. In the Unity Version dropdown, select **`6000.5.9f1`**.
   > *If `6000.5.9f1` is not installed, install it via Unity Hub > Installs > Install Editor, and ensure the **Windows Build Support (IL2CPP / Mono)** component is checked.*

---

## 3. First-Time Project Opening & Asset Import

1. Click on the project name in Unity Hub to open it.
2. Unity will import all project assets, compile C# scripts, and build the local `Library/` cache. This may take 5 to 15 minutes depending on CPU and disk speed.
3. Once the editor finishes loading, confirm there are **0 compilation errors** in the Unity Console.

---

## 4. Running the Game in Editor

### Main Menu (Recommended Full Flow)
1. In the Project window, navigate to:
   `Assets/ZombieRunner/Scenes/ZombieRunnerMainMenu.unity`
2. Double-click to open the scene.
3. Click the **Play** button at the top of the Unity Editor.
4. Interact with the Menu buttons: Start Game, Settings (Audio/Graphics), Controls, and Credits.

### Direct Gameplay Scene
1. Navigate to:
   `Assets/ZombieRunner/Scenes/ZombieRunnerGameplay.unity`
2. Double-click to open the scene.
3. Click **Play** to immediately test runner locomotion, shooting, and enemy waves.

---

## 5. Building a Standalone Executable

1. In the Unity top menu bar, select **File > Build Profiles** (or **Build Settings**).
2. Ensure the scenes are in the following order:
   - `0: Assets/ZombieRunner/Scenes/ZombieRunnerMainMenu.unity`
   - `1: Assets/ZombieRunner/Scenes/ZombieRunnerGameplay.unity`
   - `2: Assets/Scenes/SampleScene.unity` *(optional template backup)*
3. Set **Platform** to **Windows, Mac, Linux** (Target: Windows, Architecture: x86_64).
4. Click **Build**, create a new folder named `Build/`, and select it.
5. Launch the generated `ZombieRunner.exe`.
