---
description: "ECC-integrated Plan: Restate requirements, assess risks, and create step-by-step implementation plan. WAIT for user CONFIRM before touching any code."
argument-hint: "[feature description | path/to/*.prd.md]"
source: ecc/commands/plan.md
---

# Plan Command (ECC Edition)

This command creates a comprehensive implementation plan before writing any code using ECC patterns and methodologies.

**Quick Start**: Run `/plan` with requirements or a PRD file to get a structured implementation plan.

## What This Command Does

1. **Restate Requirements** - Clarify what needs to be built
2. **Identify Risks** - Surface potential issues and blockers
3. **Create Step Plan** - Break down implementation into phases
4. **Ground in ECC Patterns** - Align with ECC conventions (skills, hooks, rules)
5. **Wait for Confirmation** - MUST receive user approval before proceeding

## How to Use

### Input Modes

| Input | Mode | Behavior |
|---|---|---|
| `/plan feature description` | Conversational | Produce inline plan |
| `/plan path/to/name.prd.md` | PRD artifact | Read PRD and generate `.claude/plans/{name}.plan.md` |
| `/plan path/to/reference.md` | Reference | Read file as context and produce inline plan |
| `/plan` | Clarification | Ask what should be planned |

### Example Commands

```bash
# Plan a new feature
/plan Add multi-language support for dashboard notifications

# Plan from a PRD
/plan docs/features/notification-system.prd.md

# Plan from reference documentation
/plan repo-trend-tracker/requirements.md
```

## Plan Structure

The assistant will:

1. **Analyze the request** and restate requirements clearly
2. **Ground in ECC patterns** from the ecc dependency:
   - Skills: How to structure reusable components
   - Hooks: Integration points in workflows
   - Rules: Validation and constraints
   - Commands: Available tools and conventions
3. **Break down into phases** with specific, actionable steps
4. **Identify dependencies** between components
5. **Assess risks** and potential blockers
6. **Present the plan** and WAIT for your explicit confirmation

## Pattern Grounding

Plans should capture relevant ECC patterns:

| Category | Source | What to Look For |
|---|---|---|
| Skills Architecture | `ecc/skills/` | Skill structure, exports, validation |
| Hooks Integration | `ecc/hooks/` | Workflow hooks, event patterns |
| Rules & Validation | `ecc/rules/` | Rule structure, constraint patterns |
| Command Conventions | `ecc/commands/` | Command metadata, argument handling |
| MCP Patterns | `ecc/mcp-configs/` | MCP server patterns and configurations |

## Acceptance Criteria Template

After planning, you will see:

```markdown
# Plan: {Feature Name}

## Requirements Restatement
{Clear restatement of what needs to be done}

## Implementation Phases
### Phase 1: {name}
- {step}
- {step}

### Phase 2: {name}
- {step}

## ECC Patterns to Mirror
| Pattern | Source | Application |
|---|---|---|
| {pattern} | `ecc/path:line` | How we'll apply it |

## Dependencies
- {dependency}
- {dependency}

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|

## Acceptance Criteria
- [ ] All phases complete
- [ ] Tests pass
- [ ] ECC patterns mirrored consistently

**STATUS: AWAITING YOUR APPROVAL**
Confirm with: "yes", "proceed", "approved" - or request modifications
```

## After Approval

Once you confirm the plan:

1. Use `/tdd` to implement with test-driven development
2. Use `/diff-review` for read-only diff inspection
3. Use `/verify` for final validation checks
4. Use `/pr` to create a pull request with ECC compliance notes

## Integration with Other Commands

- **`/tdd`**: Implement the plan using test-driven development
- **`/diff-review`**: Review the diff against the accepted plan
- **`/verify`**: Run validation and acceptance checks
- **`/pr`**: Create a PR with plan reference

## Important Notes

⚠️ **CRITICAL**: This command will **NOT** write any code until you explicitly confirm the plan.

If you want changes to the plan:
- Reply with "modify: [your changes]"
- Or "different approach: [alternative]"
- Or "skip phase 2 and do phase 3 first"

## Reference

This is the ECC-integrated version of `/plan`. It mirrors patterns from the full ECC runtime at https://github.com/affaan-m/ecc but specialized for this repository's scope and workflow.

For more on ECC methodologies: See the project's [`ecc-how-to-use.md`](../ecc-how-to-use.md)
