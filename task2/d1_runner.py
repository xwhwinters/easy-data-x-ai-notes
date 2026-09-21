"""D1 示例运行器：把示例里写死的模型名换成当前可用的 OpenAI 兼容模型。

课程原本用 SiliconFlow 的 tencent/Hunyuan-MT-7B（d1_1~d1_5）和 DashScope 的
qwen-plus（d1_6）。本机没有这两个 Key，改用 DeepSeek 官方接口（同为 OpenAI 兼容），
模型名由 D1_MODEL 环境变量注入（默认 deepseek-chat）。示例代码本身一行未改：
- 走模块常量 MODEL_NAME 的（d1_1~d1_3、d1_5、d1_6）：覆盖模块属性；
- 把模型名写死在 main 里的（d1_4）：传给 main 一个 wrapper 当 model_factory。
"""
import importlib.util
import inspect
import os
import sys

NAME = sys.argv[1]
REPO = os.getcwd()
MODEL = os.environ.get("D1_MODEL", "deepseek-chat")

spec = importlib.util.spec_from_file_location(NAME, os.path.join(REPO, "code", "D1", f"{NAME}.py"))
mod = importlib.util.module_from_spec(spec)
sys.modules[NAME] = mod
spec.loader.exec_module(mod)

if hasattr(mod, "MODEL_NAME"):
    print(f"[override] MODEL_NAME: {mod.MODEL_NAME} -> {MODEL}", flush=True)
    mod.MODEL_NAME = MODEL


def make_wrapper(real):
    def wrapper(*args, **kwargs):
        if args:
            print(f"[override] 模型入参: {args[0]} -> {MODEL}", flush=True)
            args = (MODEL,) + tuple(args[1:])
        else:
            kwargs["model"] = MODEL
        return real(*args, **kwargs)

    return wrapper


params = inspect.signature(mod.main).parameters
if "model_factory" in params and params["model_factory"].default is not inspect.Parameter.empty:
    real_factory = params["model_factory"].default
    sys.exit(mod.main(model_factory=make_wrapper(real_factory)))

sys.exit(mod.main())
