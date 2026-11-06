using System.IO;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;
using ZombieRunner.World;

namespace ZombieRunner.Editor
{
    /// <summary>
    /// Transforms the Zombie Runner environment from blue nighttime to a cinematic
    /// dark red survival-horror atmosphere. Applies red ambient lighting, crimson fog,
    /// blood-red emergency lights, horror color grading, and flickering red streetlights.
    ///
    /// Run via:  ZombieRunner / Apply Red Horror Environment Upgrade
    /// </summary>
    public static class RedHorrorEnvironmentUpgrader
    {
        // ─── Target paths ────────────────────────────────────────────────────────
        private const string ScenePath          = "Assets/ZombieRunner/Scenes/ZombieRunnerGameplay.unity";
        private const string SampleProfilePath  = "Assets/Settings/SampleSceneProfile.asset";
        private const string PcRPAssetPath      = "Assets/Settings/PC_RPAsset.asset";
        private const string MobileRPAssetPath  = "Assets/Settings/Mobile_RPAsset.asset";
        private const string PcRendererPath     = "Assets/Settings/PC_Renderer.asset";

        // ─── Horror colour palette ────────────────────────────────────────────
        // Deep crimson sky / fog
        private static readonly Color DeepCrimsonFog       = new Color(0.10f, 0.00f, 0.00f, 1f); // #1A0000
        private static readonly Color BloodRedAmbientSky   = new Color(0.20f, 0.02f, 0.02f, 1f); // #330505
        private static readonly Color BloodRedAmbientEq    = new Color(0.16f, 0.01f, 0.01f, 1f); // #290303
        private static readonly Color DarkMaroonGround     = new Color(0.10f, 0.00f, 0.00f, 1f); // #1A0000
        // Moonlight – reddish-white cold fill
        private static readonly Color CrimsonMoonlight     = new Color(0.72f, 0.30f, 0.28f, 1f); // B84D47
        // Emergency red
        private static readonly Color EmergencyRed         = new Color(1.00f, 0.06f, 0.06f, 1f); // #FF1010
        // Warm orange window glow
        private static readonly Color WarmOrangeGlow       = new Color(1.00f, 0.35f, 0.14f, 1f); // #FF5924
        // Tunnel deep-red lamp
        private static readonly Color TunnelRedLamp        = new Color(0.88f, 0.04f, 0.04f, 1f); // #E00A0A
        // Tunnel main lamp (dim crimson-white to avoid pitch-black)
        private static readonly Color TunnelCeilingLamp    = new Color(0.70f, 0.18f, 0.12f, 1f); // #B22F1F

        // ─────────────────────────────────────────────────────────────────────────
        [MenuItem("ZombieRunner/Apply Red Horror Environment Upgrade")]
        public static void ApplyRedHorrorUpgrade()
        {
            if (EditorApplication.isPlayingOrWillChangePlaymode)
            {
                Debug.LogWarning("[RedHorror] Cannot apply upgrade while in Play Mode.");
                return;
            }

            Debug.Log("====================================================================");
            Debug.Log("[RedHorror] Starting DARK RED SURVIVAL-HORROR Environment Transform...");
            Debug.Log("====================================================================");

            UpgradePipelineSettings();
            UpgradeVolumeProfile();
            UpgradeMaterials();
            UpgradeEnvironmentPrefabs();
            UpgradeCharacterPrefabs();
            UpgradeGameplayScene();

            AssetDatabase.SaveAssets();
            AssetDatabase.Refresh();

            Debug.Log("====================================================================");
            Debug.Log("[RedHorror] RED HORROR Environment Transform COMPLETED!");
            Debug.Log("====================================================================");
        }

        // ─── 1. URP Pipeline Settings ────────────────────────────────────────────
        private static void UpgradePipelineSettings()
        {
            Debug.Log("[RedHorror] Upgrading URP Pipeline Assets and Renderers...");

            UniversalRenderPipelineAsset pcAsset =
                AssetDatabase.LoadAssetAtPath<UniversalRenderPipelineAsset>(PcRPAssetPath);
            if (pcAsset != null)
            {
                SerializedObject so = new SerializedObject(pcAsset);
                so.FindProperty("m_ColorGradingMode").intValue              = 1; // HDR
                so.FindProperty("m_ShadowDistance").floatValue              = 70f;
                so.FindProperty("m_SoftShadowsSupported").boolValue         = true;
                so.FindProperty("m_AdditionalLightsRenderingMode").intValue = 1; // PerPixel
                so.FindProperty("m_AdditionalLightsPerObjectLimit").intValue= 6;
                so.FindProperty("m_AdditionalLightShadowsSupported").boolValue = true;
                so.ApplyModifiedProperties();
                EditorUtility.SetDirty(pcAsset);
                Debug.Log("  -> PC_RPAsset: HDR, 70m shadows, PerPixel additional lights.");
            }

            UniversalRenderPipelineAsset mobileAsset =
                AssetDatabase.LoadAssetAtPath<UniversalRenderPipelineAsset>(MobileRPAssetPath);
            if (mobileAsset != null)
            {
                SerializedObject so = new SerializedObject(mobileAsset);
                so.FindProperty("m_ColorGradingMode").intValue              = 1; // HDR
                so.FindProperty("m_SoftShadowsSupported").boolValue         = true;
                so.FindProperty("m_AdditionalLightsRenderingMode").intValue = 1; // PerPixel
                so.FindProperty("m_AdditionalLightsPerObjectLimit").intValue= 4;
                so.ApplyModifiedProperties();
                EditorUtility.SetDirty(mobileAsset);
                Debug.Log("  -> Mobile_RPAsset: HDR, Soft Shadows.");
            }

            // SSAO – pull back a little so red indirect bounce reads clearly
            ScriptableRendererData pcRenderer =
                AssetDatabase.LoadAssetAtPath<ScriptableRendererData>(PcRendererPath);
            if (pcRenderer != null)
            {
                foreach (ScriptableRendererFeature feature in pcRenderer.rendererFeatures)
                {
                    if (feature != null &&
                        feature.GetType().Name.Contains("ScreenSpaceAmbientOcclusion"))
                    {
                        SerializedObject so       = new SerializedObject(feature);
                        SerializedProperty settings = so.FindProperty("m_Settings");
                        if (settings != null)
                        {
                            SerializedProperty intensity     = settings.FindPropertyRelative("Intensity");
                            SerializedProperty radius        = settings.FindPropertyRelative("Radius");
                            SerializedProperty directLighting= settings.FindPropertyRelative("DirectLightingStrength");
                            if (intensity      != null) intensity.floatValue      = 0.65f;
                            if (radius         != null) radius.floatValue         = 0.45f;
                            if (directLighting != null) directLighting.floatValue = 0.25f;
                            so.ApplyModifiedProperties();
                            EditorUtility.SetDirty(feature);
                            Debug.Log("  -> SSAO: Intensity=0.65, Radius=0.45, DirectLight=0.25.");
                        }
                    }
                }
                EditorUtility.SetDirty(pcRenderer);
            }
        }

