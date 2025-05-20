# 🔁 Stock Transfer Process – Internal Movements in SAP eWM

This document outlines internal stock transfer scenarios within a warehouse, combining classic SAP MM/WM movement types with SAP eWM logic.

---

## 🧭 Scenario Overview

**Use case:**  
Internal movement of stock due to space reorganization, quality segregation, or staging needs. The goal is to maintain full visibility and traceability while ensuring correct stock placement and accessibility.

---

## 🔄 Process Types

### 1. **Bin-to-Bin Transfer (Within Same Storage Type)**
- Move goods from one bin to another within the same storage type.
- Used for optimization, space management, or manual relocation.

**Example:**  
Move from BIN_A01 → BIN_A07 within storage type 0050 (High Rack).

---

### 2. **Inter-Zone Transfer (Storage Type to Storage Type)**
- Transfer between areas such as Receiving → Quality, or High Rack → Staging.
- May include status change, batch split, or HU repacking.

**Example:**  
Transfer from storage type 0100 (Goods Receipt Zone) to 0150 (Inspection Zone).

---

### 3. **Handling Unit (HU) Relocation**
- Moving entire pallets or boxes without repacking.
- Often used in automated warehouses or secure/valuable goods logistics.

**Example:**  
Relocate HU #HU_1000321 from BIN_QC_05 to BIN_DISPATCH_02.

---

### 4. **Blocked / Quarantine Area Movement**
- Stock flagged for issues can be moved to a special zone for audit or disposal.
- Often tied with inspection lot results in QM.

---

## 🧾 Real-World Use Case: Operational Insight

In previous operations, I routinely managed:

| Movement Type | Description |
|---------------|-------------|
| **311** | Classic bin-to-bin transfer within same plant/storage location |
| **309** | Material-to-material transfer (e.g. sample → production batch) |
| **313 / 315** | Movement from storage location → warehouse (and reverse) |
| **305** | Transfer between unrestricted and quality stock types |

These movements were used for:
- Inter-department transfers (production → quality → final staging),
- Sample extraction and traceability,
- Audit-controlled processes with weight-based confirmation,
- Preparation for outbound deliveries in tightly monitored conditions.

---

## 📋 Example Parameters

| Element             | Value                        |
|---------------------|------------------------------|
| Source Bin          | BIN_PROD_A1                  |
| Destination Bin     | BIN_QA_LOCKED                |
| Source Storage Type | 0050 (Production Floor)       |
| Destination Type    | 0150 (Secured QA Zone)        |
| Movement Reason     | Sampling for certification    |
| Stock Type          | Unrestricted → Quality stock |

---

## 🧰 Tools & Transactions

- `/SCWM/RFUI` – Execute and confirm physical transfers  
- `/SCWM/MON` – Monitor warehouse tasks and stock movement  
- `/SCWM/TO_CONF` – Manual task confirmation  
- `/SCWM/ADHU` – Adjust Handling Unit location  
- `/SCWM/BWMAT` – Stock overview per material/bin

---

## 🧠 Notes

- Transfers can be manually created or system-triggered (e.g., by QM inspection rules).
- Movement reason codes help with audit trails and process analytics.
- Warehouse Task confirmation updates stock in real-time and provides full traceability.

---

## 📎 Real-World Example

➡️ See [Real Case: Controlled Industrial Transfer](real-case-metal-transfer.md) for a detailed simulation based on my actual SAP logistics experience.
