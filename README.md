# Easy Data × AI 学习笔记

Datawhale 第 84 期，队「日拱一卒」，1 群。9/14 开营，29 天 9 个 Task。

笔记只此一份，每个 Task 追加一节，链接固定不变。

- 教程仓库：https://github.com/datawhalechina/easy-data-x-ai
- 在线阅读：https://datawhalechina.github.io/easy-data-x-ai

| Task | 内容 | 状态 | 日期 |
|---|---|---|---|
| Task 1 | 环境准备与课前导读 | 完成 | 9/15 |
| Task 2 | P1 场景识别 / D1 大模型 API 入门 / I1 AI 原生数据系统 | 完成（逾期补交） | 9/21 |
| Task 3 | P2 RAG 产品设计 / I2 向量数据库与 RAG | 完成（提前 1 天） | 9/21 |
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

## Task 2 P1 场景识别 / D1 大模型 API 入门（9/21）

任务窗口是 9/17–9/19，截止 9/20 03:00。我这两天在赶另一条业务线，没对照任务表确认日期，9/21 才补做。后面几个 Task 按硬日期提前一天交。

### 任务要求

1. 获取用于测试的 API Key
2. 安装 pyseekdb SDK
3. 跑通 `code/D1` 的 `d1_1` ~ `d1_6`，体验从大模型基础调用到「推理 → 行动 → 观察」多轮循环的演进

### API Key 与模型

本机没有 SiliconFlow 和 DashScope 的账号。可用的是两类 OpenAI 兼容接口：DeepSeek 官方接口，以及一个中转站。中转站的 `/v1/models` 只提供 GPT 系列，试调用返回 upstream error，不能作为测试底座，最终选 DeepSeek 官方接口。

示例代码从 `code/.env` 读配置，写入下面四项（文件权限 600）：

```
SILICONFLOW_API_KEY=<DeepSeek API Key>
SILICONFLOW_BASE_URL=https://api.deepseek.com/v1
DASHSCOPE_API_KEY=<同上>
DASHSCOPE_BASE_URL=https://api.deepseek.com/v1
```

示例里写死的模型名本机调不到：`d1_1`~`d1_5` 用 SiliconFlow 的 `tencent/Hunyuan-MT-7B`，`d1_6` 用 DashScope 的 `qwen-plus`，直接运行会拿到 400（`The supported API model names are ...`）。示例代码一行未改，用一个运行器在运行时替换模型名：

- 走模块常量 `MODEL_NAME` 的（`d1_1`~`d1_3`、`d1_5`、`d1_6`）：覆盖模块属性；
- `d1_4` 把模型名写在 `main` 函数里：改为传一个 wrapper 作为 `model_factory`。

运行器与命令见 [`task2/d1_runner.py`](task2/d1_runner.py)：

```bash
env -u PYTHONPATH -u VIRTUAL_ENV NO_PROXY='*' SEEKDB_MODE=embedded \
  PYTHONPATH=code/D1:code .venv/bin/python task2/d1_runner.py d1_1_base
```

### pyseekdb

已随 `requirements-test.txt` 装好，版本 1.4.0.post1。本机 `pylibseekdb` 可加载，走 Embedded 模式，不用 Docker 起 Server，少一层依赖。

第一次运行 `d1_5`/`d1_6` 失败，报 `Failed to download model from Hugging Face`。原因是 pyseekdb 的默认嵌入函数用 onnx 版 `all-MiniLM-L6-v2`，首次调用时才去下载，六个文件没有下全。从 hf-mirror 手动补齐到 `~/.cache/pyseekdb/onnx_models/all-MiniLM-L6-v2/onnx/` 后正常——目录完整时 pyseekdb 不再联网。

### 运行记录

| 示例 | 演示内容 | 退出码 | 日志 |
|---|---|---|---|
| `d1_1_base` | 一次基础调用 | 0 | [log](task2/logs/d1_1_base.log) |
| `d1_2_multi_turn` | 多轮对话，带上下文 | 0 | [log](task2/logs/d1_2_multi_turn.log) |
| `d1_3_streaming` | 流式输出 | 0 | [log](task2/logs/d1_3_streaming.log) |
| `d1_4_tool_use_mock` | 工具调用，知识库是本地假数据 | 0 | [log](task2/logs/d1_4_tool_use_mock.log) |
| `d1_5_tool_use_seekdb` | 工具调用，背后接真实的 seekdb | 0 | [log](task2/logs/d1_5_tool_use_seekdb.log) |
| `d1_6_agent` | `create_agent` 搭出的完整 Agent | 0 | [log](task2/logs/d1_6_agent.log) |

### 真实输出

`d1_4`：模型决定调用 `query_knowledge_base`，参数 `seekdb 支持哪些检索方式？混合检索是怎么实现的？`，拿到两条知识库文本，最后在回答里明确写出「知识库中没有检索到混合检索的具体实现」。工具调用链路通了，同时能看出模型有事实锚点时的分寸——它没有编。

