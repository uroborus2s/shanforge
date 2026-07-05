# Review Response

用于对 review feedback 给出技术回应。

## Fixed

```markdown
Fixed. <简述改动>

Verified:
- <验证命令>：<真实结果>
```

## Verified

```markdown
Verified. <说明核实结果>

Evidence:
- <文件或测试>
```

## Pushback

```markdown
I checked <code/tests/context>. This suggestion would <technical impact>.
Current behavior is required because <reason>.
Recommended action: <keep current / alternative fix / ask user>.
```

## Needs clarification

```markdown
Need clarification before implementing:
- <specific unclear point>
```

## 验证命令

只写真实执行过的命令。未执行时写明原因。
