"""D3 示例运行器：把示例里写死的模型名换成当前可用的 OpenAI 兼容模型。

d3_2 / d3_4 的模型名写死在模块常量 `MODEL = "deepseek-ai/DeepSeek-V3"`，
而本机 .env 指向的 DeepSeek 接口只认 `deepseek-flash` / `deepseek-v4-pro`。
示例代码一行不改：加载模块后覆盖 `MODEL`（顺带兼容 `MODEL_NAME`），再调用 main()。

用法（在仓库根目录）：
    PYTHONPATH=code/D3:code .venv/bin/python <此文件> d3_2_agentic_rag
"""
import importlib.util
import os
import sys

NAME = sys.argv[1]
REPO = os.getcwd()
MODEL = os.environ.get("D3_MODEL", "deepseek-flash")

spec = importlib.util.spec_from_file_location(
    NAME, os.path.join(REPO, "code", "D3", f"{NAME}.py")
)
mod = importlib.util.module_from_spec(spec)
sys.modules[NAME] = mod
spec.loader.exec_module(mod)

for attr in ("MODEL", "MODEL_NAME"):
    if hasattr(mod, attr):
        old = getattr(mod, attr)
        print(f"[override] {attr}: {old} -> {MODEL}", flush=True)
        setattr(mod, attr, MODEL)

sys.exit(mod.main())
