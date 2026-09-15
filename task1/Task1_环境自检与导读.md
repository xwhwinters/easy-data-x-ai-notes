# Easy Data × AI 第84期 · Task1 环境自检与课前导读 V1.2

- 学习者：华子（队名：日拱一卒／1群）
- 打卡硬线：2026-09-17 03:00（即 9/16 白天必须交完）
- 打卡表单：https://magicyang.feishu.cn/share/base/shrcnPJP4DBbYWnQrnUPrgRa7rf
- 教程仓库：https://github.com/datawhalechina/easy-data-x-ai
- 在线阅读：https://datawhalechina.github.io/easy-data-x-ai
- 任务安排：https://my.feishu.cn/wiki/HvQuwKiSEi0mNBkGzjBcJaldnrd
- 本文所有环境结论与运行数据均为 2026-09-15 本机实测

## 一、环境自检结果（本机实测）

| 检查项 | 实测结果 | 判定 |
|---|---|---|
| Shell | zsh 5.9（/bin/zsh，默认）；bash 3.2 也在 | ✅ 够用 |
| Python | 默认 `python3` = 3.12.13（uv 管理）；3.11.15 已装 | ⚠️ 课程要求 3.11，必须显式指定 |
| venv / pip / uv | 已建 3.11.15 虚拟环境；pip 26.2.1；uv 0.11.11 | ✅ |
| Git | git 2.54.0；**user.name / user.email 为空** | ❌ 提交前必须补 |
| 网络 | 直连 github 443 超时 75s；本机 127.0.0.1:7897 代理在听，走代理成功 | ⚠️ 拉代码走代理，装包走清华镜像 |
| 模型 API | 环境变量已有 OpenAI 兼容中转 key（https://www.yuzhixiaolongxia.com/v1） | ✅ 可复用 |
| 课程官方算力 key | 未发现阿里云百炼 / 硅基流动 key | ⚠️ 可现领，或用中转站 |
| 磁盘 | 可用 646 GB（仓库 clone 后占 309 MB） | ✅ |

## 二、一条龙执行记录（全部实测通过）

| 步骤 | 命令 | 结果 |
|---|---|---|
| 1 clone | `git clone https://github.com/datawhalechina/easy-data-x-ai.git`（走 7897 代理） | ✅ commit e5c4d076，2117 objects，落盘 309 MB |
| 2 建 3.11 venv | `uv venv --python 3.11 --seed .venv` | ✅ Python 3.11.15 |
| 3 装依赖 | `.venv/bin/python -m pip install -r code/requirements-test.txt`（清华镜像） | ✅ langchain 1.4.0 / langgraph 1.2.11 / ragas 0.2.15 / openai 3.14.0 / pyseekdb 1.4.0 等 |
| 4 依赖体检 | `.venv/bin/python -m pip check` | ✅ No broken requirements found |
| 5 离线评测 | `PYTHONPATH=code/D3:code .venv/bin/python code/D3/d3_5_evaluate.py` | ✅ 退出码 0，60 条案例，失败 0，Hit@3 = 1.0，拒答准确率 1.0 |

### 离线评测真实产出（`code/D3/reports/`）

主报告 `offline-evaluation.md`：案例 60 / 失败 0 / Hit@1 = 0.92 / Hit@3 = 1.0 / MRR = 0.9533 / 上下文召回率 1.0 / 拒答准确率 1.0 / 检索调用均值 2.73。

六类用例通过率全为 1.0：alias_rewrite、boundary、exact_identifier、insufficient_evidence、multi_hop、semantic。

### 三种检索策略对比（`strategy-comparison.md`，这才是最值钱的一段）

| 方案 | Hit@1 | Hit@3 | MRR | 拒答准确率 | P50 / P95（ms） | 检索/生成调用 | 估算 Token |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 纯向量基线 | 0.72 | 0.76 | 0.7367 | 0.6 | 0.27 / 0.32 | 1 / 0.7 | 12651 |
| 混合检索 | 0.88 | 0.98 | 0.92 | 1.0 | 0.30 / 0.34 | 1 / 0.82 | 14691 |
| 工程管线 | 0.92 | 1.0 | 0.9533 | 1.0 | 0.53 / 0.81 | 2.73 / 0.83 | 15124 |

一句话结论：**多花的代价是延迟翻倍、Token 多两成，换来的是拒答准确率从 0.6 提到 1.0、Hit@3 从 0.76 提到 1.0。** 不构造不确定场景的时候，你根本看不出纯向量的差距——差距全在「答不了的时候敢不敢说答不了」。

### 关键踩坑（打卡里最值钱的部分）

