# Báo cáo QC — TMT

## 1. Mục đích, dữ liệu và phiên bản

- Mục đích và giới hạn sử dụng: Thực hành xây dựng đặc tả guideline, thiết kế taxonomy và thực hiện quy trình QC/Calibration cho bài toán phát hiện người và phương tiện giao thông đường bộ trên ảnh 2D (Day 07). Bộ 40 ảnh được tuyển chọn chứa nhiều ca biên (tuk-tuk, xe chở xe, tượng, ma-nơ-canh, phản chiếu, nhòe chuyển động) nên độ đại diện cho dữ liệu vận hành thực tế chưa được đánh giá.
- Nguồn và phép sử dụng dữ liệu: Toàn bộ 40 ảnh (`img_001.jpg` đến `img_040.jpg`) có nguồn gốc từ Wikimedia Commons với đầy đủ thông tin tác giả, giấy phép (CC BY, CC BY-SA, CC0, Public domain) và liên kết gốc được lưu trữ nguyên vẹn trong `data/ATTRIBUTION.csv`.
- Manifest và checksum nhãn cuối: `submission/qc/batch_manifest.json`; bản nhãn cuối `submission/qc/labels_calibrated.json` có SHA-256 là `876a537fa1df3b4f5a6730ffd0d0c5577633c405a358dc038ce266981cdc03ac` (40 ảnh, 437 annotations gồm 428 đối tượng và 9 vùng `ignore_region`; CSV `submission/qc/labels_calibrated.csv` có SHA-256 `7d87353bcb293bd048a7f096b811623ace9aa2f9f0e6caabd12c0eaeda14a98d`).
- Guideline và taxonomy khi gán / khi bàn giao: Khi gán độc lập ở Pha 3 dùng `submission/guidelines/guideline_v1.0_agreed.md` và `submission/taxonomy.json` (`version = v1.0`, 8 lớp). Khi bàn giao ở Pha 5–6 dùng `submission/guidelines/guideline_v1.1_calibrated.md` (`kind = editorial` trong `submission/guideline_change.json`, giữ nguyên cấu trúc `submission/taxonomy.json` `v1.0`, bổ sung làm rõ cách áp dụng quy tắc biên box và vùng ignore).

## 2. Phân công và đồng thuận trước calibration

- Lượt hoàn thành / được giao: `80/80 = 100.0%` lượt gán độc lập trên 40 ảnh (thành viên `106`: `26/26` ảnh, thành viên `127`: `27/27` ảnh, thành viên `157`: `27/27` ảnh theo `submission/qc/assignment.csv`, `seed=42`).
- Số cặp box ghép, IoU TB, đồng thuận lớp và mẫu số: Tổng cộng `123` cặp box ghép 1–1 (`match_iou >= 0.5`) trên 40 ảnh; IoU trung bình đạt `0.749` (mẫu số: `123` cặp box ghép, thấp hơn ngưỡng `0.85`); đồng thuận lớp đạt `119/123 = 96.7%` (vượt ngưỡng `95.0%`); đồng thuận `occluded_level` đạt `84/123 = 68.3%`; đồng thuận `truncated` đạt `111/123 = 90.2%`. Cụ thể theo từng cặp thành viên: cặp `106|157` (13 ảnh) ghép được `100` cặp box với IoU TB `0.767`, cùng lớp `98/100 = 98.0%`, cùng `truncated` `97/100 = 97.0%`; cặp `106|127` (13 ảnh) ghép `13` cặp box với IoU TB `0.635`, cùng lớp `11/13 = 84.6%`; cặp `127|157` (14 ảnh) ghép `10` cặp box với IoU TB `0.719`, cùng lớp `10/10 = 100.0%`.
- Box chưa ghép, loại do ignore, bất đồng vùng ignore: Có `171/215` box chưa ghép được (A/B) và `59` ca bất đồng vùng `ignore_region` (`bat_dong_ignore`), tổng cộng `541` ca bất thường trên `35/40` ảnh (`bo_sot_thua`: 341, `iou_thap`: 89, `bat_dong_ignore`: 59, `sai_thuoc_tinh`: 46, `sai_lop`: 4, `co_can_review`: 2). Nguyên nhân chính là bản gán của `127` chỉ vẽ 90 box và lạm dụng `ignore_region` phủ lên cả các vật thể rõ `>= 20 px`, trong khi `106` (253 box) và `157` (308 box) gán chi tiết từng cá thể.
- Ca hai người có thể cùng sai sau khi đối chiếu tham chiếu: Trường hợp tượng đồng người cưỡi ngựa (`img_017.jpg`) hoặc tượng xe bán tải (`img_027.jpg`) — nếu hai người gán cùng hiểu sai và cùng vẽ `person` hoặc `truck` lên bức tượng thì chỉ số IAA trên ảnh đó vẫn đạt `100%` đồng thuận nhưng nhãn vẫn sai hoàn toàn so với mục tiêu bài toán (`R-05`). Trong lô của nhóm, cả hai người phụ trách `img_017.jpg`, `img_020.jpg`, `img_033.jpg`, `img_038.jpg` đều tuân thủ đúng `R-05` (không gán vật giả/phản chiếu).

## 3. Calibration và kiểm lại

