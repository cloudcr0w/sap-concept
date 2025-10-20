#!/usr/bin/env python3
"""
Lightweight SAP eWM inbound simulation:
- reads process steps (YAML/JSON)
- reads inbound event (YAML/JSON)
- optional master bin config (YAML/JSON)
- prints step-by-step log and writes result JSON

Usage:
  python sap-ewm/simulate_inbound.py \
    --process sap-ewm/inbound_process.yaml \
    --event sap-ewm/samples/inbound_event.yaml \
    --bins sap-ewm/data/master_bins.yaml \
    --out sap-ewm/out/inbound_result.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime


def _load(path: Path) -> dict:
    """Load YAML if PyYAML is available, otherwise JSON (by extension or fallback)."""
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in {".yaml", ".yml"}:
        try:
            import yaml  # type: ignore

            return yaml.safe_load(text) or {}
        except Exception:
            # fallback: try JSON
            return json.loads(text)
    # default JSON
    return json.loads(text)


def _ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def simulate(process: dict, event: dict, bins: dict | None) -> dict:
    steps = process.get("steps", [])
    result = {
        "process": "inbound",
        "status": "STARTED",
        "timestamp": _ts(),
        "po_number": event.get("po_number"),
        "delivery": event.get("delivery"),
        "items": [],
        "log": [],
    }

    def log(msg: str) -> None:
        line = f"[{_ts()}] {msg}"
        print(line)
        result["log"].append(line)

    # 1) Delivery creation (ERP → EWM)
    if "create_inbound_delivery" in steps:
        log(f"Inbound Delivery created from PO {event.get('po_number')} → {event.get('delivery')}")

    # Build item context
    items = event.get("items", [])
    # 2) Goods arrival / unloading
    if "unload_goods" in steps:
        log("Goods arrived at dock. Unloading confirmed (RF/desktop).")

    # 3) Goods receipt posting
    if "post_goods_receipt" in steps:
        log("Goods Receipt posted in EWM → stock status: RECEIVED (not available for outbound).")

    # 4) Putaway task creation
    putaway_tasks = []
    if "create_putaway_task" in steps:
        for it in items:
            product = it.get("material")
            qty = it.get("qty")
            pg = it.get("product_group")
            hu = it.get("hu_type", "EURO_PALLET")
            st = "0100"  # GR zone default
            target_type = None
            target_bin = None
            if bins:
                # simple routing: product_group → storage_type/bin
                mapping = bins.get("product_groups", {}).get(pg or "", {})
                target_type = mapping.get("storage_type", "0050")  # High rack default
                target_bin = mapping.get("bin", "HR-01-01")
            else:
                target_type = "0050"
                target_bin = "HR-01-01"

            putaway_tasks.append(
                {
                    "material": product,
                    "qty": qty,
                    "hu_type": hu,
                    "from_type": st,
                    "to_type": target_type,
                    "to_bin": target_bin,
                    "strategy": it.get("strategy", "FIFO"),
                }
            )
        log(f"Created {len(putaway_tasks)} putaway task(s) (strategy/rules applied).")

    # 5) Putaway execution
    if "confirm_putaway" in steps and putaway_tasks:
        for t in putaway_tasks:
            log(
                f"Putaway confirmed: {t['material']} x{t['qty']} → "
                f"type {t['to_type']}, bin {t['to_bin']} (HU={t['hu_type']})"
            )

    # finalize
    for it in items:
        # mark availability after putaway
        availability = "AVAILABLE" if "confirm_putaway" in steps else "RECEIVED"
        result["items"].append(
            {
                "material": it.get("material"),
                "qty": it.get("qty"),
                "status": availability,
            }
        )

    result["status"] = "COMPLETED" if "confirm_putaway" in steps else "RECEIVED"
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--process", required=True, type=Path)
    ap.add_argument("--event", required=True, type=Path)
    ap.add_argument("--bins", type=Path, default=None)
    ap.add_argument("--out", type=Path, default=Path("sap-ewm/out/inbound_result.json"))
    args = ap.parse_args()

    process = _load(args.process)
    event = _load(args.event)
    bins = _load(args.bins) if args.bins and args.bins.exists() else None

    out_dir = args.out.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    res = simulate(process, event, bins)
    args.out.write_text(json.dumps(res, indent=2), encoding="utf-8")
    print(f"\n✅ Result written to: {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