        // ─── 2. Post-Processing Volume Profile ───────────────────────────────────
        private static void UpgradeVolumeProfile()
        {
            Debug.Log("[RedHorror] Upgrading Post-Processing Volume Profile for red horror...");

            VolumeProfile profile =
                AssetDatabase.LoadAssetAtPath<VolumeProfile>(SampleProfilePath);
            if (profile == null)
            {
                Debug.LogError("[RedHorror] Cannot load VolumeProfile at " + SampleProfilePath);
                return;
            }

            // 1. Tonemapping – ACES keeps the crimson palette from blowing out
            if (!profile.TryGet(out Tonemapping tonemapping))
                tonemapping = profile.Add<Tonemapping>(true);
            tonemapping.mode.overrideState = true;
            tonemapping.mode.value         = TonemappingMode.ACES;

            // 2. Bloom – tight red bloom around emergency fixtures
            if (!profile.TryGet(out Bloom bloom))
                bloom = profile.Add<Bloom>(true);
            bloom.threshold.overrideState          = true;
            bloom.threshold.value                  = 0.80f;    // lower so emergency reds bloom
            bloom.intensity.overrideState          = true;
            bloom.intensity.value                  = 1.10f;    // stronger than the neutral version
            bloom.scatter.overrideState            = true;
            bloom.scatter.value                    = 0.55f;    // contained scatter
            bloom.tint.overrideState               = true;
            bloom.tint.value                       = new Color(1.0f, 0.15f, 0.10f, 1f); // blood-red tint
            bloom.highQualityFiltering.overrideState = true;
            bloom.highQualityFiltering.value       = true;

            // 3. Color Adjustments – darken exposure, boost contrast, crimson filter
            if (!profile.TryGet(out ColorAdjustments colorAdj))
                colorAdj = profile.Add<ColorAdjustments>(true);
            colorAdj.postExposure.overrideState = true;
            colorAdj.postExposure.value         = -0.15f;    // slightly darker scene
            colorAdj.contrast.overrideState     = true;
            colorAdj.contrast.value             = 24f;       // cinematic high contrast
            colorAdj.saturation.overrideState   = true;
            colorAdj.saturation.value           = -15f;      // desaturate base colours → red stands out
            colorAdj.colorFilter.overrideState  = true;
            colorAdj.colorFilter.value          = new Color(1.0f, 0.80f, 0.78f, 1f); // subtle red-warm tint

            // 4. Shadows, Midtones, Highlights
            //    Shadows → deep maroon black
            //    Highlights → keep relatively neutral so emergency lights read as red
            if (!profile.TryGet(out ShadowsMidtonesHighlights smh))
                smh = profile.Add<ShadowsMidtonesHighlights>(true);
            smh.shadows.overrideState     = true;
            smh.shadows.value             = new Vector4(1.10f, 0.82f, 0.82f, 0f); // red-biased shadows
            smh.midtones.overrideState    = true;
            smh.midtones.value            = new Vector4(1.05f, 0.90f, 0.88f, 0f); // slightly red midtones
            smh.highlights.overrideState  = true;
            smh.highlights.value          = new Vector4(1.08f, 0.88f, 0.85f, 0f); // warm-red highlights
            smh.shadowsStart.overrideState= true;
            smh.shadowsStart.value        = 0f;
            smh.shadowsEnd.overrideState  = true;
            smh.shadowsEnd.value          = 0.38f;
            smh.highlightsStart.overrideState = true;
            smh.highlightsStart.value     = 0.52f;
            smh.highlightsEnd.overrideState = true;
            smh.highlightsEnd.value       = 1.0f;

            // 5. Vignette – heavy dark vignette for horror framing
            if (!profile.TryGet(out Vignette vignette))
                vignette = profile.Add<Vignette>(true);
            vignette.color.overrideState      = true;
            vignette.color.value              = new Color(0.12f, 0.00f, 0.00f, 1f); // dark crimson vignette
            vignette.intensity.overrideState  = true;
            vignette.intensity.value          = 0.38f;
            vignette.smoothness.overrideState = true;
            vignette.smoothness.value         = 0.45f;

            // 6. Chromatic Aberration – subtle horror fringe
            if (!profile.TryGet(out ChromaticAberration ca))
                ca = profile.Add<ChromaticAberration>(true);
            ca.intensity.overrideState = true;
            ca.intensity.value         = 0.08f;

            // 7. Film Grain – cinematic film grain for gritty look
            if (!profile.TryGet(out FilmGrain grain))
                grain = profile.Add<FilmGrain>(true);
            grain.type.overrideState      = true;
            grain.type.value              = FilmGrainLookup.Thin1;
            grain.intensity.overrideState = true;
            grain.intensity.value         = 0.18f;
            grain.response.overrideState  = true;
            grain.response.value          = 0.80f;

            EditorUtility.SetDirty(profile);
            Debug.Log("  -> Volume profile: ACES, red-tint Bloom, red-biased SMH, Vignette, ChromaticAberration, FilmGrain.");
        }