- Ca đã xử lý, rule ID, bản sửa và người xác nhận: Đã rà soát và ghi nhận quyết định cho toàn bộ `541/541` ca (`C001` đến `C541`) trên `35/40` ảnh bị cờ trong `submission/qc/calibration_decisions.csv`, dẫn chiếu tới các quy tắc `R-01`, `R-02`, `R-03`, `R-06`, `R-09`, `R-11` của `guideline_v1.1_calibrated.md`. Người điều phối chốt quyết định là `106`, người kiểm lại trên ảnh gốc là `157`, bản xuất sau sửa được lưu tại `submission/qc/labels_calibrated_6f047668d34354bc.json`.
- Tác động v1.1 lên nhãn và ảnh: Thay đổi thuộc loại `editorial` (`submission/guideline_change.json`), giữ nguyên schema 8 lớp của `taxonomy.json`. Toàn bộ 35 ảnh trong phạm vi `flagged_images.txt` đã được hợp nhất lại theo chuẩn chi tiết của `106` và `157` (loại bỏ các vùng `ignore_region` bao trùm sai của `127`, chuẩn hóa biên box, đồng bộ thuộc tính `occluded_level`/`truncated`, và đóng 2 cờ `can_review` tại `img_015.jpg` thành `false`).
- Tham chiếu bằng chứng khi Rework: Lô hiện tại hoàn tất校准 (calibration) và đạt yêu cầu ngay tại Vòng QC 1 (`round-01`, duyệt toàn lô `40/40` ảnh sau calibration đạt `0/40` ảnh lỗi) nên không phát sinh vòng Rework thứ hai.

## 4. Kết quả duyệt

- Vòng QC: 1
- Người review và ngày: 157, ngày 2026-11-17
- Đã duyệt / cả lô: `40/40 = 100.0%` ảnh trong lô (`mode = full`, gồm `35/35` ảnh nhóm `ca_kho` và `5/5` ảnh nhóm `con_lai` theo `submission/qc/reviews/round-01/qc_sample.csv`).
- Ảnh lỗi / ảnh đã duyệt: `0/40 = 0.0%` (nhỏ hơn ngưỡng tối đa `2.0%` của lab; nhóm `ca_kho`: `0/35 = 0.0%`, nhóm `con_lai`: `0/5 = 0.0%`).
- Annotation đối tượng hiện có bị lỗi / annotation đối tượng đã duyệt: `0/428 = 0.0%` (trên tổng số 428 bounding box đối tượng và 9 vùng `ignore_region`, tổng 437 annotations trong `labels_calibrated.json`).
- Vật bỏ sót, ảnh và vùng: `0` vật bỏ sót (các cá thể bị thiếu ở bản độc lập đã được bổ sung đầy đủ trong bước hợp nhất calibration trước khi mở Vòng QC 1).
- Ca khó / phần còn lại, lỗi lặp và ví dụ: Dẫn chiếu trực tiếp phiếu duyệt `submission/qc/reviews/round-01/qc_review.csv` và báo cáo tự động `submission/qc/reviews/round-01/qc_report_auto.md` (`0` lỗi lặp, tất cả 40 ảnh đều được xác nhận `error_type = khong` sau khi đã xử lý triệt để các ca như xe chở xe ở `img_002.jpg`, nhòe chuyển động ở `img_015.jpg`, tuk-tuk ở `img_004.jpg`/`img_016.jpg`/`img_035.jpg`).
- Một lỗi máy chặn được và một lỗi cần người đọc ảnh: Lỗi máy (`validate_labels.py`) chặn được tự động là box có chiều cao nhỏ hơn `20 px` (ví dụ box click nhầm cao `15.8 px` ở `img_008.jpg` đã bị phát hiện và loại bỏ) hoặc tên lớp/thuộc tính sai schema. Lỗi máy không biết mà bắt buộc cần mắt người đọc ảnh là việc vẽ box đè lên tượng/ma-nơ-canh/phản chiếu (`img_017.jpg`, `img_033.jpg`) hoặc lạm dụng `ignore_region` phủ lên phương tiện rõ ở tiền cảnh.

## 5. Quyết định bàn giao

- Quyết định: Release
- Lý do, người nhận và phạm vi sử dụng: Lô 40 ảnh đã hoàn thành đủ `80/80` lượt gán độc lập, giải quyết `541/541` ca calibration trên 35 ảnh bị cờ, cập nhật `guideline_v1.1_calibrated.md`, và được reviewer `157` duyệt toàn bộ lô (`40/40` ảnh) tại Vòng 1 với tỉ lệ ảnh lỗi `0/40 = 0.0% <= 2.0%` và `0/428 = 0.0%` lỗi đối tượng. Bàn giao cho Lab Coach / giảng viên để nghiệm thu thực hành Day 07 (chỉ dùng trong phạm vi học tập, không dùng trực tiếp cho hệ thống xe tự lái vận hành thực tế).
- Nếu còn việc: Không còn ca tồn đọng; lưu giữ trọn vẹn hồ sơ truy vết từ nhãn độc lập (`submission/labels/*.json`) tới nhãn cuối (`submission/qc/labels_calibrated.json`).
- Kiểm ngược từ báo cáo tới ảnh, rule và nhãn: Ca `C197` và `C203` trên ảnh `data/images/img_015.jpg` (hai xe ô tô chạy ngược chiều bị nhòe chuyển động) → đối chiếu quy tắc `R-11` (biên theo thân xe thực tế, không ôm vệt nhòe) và `R-09` (chốt lớp `car`) trong `submission/guidelines/guideline_v1.1_calibrated.md` → ghi nhận tại dòng `C197`, `C203` trong `submission/qc/calibration_decisions.csv` → kiểm tra trong `submission/qc/labels_calibrated.json` (`image_id = 15`, `file_name = "img_015.jpg"`): cả hai box đều mang lớp `car` (`category_id = 1`), tọa độ `[232.8, 114.8, 164.1, 88.4]` và `[424.9, 126.6, 175.0, 76.6]`, thuộc tính `can_review = "false"`, khớp hoàn toàn với phiếu duyệt `submission/qc/reviews/round-01/qc_review.csv`.
