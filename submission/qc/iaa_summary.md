# Tóm tắt IAA (taxonomy v1.0)

- Ảnh được so sánh (có >=2 người gán): **40**; số người gán: 3
- Lượt gán đủ **80/80**.
- IoU trung bình và % cùng lớp **chỉ tính trên các cặp box đã ghép** (IoU >= 0.5, ghép 1-1 không phân biệt lớp). Box chưa ghép được thống kê riêng ở cột bỏ sót/thừa.
- Mẫu số: 123 cặp box ghép (tổng mọi cặp người gán, ảnh chung).

| Cặp | Ảnh | Cặp box ghép | IoU TB | Cùng lớp | Cùng occluded_level | Cùng truncated | Chưa ghép (A/B) | Bỏ qua do ignore | Đạt IAA |
|---|---|---|---|---|---|---|---|---|---|
| **TỔNG** | 40 | 123 | 0.749 | 96.7% | 68.3% | 90.2% | 171/215 | 0 | CHƯA ĐẠT |
| 106|127 | 13 | 13 | 0.635 | 84.6% | 61.5% | 53.8% | 118/31 | 0 | CHƯA ĐẠT |
| 106|157 | 13 | 100 | 0.767 | 98.0% | 70.0% | 97.0% | 22/78 | 0 | CHƯA ĐẠT |
| 127|157 | 14 | 10 | 0.719 | 100.0% | 60.0% | 70.0% | 31/106 | 0 | CHƯA ĐẠT |

Ngưỡng IAA: IoU TB >= 0.85, đồng thuận lớp >= 95%.

Số ca bất thường: 541 ({'bo_sot_thua': 341, 'iou_thap': 89, 'sai_thuoc_tinh': 46, 'bat_dong_ignore': 59, 'sai_lop': 4, 'co_can_review': 2}), trên 35 ảnh cần calibration.
