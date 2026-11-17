# Thông tin nhóm

- Tên nhóm: TMT.
- Mã thành viên: 106, 127, 157.
- Người điều phối: 106.
- Người review bản cuối theo phân công: 157; chưa thực hiện duyệt nhãn cuối.
- Commit chốt bài: ghi tại kênh nộp sau khi commit.
- Trạng thái hiện tại: Hold — chưa hoàn thành calibration và QC nhãn cuối.

## 1. Guideline và taxonomy

- Có ba guideline cá nhân:
  - [106](submission/guidelines/individual/guideline_106.md).
  - [127](submission/guidelines/individual/guideline_127.md).
  - [157](submission/guidelines/individual/guideline_157.md).
- Có [guideline chung v1.0](submission/guidelines/guideline_v1.0_agreed.md).
- Taxonomy v1.0 gồm bảy lớp đối tượng: car, truck, van, bus, tuk_tuk, motorcycle, person; và vùng ignore_region.
- Cấu hình nhãn CVAT: [labels_generated.json](cvat/labels_generated.json).
- Giữ nguyên các ngưỡng rules của lab.
- Xác nhận của cả nhóm và mốc khóa guideline v1.0: chưa được ghi nhận trong tài liệu.

## 2. Phân công và nhãn độc lập

Bộ dữ liệu gồm 40 ảnh. Mỗi ảnh được phân cho hai người gán, tổng cộng 80 lượt.

| Mã thành viên | Ảnh được giao | Ảnh có trong COCO | Kiểm tra cấu trúc |
|---|---:|---:|---|
| 106 | 26 | 26 | Hợp lệ |
| 127 | 27 | 27 | Hợp lệ |
| 157 | 27 | 27 | Hợp lệ |
| Tổng | 80 lượt | 80 lượt | Cả ba file hợp lệ |

- Bảng phân công: [assignment.csv](submission/qc/assignment.csv).
- Nhãn độc lập:
  - [106.json](submission/labels/106.json).
  - [127.json](submission/labels/127.json).
  - [157.json](submission/labels/157.json).
- Đã chạy validate_labels.py --all, cả ba file hợp lệ về cấu trúc.
- Kết quả kiểm tra cấu trúc không xác nhận box đúng vật, đúng lớp, sát biên hoặc không bỏ sót.
- Giữ nguyên các bản độc lập để đối chiếu trong calibration.

## 3. Kết quả IAA trước calibration

- Ảnh được so sánh: 40/40.
- Lượt gán hợp lệ: 80/80.
- Số người gán: 3.
- Số cặp box ghép: 123.
- IoU trung bình: 0,749; yêu cầu tối thiểu 0,85.
- Đồng thuận lớp: 96,7%; yêu cầu tối thiểu 95%.
- Đồng thuận occluded_level: 68,3%.
- Đồng thuận truncated: 90,2%.
- Kết luận IAA: chưa đạt.

IoU trung bình và các tỷ lệ đồng thuận trên chỉ tính trên 123 cặp box đã ghép một–một với IoU từ 0,5 trở lên. Các box chưa ghép được xem riêng; đồng thuận cao không chứng minh mọi nhãn đều đúng.

| Loại ca cần xem | Số ca |
|---|---:|
| Bỏ sót/thừa hoặc box chưa ghép | 341 |
| IoU thấp | 89 |
| Sai khác thuộc tính | 46 |
| Bất đồng vùng ignore | 59 |
| Sai khác lớp | 4 |
| Có can_review | 2 |
| Tổng | 541 |

- Số ảnh cần calibration: 35/40.
- 541 là số ca cần xem, không phải số lỗi đã được reviewer xác nhận.
- Báo cáo: [iaa_summary.md](submission/qc/iaa_summary.md).
- Danh sách ca: [calibration_candidates.csv](submission/qc/calibration_candidates.csv).
- Đã tạo ảnh chồng nhãn trong work/viz/ để xem cục bộ; không đưa work/ vào gói nộp.

## 4. Trạng thái calibration và QC

- Đã tạo [calibration_decisions.csv](submission/qc/calibration_decisions.csv).
- Chưa hoàn thành xác nhận và quyết định xử lý 541 ca.
- Chưa hoàn thành sửa nhãn và kiểm lại sau calibration.
- Chưa hoàn thiện guideline_v1.1_calibrated.md.
- Chưa tạo thành công bộ nhãn cuối được kiểm duyệt.
- Chưa thực hiện vòng QC nhãn cuối trên toàn bộ 40 ảnh.
- Tỷ lệ lỗi theo ảnh: chưa đo.
- Tỷ lệ lỗi theo đối tượng: chưa đo.
- build_final.py chưa hoàn tất do bảng quyết định và guideline sau calibration chưa đầy đủ.
- Chưa có kết quả check_submission.py xác nhận gói bàn giao đầy đủ.

## 5. Quyết định và phần còn thiếu

**Quyết định: Hold.**

Lý do: đã đủ lượt gán và có báo cáo IAA, nhưng IoU trung bình chưa đạt; còn 541 ca trên 35 ảnh cần calibration. Chưa có nhãn cuối và bằng chứng QC toàn lô để xác nhận Release.

Phân công tiếp tục theo vai trò của nhóm:

| Phần còn thiếu | Người phụ trách |
|---|---|
| Điều phối calibration và thống nhất quyết định | 106 |
| Đối chiếu ảnh, quy tắc và các ca bất đồng | 106, 127, 157 |

Đây là phân công xử lý tiếp, không phải xác nhận các công việc đã hoàn thành. Thời gian bổ sung theo thống nhất của nhóm và hướng dẫn coach.

Nhóm nộp bằng chứng đã có qua kênh lớp theo hướng dẫn dành cho bài còn Hold trong SUBMISSION.md. Trạng thái Hold không đồng nghĩa bài đã hoàn thành đầy đủ hoặc được nghiệm thu.