`d1_5`：两次调用 `search_seekdb`，参数分别是 `{'query': 'seekdb 支持哪些检索方式 向量检索 全文检索'}` 和 `{'query': 'seekdb 混合检索 hybrid search 实现'}`；每次返回三条文档，最终回答落到 RRF（倒数排名融合）。与 `d1_4` 的差别在于工具背后真的连着一个向量库。

`d1_6`：3 个问题，8 次工具调用，8 次观察。第一个问题问 Agentic RAG 与传统 RAG 的区别，Agent 连着检索两次（换角度再查一遍），然后给出「传统 RAG 是每次都查、只查一次；Agentic RAG 是按需查、可反复查」。这就是 F2 讲的「感知 → 推理 → 行动」循环，也解释了为什么把 Agent 放在 D1 的最后一个示例。

一句关于模型选型的补充：`Hunyuan-MT-7B` 本身是翻译模型，`d1_1` 问它「什么是 RAG」它照样答对了。课程示例的模型选型不必照抄，链路和边界才是重点；换成 `deepseek-chat` 后六个示例的输出都可用。

### 踩坑

1. 模型名有两处硬编码：模块常量 `MODEL_NAME`（`d1_1`~`d1_3`、`d1_5`、`d1_6`）和 `main` 函数内部（`d1_4`）。只覆盖常量对 `d1_4` 无效。
2. 缺 `code/.env` 时，示例在创建模型之前就停下（`require_api_key` 做的边界校验），不产生任何外部调用。这个设计值得自己写代码时借鉴。
3. onnx 嵌入模型是首次调用时才下载，失败提示只写「检查网络」，看代码才知道实际是下载中断、目录不完整。报错文案和真实原因差一层。
4. 本机代理 7897 当时不可用，hf-mirror 直连反而通（`NO_PROXY='*'`），与拉 GitHub 代码的结论相反。

### P1 阅读笔记

一句话判断：90% 的 AI 功能失败不是模型不行，而是立项时没人问一句「数据在哪」。

- 能力上限 = 数据质量 × 模型能力 + 流程编排。
- 三个维度：数据可得性（地基，最容易被低估，也最容易在立项阶段验证）、任务可定义性（LLM 是概率生成，「怎么算做对」比传统软件复杂，关键看有没有事实锚点）、流程编排（Agent 与 Workflow 是一个光谱，第一个 AI 项目优先 Workflow）。
- Agent 的三个甜区：意图模糊需要语义理解、需要调用外部工具、需要持续交互。命中两个以上才值得考虑。
- 不该上 Agent 的三类：固定答案的 FAQ、结构化数据查询、对准确性零容忍的计算。用 Agent 做这三件事是过度工程化，代价不只是浪费开发资源，还比原方案更慢、更贵、更容易出错。

### 用 Checklist 评估手上的一个需求

我手上有一个门店类业务，一线最常问的是流程和标准（怎么报单、提成怎么算、活动怎么执行），新人反复问同一批问题。用 P1 的 Checklist 过了一遍：

| 维度 | 判断 |
|---|---|
| 场景匹配 | 意图不精确、答案散在多个文档和群聊记录里、同一批问题反复被问 —— 命中，值得考虑 |
| 数据可得性 | 部分存在。SOP 有文档，但版本多、散落在几处，最近一次统一整理是几个月前。10 个典型问题的答案数据核对还没做完，先按「部分存在」计 |
| 任务可定义性 | 有事实锚点（答案就是文档里的某一段，可以回读原文对照），能定义 |
| 流程编排 | 选 Workflow。第一版只做「检索 → 回答 → 人工可确认」，不做全自主 Agent。答错政策条款的代价不能接受 |

结论：先投数据层——把散在各处的 SOP 收敛成一份有版本号、可检索的文档，再谈 Agent。这跟 P1 的判断一致：数据可得性是立项阶段最容易验证的一维，半天就能查完，能省下几个月的弯路。

---

## Task 3 P2 RAG 产品设计 / I2 向量数据库与 RAG（9/21）

截止 09-23 03:00，提前一天半做完。

### 任务要求

1. 了解 RAG 的基础流程，以及向量数据库中混合搜索的含义
2. 预习并跑通 `code/D2` 的 `d2_1` 到 `d2_2`

### 运行记录

| 示例 | 内容 | 退出码 | 日志 |
|---|---|---|---|
| `d2_1_ingest` | 8 条原始文档切分后写入 seekdb | 0 | [log](task3/logs/d2_1_ingest.log) |
| `d2_2_vector_search` | 语义检索 + 精确编号检索 | 0 | [log](task3/logs/d2_2_vector_search.log) |

### 第一次跑 d2_2 返回 0 条

`d2_1` 正常：8 条文档、8 个片段、8 条入库。接着跑 `d2_2`，两路检索都是「（无结果）」，脚本自己判定「不能断言语义检索成功」。数据明明在库里，`get()` 能读回全部原文和 metadata，`count()` 也是 8，查询却一条不返。

排查顺序：

