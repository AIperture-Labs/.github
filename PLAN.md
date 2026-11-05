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

## Open questions

Settled one at a time; each answer moves to *Decisions* and, if it changes
code, becomes an issue.

- **Toolchain** — Clang everywhere (clang-cl on Windows), or GCC + MSVC?
- **Engine architecture** — module boundaries, ECS (custom, EnTT), plugin
  model.
- **Scripting runtimes** — how Python and Lua are embedded and installed
  (uv-managed Python as in legacy? Lua 5.4 or LuaJIT?).
- **Tooling** — tests (doctest?), CI (GitHub Actions), profiling (Tracy),
  logging.
- **Neovim integration** — what it means concretely (embedded editor, RPC,
  plugin).

## Milestones

### AetherEngine

| Milestone | Goal | Done when |
| --- | --- | --- |
| **M0 · Foundations** | Repository settings, CMake + Ninja skeleton, format/lint configs, one empty module with a test, CI | `cmake --preset` configures, builds and runs the tests, locally and in CI |
| **M1 · Vulkan bootstrap** | Window, instance with validation layers, device selection, swapchain, clear color | A window clears to a color with no validation error, and survives a resize |
| **M2 · First triangle** | Graphics pipeline, shaders compiled at build, frame synchronization | A triangle is drawn, frames in flight, clean shutdown |
| **M3 · Rendering basics** | Buffers, uniforms, textures, depth, camera, mesh loading | A textured model is drawn with a moving camera |
| **M4 · Ray tracing** | Ray tracing extensions, acceleration structures, ray tracing pipeline | A scene is rendered with ray-traced shadows |

### .github

| Milestone | Goal | Done when |
| --- | --- | --- |
| **Visual identity** | Rework the look of the profile and the roadmap SVG: fonts, colors, layout. A font must be embedded in the SVG (base64 `@font-face`), since GitHub blocks external fonts in images | The profile page and the roadmap share one identity, reused later by the website |

### Later (not scheduled)

Engine architecture and ECS, editor UI, Python automation, Lua scripting,
asset pipeline, Neovim integration, test projects, the game, website, MCP
tools.
