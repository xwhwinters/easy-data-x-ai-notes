# Easy Data × AI 学习笔记

Datawhale 第 84 期，队「日拱一卒」，我在 1 群。9/14 开营，29 天 9 个 Task。

这份笔记只有一份，每学完一个 Task 往下加一节，链接从头用到尾。

- 教程仓库：https://github.com/datawhalechina/easy-data-x-ai
- 在线阅读：https://datawhalechina.github.io/easy-data-x-ai

| Task | 干什么 | 状态 | 日期 |
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

### 先把自己机器查清楚

开工第一件事不是读教程，是查环境。逐项跑了一遍：

| 检查项 | 实测 | 判定 |
|---|---|---|
| Shell | zsh 5.9（/bin/zsh 是默认） | 够用 |
| Python | 默认 `python3` 是 3.12.13，3.11.15 也装了但没在用 | 课程要 3.11，得手动指定 |
| venv / pip / uv | 都正常，建出来的环境是 3.11.15 | 通过 |
| Git | 2.54.0，但 user.name / user.email 是空的 | 补配置 |
| 网络 | github 直连 443 超时，走本机代理才通 | 得配代理 |
| 模型 API | 手上有个 OpenAI 兼容的中转 key，能用 | 通过 |
| 磁盘 | 剩 646G | 通过 |

两个地方值得单说。

一个是 Python 版本。我机器上敲 `python3` 出来的是 3.12.13，课程要求 3.11。照文档直接 `python3 -m venv .venv` 建出来的就是 3.12 环境，后面会不会出问题全看运气。还是老实指定版本：`uv venv --python 3.11 --seed .venv`。这类坑最烦，它不当场炸，专挑你忘了的时候炸。

另一个是网络。github 直连卡了 75 秒然后失败，443 根本不通，得走本机代理才把仓库拉下来。有意思的是装依赖反过来：走国内 PyPI 镜像的时候要绕开代理才快。同一个出口，两种走法，第一次配环境的人基本都要栽一下。

还有 Git 身份是空的。这个不算坑，算懒，顺手配掉就完事了，不然以后交 PR 一定卡。

### 把课程给的代码真跑一遍

clone、建环境、装依赖、`pip check`，一路绿灯。然后跑那个不用 API Key 的离线评测：

```
PYTHONPATH=code/D3:code python code/D3/d3_5_evaluate.py
```

60 条案例，失败 0 条，Hit@1 = 0.92，Hit@3 = 1.0，MRR = 0.9533，拒答准确率 1.0。六类用例（alias_rewrite、boundary、exact_identifier、insufficient_evidence、multi_hop、semantic）通过率全是 1.0。

原始报告我原样放进仓库了：[`task1/reports/offline-evaluation.md`](task1/reports/offline-evaluation.md)。

### 那张三种策略的对比表，我盯了很久

同一次运行里还给了三种检索方案的对比：

| 方案 | Hit@1 | Hit@3 | 拒答准确率 | P50 / P95（ms） | 估算 Token |
|---|---:|---:|---:|---:|---:|
| 纯向量基线 | 0.72 | 0.76 | 0.6 | 0.27 / 0.32 | 12651 |
| 混合检索 | 0.88 | 0.98 | 1.0 | 0.30 / 0.34 | 14691 |
| 工程管线 | 0.92 | 1.0 | 1.0 | 0.53 / 0.81 | 15124 |

原始报告：[`task1/reports/strategy-comparison.md`](task1/reports/strategy-comparison.md)。

我想说的不是那几个小数。

纯向量基线在"证据够"的问题上看着完全能用，Hit@3 也有 0.76，延迟还最短。差别全在证据不够的时候冒出来：它的拒答准确率只有 0.6，也就是说十个答不了的问题里有四个，它会硬编一个答案给你。混合检索和工程管线把这一项做到 1.0，代价是延迟翻倍、Token 多两成。

这跟我自己做企业 IT 方案碰到的是同一个问题。纯向量检索好看，是因为评测集里"答案就在库里"的题多；一上真实业务，用户问的十有八九是库里没有的东西。到那时候系统能不能管住自己的嘴，比它答得多流畅重要得多。

### 踩过的坑，记下来免得再踩

1. 默认 `python3` 是 3.12，课程要 3.11，必须 `uv venv --python 3.11`。
2. github 直连不通，拉代码走代理，装包走国内镜像并且绕开代理。
3. 本机有别的 Python 环境变量在捣乱，跑课程脚本前要 `env -u PYTHONPATH -u VIRTUAL_ENV` 清一遍，否则会串解释器。
4. Git 的 `user.name` / `user.email` 是空的一定要补。
5. 报告里的 Token 是字符长度估算的，延迟也只算本地编排开销，别当服务商账单看。

### 导读看下来，记住一句话

F1《大模型的本质与边界》和 F2《AI Agent 全景图》两篇公共基础都看了。课程本身分「道篇」和「术篇」，道篇讲怎么做判断（P1 到 P5），术篇讲怎么动手写（D1 到 D5），后面还有产业篇和扩展章。

记住的是一句听着很扫兴的话：不是所有需求都该做成 Agent。它的边界在数据层，不在模型层。我今天跑的那个评测正好在印证这件事，指标的天花板是数据给的，不是模型给的。

---

## 引用来源

- 教程仓库：https://github.com/datawhalechina/easy-data-x-ai
- 在线阅读：https://datawhalechina.github.io/easy-data-x-ai
- Task 安排：https://my.feishu.cn/wiki/HvQuwKiSEi0mNBkGzjBcJaldnrd
- 打卡表单：https://magicyang.feishu.cn/share/base/shrcnPJP4DBbYWnQrnUPrgRa7rf
- 评测数据：教程仓库 `code/D3/reports/offline-evaluation.md`、`code/D3/reports/strategy-comparison.md`
- 环境与运行记录：本人 2026-09-15 在 macOS 上实测
