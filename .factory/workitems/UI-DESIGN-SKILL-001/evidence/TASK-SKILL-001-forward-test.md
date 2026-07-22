# TASK-SKILL-001 Forward Test

- Work item: `UI-DESIGN-SKILL-001`
- Task: `TASK-SKILL-001`
- Date: `2026-07-22`
- Method: three isolated read-only subagents, each starting without the implementer conversation and using only the rebuilt skill files.

## Scenarios

### Web + WeChat mini program

The reviewer designed a coffee membership journey for responsive Web and WeChat mini program. The output included shared information architecture, page/state matrices, shared tokens, platform mappings, permissions, weak-network and long-copy states, motion/reduced-motion rules, and acceptance checks.

Finding: the first result mechanically described `44 CSS px` as approximately `88rpx`. The skill was tightened to prohibit treating a fixed `88rpx` conversion as a universal mini-program rule and to require host logical-size plus real-device hit-area validation.

### iOS/iPadOS + Android

The reviewer designed a medication reminder flow using a common semantic state model and explicit platform forks. It covered notification permission timing, phone/tablet/foldable layouts, Dynamic Type/TalkBack/VoiceOver, predictive back, gesture interruption, reduced motion, handoff fields, and verification limits.

Result: no blocking coverage gap found.

### Windows/macOS/Linux desktop + motion

The reviewer designed an Avalonia video annotation client. It covered windows, commands, keyboard and drag input, shortcuts, multi-display and DPI behavior, platform-specific conventions, component states, animation budgets, reduced motion, and desktop verification. It also rejected a visually attractive database style that conflicted with the product task.

Result: no blocking coverage gap found.

## Cross-scenario finding

All three agents produced useful deliverables but did not consistently end with the exact `status / outputs / evidence / verification / needs` envelope. The main skill now requires those five fields as a separate final block, with `none` for empty fields and reasons for unexecuted checks.

## Outcome

- Coverage: Web, mini program, iOS/iPadOS, Android, Windows/macOS/Linux, cross-platform motion.
- Critical findings: 0
- Important findings fixed: 2
- Remaining known limitation: generated design proposals still require target-platform browser, simulator, or real-device verification before claiming implementation quality.