        // ─── 3. Materials ────────────────────────────────────────────────────────
        private static void UpgradeMaterials()
        {
            Debug.Log("[RedHorror] Upgrading materials to red horror palette...");

            // ── Asphalt – keep albedo neutral, raise smoothness for dark-red reflections
            UpgradeMat("Assets/ZombieRunner/Materials/WR_Asphalt.mat", m =>
            {
                m.SetColor("_BaseColor",   new Color(0.32f, 0.28f, 0.28f, 1f)); // slightly red-tinted dark road
                m.SetFloat("_Smoothness",  0.42f);   // wetter → reflects emergency red
                m.SetFloat("_BumpScale",   1.25f);
                m.SetFloat("_GlossyReflections", 1f);
                m.SetFloat("_EnvironmentReflections", 1f);
                if (m.HasProperty("_SpecColor"))
                    m.SetColor("_SpecColor", new Color(0.35f, 0.12f, 0.10f, 1f)); // dark red spec
                Debug.Log("  -> WR_Asphalt: dark red-tinted road, Smoothness=0.42.");
            });

            // ── Lane paint – dim orange-red for road markings under emergency lights
            UpgradeMat("Assets/ZombieRunner/Materials/WR_LanePaint.mat", m =>
            {
                m.SetColor("_BaseColor", new Color(0.65f, 0.40f, 0.30f, 1f));
                m.SetFloat("_Smoothness", 0.36f);
                m.SetFloat("_GlossyReflections", 1f);
                Debug.Log("  -> WR_LanePaint: orange-red marking.");
            });

            // ── Concrete / building walls – very dark with subtle red emission in cracks
            UpgradeMat("Assets/ZombieRunner/Materials/WR_Concrete.mat", m =>
            {
                m.SetColor("_BaseColor", new Color(0.28f, 0.24f, 0.24f, 1f)); // dark warm-grey
                m.SetFloat("_Smoothness", 0.22f);
                m.SetFloat("_GlossyReflections", 1f);
                Debug.Log("  -> WR_Concrete: darkened, slight warm-grey.");
            });

            // ── Ruins / building facades – preserved geometry, red-tinted base
            UpgradeMat("Assets/ZombieRunner/Materials/WR_Ruins.mat", m =>
            {
                m.SetColor("_BaseColor", new Color(0.55f, 0.46f, 0.46f, 1f)); // keep readable but red-tinted
                m.SetFloat("_Smoothness", 0.22f);
                m.SetFloat("_GlossyReflections", 1f);
                // Warm-crimson window emission driven by existing emission map
                m.EnableKeyword("_EMISSION");
                m.SetColor("_EmissionColor", new Color(1.4f, 0.30f, 0.08f, 1f)); // orange-red window glow
                Debug.Log("  -> WR_Ruins: red-tinted facade, orange-red window emission.");
            });

            // ── Subway Concrete – dark red-brown tunnel walls
            UpgradeMat("Assets/ZombieRunner/Materials/WR_SubwayConcrete.mat", m =>
            {
                m.SetColor("_BaseColor", new Color(0.30f, 0.22f, 0.22f, 1f));
                m.SetFloat("_Smoothness", 0.28f);
                m.SetFloat("_GlossyReflections", 1f);
                Debug.Log("  -> WR_SubwayConcrete: dark red-brown.");
            });

            // ── Subway Tile – slightly lighter, reflects red emergency lamps nicely
            UpgradeMat("Assets/ZombieRunner/Materials/WR_SubwayTile.mat", m =>
            {
                m.SetColor("_BaseColor", new Color(0.38f, 0.28f, 0.28f, 1f));
                m.SetFloat("_Smoothness", 0.42f);
                m.SetFloat("_GlossyReflections", 1f);
                Debug.Log("  -> WR_SubwayTile: red-tinted tile, Smoothness=0.42.");
            });

            // ── Car paint – rusted dark red
            UpgradeMat("Assets/ZombieRunner/Materials/WR_CarPaint.mat", m =>
            {
                m.SetColor("_BaseColor", new Color(0.28f, 0.06f, 0.06f, 1f)); // dark rusted red
                m.SetFloat("_Metallic",  0.70f);
                m.SetFloat("_Smoothness",0.45f);
                m.SetFloat("_GlossyReflections", 1f);
                Debug.Log("  -> WR_CarPaint: rusted dark red.");
            });

            // ── Metal surfaces – dark industrial, hint of red oxidation
            string[] metalPaths = new[]
            {
                "Assets/ZombieRunner/Materials/WR_Metal.mat",
                "Assets/ZombieRunner/Materials/WR_WeaponMetal.mat",
                "Assets/ZombieRunner/Materials/WR_FactoryMetal.mat",
                "Assets/ZombieRunner/Materials/WR_Pipe.mat",
                "Assets/ZombieRunner/Materials/WR_TunnelIndustrialMetal.mat"
            };
            foreach (string p in metalPaths)
                UpgradeMat(p, m =>
                {
                    m.SetFloat("_Metallic",  0.80f);
                    m.SetFloat("_Smoothness",0.42f);
                    m.SetFloat("_GlossyReflections", 1f);
                });

            // ── Tunnel hazard strips – blood-orange warning
            UpgradeMat("Assets/ZombieRunner/Materials/WR_TunnelHazard.mat", m =>
            {
                m.SetColor("_BaseColor", new Color(0.85f, 0.28f, 0.06f, 1f));
                m.EnableKeyword("_EMISSION");
                m.SetColor("_EmissionColor", new Color(1.5f, 0.30f, 0.05f, 1f));
                Debug.Log("  -> WR_TunnelHazard: blood-orange hazard strips.");
            });

            // ── Factory warning signs – emergency red
            UpgradeMat("Assets/ZombieRunner/Materials/WR_FactoryWarning.mat", m =>
            {
                m.SetColor("_BaseColor", new Color(0.80f, 0.08f, 0.05f, 1f));
                m.EnableKeyword("_EMISSION");
                m.SetColor("_EmissionColor", new Color(2.0f, 0.12f, 0.08f, 1f));
                Debug.Log("  -> WR_FactoryWarning: emergency red.");
            });

            // ── Hazard orange barrels – rusted orange-red
            UpgradeMat("Assets/ZombieRunner/Materials/WR_HazardOrange.mat", m =>
            {
                m.SetColor("_BaseColor", new Color(0.72f, 0.22f, 0.08f, 1f));
                Debug.Log("  -> WR_HazardOrange: rusted orange-red.");
            });

            UpgradeMat("Assets/ZombieRunner/Materials/WR_BarrelOrange.mat", m =>
            {
                m.SetColor("_BaseColor", new Color(0.65f, 0.18f, 0.06f, 1f));
            });

            // ── Emergency Lamp fixture – bright red emissive bulb
            UpgradeMat("Assets/ZombieRunner/Materials/WR_EmergencyLamp.mat", m =>
            {
                m.SetColor("_BaseColor", new Color(1.0f, 0.08f, 0.05f, 1f));
                m.EnableKeyword("_EMISSION");
                m.SetColor("_EmissionColor", new Color(5.5f, 0.20f, 0.12f, 1f)); // intense red emission
                m.SetFloat("_Smoothness", 0.85f);
                Debug.Log("  -> WR_EmergencyLamp: intense red emissive.");
            });

            // ── Tunnel Lamp fixture – deep crimson lamp
            UpgradeMat("Assets/ZombieRunner/Materials/WR_TunnelLamp.mat", m =>
            {
                m.SetColor("_BaseColor", new Color(0.90f, 0.12f, 0.08f, 1f));
                m.EnableKeyword("_EMISSION");
                m.SetColor("_EmissionColor", new Color(4.8f, 0.18f, 0.10f, 1f)); // deep red
                m.SetFloat("_Smoothness", 0.85f);
                Debug.Log("  -> WR_TunnelLamp: deep crimson emissive.");
            });

            // ── Skybox – dark blood-red sky replacing the blue night
            UpgradeMat("Assets/ZombieRunner/Materials/WR_NightSkybox.mat", m =>
            {
                m.SetFloat("_Exposure",          0.30f);    // darker sky
                m.SetColor("_SkyTint",           new Color(0.18f, 0.02f, 0.02f, 1f)); // blood red
                m.SetColor("_GroundColor",       new Color(0.08f, 0.00f, 0.00f, 1f)); // near-black ground
                m.SetFloat("_AtmosphereThickness",0.08f);
                Debug.Log("  -> WR_NightSkybox: blood-red sky.");
            });

            // ── Health / power-up accents – keep visible against red
            UpgradeMat("Assets/ZombieRunner/Materials/WR_HealthAccent.mat", m =>
            {
                m.SetColor("_BaseColor", new Color(0.0f, 0.65f, 0.10f, 1f)); // contrasting green
            });

            // ── Power-up glow – electric blue to contrast red environment
            UpgradeMat("Assets/ZombieRunner/Materials/WR_PowerUp.mat", m =>
            {
                m.EnableKeyword("_EMISSION");
                m.SetColor("_EmissionColor", new Color(0.20f, 0.60f, 2.0f, 1f));
            });

            // ── Muzzle flash – orange-red hot flash
            UpgradeMat("Assets/ZombieRunner/Materials/WR_MuzzleFlash.mat", m =>
            {
                m.EnableKeyword("_EMISSION");
                m.SetColor("_EmissionColor", new Color(3.5f, 1.2f, 0.2f, 1f));
            });

            // ── Military canvas – dirty dark olive-green (preserve to contrast red)
            // No change needed – the green-grey palette contrasts well with red lighting.

            Debug.Log("[RedHorror] Material upgrades complete.");
        }

