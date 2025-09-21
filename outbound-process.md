# 🚚 Outbound Process – Picking, Packing & Shipping in SAP EWM

This document describes the conceptual outbound flow in a warehouse managed by SAP Extended Warehouse Management (EWM).

---

## 🧭 Scenario Overview
**Use case:** A sales order is created. Goods must be picked, packed and staged for shipping with full traceability and bin-level control.

---

## 🔄 Process Steps
1. **Demand Creation (ERP → EWM)**
   - Sales Order / Outbound Delivery created in SAP ERP.
   - Outbound delivery is distributed to EWM.

2. **Wave / Picking Task Creation**
   - EWM generates Warehouse Tasks (WT) based on picking strategy (e.g., FIFO, by activity area).
   - Optional: wave picking / clustering for efficiency.

3. **Picking Execution**
   - Operator confirms WT via RF (`/SCWM/RFUI`) from storage type **0050** to **0200** (staging).
   - HU handling if applicable.

4. **Packing**
   - Packing into HUs (e.g., cartons, pallets) with labels and content confirmation (`/SCWM/PACK`).

5. **Staging & Loading**
   - Goods moved to **0200 (Outbound/Staging)** and assigned to door/route.
   - Loading confirmation and shipping documents.

6. **Goods Issue Posting**
   - Goods Issue posted; stock leaves the warehouse.
   - Status updated across ERP/EWM.

---

## 📦 Sample Parameters

| Element              | Example Value            |
|----------------------|--------------------------|
| Picking Strategy     | FIFO / activity-area     |
| Source Storage Type  | 0050 (High-Rack Storage) |
| Staging Storage Type | 0200 (Outbound / Staging)|
| HU Type              | PALLET_EU / CARTON       |

---

## 🧰 Key Transactions / Tools
- `/SCWM/PRDO` – Process Outbound Delivery  
- `/SCWM/RFUI` – RF Picking / Confirmation  
- `/SCWM/PACK` – Packing / HU processing  
- `/SCWM/MON` – Monitor Outbound / Waves

---

## 📎 See also
- [Inbound Process](inbound-process.md)  
- [Stock Transfer](stock-transfer.md)  
- [Warehouse Layout & Bins](storage-bins-layout.md)
