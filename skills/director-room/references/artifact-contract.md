# 导演部门 Artifact 契约

每个员工子任务返回一个结构化 envelope。主协调代理检查、评分并写入文件。员工不得自行修改共享文件，除非主协调代理明确分配互不重叠的写入集合。

## Envelope

```json
{
  "status": "success",
  "summary": "一句话说明本员工完成了什么。",
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

- `success`：产物可进入评审。
- `warning`：产物可评审，但存在风险；主协调代理必须保留风险并纳入评分。
- `blocked`：缺少必需输入、工具、配置或事实，员工无法继续。

## Artifact 规则

- 路径必须是项目相对路径。
- Markdown 用于导演阐述、摄影说明、分镜计划、低模导出计划、音频/后期计划和交接说明。
- JSON 用于场景拆解、分镜表、视觉连续性、生成策略、提示词、工作流计划、渲染登记、评分记录和资源索引。
- 员工输出不得包含绝对路径；主协调代理负责解析实际项目根。
- artifact 内容必须完整到可以直接写入文件。
- 不得重写源剧本、角色设定、场景设定、连续性报告或评分报告。
- 若产物涉及场景图片资源或控制图，必须说明其状态：`ready`、`planned`、`needs_config`、`missing_asset` 或 `blocked`。

## 必需交接字段

- `main_output`：一个项目相对路径。
- `assumptions`：本员工做出的具体假设。
- `quality_notes`：本员工发现的风险、取舍或优势。
- `blocked_questions`：仅在 `status` 为 `blocked` 时填写；缺少固定必需输入时不要提问，直接报错。

## 评审 envelope

主协调代理对每个员工产物生成评审记录：

```json
{
  "agent": "shot-planner-agent",
  "attempt": 2,
  "status": "passed",
  "score": 91,
  "threshold": 90,
  "checks": [
    {"name": "schema", "status": "passed"},
    {"name": "source_refs", "status": "passed"}
  ],
  "revision_request": [],
  "reviewer_notes": []
}
```

评分未达标时，`status` 为 `needs_revision`，`revision_request` 必须足够具体，便于同一员工返工。
