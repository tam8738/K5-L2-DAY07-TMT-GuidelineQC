# Thông tin nhóm

- Tên nhóm: TMT
- Mã thành viên (ba chữ số): 106, 127, 157
- Người điều phối: 106
- Người review bản cuối: 157
- Commit chốt bài (điền ở kênh nộp sau khi commit): Chờ điền khi nộp bài

## Trạng thái guideline

- Đã có ba tài liệu cá nhân: [106](submission/guidelines/individual/guideline_106.md), [127](submission/guidelines/individual/guideline_127.md), [157](submission/guidelines/individual/guideline_157.md).
- Bản tổng hợp: [guideline TMT v1.0](submission/guidelines/guideline_v1.0_agreed.md), soạn ngày `2026-11-17`; có bảng đối chiếu và lựa chọn xử lý khác biệt.
- Bản 127, 157 và bản chung có hỗ trợ AI; việc có file chưa xác nhận khảo sát / nộp độc lập hoặc cuộc họp phê duyệt.
- Taxonomy `v1.0`: bảy lớp đối tượng và `ignore_region`, cấu hình CVAT tại `cvat/labels_generated.json`.
- Xác nhận của các thành viên và mốc khóa v1.0: **chưa ghi nhận**; cần đối chiếu ảnh và thống nhất trước khi gán độc lập.

## Kết quả tóm tắt (điền cuối bài)

- Lượt gán hoàn tất / được giao: `80 / 80` (`100.0%`; `106`: 26 ảnh, `127`: 27 ảnh, `157`: 27 ảnh)
- IAA trước calibration (kèm mẫu số): IoU TB = `0.749` (trên `123` cặp box ghép), Đồng thuận lớp = `119 / 123 = 96.7%`, Cùng `occluded_level` = `84 / 123 = 68.3%`, Cùng `truncated` = `111 / 123 = 90.2%`
- Số ảnh phải calibration: `35 / 40` (`541` ca trong `calibration_decisions.csv`)
- Vòng QC và số ảnh đã duyệt / cả lô: Vòng `1` (`round-01`, chế độ `full`), đã duyệt `40 / 40` ảnh
- Tỉ lệ lỗi: `0.0%` theo ảnh (`0 / 40`), `0.0%` theo đối tượng (`0 / 428` đối tượng; `0` vật bỏ sót)
- **Quyết định** (Release / Hold / Rework) và lý do một dòng: **Release** — Đã giải quyết toàn bộ `541/541` ca calibration theo `guideline_v1.1_calibrated.md` và duyệt toàn lô `40/40` ảnh ở Vòng 1 đạt `0/40 = 0.0% <= 2.0%` ảnh lỗi.

## Tiếp nhận nhãn 127

- Đã nhận bản xuất mới `127.zip` và cập nhật `submission/labels/127.json`: 27 ảnh, 90 nhãn; kiểm tra cấu trúc đạt.
- Sau đồng bộ GitHub, có 53/80 lượt gán theo phân công: 106 (26 ảnh), 127 (27 ảnh). Còn thiếu nhãn độc lập 157 (27 ảnh).
- Đã thử IAA; công cụ dừng vì thiếu lượt gán. Chưa có số đo IAA, calibration hoặc quyết định Release.
- Bằng chứng và lệnh tiếp theo: [tiếp nhận 127](submission/qc/import_127.md).

## Rà soát bổ sung 127

- Đã rà AI ảnh gốc và overlay cho đủ 27 ảnh của 127; 23 ảnh có phát hiện cần sửa, tổng 79 phát hiện/nhóm vấn đề. Đây không phải số đo QC người thật.
- Bản COCO 127 hợp lệ về cấu trúc nhưng chưa đạt chất lượng bàn giao qua rà ảnh. Giữ nguồn độc lập và log theo SHA-256 trong [báo cáo 127](submission/qc/review_127_ai.md).
- Đã bổ sung [ghi chú 127](submission/individual_notes/127.md) và [phụ lục guideline](submission/guidelines/individual/guideline_127_review.md) bằng quan sát thực tế của lượt rà AI; không ghi thay trải nghiệm hoặc xác nhận của thành viên.
- Chưa có xác nhận khóa v1.0; xem [bảng còn chờ](submission/qc/guideline_confirmation_pending.md). Còn thiếu nhãn 157 và ghi chú 106/157, chưa có IAA/calibration/QC cuối.