        // ─── 4. Environment Prefabs ──────────────────────────────────────────────
        private static void UpgradeEnvironmentPrefabs()
        {
            Debug.Log("[RedHorror] Upgrading Environment Prefabs...");

            // ── City Ruins ─────────────────────────────────────────────────────
            const string cityPrefabPath = "Assets/ZombieRunner/Prefabs/Environment/EnvironmentSegment_CityRuins.prefab";
            GameObject city = PrefabUtility.LoadPrefabContents(cityPrefabPath);
            if (city != null)
            {
                // --- Existing streetlight: convert to emergency red flicker ---
                Transform sodiumLamp = city.transform.Find("SodiumStreetlight_Arm/Flickering_SodiumLamp");
                if (sodiumLamp == null)
                    sodiumLamp = city.transform.Find("Flickering_SodiumLamp");

                if (sodiumLamp != null)
                {
                    Light lc = sodiumLamp.GetComponent<Light>();
                    if (lc != null)
                    {
                        lc.type         = LightType.Spot;
                        lc.range        = 15.0f;
                        lc.intensity    = 3.8f;
                        lc.spotAngle    = 90f;
                        lc.innerSpotAngle= 55f;
                        lc.color        = EmergencyRed;
                        lc.shadows      = LightShadows.None;
                        sodiumLamp.localEulerAngles = new Vector3(80f, 0f, 0f);
                    }

                    StreetlightFlicker flicker = sodiumLamp.GetComponent<StreetlightFlicker>();
                    if (flicker != null)
                    {
                        SerializedObject so = new SerializedObject(flicker);
                        so.FindProperty("baseIntensity").floatValue        = 3.8f;
                        so.FindProperty("lightColor").colorValue           = EmergencyRed;
                        so.FindProperty("baseEmissionColor").colorValue    = new Color(5.5f, 0.20f, 0.12f, 1f);
                        so.FindProperty("flickerFrequency").floatValue     = 18f;
                        so.FindProperty("microFlickerAmount").floatValue   = 0.12f;
                        so.FindProperty("allowBlackouts").boolValue        = true;
                        so.FindProperty("minBlackoutInterval").floatValue  = 1.5f;
                        so.FindProperty("maxBlackoutInterval").floatValue  = 5.0f;
                        so.FindProperty("blackoutDuration").floatValue     = 0.09f;
                        so.ApplyModifiedProperties();
                    }
                    Debug.Log("  -> CityRuins main streetlight: emergency red flicker.");
                }

                // --- Broken fixture: intense orange-red dangling beacon ---
                Transform brokenFixture = city.transform.Find("BrokenStreetlight_FixtureDangling");
                if (brokenFixture != null)
                {
                    Light bl = brokenFixture.GetComponent<Light>();
                    if (bl == null) bl = brokenFixture.gameObject.AddComponent<Light>();
                    bl.type      = LightType.Point;
                    bl.range     = 12.0f;
                    bl.intensity = 2.6f;
                    bl.color     = WarmOrangeGlow;
                    bl.shadows   = LightShadows.None;

                    StreetlightFlicker bf = brokenFixture.GetComponent<StreetlightFlicker>();
                    if (bf == null) bf = brokenFixture.gameObject.AddComponent<StreetlightFlicker>();
                    SerializedObject bso = new SerializedObject(bf);
                    bso.FindProperty("targetLight").objectReferenceValue         = bl;
                    bso.FindProperty("fixtureRenderer").objectReferenceValue     = brokenFixture.GetComponent<Renderer>();
                    bso.FindProperty("baseIntensity").floatValue                 = 2.6f;
                    bso.FindProperty("lightColor").colorValue                    = WarmOrangeGlow;
                    bso.FindProperty("baseEmissionColor").colorValue             = new Color(3.8f, 0.80f, 0.12f, 1f);
                    bso.FindProperty("flickerFrequency").floatValue              = 22f;
                    bso.FindProperty("microFlickerAmount").floatValue            = 0.18f;
                    bso.FindProperty("allowBlackouts").boolValue                 = true;
                    bso.FindProperty("minBlackoutInterval").floatValue           = 0.8f;
                    bso.FindProperty("maxBlackoutInterval").floatValue           = 3.5f;
                    bso.FindProperty("blackoutDuration").floatValue              = 0.14f;
                    bso.ApplyModifiedProperties();
                    Debug.Log("  -> CityRuins broken fixture: orange-red broken beacon.");
                }

                // --- Add road-level emergency red point lights (simulate strobes) ---
                EnsureRedRoadLight(city.transform, "EmergencyRoadLight_L",
                    new Vector3(-3.5f, 0.4f, -8f));
                EnsureRedRoadLight(city.transform, "EmergencyRoadLight_R",
                    new Vector3( 3.5f, 0.4f,  8f));

                // --- Building window warm fill ---
                Transform signboard = city.transform.Find("B_Signboard");
                if (signboard != null)
                {
                    EnsureNamedChild<Light>(signboard, "Window_OrangeGlow", go =>
                    {
                        go.transform.localPosition = new Vector3(0.5f, -0.5f, 0f);
                        Light sl = go.AddComponent<Light>();
                        sl.type      = LightType.Point;
                        sl.range     = 7.0f;
                        sl.intensity = 1.8f;
                        sl.color     = WarmOrangeGlow;
                        sl.shadows   = LightShadows.None;
                    });
                }

                PrefabUtility.SaveAsPrefabAsset(city, cityPrefabPath);
                PrefabUtility.UnloadPrefabContents(city);
            }

            // ── Subway Tunnel Interior ─────────────────────────────────────────
            UpgradeTunnelPrefab(
                "Assets/ZombieRunner/Prefabs/Environment/EnvironmentSegment_SubwayTunnel.prefab",
                "SubwayTunnel");

            // ── Tunnel Entrance ───────────────────────────────────────────────
            UpgradeTunnelPrefab(
                "Assets/ZombieRunner/Prefabs/Environment/EnvironmentSegment_TunnelEntrance.prefab",
                "TunnelEntrance");

            // ── Tunnel Exit ────────────────────────────────────────────────────
            UpgradeTunnelPrefab(
                "Assets/ZombieRunner/Prefabs/Environment/EnvironmentSegment_TunnelExit.prefab",
                "TunnelExit");
        }

