"""D4 示例运行器：把示例里写死的模型名换成当前可用的 OpenAI 兼容模型。

D4 的八个示例都在模块常量 `MODEL = "deepseek-ai/DeepSeek-V3"`，
而本机 .env 指向的 DeepSeek 接口只认 `deepseek-flash` / `deepseek-v4-pro`。
示例代码一行不改：加载模块后覆盖 MODEL，再调用 main()。

用法（在仓库根目录）：
    env -u PYTHONPATH -u VIRTUAL_ENV NO_PROXY='*' SEEKDB_MODE=embedded \
      PYTHONPATH=code/D4:code .venv/bin/python <此文件> d4_1_react_loop
"""
import importlib.util
import os
import sys

NAME = sys.argv[1]
REPO = os.getcwd()
MODEL = os.environ.get("D4_MODEL", "deepseek-flash")

spec = importlib.util.spec_from_file_location(
    NAME, os.path.join(REPO, "code", "D4", f"{NAME}.py")
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
