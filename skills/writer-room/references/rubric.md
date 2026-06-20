# Writer Room Script Rubric

Score each script on a 100-point scale.

| Dimension | Points | Criteria |
| --- | ---: | --- |
| Hook | 15 | First 5 seconds create a visible question, shock, danger, or emotional pull. |
| Motivation | 15 | The protagonist has a concrete reason to act now. |
| Conflict | 15 | Pressure escalates and retreat becomes costly. |
| Pacing | 15 | Beats are clear, short, and avoid filler. |
| Dialogue | 15 | Dialogue is speakable, subtextual, and not exposition-heavy. |
| Filmability | 20 | Actions, settings, props, and effects can be generated or shot with controlled resources. |
| Continuity | 5 | Character, prop, location, and emotional continuity are stable. |

## Decisions

- `pass`: total >= 85 and no severe continuity issue.
- `revise`: total 70-84 or fixable continuity issue.
- `reject`: total < 70, missing core premise, or unfilmable script.

## Rewrite Gate

Default to one automatic rewrite loop when:

- total score is below 85;
- `decision` is `revise`;
- any issue severity is `high`;
- the user explicitly requests another pass.

Do not run unlimited loops. If the rewrite loop still fails, return the best
script with a clear warning and next action.