        /// <summary>Upgrade lights inside any tunnel-type prefab to red horror palette.</summary>
        private static void UpgradeTunnelPrefab(string prefabPath, string label)
        {
            if (!File.Exists(prefabPath)) return;

            GameObject prefab = PrefabUtility.LoadPrefabContents(prefabPath);
            if (prefab == null) return;

            Light[] lights = prefab.GetComponentsInChildren<Light>(true);
            foreach (Light l in lights)
            {
                // Heuristic: if the original light was already red-ish, treat as emergency lamp
                bool wasEmergency = (l.color.r > 0.7f && l.color.g < 0.3f);
                if (wasEmergency)
                {
                    l.color     = EmergencyRed;
                    l.intensity = 1.60f;
                    l.range     = 10f;
                }
                else
                {
                    // Main tunnel ceiling / wall lamp → dim crimson fill
                    l.color     = TunnelCeilingLamp;
                    l.intensity = 2.0f;
                    l.range     = 18f;
                }
            }

            // Add additional red warning strip lights if none exist
            if (lights.Length == 0)
            {
                AddTunnelWarningLight(prefab.transform, "TunnelWarn_L", new Vector3(-2.4f, 2.8f, 0f));
                AddTunnelWarningLight(prefab.transform, "TunnelWarn_R", new Vector3( 2.4f, 2.8f, 0f));
            }

            PrefabUtility.SaveAsPrefabAsset(prefab, prefabPath);
            PrefabUtility.UnloadPrefabContents(prefab);
            Debug.Log($"  -> {label}: lights converted to red horror palette.");
        }

