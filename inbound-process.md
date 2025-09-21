# 📥 Inbound Process – Goods Receipt in SAP EWM

This document describes the conceptual flow of an inbound process in a warehouse managed by SAP Extended Warehouse Management (EWM).

---

## 🔄 Scenario Overview

**Use case:**  
A delivery of raw materials arrives at the warehouse dock. The materials must be received, verified, and placed in the appropriate storage bin.

---

## 🧭 Process Steps

1. **Delivery Creation (ERP → EWM)**  
   - A purchase order is created in SAP ERP.  
   - An inbound delivery is generated and distributed to EWM.

2. **Goods Arrival and Unloading**  
   - Goods are physically received at the warehouse dock.  
   - Dock workers confirm unloading using RF or desktop transactions (e.g. /SCWM/PRDI).

3. **Goods Receipt Posting**  
   - Goods receipt is posted in EWM, updating stock levels.  
   - Status is set to “Received” but not yet available for outbound use.

4. **Putaway Task Creation**  
   - EWM creates warehouse tasks for putaway based on rules (e.g., product type, HU, volume).  
   - Storage type search strategy is applied.

5. **Putaway Execution**  
   - Warehouse worker confirms task via RF device.  
   - Stock is moved to final bin (e.g., high-rack or bulk storage).  
   - Status is updated to “Available.”

---

## 📦 Sample Parameters

| Element              | Example Value                |
|----------------------|------------------------------|
| Storage Type         | 0100 (Goods Receipt Zone)    |
| Putaway Storage Type | 0050 (High Rack Storage)     |
| HU Type              | EURO_PALLET                  |
| Product Group        | RAW_MATERIALS                |
| Strategy             | FIFO, volume-based           |

---

## 🧰 Key Transactions / Tools

- `/SCWM/PRDI` – Process Inbound Delivery  
- `/SCWM/RFUI` – RF Interface for Unloading and Putaway  
- `/SCWM/MON` – Monitor Inbound Deliveries  
- `/SCWM/PACK` – Packing of HUs if needed

---

## 📌 Notes

- Handling Units (HUs) may be generated or scanned depending on delivery setup.
- Putaway strategy can vary: fixed bin, open bin, near-bin logic, etc.
- Confirmation of putaway updates stock status in real time.

---

## 🔗 Next Step

➡️ See [Outbound Process](outbound-process.md) for the follow-up steps in warehouse logistics.
