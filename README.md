# Easy Data × AI 学习笔记（第84期 · 日拱一卒）

> 滚动笔记：每个 Task 一节，就这一个链接，从 Task1 用到 Task9。
> 学习者：华子 ｜ 群：1群 ｜ 队：日拱一卒 ｜ 周期：2026-09-14 起 29 天 / 9 个 Task
> 课程：Datawhale 第84期《Easy Data × AI》
> 教程仓库：https://github.com/datawhalechina/easy-data-x-ai ｜ 在线阅读：https://datawhalechina.github.io/easy-data-x-ai

## 进度总表

| Task | 内容 | 状态 | 完成日期 |
|---|---|---|---|
| Task 1 | 环境准备与课前导读 | ✅ | 2026-09-15 |
| Task 2 | — | ⏳ | |
| Task 3 | — | ⏳ | |
| Task 4 | — | ⏳ | |
| Task 5 | — | ⏳ | |
| Task 6 | — | ⏳ | |
| Task 7 | — | ⏳ | |
| Task 8 | — | ⏳ | |
| Task 9 | — | ⏳ | |

---

## Task 1：环境准备与课前导读（2026-09-15）

详细记录：[task1/Task1_环境自检与导读.md](task1/Task1_环境自检与导读.md)

### 1. 环境自检

| 检查项 | 实测结果 | 判定 |
|---|---|---|
| Shell | zsh 5.9（/bin/zsh 默认） | ✅ |
| Python | 默认 `python3` = 3.12.13；3.11.15 已装（uv 管理） | ⚠️ 课程要求 3.11，须显式指定 |
| venv / pip / uv | 已建 3.11.15 虚拟环境；pip 26.2.1；uv 0.11.11 | ✅ |
| Git | git 2.54.0；身份原先为空，已补 | ✅ |
| 网络 | github 直连 443 超时，走本机代理 127.0.0.1:7897 成功 | ⚠️ 拉代码走代理，装包走镜像 |
| 模型 API | OpenAI 兼容中转 key 可用 | ✅ |
| 磁盘 | 可用 646 GB | ✅ |

### 2. 一条龙执行记录

| 步骤 | 命令 | 结果 |
|---|---|---|
| clone | `git clone https://github.com/datawhalechina/easy-data-x-ai.git` | ✅ commit e5c4d076，落盘 309 MB |
| 建环境 | `uv venv --python 3.11 --seed .venv` | ✅ Python 3.11.15 |
| 装依赖 | `pip install -r code/requirements-test.txt` | ✅ langchain 1.4.0 / langgraph 1.2.11 / ragas 0.2.15 / pyseekdb 1.4.0 等 |
| 体检 | `pip check` | ✅ No broken requirements found |
| 离线评测 | `PYTHONPATH=code/D3:code python code/D3/d3_5_evaluate.py` | ✅ 退出码 0，60 条案例，失败 0 |

### 3. 离线评测真实数据

原始报告：[`task1/reports/offline-evaluation.md`](task1/reports/offline-evaluation.md)

案例 60 / 失败 0 / Hit@1 = 0.92 / Hit@3 = 1.0 / MRR = 0.9533 / 上下文召回率 1.0 / 拒答准确率 1.0 / 平均检索调用 2.73。
六类用例通过率全 1.0：alias_rewrite、boundary、exact_identifier、insufficient_evidence、multi_hop、semantic。

### 三种检索策略对比

原始报告：[`task1/reports/strategy-comparison.md`](task1/reports/strategy-comparison.md)

| 方案 | Hit@1 | Hit@3 | MRR | 拒答准确率 | P50 / P95（ms） | 检索/生成调用 | 估算 Token |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 纯向量基线 | 0.72 | 0.76 | 0.7367 | 0.6 | 0.27 / 0.32 | 1 / 0.7 | 12651 |
| 混合检索 | 0.88 | 0.98 | 0.92 | 1.0 | 0.30 / 0.34 | 1 / 0.82 | 14691 |
| 工程管线 | 0.92 | 1.0 | 0.9533 | 1.0 | 0.53 / 0.81 | 2.73 / 0.83 | 15124 |

**结论：多花约一倍延迟、两成 Token，换来拒答准确率 0.6 → 1.0、Hit@3 0.76 → 1.0。**
不构造不确定场景，看不出纯向量基线的差距——差距全在「答不了的时候敢不敢说答不了」。

### 4. 踩坑与填坑

1. **Python 版本**：默认 3.12.13，课程要 3.11，必须 `uv venv --python 3.11`，否则埋雷。
2. **网络出口**：github 直连 443 超时 75s，走本机代理才通；装包反过来要用国内镜像、绕开代理。
3. **环境变量污染**：本机 Hermes 自带 venv 与 PYTHONPATH，跑课程脚本要 `env -u PYTHONPATH -u VIRTUAL_ENV` 清一遍。
4. **Git 身份为空**：`user.name` / `user.email` 未配置，提交前必须补。
5. **报告口径**：报告里的 Token 是字符长度推算值、延迟只含本地编排开销，不能当服务商账单。

### 5. 课前导读笔记

- 公共基础篇 F1《大模型的本质与边界》、F2《AI Agent 的全景图》——所有人都要先看。
- 课程分「道篇（P1–P5，产品/决策视角）」与「术篇（D1–D5，开发者视角）」，另有产业篇 I 与扩展章 X。
- 一句话收获：**不是所有需求都该做成 Agent**——边界在数据层，不在模型层。先把数据理顺，再谈智能。

---

## Task 2（待填）

## Task 3（待填）

## Task 4（待填）

## Task 5（待填）

## Task 6（待填）

## Task 7（待填）

## Task 8（待填）

## Task 9（待填）

---

## 引用来源

- 教程仓库：https://github.com/datawhalechina/easy-data-x-ai
- 在线阅读：https://datawhalechina.github.io/easy-data-x-ai
- Task 安排：https://my.feishu.cn/wiki/HvQuwKiSEi0mNBkGzjBcJaldnrd
- 打卡表单：https://magicyang.feishu.cn/share/base/shrcnPJP4DBbYWnQrnUPrgRa7rf
- 评测数据出处：教程仓库 `code/D3/reports/offline-evaluation.md`、`code/D3/reports/strategy-comparison.md`
- 本机环境与运行记录：本人 2026-09-15 实测