        // ─── 5. Character Prefabs ─────────────────────────────────────────────────
        private static void UpgradeCharacterPrefabs()
        {
            Debug.Log("[RedHorror] Upgrading Character Prefabs (red rim lighting)...");

            // ── Player – red-tinted cool rim for horror silhouette ─────────────
            const string playerPrefabPath = "Assets/ZombieRunner/Prefabs/Player/PlayerPlaceholder.prefab";
            GameObject player = PrefabUtility.LoadPrefabContents(playerPrefabPath);
            if (player != null)
            {
                // Weapon flashlight – keep as a neutral light beam (player safety)
                Transform weapon = player.transform.Find("Weapon Placeholder/Muzzle");
                if (weapon == null) weapon = player.transform.Find("Weapon Placeholder");
                if (weapon != null)
                {
                    EnsureNamedChild<Light>(weapon, "Tactical_Flashlight_Beam", go =>
                    {
                        Light fl = go.AddComponent<Light>();
                        fl.type          = LightType.Spot;
                        fl.range         = 32f;
                        fl.spotAngle     = 46f;
                        fl.innerSpotAngle= 26f;
                        fl.intensity     = 2.4f;
                        fl.color         = new Color(0.98f, 0.90f, 0.86f, 1f); // warm white tactical
                        fl.shadows       = LightShadows.None;
                    });
                }

                // Red-tinted player rim backlight
                EnsureNamedChild<Light>(player.transform, "Player_Horror_Rim_Light", go =>
                {
                    go.transform.localPosition = new Vector3(0f, 1.7f, -0.65f);
                    Light rim = go.AddComponent<Light>();
                    rim.type      = LightType.Point;
                    rim.range     = 2.5f;
                    rim.intensity = 1.6f;
                    rim.color     = new Color(0.90f, 0.15f, 0.10f, 1f); // blood red rim
                    rim.shadows   = LightShadows.None;
                });

                PrefabUtility.SaveAsPrefabAsset(player, playerPrefabPath);
                PrefabUtility.UnloadPrefabContents(player);
                Debug.Log("  -> Player: red horror rim light.");
            }

            // ── Zombies – red-orange menacing back rim ────────────────────────
            string[] zombiePaths = new[]
            {
                "Assets/ZombieRunner/Prefabs/Zombies/NormalZombie.prefab",
                "Assets/ZombieRunner/Prefabs/Zombies/FastZombie.prefab",
                "Assets/ZombieRunner/Prefabs/Zombies/BigZombie.prefab"
            };

            foreach (string zPath in zombiePaths)
            {
                GameObject z = PrefabUtility.LoadPrefabContents(zPath);
                if (z == null) continue;

                // Replace or add rim light
                Transform existingRim = z.transform.Find("Visual - Cool Rim Light");
                if (existingRim != null)
                {
                    Light rimL = existingRim.GetComponent<Light>();
                    if (rimL != null)
                    {
                        rimL.color     = new Color(0.85f, 0.12f, 0.08f, 1f); // blood red zombie rim
                        rimL.intensity = 1.8f;
                    }
                }
                else
                {
                    EnsureNamedChild<Light>(z.transform, "Visual - Red Rim Light", go =>
                    {
                        go.transform.localPosition = new Vector3(0f, 1.85f, 0.75f);
                        Light rim = go.AddComponent<Light>();
                        rim.type      = LightType.Point;
                        rim.range     = 2.8f;
                        rim.intensity = 1.8f;
                        rim.color     = new Color(0.85f, 0.12f, 0.08f, 1f);
                        rim.shadows   = LightShadows.None;
                    });
                }

                PrefabUtility.SaveAsPrefabAsset(z, zPath);
                PrefabUtility.UnloadPrefabContents(z);
                Debug.Log($"  -> {z.name}: red horror zombie rim.");
            }
        }

