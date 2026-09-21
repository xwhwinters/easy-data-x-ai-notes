"""补建向量索引：对 d2_knowledge_base 调 refresh_index()，让 APPROXIMATE 检索能出结果。"""
import sys
from pathlib import Path

REPO = Path("/Users/niuniu/Documents/Codex workspace/Personal/Datawhale_easy-data-x-ai/easy-data-x-ai")
sys.path.insert(0, str(REPO / "code"))
sys.path.insert(0, str(REPO / "code" / "D2"))
from seekdb_runtime import create_seekdb_client

db = create_seekdb_client(path=str(REPO / "code" / "D2" / "seekdb"))
col = db.get_collection("d2_knowledge_base")
print("集合:", col.name, "| 条数:", col.count(), "| 建索引前 has_vector_index:", col.has_vector_index)
before = len(col.query(query_texts="怎么设计用户权限", n_results=3).get("documents", [[]])[0])
print("建索引前查询结果数:", before)
col.refresh_index()
after = len(col.query(query_texts="怎么设计用户权限", n_results=3).get("documents", [[]])[0])
print("refresh_index() 已执行 | 建索引后 has_vector_index:", col.has_vector_index, "| 查询结果数:", after)
