"""定位根因：collection 到底有没有向量索引；显式建 HNSW 索引后能否查到。"""
import sys
from pathlib import Path

REPO = Path("/Users/niuniu/Documents/Codex workspace/Personal/Datawhale_easy-data-x-ai/easy-data-x-ai")
sys.path.insert(0, str(REPO / "code"))
import pyseekdb
from seekdb_runtime import create_seekdb_client

DOCS = ["访问控制架构设计：基于 RBAC 实现用户权限管理。",
        "错误码 E-4012 表示数据库连接超时。",
        "数据备份与恢复：每天全量备份。"]
IDS = ["a", "b", "c"]
META = [{"k": 1}, {"k": 2}, {"k": 3}]

# A：默认建集合（课程写法）
db = create_seekdb_client(path="/tmp/seekdb_a")
if db.has_collection("a"):
    db.delete_collection("a")
col = db.create_collection(name="a")
print("A 默认建集合 | has_vector_index =", col.has_vector_index)
col.add(ids=IDS, documents=DOCS, metadatas=META)
print("A count =", col.count(), "| 查询结果数 =", len(col.query(query_texts="怎么设计用户权限", n_results=3).get("documents", [[]])[0]))
print("A refresh_index ->", col.refresh_index())
print("A refresh 后查询结果数 =", len(col.query(query_texts="怎么设计用户权限", n_results=3).get("documents", [[]])[0]))

# B：显式 HNSW 配置
db2 = create_seekdb_client(path="/tmp/seekdb_b")
if db2.has_collection("b"):
    db2.delete_collection("b")
cfg = pyseekdb.HNSWConfiguration(dimension=384)
col2 = db2.create_collection(name="b", configuration=cfg)
print("B 显式 HNSW | has_vector_index =", col2.has_vector_index)
col2.add(ids=IDS, documents=DOCS, metadatas=META)
r = col2.query(query_texts="怎么设计用户权限", n_results=3)
docs = r.get("documents", [[]])[0]
print("B count =", col2.count(), "| 查询结果数 =", len(docs))
for d in docs:
    print("     ", (d or "")[:50])
