# Easy Data × AI 学习笔记

Datawhale 第 84 期，队「日拱一卒」，1 群。9/14 开营，29 天 9 个 Task。

笔记只此一份，每个 Task 追加一节，链接固定不变。

- 教程仓库：https://github.com/datawhalechina/easy-data-x-ai
- 在线阅读：https://datawhalechina.github.io/easy-data-x-ai

| Task | 内容 | 状态 | 日期 |
|---|---|---|---|
| Task 1 | 环境准备与课前导读 | 完成 | 9/15 |
| Task 2 | | | |
| Task 3 | | | |
| Task 4 | | | |
| Task 5 | | | |
| Task 6 | | | |
| Task 7 | | | |
| Task 8 | | | |
| Task 9 | | | |

---

## Task 1 环境准备与课前导读（9/15）

### 环境自检

| 检查项 | 实测 | 判定 |
|---|---|---|
| Shell | zsh 5.9，/bin/zsh 为默认 | 可用 |
| Python | 默认 `python3` 为 3.12.13，3.11.15 已安装但非默认 | 需显式指定 3.11 |
| venv / pip / uv | 建出 3.11.15 环境，pip 26.2.1，uv 0.11.11 | 可用 |
| Git | 2.54.0，user.name / user.email 为空 | 已补配置 |
| 网络 | github 直连 443 超时 75 秒，走本机代理 127.0.0.1:7897 成功 | 拉代码走代理 |
| 模型 API | 已有 OpenAI 兼容接口的中转 key | 可用 |
| 磁盘 | 可用 646 GB，仓库 clone 后占 309 MB | 充足 |

三处需要处理：

Python 版本不一致。本机默认 `python3` 是 3.12.13，课程要求 3.11。按文档直接执行 `python3 -m venv .venv` 会建出 3.12 环境，问题不会立刻暴露。正确做法是显式指定版本：`uv venv --python 3.11 --seed .venv`。

网络出口分两种情况。github 直连 443 端口超时，拉取代码必须走本机代理；安装依赖相反，走国内 PyPI 镜像并绕开代理更快。同一条网络，两个方向的处理方式不同，初次配置容易只记住其中一种。

Git 全局身份为空。不补 `user.name` 和 `user.email`，后续提交会直接失败，已配置。

### 运行记录

| 步骤 | 命令 | 结果 |
|---|---|---|
| clone | `git clone https://github.com/datawhalechina/easy-data-x-ai.git` | commit e5c4d076，落盘 309 MB |
| 建环境 | `uv venv --python 3.11 --seed .venv` | Python 3.11.15 |
| 装依赖 | `pip install -r code/requirements-test.txt` | langchain 1.4.0、langgraph 1.2.11、ragas 0.2.15、openai 3.14.0、pyseekdb 1.4.0 等 |
| 依赖体检 | `pip check` | No broken requirements found |
| 离线评测 | `PYTHONPATH=code/D3:code python code/D3/d3_5_evaluate.py` | 退出码 0，60 条案例，失败 0 |

离线评测不需要 API Key，因此无需等待模型额度即可验证整条链路。

### 离线评测结果

原始报告：[`task1/reports/offline-evaluation.md`](task1/reports/offline-evaluation.md)

60 条案例，失败 0。Hit@1 = 0.92，Hit@3 = 1.0，MRR = 0.9533，上下文召回率 1.0，拒答准确率 1.0。六类用例（alias_rewrite、boundary、exact_identifier、insufficient_evidence、multi_hop、semantic）通过率均为 1.0。

同一次运行还给出三种检索方案的对比：[`task1/reports/strategy-comparison.md`](task1/reports/strategy-comparison.md)

| 方案 | Hit@1 | Hit@3 | 拒答准确率 | P50 / P95（ms） | 估算 Token |
|---|---:|---:|---:|---:|---:|
| 纯向量基线 | 0.72 | 0.76 | 0.6 | 0.27 / 0.32 | 12651 |
| 混合检索 | 0.88 | 0.98 | 1.0 | 0.30 / 0.34 | 14691 |
| 工程管线 | 0.92 | 1.0 | 1.0 | 0.53 / 0.81 | 15124 |

命中率上三者差距有限，纯向量基线 Hit@3 也有 0.76。真正的差别在拒答准确率：纯向量基线 0.6，混合检索与工程管线均为 1.0，即十个证据不足的问题里，纯向量方案仍有四个会给出答案。代价是延迟约翻倍、Token 多两成。

报告的指标口径也需注意：Token 为字符长度推算值，延迟只含本地编排开销，均不等同于服务商账单。

### 踩坑

1. 默认 `python3` 是 3.12，课程要 3.11，必须 `uv venv --python 3.11`。
2. github 直连不通：拉代码走代理，装包走国内镜像并绕开代理。
3. 本机已有其他 Python 环境变量，运行课程脚本前需 `env -u PYTHONPATH -u VIRTUAL_ENV` 清理，否则会串到别的解释器。
4. Git 的 `user.name` / `user.email` 为空必须补，否则提交失败。
5. 报告中的 Token 与延迟口径有限，不能当作账单依据。

### 导读

F1《大模型的本质与边界》、F2《AI Agent 全景图》两篇公共基础已读。课程分「道篇」P1–P5（判断力）与「术篇」D1–D5（工程实现），另有产业篇与扩展章。

F1、F2 的结论可以直接对应到今天的评测数据：不是所有需求都该做成 Agent，边界在数据层而非模型层。指标的上限由数据决定，不由模型决定。

---

## 引用来源

- 教程仓库：https://github.com/datawhalechina/easy-data-x-ai
- 在线阅读：https://datawhalechina.github.io/easy-data-x-ai
- Task 安排：https://my.feishu.cn/wiki/HvQuwKiSEi0mNBkGzjBcJaldnrd
- 打卡表单：https://magicyang.feishu.cn/share/base/shrcnPJP4DBbYWnQrnUPrgRa7rf
- 评测数据：教程仓库 `code/D3/reports/offline-evaluation.md`、`code/D3/reports/strategy-comparison.md`
- 环境与运行记录：2026-09-15 于 macOS 实测
