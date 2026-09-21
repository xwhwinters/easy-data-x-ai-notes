"""最小复现：全新 embedded 库，写入 3 条再查，看向量检索是否可用。"""
import sys
from pathlib import Path

REPO = Path("/Users/niuniu/Documents/Codex workspace/Personal/Datawhale_easy-data-x-ai/easy-data-x-ai")
sys.path.insert(0, str(REPO / "code"))
from seekdb_runtime import create_seekdb_client

p = Path("/tmp/seekdb_mini")
db = create_seekdb_client(path=str(p))
if db.has_collection("mini"):
    db.delete_collection("mini")
col = db.create_collection(name="mini")
col.add(ids=["a", "b", "c"],
        documents=["访问控制架构设计：基于 RBAC 实现用户权限管理。",
                   "错误码 E-4012 表示数据库连接超时。",
                   "数据备份与恢复：每天全量备份。"],
        metadatas=[{"k": 1}, {"k": 2}, {"k": 3}])
print("count:", col.count())
r = col.query(query_texts="怎么设计用户权限", n_results=3)
docs = r.get("documents", [[]])[0]
print("查询结果:", len(docs))
for d in docs:
    print("   ", (d or "")[:50])

# 直接看 collection 拿到的是什么
print("collection 对象:", col)
print("collection name:", getattr(col, "name", None), "| id:", getattr(col, "collection_id", None) or getattr(col, "id", None))
try:
    from db_lifecycle import close_database
    close_database(db)
except Exception:
    pass