1. **Python 版本陷阱**：默认 `python3` 是 3.12.13，课程要求 3.11，必须 `uv venv --python 3.11`。
2. **网络出口陷阱**：github 直连 443 超时，必须走本机代理；装包反而要走清华镜像、绕开代理。
3. **环境变量污染**：本机 Hermes 自带 venv 与 PYTHONPATH，跑课程脚本要 `env -u PYTHONPATH -u VIRTUAL_ENV` 清一遍，否则串解释器。
4. **Git 身份为空**：`user.name` / `user.email` 没填，后面交 PR 一定卡。
5. **离线报告不能当账单选**：报告里的 Token 是字符长度推算值，延迟只反映本地编排开销，真实数据库与模型延迟要另测。

## 三、Task1 学什么（2天）

课程稿都在本地 docs 里，可直接读：

| 篇 | 文件 |
|---|---|
| 公共基础 | `docs/base_knowledge/F0 课程稿：课前闲聊 —— OpenClaw 为什么越用越好用？.md`<br>`docs/base_knowledge/F1 课程稿：AI 必知必会（一） —— 大模型的本质与边界.md`<br>`docs/base_knowledge/F2 课程稿：AI 必知必会（二） —— AI Agent 全景图.md` |
| 课程导论 | `docs/course-intro.md` |
| 道篇起点 | `docs/pm/P1 课程稿：AI Agent 场景识别.md` |

- Day1（9/15）：环境自检 + clone + 3.11 venv + 跑通离线评测 ✅ 已完成
- Day2（9/16）：通读 F1/F2，翻一遍 P1 与 D1 目录建立地图，写打卡

常用命令：

```shell
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"
cd "/Users/niuniu/Documents/Codex workspace/Personal/Datawhale_easy-data-x-ai/easy-data-x-ai"
source .venv/bin/activate
PYTHONPATH=code/D3:code python code/D3/d3_5_evaluate.py      # 离线，不需要 key
cp code/.env.example code/.env                                # 要跑真实模型时再填
python code/D1/d1_1_base.py
```

## 四、打卡正文草稿（≥50字，非教程原文）

今天先把环境和课程地图理清楚，三件事：
一、环境自检过了 Shell、Python、Git，实测踩出几个坑——本机默认 python3 是 3.12，课程要求 3.11，必须专门指定 3.11 建虚拟环境；github 直连 443 超时，得走本机代理才能 clone，装包反而要走镜像绕开代理；Git 的 user.name / user.email 是空的，不补上后面没法提交。
二、模型 API 这块课程示例走 OpenAI 兼容接口，在 `code/.env` 填 base_url / api_key / model 就能跑，手上已有的中转站 key 可直接复用，不必等官方额度。
三、把不需要 Key 的离线评测跑通了：60 条案例、失败 0 条、Hit@3 = 1.0、拒答准确率 1.0。顺手看了三种检索策略的对比——纯向量基线 Hit@3 只有 0.76、拒答准确率 0.6，混合检索提到 0.98 / 1.0，工程管线 1.0 / 1.0，代价是延迟从 0.27ms 涨到 0.53ms、Token 多约 20%。最大的收获不是那几个小数，而是：不构造不确定场景，你根本看不出纯向量的差距——差距全在「答不了的时候敢不敢说答不了」。这和我做企业 IT 方案的判断一致：先把数据理顺，再谈智能。

## 五、打卡表单字段对照

| 字段 | 填什么 |
|---|---|
| 微信昵称 | 你自己的群昵称 |
| 队名 | 日拱一卒 |
| 所学课程 | Easy Data × AI |
| 群号 | 1群 |
| 任务名称 | task1 |
| 学习心得 | 上面第四部分，≥50字 |
| 课程评价 / 反馈 | 如实写，别写套话 |
| 笔记链接 | 公开可读链接（此为评优资格项） |
| 证书昵称 | 想印在证书上的名字 |

## 六、口径冲突提醒

公告写「打卡截止 9月17日03:00（周二晚上睡前）」，但 9/17 03:00 实为周三凌晨，「周二」与日期不符；组队截止写「周二（9月15日）中午11点」，9/15 才是周二。以硬日期 9/17 03:00 为准，倒推到 9/16 白天交完最稳。

## 七、引用来源

- 教程仓库：https://github.com/datawhalechina/easy-data-x-ai
- 在线阅读：https://datawhalechina.github.io/easy-data-x-ai
- Task 安排：https://my.feishu.cn/wiki/HvQuwKiSEi0mNBkGzjBcJaldnrd
- 打卡表单：https://magicyang.feishu.cn/share/base/shrcnPJP4DBbYWnQrnUPrgRa7rf
- 评测数据出处：本仓库 `code/D3/reports/offline-evaluation.md`、`code/D3/reports/strategy-comparison.md`
- 本机环境与执行记录：本文实测，2026-09-15
