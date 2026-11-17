# Tiếp nhận bản COCO mới — 127

- Nguồn: `127.zip`; lấy nguyên file `annotations/instances_default.json`.
- Đích: `submission/labels/127.json`.
- SHA-256 JSON: `c7e2bf3be1d32a1a3b308b92d53a0584eb9dd2314a3a3163224c9874946ef35d`.
- Số ảnh: **27/27** theo phân công; số nhãn: **90**.
- `can_review=true`: **0** nhãn.
- `validate_labels.py`: **đạt**, mã thoát 0; kiểm cả kích thước ảnh gốc, hình học, lớp, thuộc tính và tập ảnh được giao.
- Không còn lỗi box vượt biên trong bản xuất mới. Kiểm tra cấu trúc chưa xác nhận chất lượng thị giác.
- Bản xuất nguồn và nhãn cũ được giữ cục bộ tại `work/127/imports/c7e2bf3be1d3/`.

## Bước tiếp theo

Đã thử `python scripts/qc_compare.py`, mã thoát 2.
Sau đồng bộ GitHub, hiện có **53/80 lượt gán** của nhóm (106 và 127).
Còn thiếu bản độc lập: **157: 27 ảnh**. Bản 106 đã được đồng bộ và qua kiểm tra cấu trúc.
Chưa đủ đầu vào để tính IAA, calibration, tạo nhãn cuối và quyết định QC của nhóm.
Nhận thêm `157.json` khi thành viên đã nộp độc lập, lưu vào `submission/labels/`, rồi chạy:

```powershell
$env:PYTHONUTF8 = '1'
python scripts/validate_labels.py --all
python scripts/qc_compare.py
python scripts/viz_disagreement.py --images flagged
```

Sau đó đối chiếu ảnh và guideline theo `GUIDE.md`, Pha 5–6. Không sao chép bản 127 làm nhãn của người khác.

Bằng chứng có thể kiểm lại sau khi clone: [trạng thái và lệnh](evidence_127/status.json), [validator](evidence_127/validation.txt), [IAA còn thiếu đầu vào](evidence_127/iaa.txt).
