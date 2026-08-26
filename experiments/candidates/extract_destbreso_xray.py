"""Extract destbreso week-four x-ray tables without executing plotting cells."""

from __future__ import annotations

import ast
import json
from pathlib import Path

NB = (
    Path(__file__).resolve().parents[2]
    / "artifacts/public_sources/_hunt_20260824b/a-week-four-x-ray-of-the-top-twelve.ipynb"
)


def cell_source(cell: dict) -> str:
    source = cell.get("source") or ""
    return "".join(source) if isinstance(source, list) else str(source)


def main() -> None:
    notebook = json.loads(NB.read_text(encoding="utf-8"))
    payload = None
    for cell in notebook.get("cells", []):
        source = cell_source(cell)
        if "P =" not in source and "P=" not in source and "PAYLOAD" not in source:
            if "board" in source and "rank_now" in source:
                pass
        try:
            tree = ast.parse(source)
        except SyntaxError:
            continue
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id in {"P", "PAYLOAD", "DATA"} for t in node.targets
            ):
                name = node.targets[0].id  # type: ignore[attr-defined]
                value = ast.literal_eval(node.value)
                payload = {"name": name, "value": value}
                break
        if payload:
            break
    if payload is None:
        # dump assignment names in first code cell
        cell0 = cell_source(notebook["cells"][1])
        print("first code cell prefix:\n", cell0[:1500])
        tree = ast.parse(cell0)
        names = []
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for t in node.targets:
                    if isinstance(t, ast.Name):
                        names.append(t.id)
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                names.append(node.target.id)
        print("assign names", names)
        return
    value = payload["value"]
    out: dict = {"payload_name": payload["name"], "keys": list(value) if isinstance(value, dict) else type(value).__name__}
    if isinstance(value, dict):
        for key in ("rows", "board", "golive", "public_parent", "labels", "mine", "hinge"):
            if key in value:
                item = value[key]
                if key == "board" and isinstance(item, list):
                    out["board"] = [
                        {k: r.get(k) for k in ("rank_now", "team", "rank_0819", "score") if k in r}
                        for r in item[:20]
                    ]
                else:
                    out[key] = item if not isinstance(item, list) else item[:20]
        if "rows" in value:
            compact = []
            for row in value["rows"]:
                compact.append(
                    {
                        "rank": row.get("rank"),
                        "team": row.get("team"),
                        "band_within_agree": row.get("band_within_agree"),
                        "plan_agree": row.get("plan_agree"),
                        "in_0819_store": row.get("in_0819_store"),
                        "sells": row.get("sells") or row.get("economy"),
                    }
                )
            out["rows_compact"] = compact
    dest = Path(__file__).resolve().parent / "destbreso_xray_20260824.json"
    dest.write_text(json.dumps(out, indent=2, default=str)[:200000] + "\n", encoding="utf-8")
    print("WROTE", dest, "keys", out.get("keys"))


if __name__ == "__main__":
    main()
