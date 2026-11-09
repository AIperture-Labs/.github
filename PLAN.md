# AIperture Labs — Global plan

The single planning document of the organization. Everything else is
dispatched from here:

1. A decision is taken (usually in conversation) and recorded below.
2. A milestone is created in the repository concerned, named `M<n> · <name>`,
   and split into issues. Each issue states its goal and how to verify it.
3. Issues are added to the organization's GitHub Project
   [AIperture Labs Roadmap](https://github.com/orgs/AIperture-Labs/projects),
   with an *Area* field: Engine, Website, Test projects, Game.
4. Coding agents (Claude Code, Mistral Vibe) pick an issue, work on a branch
   from `dev` and open a PR into `dev`, following the repository's
   `AGENTS.md`. `dev` is merged into `main` for releases.

This is the reference plan; repositories may keep their own notes when
useful, but the work itself is tracked in issues and PRs. The roadmap picture on the profile page
(`profile/roadmap.svg`) is regenerated every day from the milestones by
`scripts/roadmap.py`.

## Agent tasks

Commands that an agent runs on Xavier's machine (where `git` and `gh` are
authenticated), from the `AIperture-Labs/` folder that holds the clones.

Convention: a code block whose info string contains `agent` is meant to be
executed by an agent, e.g. ```` ```bash agent model=haiku ````; `model=` is the
suggested Claude Code model (`haiku` for mechanical tasks, `sonnet` by
default, `opus` for design or hard debugging). The agent checks the current
state first, asks before anything destructive, runs the block, then removes
the task from this section in a `docs(plan)` commit and reports what it did.
Blocks without `agent` are examples for humans.

No task pending.

## Repositories

| Repository | Role | Status |
| --- | --- | --- |
| [AetherEngine](https://github.com/AIperture-Labs/AetherEngine) | The engine | Restarted 2026-11-05 |
| [AetherEngine-legacy](https://github.com/AIperture-Labs/AetherEngine-legacy) | Previous code base, reference only (`backup/*` branches, wiki) | Archived |
| [.github](https://github.com/AIperture-Labs/.github) | Organization profile and this plan | Active |
| [tutorial-how-to-vulkan](https://github.com/AIperture-Labs/tutorial-how-to-vulkan) | Sascha Willems' *How to Vulkan*, up to the swapchain | Learning |
| [project-aether](https://github.com/AIperture-Labs/project-aether) | Vulkan notes and examples | Learning |
| Dependency forks (glm, doctest, yasm, libjpeg-turbo) | Pinned for the legacy build | To review |
| Test projects | Small repositories exercising the engine, one feature each | Planned |
| Game | A first game built on the engine | Planned |
| Website | Project site, its own repository | Planned (secondary) |
| Tools (MCP servers…) | One repository per tool | Planned |

## Decisions

| Date | Decision |
| --- | --- |
| 2026-11-05 | AetherEngine restarts from an empty repository; the old one is archived as `AetherEngine-legacy` and used as a source to pick from. |
| 2026-11-05 | License: MPL-2.0. Games can stay closed; modified engine files must be published with them. |
| 2026-11-05 | C++23, Vulkan, CMake with the Ninja generator. |
| 2026-11-05 | Python for editor automation (Blender/FreeCAD style); Lua for game scripting shipped in builds. |
| 2026-11-05 | VS Code support is dropped; Neovim will be integrated later. |
| 2026-11-05 | Agent setup carried over: `AGENTS.md` (no `CLAUDE.md`), `.agents/` instructions and skills, `.claude/skills` symlink. |
| 2026-11-05 | Documentation lives in each repository's `docs/`; no GitHub wiki. |
| 2026-11-05 | Branches: features → `dev` (squash merge), `dev` → `main` (merge commit); `dev` is the default branch. |
| 2026-11-05 | Priorities: the engine first, then test projects and a game; the website is secondary. |
| 2026-11-05 | Planning: this file, then milestones and issues per repository, and one organization-level GitHub Project. |
| 2026-11-05 | Targets: Linux and Windows. All OS-specific code lives in an isolated `platform` module, so Android, VR or macOS can be added later. |
| 2026-11-05 | Dependencies: vcpkg in manifest mode, pinned with a baseline and per-library overrides; overlay ports for patched libraries or our forks. |
| 2026-11-05 | Window and input: SDL3. |
| 2026-11-05 | UI: Dear ImGui (docking branch) and its extensions for the editor; RmlUi for in-game UI. Editor panels may be described from Python, Blender-style. |
| 2026-11-05 | Vulkan: the C API with volk and VMA, wrapped in thin C++ RAII types with a deferred deletion queue. Minimum version 1.4. |
| 2026-11-05 | Shaders: Slang, compiled to SPIR-V at build time. |
| 2026-11-05 | Toolchain: Clang everywhere (clang-cl on Windows, which still needs the Visual Studio Build Tools for the MS STL); an MSVC CI job may come later. |
| 2026-11-05 | Tests: doctest. |
| 2026-11-05 | CI: GitHub Actions on hosted Linux and Windows runners, Vulkan tests on lavapipe. Performance tests on a self-hosted GPU runner (homelab), triggered manually or from `dev`, never from fork PRs. Wine/Proton for quick local Windows checks. |
| 2026-11-05 | Profiling: Tracy (CPU/GPU timings, memory, locks). GPU debugging: RenderDoc, with its in-app capture API later. |
| 2026-11-05 | Logging: in-house logger with severities, per-module categories, console and file sinks. The interface is async-ready; a synchronous version first, then a background thread that flushes on fatal errors. |
| 2026-11-05 | Linking: engine core modules are static by default, shared with a CMake option; export macros from the first module, and a CI job building shared. Plugins and optional modules are shared by default (hot reload) and can be linked statically for a monolithic shipping build. |
| 2026-11-05 | First modules, each depending only on those below it: `core` (types, logger, assertions, `std::expected` errors, memory), `platform` (the only module talking to the OS, via SDL3: window, input, files, time, shared-library loading, Vulkan surface), `render` (Vulkan: device, swapchain, pipelines, frame sync, deferred deletion, Slang shaders). |
| 2026-11-05 | Content (a demo, a game) is a shared-library module with a standard entry point, run by two hosts: the `player` (standalone executable) and the editor (in its viewport). `render` always draws to an offscreen image, then presents it to the window or shows it in an ImGui panel. |
| 2026-11-05 | Milestones reorganized: the engine skeleton and the editor come first; rendering features (triangle, basics, ray tracing) are demos running inside the engine. |
| 2026-11-05 | Math: glm via vcpkg. `core` defines the engine nomenclature as aliases (`u32`, `f32`, `Vec3`, `Mat4`, `Quat`…); real wrapper classes only where a need appears. |
| 2026-11-05 | ECS: an external library behind our interface. EnTT and flecs are prototyped on critical cases (large scene hierarchy, iterating thousands of entities, frequent component add/remove, exposure to the editor and Lua) before choosing; an in-house ECS stays possible later. |
| 2026-11-05 | Game scripting: Lua 5.4. The C++ binding (sol2 or LuaBridge3) is chosen after a prototype. |
| 2026-11-05 | Editor automation: Python embedded in the editor only (Blender-style), never in shipped games. CPython comes from vcpkg like every other dependency; uv only manages the script packages. Bindings: nanobind. |
| 2026-11-05 | Jobs: one task system for the whole engine (Jolt and others plug into it), behind our interface. enkiTS and Taskflow are prototyped before choosing; an in-house system stays possible later. |
| 2026-11-05 | Reflection: registration macros behind a `reflect<T>()` interface designed to switch to C++26 static reflection. GCC 16 already implements it, Clang not yet: the switch is prototyped with GCC 16 until Clang ships it. Used by the editor, serialization, Lua and Python. |
| 2026-11-05 | Audio: miniaudio (output, mixing, decoding, node graph) and Steam Audio (HRTF spatialization, occlusion, reverb). A modular synthesizer lives in the audio engine as graph nodes, edited as nodes in the editor: first basic C++ modules (oscillators, filters, envelopes, noise) for demos, advanced modules later in Pure Data (libpd) and Faust. Real-time DSP is C++ or compiled Faust only; Python assembles graphs and generates sounds offline. |
| 2026-11-05 | Physics: Jolt Physics. |
| 2026-11-05 | 3D assets: glTF 2.0 as the main import path (fastgltf), textures in KTX2 with Basis Universal, converted to an engine runtime format. Other formats come later as import/export plugins: ufbx for FBX, Assimp for the rest. |
| 2026-11-05 | Serialization: scenes and assets as JSON (glaze) in the editor, splittable per entity or zone for large scenes; binary compressed with zstd or LZ4 in shipped games. Configuration files in TOML (toml++). |
| 2026-11-05 | Debugger: LLDB on Linux and Windows, driven from Neovim through DAP (nvim-dap, lldb-dap). |
| 2026-11-05 | Neovim: first as the external code editor (open a file at a line, hot reload on save) with a Neovim plugin to drive the engine; embedding it in an editor panel comes later. |
| 2026-11-05 | Modules and plugins, Unreal-style: a module is a unit of compiled code; a plugin packages modules and assets with a TOML descriptor (name, version, dependencies), at engine or project level. Gameplay features are plugins that can be toggled at runtime. |
| 2026-11-05 | Plugin contract: C++ first (plugins use the engine classes directly, with a version check at load). A stable C interface for external plugins and other languages (Rust…), generated from reflection like Godot's GDExtension, is a later track; reflection must therefore describe functions as well as fields. |
| 2026-11-05 | Projects, Unreal-style: a folder with `project.toml` (name, engine version, modules, enabled plugins) and `source/`, `content/`, `scripts/`, `config/`, `plugins/`. The engine lives apart and is found through a small registry of installations: built from source first, prebuilt releases on GitHub Releases later. A template generates new projects. |
| 2026-11-05 | Rendering architecture: a render graph from the start (passes declare what they read and write; the engine derives order, barriers and transient memory) with bindless resources. |
| 2026-11-05 | Advanced rendering, after ray tracing and in this order, each as a demo: path tracing (reference renderer), real-time global illumination, GPU particles, fluids (compute), virtualized geometry with meshlets and mesh shaders (meshoptimizer). |
| 2026-11-05 | Networking: client-server with an authoritative server (listen server for co-op, headless dedicated server otherwise), transport with GameNetworkingSockets, replication driven by reflection with relevancy and delta updates, designed for about a hundred players per server. Multi-server worlds later. Comes after the ECS. |
| 2026-11-05 | Animation: ozz-animation behind our interface (skeletal animation from glTF, blending, IK), ACL optional for compression; state machines and an animation node graph in the editor. Motion matching later. |
| 2026-11-05 | Input: action-based mapping (Enhanced Input-like) over SDL3, with contexts and rebinding. Actions bind to scancodes so layouts (QWERTY, AZERTY…) work unchanged; key names are shown in the player's layout; letter shortcuts in the editor use keycodes. |
| 2026-11-05 | Localization: text keys, never hard-coded strings, translated with Fluent; text rendering with FreeType and HarfBuzz. |
| 2026-11-05 | Assets: each asset has a unique ID in a TOML sidecar file next to it, so moving or renaming never breaks references. Imported data goes to a git-ignored cache. The editor watches files and hot-reloads textures, shaders, sounds and scripts. |
| 2026-11-05 | Node graphs: one shared node graph system for audio, animation, materials and AI pipelines. |
| 2026-11-05 | AI plugin: inference in C++, usable in the editor and in games (ONNX Runtime; ggml family: llama.cpp, whisper.cpp, stable-diffusion.cpp); models managed as assets with ID and version, downloadable from Hugging Face, each with its license checked; ComfyUI-like pipelines as node graphs in the editor for textures, images, 3D, sounds and voices. In games, only lightweight models. Blender/GIMP-like editing tools are a separate long-term track. |
| 2026-11-05 | Export (cooking): scenes and assets converted to compressed binary and packed into archives (`.pak`-like), splittable for updates and DLC, shipped with the player and the game code linked statically, per platform. |
| 2026-11-05 | Modding: a virtual file system mounting mod archives and folders over the game's, with priorities; mods are plugins with the same TOML descriptor, dependencies and load order; Lua as the modding language in a sandbox; native mods possible later through the stable C interface; the editor doubles as the modding kit with a mod project template. Steam Workshop / mod.io later. |
| 2026-11-05 | Priorities: test projects come next to the engine, each one demonstrating and validating features as they are developed; the game follows afterwards; the website is secondary. |
| 2026-11-05 | Test projects: one samples repository, one folder per test project, each validating one feature (triangle, audio…); a project that grows can move to its own repository. |
| 2026-11-05 | Navigation and NPC AI: Recast and Detour (navmesh, pathfinding); behavior trees with BehaviorTree.CPP or in-house on the node graph (to compare). |
| 2026-11-05 | Large worlds: double-precision world coordinates (Jolt supports them), zone streaming, terrain and vegetation in-house with GPU instancing. |
| 2026-11-05 | Procedural terrain, Houdini/Gaea-style: a heightmap sculpted by hand and generated by a non-destructive node graph (noises with FastNoise2, erosion in compute shaders, masks). Caves and overhangs need voxels, later. |
| 2026-11-05 | Procedural placement, like Unreal's PCG: a rule graph places props and vegetation on surfaces or along splines (density, slope, altitude, exclusion zones) and re-runs when something moves; in the editor with a frozen result at export, or at runtime for generated content. |
| 2026-11-05 | Editor basics: undo/redo through a command system, selection, gizmos with ImGuizmo; node editing with imgui-node-editor for every node graph. |
| 2026-11-05 | Cinematics: an in-house sequencer timeline, displayed with ImSequencer. |
| 2026-11-05 | Serialization: one reflection-based serializer for scenes, save games and network replication. |
| 2026-11-05 | Crash reporting with Sentry Native (minidumps). Memory: allocation tracking per subsystem through our allocators and Tracy, leak detection at shutdown, dumps on crash. |
| 2026-11-05 | Visual effects: a node-based VFX system (Niagara-like) with GPU particles; volumetric fire and smoke as grid fluid simulation in compute shaders, with volumetric rendering also used for fog and clouds; a water system (ocean waves, rivers, lakes, reflections, refraction, caustics) and particle-based liquid simulation. Part of the fluids milestone. |
| 2026-11-05 | Destruction, like Chaos Destruction: Voronoi fracture prepared in the editor with several levels; at runtime pieces break off past damage thresholds and become Jolt bodies; debris lifetime, pooling and limits, with dust and sparks from particles. Free-form voxel destruction (Teardown-like) later. |
| 2026-11-05 | Motion capture from video: an AI plugin pipeline producing animation assets (pose detection with MediaPipe or an ONNX model, cleanup and foot locking, retargeting to the character skeleton, saved as a regular animation played by ozz), with its own editor tool. |
| 2026-11-08 | vcpkg is the `extern/vcpkg` git submodule, pinned to the `builtin-baseline` commit; the presets load its toolchain, which bootstraps vcpkg on the first configure. No system install, no `VCPKG_ROOT`. |
| 2026-11-08 | Version: `VERSION` in `project()` only, set by a release PR before each tag; pre-releases (`-alpha.N`, `-beta.N`, `-rc.N`) are carried by the tag. |
| 2026-11-08 | Tooling: LLVM 23 minimum for clang-format and clang-tidy. The C++ standard and the warning flags are set in CMake only; clang-format detects the standard, clangd reads `compile_commands.json`. |
| 2026-11-08 | Header comment of source and config files: organization copyright, SPDX identifier, optional doc link; no contributors list (authorship is in git). |
| 2026-11-08 | Labels: `scope:` (part of the repository), `agent:` and `model:` (who does the work); the Project's Area field stays the product. |
| 2026-11-09 | CI Linux jobs run on Ubuntu 26.04 runners (Clang 20+), needed for `std::expected`. |
| 2026-11-09 | Errors: engine code avoids exceptions, so a failure never stops the program: `Result<T>` / `Status` over `std::expected`, the standard APIs that do not throw, out-of-memory is fatal. Building without exceptions is decided after measurements (AetherEngine #32). |
| 2026-11-09 | Naming: kind prefixes (`E` enum, `I` interface, `T` template parameter, `k` constant, `b` boolean) and scope prefixes (`m_`, `s_`, `g_`), so a review reads right without an IDE; checked by clang-tidy (`docs/naming.md`). |
| 2026-11-09 | Memory: the allocator strategy (mimalloc or rpmalloc as global allocator, `std::pmr` frame arenas and pools, no separate container library by default) is chosen from Tracy measurements (AetherEngine #31, #34). |

## Open questions

Settled one at a time; each answer moves to *Decisions* and, if it changes
code, becomes an issue.

- **Plugin model** — the content module entry point, and how plugins
  register in shared and static modes. To settle at M1.
- **Stable C interface** — to be checked: actual cost, generator design,
  memory ownership rules across the boundary, and whether it is worth it
  before a first Rust plugin.
- **Visual scripting** — something more technical than Blueprints, for
  example nodes holding code blocks (Lua), like Houdini's code nodes. To think
  through later.

## Prototypes

Comparisons to run when the feature is implemented, before choosing:

- ECS: EnTT vs flecs.
- Lua binding: sol2 vs LuaBridge3.
- Jobs: enkiTS vs Taskflow.
- Reflection: the C++26 switch, with GCC 16.
- Behavior trees: BehaviorTree.CPP vs in-house on the node graph.

## Milestones

### AetherEngine

| Milestone | Goal | Done when |
| --- | --- | --- |
| **M0 · Foundations** | Repository settings, CMake + Ninja presets with Clang, vcpkg manifest, `core` with the logger, doctest, CI on Linux and Windows | The presets configure, build and run the tests, locally and in CI, in static and shared modes |
| **M1 · Engine skeleton** | `platform` (SDL3), main loop, loading of content modules, the `player` host, a minimal `render` clearing an offscreen image presented to the window, Tracy profiling | The player loads an empty content module and shows a cleared window, with no validation error, surviving a resize |
| **M2 · Editor shell** | Editor host with Dear ImGui docking, a viewport showing the offscreen image, a log console, the same content module loaded inside | The same content module runs in the player and in the editor viewport |
| **M3 · First triangle** | A "triangle" demo: graphics pipeline, Slang shaders compiled at build, frame synchronization | The triangle demo runs in both hosts, frames in flight, clean shutdown |
| **M4 · Audio basics** | miniaudio output, Steam Audio spatialization, the audio node graph with basic synth modules, as a demo | A demo plays a sound moving around the listener and a small synth patch, in both hosts |
| **M5 · Rendering basics** | Buffers, uniforms, textures, depth, camera, mesh loading, as demos; the allocator strategy and the no-exceptions measurement, on this first real workload | A textured model is drawn with a moving camera |
| **M6 · Ray tracing** | Ray tracing extensions, acceleration structures, ray tracing pipeline, as a demo | A scene is rendered with ray-traced shadows |

### .github

| Milestone | Goal | Done when |
| --- | --- | --- |
| **Visual identity** | Rework the look of the profile and the roadmap SVG: fonts, colors, layout. A font must be embedded in the SVG (base64 `@font-face`), since GitHub blocks external fonts in images | The profile page and the roadmap share one identity, reused later by the website |

### Later (not scheduled)

Advanced rendering in this order: path tracing, real-time global
illumination, GPU particles, fluids, virtualized geometry. Networking after
the ECS. Animation, input actions, localization, export and modding. Navigation and
behavior trees, large worlds, procedural terrain and placement, editor
basics, cinematics, save games, crash reporting and memory tracking, VFX and
water, destruction, motion capture from video.

ECS and plugins, Python automation, Lua scripting, physics, asset pipeline
and FBX/Assimp plugins, Pure Data and Faust synth modules, AI subsystem,
Neovim plugin then embedded panel, test projects, the game, website, MCP
tools.
