# tinycart

> 分享《How to trust agent in this repo：从零搭一条 verification 生产线》的演示 repo。
> Demo repo for the talk "How to trust agent in this repo": building a verification pipeline from zero.

一个只有几十行的购物车总价命令行工具：买满 3 件同一商品，该行打 9 折；支持优惠券 SAVE10 / VIP20。
代码里**故意埋了两个 bug**。每一级 verification 都会抓到上一级漏掉的东西，每一级对应一个 git tag。

技术栈：Python 3.12+、[uv](https://docs.astral.sh/uv/)、[ruff](https://docs.astral.sh/ruff/)、[ty](https://docs.astral.sh/ty/)（beta）、pytest、GitHub Actions。

## 每一级（tag）

| tag | 这一级加了什么 | `make verify` | `make drive` | 看点 |
|---|---|---|---|---|
| `L0` | 业务代码 + 2 个测试 | 还没有 | 还没有 | pytest 全绿，但两个 bug 都在 |
| `L1-red` | `make verify`（ruff + ty + pytest）+ CI | **FAIL**（ty） | 还没有 | ty 抓到未知券码时访问 `None.percent` |
| `L1` | 修掉 None | PASS | 还没有 | 绿了，但买 3 件还是 30.00 |
| `L2` | feature map + `scripts/drive.py` + verify skill | PASS | **FAIL** | 驱动真实 CLI，`bulk_at_3` 期望 27.00、实际 30.00 |
| `L3-red` | 先提交失败的测试 | **FAIL** | FAIL | RED 被证明 |
| `L3-green` | 修复：`>` → `>=` | PASS | OK | 一行修复，证据齐全 |
| `mistake-float` | agent 加 `--json` 时写了 `float(total)` | PASS | OK | 现有检查管不到，输出 `{"total": 27.0}` |
| `flywheel` | `tests/test_guards.py`：禁止 money 代码里出现 `float()` | PASS | OK | 新 check 在 `mistake-float` 的代码上 FAIL |

分支：`main` 停在 `L2` 之上（分享开始时的状态）；`fix/bulk-threshold` = L3（PR #1）；`feat/json-output` = 飞轮（PR #2）。

## 自己重放一遍

```bash
git clone https://github.com/QingYunA/tinycart && cd tinycart
uv sync

git checkout L0 && uv run pytest -q && uv run tinycart cart.json   # 2 passed，TOTAL 30.00（应为 27.00）
git checkout L1-red && ./scripts/verify.sh                          # ty: unresolved-attribute
git checkout L1 && ./scripts/verify.sh && uv run tinycart cart.json # VERIFY: PASS，但还是 30.00
git checkout L2 && uv run python scripts/drive.py                   # FAIL bulk_at_3，证据写进 evidence/
git checkout L3-red && ./scripts/verify.sh                          # 新测试 FAIL
git checkout L3-green && ./scripts/verify.sh && uv run python scripts/drive.py

# 飞轮：证明新 check 在旧代码上会红
git checkout flywheel
git checkout mistake-float -- src/ && uv run pytest -q tests/test_guards.py   # 1 failed
git checkout HEAD -- src/          && uv run pytest -q tests/test_guards.py   # 1 passed
```

有 `make` 的话，`make verify` / `make drive` 等价于上面的脚本。

## 文件地图

- `AGENTS.md`：给 agent 的 25 行指南：完成标准、地图、规则表（每条规则写明由哪个 check 管）
- `features/`：每个功能从用户视角怎么用、怎么驱动、有什么坑
- `scripts/verify.sh`：L1，本地和 CI 跑同一条命令；CI 里的 job 名 `verify` 就是 required check
- `scripts/drive.py` + `scripts/scenarios.json`：L2，调用真实安装的 `tinycart` 命令，证据写进 `evidence/`
- `.claude/skills/verify-tinycart/SKILL.md`：L2 verify skill（Launch / Doctor / Drive / Evidence / Cleanup）
- `tests/test_guards.py`：飞轮，带修复说明的报错信息

## 注意

- ty 是 beta（0.0.x），diagnostic 文案可能随版本变；版本锁在 `uv.lock`，CI 用 `uv sync --locked`。
- ruff 的 RUF001–003 会对中文全角标点报错，所以代码注释用英文。
- 这是演示 repo，bug 是故意的。
