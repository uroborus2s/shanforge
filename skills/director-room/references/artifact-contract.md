# 导演分镜部 Artifact 契约

每个子 Codex 代理只返回一个结构化 envelope。父级 Codex 协调器检查 envelope 后，统一把文件写入项目目录。子代理不得自行改动共享文件，除非父级明确分配了互不重叠的写入范围。

## Envelope

```json
{
  "status": "success",
  "summary": "一句话说明本角色完成了什么。",
  "artifacts": [
    {
      "path": "{episode-id}/shots/shot-list.json",
      "kind": "json",
      "content": "{ \"shots\": [] }"
    }
  ],
  "next_actions": ["cinematographer-agent"],
  "warnings": [],
  "handoff": {
    "main_output": "{episode-id}/shots/shot-list.json",
    "assumptions": [],
    "quality_notes": [],
    "blocked_questions": []
  }
}
```

## 状态值

- `success`：产物已经可以交给下一个角色使用。
- `warning`：产物可用，但存在风险；父级协调器必须保留这些风险，不得在汇总时消除。
- `blocked`：当前角色缺少必要输入，无法继续；问题应交回父级协调器或用户。

## Artifact 规则

- 路径必须是项目相对路径。
- 导演阐述、摄影说明、分镜计划、低模导出计划和后期计划使用 Markdown。
- 场景拆解、分镜表、视觉连续性、生成策略、提示词草稿、ComfyUI 提示词、工作流计划、渲染登记和质检结果使用 JSON。
- 子代理输出不得包含绝对路径；父级协调器负责解析实际项目根。
- artifact 内容必须完整到可以直接写入文件。
- 不得重写或复述源剧本、角色圣经、场景圣经；只有下游产物需要引用依据时，才写短引用或 `source_refs`。
- 若产物涉及场景控制包，必须写明它是计划、占位、已生成文件，还是等待 Blender/Unreal/ComfyUI 导出的依赖。

## 必需交接字段

- `main_output`：一个项目相对路径。
- `assumptions`：本角色作出的具体假设。
- `quality_notes`：本角色发现的风险、取舍或优势。
- `blocked_questions`：仅在 `status` 为 `blocked` 时填写。