1. 换 `query_embeddings` 自己传 384 维向量 → 还是 0 条。
2. 换 `QueryHint(vector_index=False)` 关掉向量索引提示 → 还是 0 条。
3. 做最小复现（[`task3/d2_minimal_repro.py`](task3/d2_minimal_repro.py)）：全新 embedded 库，建集合、写 3 条、直接查 → **依然 0 条**。到这一步可以断定与课程代码无关，是本机 pyseekdb 1.4.0.post1 embedded 模式下向量查询的问题。
4. 看 `code/D2/seekdb/log/seekdb.log`：查询期出现 `check_table_exist_or_not ... table not exist(..., table_name=c$v1$d2_knowledge_base, ret=-5019)`，同时能看到 HNSW 参数里 `sync_mode_async:true, sync_interval_value:10`。
5. 查 `Collection` 的接口，发现 `has_vector_index` 属性为 **False**，并有 `refresh_index()` 方法。定位到根因：**集合建出来了、数据写进去了，但向量索引没有真正建起来；而查询语句带 `APPROXIMATE`，没有索引就查不出东西。**

修复：在写入之后补一步 `collection.refresh_index()`（[`task3/d2_refresh_index.py`](task3/d2_refresh_index.py)）。这个动作对课程代码零侵入，索引建好后 `d2_2` 立刻正常。

```
集合: d2_knowledge_base | 条数: 8 | 建索引前 has_vector_index: False
建索引前查询结果数: 0
refresh_index() 已执行 | 建索引后查询结果数: 3
```

（`has_vector_index` 在 refresh 之后仍显示 False，实际检索已可用，属性刷新时机与索引状态不完全同步，属于库自身的行为。）

课程 README 里写了 macOS 没有匹配的原生扩展时应改走 Server 模式，本来想按那条路再验一遍；本机 Docker Desktop 的 daemon 起不来（只有 `com.docker.vmnetd` 在跑，`docker.sock` 不存在），这一步留作待办，走的是 embedded + `refresh_index()` 这条。

### 修复后的真实输出

**语义检索**，问「怎么设计用户权限」，返回 3 条，分数 0.4674 / 0.5577 / 0.5729，内容分别是连接池配置、数据备份、查询性能优化，**没有一条命中知识库里的 RBAC 访问控制文档**——脚本自己也打了 ⚠️。

**精确编号检索**，问「错误码 E-4012 的解决方案」，第一名恰好是 E-4012，分数 0.2061。

这两条结果放在一起，正好是这节课要讲的东西：纯向量检索会漏语义（问「用户权限」没召回 RBAC 那条），也能在精确编号上偶然命中，但名次不保证。要稳定，就得混合搜索——向量、全文、标量过滤一起上。这就是 P2 第四部分说的三层作用。

### P2 阅读笔记

- RAG 基础流程六步：数据准备 → 改写与路由 → 搜索召回 → 融合与重排 → 上下文组织与生成 → 评估与反馈闭环。
- 传统 RAG 是无环流程，可以很复杂，但流程是写死的；Agentic RAG 的关键不是更复杂，而是有了**循环**——能判断要不要搜、够不够、换不换角度再搜一次。D1 的 `d1_6` 里那个连着检索两次的 Agent，就是这条的实证。
- 混合搜索：同时支持向量语义搜索、关键词全文搜索、标量过滤，把复杂度内置到数据库层。它的价值不只是「搜得更准一点」，而是决定 RAG 能不能自然演进成可编排、可评估的系统。
- 三层归因框架：数据层（检索不到 / 检索到了错的）、模型层（幻觉）、业务层（答案对但不合场景）。实践里 60%~80% 的问题在数据层，模型幻觉只占 10%~20%。PM 最常见的误诊是「换个更好的模型」。
- 要留下的印象：用户说「AI 答得不好」，第一反应不该是换模型，而是先问 R 做对了吗、数据准备对了吗、检索路径对了吗。

### 课后行动（初步）

拿归因决策树看手上的门店业务问答：一线问「提成怎么算」答错时，先查知识库里有没有正确答案——现在是散落的旧版本，属数据层·内容覆盖；再看检索路径——现在基本靠关键词命中，属数据层·检索策略；最后才轮到模型。结论和 Task 2 那次评估一致：先收数据，再谈检索策略，模型层排最后。

---

## 引用来源

- 教程仓库：https://github.com/datawhalechina/easy-data-x-ai
- 在线阅读：https://datawhalechina.github.io/easy-data-x-ai
- Task 安排：https://my.feishu.cn/wiki/HvQuwKiSEi0mNBkGzjBcJaldnrd
- 打卡表单：https://magicyang.feishu.cn/share/base/shrcnPJP4DBbYWnQrnUPrgRa7rf
- 评测数据：教程仓库 `code/D3/reports/offline-evaluation.md`、`code/D3/reports/strategy-comparison.md`
- 运行日志：本仓库 `task2/logs/*.log`、`task3/logs/*.log`（2026-09-21 实跑）
- 课程稿：`docs/pm/P1 课程稿：AI Agent 场景识别.md`、`docs/dev/D1 课程稿：大模型 API 工程化基础.md`
- 环境与运行记录：2026-09-15 于 macOS 实测