        // ─── 6. Gameplay Scene Settings ───────────────────────────────────────────
        private static void UpgradeGameplayScene()
        {
            Debug.Log("[RedHorror] Upgrading Gameplay Scene render settings...");

            if (EditorApplication.isPlaying)
            {
                Debug.LogWarning("[RedHorror] Scene upgrade deferred – editor is in Play Mode.");
                return;
            }

            var activeScene = UnityEngine.SceneManagement.SceneManager.GetActiveScene();
            var scene = (activeScene.IsValid() && activeScene.path == ScenePath)
                ? activeScene
                : EditorSceneManager.OpenScene(ScenePath, OpenSceneMode.Single);

            // ── Camera ─────────────────────────────────────────────────────────
            Camera mainCam = Camera.main;
            if (mainCam != null)
            {
                mainCam.backgroundColor = new Color(0.08f, 0.00f, 0.00f, 1f); // dark crimson clear colour
                mainCam.farClipPlane    = 220f;
                mainCam.fieldOfView     = 58f;

                UniversalAdditionalCameraData camData = mainCam.GetUniversalAdditionalCameraData();
                if (camData != null)
                {
                    camData.renderPostProcessing   = true;
                    camData.antialiasing           = AntialiasingMode.FastApproximateAntialiasing;
                    camData.dithering              = true;
                    camData.requiresDepthTexture   = true;
                    camData.requiresColorTexture   = true;
                    EditorUtility.SetDirty(camData);
                }
                Debug.Log("  -> Camera: crimson background, FOV=58, far=220.");
            }

            // ── Global Directional Moon / Key Light ────────────────────────────
            Light keyLight = null;
            foreach (Light l in Object.FindObjectsByType<Light>())
            {
                if (l.type == LightType.Directional) { keyLight = l; break; }
            }
            if (keyLight != null)
            {
                // Reddish-white moonlight – not pure red to keep scene readable
                keyLight.color           = CrimsonMoonlight;
                keyLight.intensity       = 1.20f;   // dimmer for horror atmosphere
                keyLight.shadows         = LightShadows.Soft;
                keyLight.shadowStrength  = 0.85f;   // deep shadows
                keyLight.shadowBias      = 0.04f;
                keyLight.shadowNormalBias= 0.30f;
                keyLight.transform.rotation = Quaternion.Euler(48f, 42f, 0f);
                EditorUtility.SetDirty(keyLight);
                Debug.Log("  -> Directional Key Light: crimson-tinted moonlight, Intensity=1.20.");
            }

            // ── Post-Processing Volume ─────────────────────────────────────────
            Volume sceneVolume = Object.FindAnyObjectByType<Volume>();
            if (sceneVolume == null)
            {
                GameObject volGo = new GameObject("Global Post-Processing Volume");
                sceneVolume = volGo.AddComponent<Volume>();
                sceneVolume.isGlobal  = true;
                sceneVolume.priority  = 1;
                VolumeProfile profile = AssetDatabase.LoadAssetAtPath<VolumeProfile>(SampleProfilePath);
                if (profile != null) sceneVolume.sharedProfile = profile;
                Debug.Log("  -> Created Global Post-Processing Volume with horror profile.");
            }
            else
            {
                sceneVolume.isGlobal = true;
                if (sceneVolume.sharedProfile == null)
                    sceneVolume.sharedProfile = AssetDatabase.LoadAssetAtPath<VolumeProfile>(SampleProfilePath);
                EditorUtility.SetDirty(sceneVolume);
                Debug.Log("  -> Existing Post-Processing Volume updated.");
            }

            // ── Environment Theme Manager – City & Tunnel profiles ─────────────
            EnvironmentThemeManager themeMgr = Object.FindAnyObjectByType<EnvironmentThemeManager>();
            if (themeMgr != null)
            {
                SerializedObject so            = new SerializedObject(themeMgr);
                SerializedProperty profilesProp= so.FindProperty("themeProfiles");

                if (profilesProp != null && profilesProp.arraySize >= 4)
                {
                    // CityRuins: deep crimson outdoor horror
                    SetThemeProfile(profilesProp.GetArrayElementAtIndex(0),
                        fogColor:    new Color(0.10f, 0.00f, 0.00f),  // deep crimson fog
                        ambient:     new Color(0.14f, 0.02f, 0.02f),
                        sky:         new Color(0.20f, 0.03f, 0.03f),
                        equator:     new Color(0.14f, 0.02f, 0.02f),
                        ground:      new Color(0.08f, 0.00f, 0.00f),
                        keyColor:    CrimsonMoonlight,
                        keyIntensity:1.20f,
                        fogStart:    35f, fogEnd: 140f);

                    // SubwayTunnel: intense underground red horror
                    SetThemeProfile(profilesProp.GetArrayElementAtIndex(1),
                        fogColor:    new Color(0.08f, 0.00f, 0.00f),
                        ambient:     new Color(0.12f, 0.01f, 0.01f),
                        sky:         new Color(0.15f, 0.02f, 0.02f),
                        equator:     new Color(0.10f, 0.01f, 0.01f),
                        ground:      new Color(0.06f, 0.00f, 0.00f),
                        keyColor:    TunnelRedLamp,
                        keyIntensity:0.35f,
                        fogStart:    25f, fogEnd: 95f);

                    // MilitaryBase: dark olive-crimson
                    SetThemeProfile(profilesProp.GetArrayElementAtIndex(2),
                        fogColor:    new Color(0.09f, 0.03f, 0.02f),
                        ambient:     new Color(0.14f, 0.04f, 0.03f),
                        sky:         new Color(0.18f, 0.05f, 0.03f),
                        equator:     new Color(0.14f, 0.04f, 0.03f),
                        ground:      new Color(0.09f, 0.02f, 0.02f),
                        keyColor:    new Color(0.65f, 0.28f, 0.24f),
                        keyIntensity:1.10f,
                        fogStart:    40f, fogEnd: 155f);

                    // Factory: industrial orange-crimson
                    SetThemeProfile(profilesProp.GetArrayElementAtIndex(3),
                        fogColor:    new Color(0.12f, 0.03f, 0.01f),
                        ambient:     new Color(0.18f, 0.05f, 0.02f),
                        sky:         new Color(0.22f, 0.06f, 0.02f),
                        equator:     new Color(0.18f, 0.05f, 0.02f),
                        ground:      new Color(0.12f, 0.03f, 0.01f),
                        keyColor:    new Color(0.85f, 0.35f, 0.20f),
                        keyIntensity:1.40f,
                        fogStart:    38f, fogEnd: 150f);

                    so.ApplyModifiedProperties();
                    EditorUtility.SetDirty(themeMgr);
                    Debug.Log("  -> EnvironmentThemeManager: all 4 profiles set to red horror palette.");
                }

                // Also set the cityProfile / tunnelProfile inline structs used by ApplyLightingBlend()
                SerializedProperty cityP   = so.FindProperty("cityProfile");
                SerializedProperty tunnelP = so.FindProperty("tunnelProfile");
                if (cityP != null)
                {
                    SetLightingProfile(cityP,
                        fogColor:    new Color(0.10f, 0.00f, 0.00f),
                        skyColor:    new Color(0.20f, 0.03f, 0.03f),
                        equatorColor:new Color(0.14f, 0.02f, 0.02f),
                        groundColor: new Color(0.08f, 0.00f, 0.00f),
                        keyColor:    CrimsonMoonlight,
                        keyIntensity:1.20f,
                        fogStart:    35f, fogEnd: 140f);
                    so.ApplyModifiedProperties();
                    EditorUtility.SetDirty(themeMgr);
                }
                if (tunnelP != null)
                {
                    SetLightingProfile(tunnelP,
                        fogColor:    new Color(0.08f, 0.00f, 0.00f),
                        skyColor:    new Color(0.15f, 0.02f, 0.02f),
                        equatorColor:new Color(0.10f, 0.01f, 0.01f),
                        groundColor: new Color(0.06f, 0.00f, 0.00f),
                        keyColor:    TunnelRedLamp,
                        keyIntensity:0.35f,
                        fogStart:    25f, fogEnd: 95f);
                    so.ApplyModifiedProperties();
                    EditorUtility.SetDirty(themeMgr);
                }
            }

            // ── Global RenderSettings ──────────────────────────────────────────
            RenderSettings.skybox              = AssetDatabase.LoadAssetAtPath<Material>(
                "Assets/ZombieRunner/Materials/WR_NightSkybox.mat");
            RenderSettings.ambientMode         = AmbientMode.Trilight;
            RenderSettings.ambientSkyColor     = BloodRedAmbientSky;
            RenderSettings.ambientEquatorColor  = BloodRedAmbientEq;
            RenderSettings.ambientGroundColor   = DarkMaroonGround;
            RenderSettings.ambientLight         = BloodRedAmbientEq;
            RenderSettings.fog                  = true;
            RenderSettings.fogMode              = FogMode.Linear;
            RenderSettings.fogColor             = DeepCrimsonFog;
            RenderSettings.fogStartDistance     = 35f;
            RenderSettings.fogEndDistance       = 140f;

            EditorSceneManager.MarkSceneDirty(scene);
            EditorSceneManager.SaveScene(scene);
            Debug.Log("  -> Scene RenderSettings saved: deep crimson ambient + fog.");
        }

