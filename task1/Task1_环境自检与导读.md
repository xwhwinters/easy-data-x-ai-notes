# Task 1 环境准备与课前导读（9/15）

主笔记见仓库首页 [README.md](../README.md)。此份为原始记录，保留备查。

## 环境自检

| 检查项 | 实测 | 判定 |
|---|---|---|
| Shell | zsh 5.9，/bin/zsh 为默认 | 可用 |
| Python | 默认 `python3` 为 3.12.13（uv 管理），3.11.15 已安装 | 需显式指定 3.11 |
| venv / pip / uv | 建出 3.11.15 环境，pip 26.2.1，uv 0.11.11 | 可用 |
| Git | 2.54.0，user.name / user.email 为空 | 已补配置 |
| 网络 | github 直连 443 超时 75 秒，走 127.0.0.1:7897 代理成功 | 拉代码走代理 |
| 模型 API | 已有 OpenAI 兼容接口的中转 key | 可用 |
| 磁盘 | 可用 646 GB，仓库占 309 MB | 充足 |

## 运行记录

| 步骤 | 命令 | 结果 |
|---|---|---|
| clone | `git clone https://github.com/datawhalechina/easy-data-x-ai.git` | commit e5c4d076，309 MB |
| 建环境 | `uv venv --python 3.11 --seed .venv` | Python 3.11.15 |
| 装依赖 | `pip install -r code/requirements-test.txt` | langchain 1.4.0、langgraph 1.2.11、ragas 0.2.15、openai 3.14.0、pyseekdb 1.4.0 |
| 依赖体检 | `pip check` | No broken requirements found |
| 离线评测 | `PYTHONPATH=code/D3:code python code/D3/d3_5_evaluate.py` | 退出码 0，60 条案例，失败 0 |

## 评测产出

[`reports/offline-evaluation.md`](reports/offline-evaluation.md)：60 条案例，失败 0，Hit@1 = 0.92，Hit@3 = 1.0，MRR = 0.9533，上下文召回率 1.0，拒答准确率 1.0，平均检索调用 2.73。六类用例通过率均为 1.0。

[`reports/strategy-comparison.md`](reports/strategy-comparison.md)：

| 方案 | Hit@1 | Hit@3 | MRR | 拒答准确率 | P50 / P95（ms） | 检索/生成调用 | 估算 Token |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 纯向量基线 | 0.72 | 0.76 | 0.7367 | 0.6 | 0.27 / 0.32 | 1 / 0.7 | 12651 |
| 混合检索 | 0.88 | 0.98 | 0.92 | 1.0 | 0.30 / 0.34 | 1 / 0.82 | 14691 |
| 工程管线 | 0.92 | 1.0 | 0.9533 | 1.0 | 0.53 / 0.81 | 2.73 / 0.83 | 15124 |

命中率差距有限，差别集中在拒答准确率：纯向量基线 0.6，其余两者 1.0。代价为延迟约翻倍、Token 多两成。

## 踩坑

1. 默认 `python3` 为 3.12.13，课程要求 3.11，须 `uv venv --python 3.11`。
2. github 直连 443 超时：拉代码走代理，装包走国内镜像并绕开代理。
3. 本机存在其他 Python 环境变量，运行课程脚本前需 `env -u PYTHONPATH -u VIRTUAL_ENV` 清理。
4. Git 的 `user.name` / `user.email` 为空，提交前须补。
5. 报告中的 Token 为字符长度推算值、延迟仅含本地编排开销，不等同于服务商账单。

## 导读

- F1《大模型的本质与边界》、F2《AI Agent 全景图》，公共基础必读。
- 课程结构：「道篇」P1–P5 判断力，「术篇」D1–D5 工程实现，另有产业篇 I 与扩展章 X。
- 结论：不是所有需求都该做成 Agent，边界在数据层而非模型层。

## 引用来源

- 教程仓库：https://github.com/datawhalechina/easy-data-x-ai
- 在线阅读：https://datawhalechina.github.io/easy-data-x-ai
- Task 安排：https://my.feishu.cn/wiki/HvQuwKiSEi0mNBkGzjBcJaldnrd
- 评测数据：教程仓库 `code/D3/reports/offline-evaluation.md`、`code/D3/reports/strategy-comparison.md`
- 环境与运行记录：2026-09-15 于 macOS 实测
