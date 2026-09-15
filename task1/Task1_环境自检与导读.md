# Task 1 环境准备与课前导读（9/15）

主笔记在仓库首页：[README.md](../README.md)。这一份是当时的详细记录，留着当底账。

## 环境自检

| 检查项 | 实测 | 判定 |
|---|---|---|
| Shell | zsh 5.9（/bin/zsh 默认） | 够用 |
| Python | 默认 `python3` 是 3.12.13（uv 管理），3.11.15 已装 | 课程要 3.11，必须显式指定 |
| venv / pip / uv | 建出 3.11.15 环境，pip 26.2.1，uv 0.11.11 | 通过 |
| Git | git 2.54.0，user.name / user.email 原本是空的 | 已补 |
| 网络 | github 直连 443 超时 75 秒，走本机代理 127.0.0.1:7897 成功 | 拉代码走代理，装包走镜像 |
| 模型 API | 环境变量里已有 OpenAI 兼容的中转 key | 通过 |
| 磁盘 | 可用 646 GB（仓库 clone 后占 309 MB） | 通过 |

## 执行记录

| 步骤 | 命令 | 结果 |
|---|---|---|
| clone | `git clone https://github.com/datawhalechina/easy-data-x-ai.git` | commit e5c4d076，落盘 309 MB |
| 建环境 | `uv venv --python 3.11 --seed .venv` | Python 3.11.15 |
| 装依赖 | `pip install -r code/requirements-test.txt` | langchain 1.4.0、langgraph 1.2.11、ragas 0.2.15、openai 3.14.0、pyseekdb 1.4.0 等 |
| 依赖体检 | `pip check` | No broken requirements found |
| 离线评测 | `PYTHONPATH=code/D3:code python code/D3/d3_5_evaluate.py` | 退出码 0，60 条案例，失败 0 |

## 离线评测产出

[`reports/offline-evaluation.md`](reports/offline-evaluation.md)：60 条案例、失败 0、Hit@1 = 0.92、Hit@3 = 1.0、MRR = 0.9533、上下文召回率 1.0、拒答准确率 1.0、平均检索调用 2.73。
六类用例通过率全为 1.0：alias_rewrite、boundary、exact_identifier、insufficient_evidence、multi_hop、semantic。

[`reports/strategy-comparison.md`](reports/strategy-comparison.md)：

| 方案 | Hit@1 | Hit@3 | MRR | 拒答准确率 | P50 / P95（ms） | 检索/生成调用 | 估算 Token |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 纯向量基线 | 0.72 | 0.76 | 0.7367 | 0.6 | 0.27 / 0.32 | 1 / 0.7 | 12651 |
| 混合检索 | 0.88 | 0.98 | 0.92 | 1.0 | 0.30 / 0.34 | 1 / 0.82 | 14691 |
| 工程管线 | 0.92 | 1.0 | 0.9533 | 1.0 | 0.53 / 0.81 | 2.73 / 0.83 | 15124 |

多花约一倍延迟、两成 Token，换来的是拒答准确率从 0.6 到 1.0、Hit@3 从 0.76 到 1.0。纯向量在证据充足的题上看不出毛病，差别全在证据不足时它敢不敢说"我答不了"。

## 踩坑与填坑

1. 默认 `python3` 是 3.12.13，课程要求 3.11，必须 `uv venv --python 3.11`，否则建出来的环境版本不对。
2. github 直连 443 超时，拉代码必须走本机代理；装包反过来要走国内镜像并绕开代理。
3. 本机存在别的 Python 环境变量，跑课程脚本前要 `env -u PYTHONPATH -u VIRTUAL_ENV` 清一遍，否则会串解释器。
4. Git 的 `user.name` / `user.email` 为空，提交前必须补。
5. 报告里的 Token 是字符长度推算值、延迟只含本地编排开销，不能当服务商账单。

## 导读

- 公共基础篇 F1《大模型的本质与边界》、F2《AI Agent 全景图》，所有人都要先看。
- 课程分「道篇 P1–P5（做判断）」与「术篇 D1–D5（动手写）」，另有产业篇 I 和扩展章 X。
- 记住的一句：不是所有需求都该做成 Agent。边界在数据层，不在模型层。

## 引用来源

- 教程仓库：https://github.com/datawhalechina/easy-data-x-ai
- 在线阅读：https://datawhalechina.github.io/easy-data-x-ai
- Task 安排：https://my.feishu.cn/wiki/HvQuwKiSEi0mNBkGzjBcJaldnrd
- 评测数据：教程仓库 `code/D3/reports/offline-evaluation.md`、`code/D3/reports/strategy-comparison.md`
- 环境与运行记录：本人 2026-09-15 在 macOS 上实测