        // ─── Helpers ─────────────────────────────────────────────────────────────

        private static void UpgradeMat(string path, System.Action<Material> configure)
        {
            Material m = AssetDatabase.LoadAssetAtPath<Material>(path);
            if (m == null) return;
            configure(m);
            EditorUtility.SetDirty(m);
        }

        /// <summary>Find or create a named child and invoke setup only when newly created.</summary>
        private static void EnsureNamedChild<T>(Transform parent, string name,
            System.Action<GameObject> setupNewGo) where T : Component
        {
            if (parent.Find(name) != null) return; // already exists
            GameObject go = new GameObject(name);
            go.transform.SetParent(parent, false);
            setupNewGo(go);
        }

        private static void EnsureRedRoadLight(Transform parent, string name, Vector3 localPos)
        {
            if (parent.Find(name) != null) return;
            GameObject go = new GameObject(name);
            go.transform.SetParent(parent, false);
            go.transform.localPosition = localPos;
            Light l   = go.AddComponent<Light>();
            l.type    = LightType.Point;
            l.range   = 8f;
            l.intensity = 1.80f;
            l.color   = EmergencyRed;
            l.shadows = LightShadows.None;

            // Flicker it like an emergency strobe
            StreetlightFlicker flicker = go.AddComponent<StreetlightFlicker>();
            SerializedObject so = new SerializedObject(flicker);
            so.FindProperty("targetLight").objectReferenceValue  = l;
            so.FindProperty("baseIntensity").floatValue          = 1.80f;
            so.FindProperty("lightColor").colorValue             = EmergencyRed;
            so.FindProperty("baseEmissionColor").colorValue      = new Color(5.5f, 0.20f, 0.12f, 1f);
            so.FindProperty("flickerFrequency").floatValue       = 24f;
            so.FindProperty("microFlickerAmount").floatValue     = 0.14f;
            so.FindProperty("allowBlackouts").boolValue          = true;
            so.FindProperty("minBlackoutInterval").floatValue    = 0.6f;
            so.FindProperty("maxBlackoutInterval").floatValue    = 2.5f;
            so.FindProperty("blackoutDuration").floatValue       = 0.08f;
            so.ApplyModifiedProperties();
        }

        private static void AddTunnelWarningLight(Transform parent, string name, Vector3 localPos)
        {
            if (parent.Find(name) != null) return;
            GameObject go = new GameObject(name);
            go.transform.SetParent(parent, false);
            go.transform.localPosition = localPos;
            Light l = go.AddComponent<Light>();
            l.type    = LightType.Point;
            l.range   = 9f;
            l.intensity = 1.60f;
            l.color   = TunnelRedLamp;
            l.shadows = LightShadows.None;
        }

        private static void SetThemeProfile(SerializedProperty elem,
            Color fogColor, Color ambient, Color sky, Color equator, Color ground,
            Color keyColor, float keyIntensity, float fogStart, float fogEnd)
        {
            if (elem == null) return;
            SetColorProp(elem, "fogColor",           fogColor);
            SetColorProp(elem, "ambientColor",       ambient);
            SetColorProp(elem, "ambientSkyColor",    sky);
            SetColorProp(elem, "ambientEquatorColor",equator);
            SetColorProp(elem, "ambientGroundColor", ground);
            SetColorProp(elem, "keyLightColor",      keyColor);
            SetFloatProp(elem, "keyLightIntensity",  keyIntensity);
            SetFloatProp(elem, "fogStart",           fogStart);
            SetFloatProp(elem, "fogEnd",             fogEnd);
        }

        private static void SetLightingProfile(SerializedProperty elem,
            Color fogColor, Color skyColor, Color equatorColor, Color groundColor,
            Color keyColor, float keyIntensity, float fogStart, float fogEnd)
        {
            if (elem == null) return;
            SetColorProp(elem, "fogColor",           fogColor);
            SetColorProp(elem, "ambientSkyColor",    skyColor);
            SetColorProp(elem, "ambientEquatorColor",equatorColor);
            SetColorProp(elem, "ambientGroundColor", groundColor);
            SetColorProp(elem, "keyLightColor",      keyColor);
            SetFloatProp(elem, "keyLightIntensity",  keyIntensity);
            SetFloatProp(elem, "fogStart",           fogStart);
            SetFloatProp(elem, "fogEnd",             fogEnd);
        }

        private static void SetColorProp(SerializedProperty parent, string name, Color value)
        {
            SerializedProperty p = parent.FindPropertyRelative(name);
            if (p != null) p.colorValue = value;
        }

        private static void SetFloatProp(SerializedProperty parent, string name, float value)
        {
            SerializedProperty p = parent.FindPropertyRelative(name);
            if (p != null) p.floatValue = value;
        }
    }
}
