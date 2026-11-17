# Bắt đầu Day 07 — thành viên 127

Nhóm TMT gồm `106`, `127`, `157`. Người điều phối: `106`; người review bản cuối: `157`, theo `TEAM.md`.

Đã chạy chia ảnh theo yêu cầu với seed mặc định `42`: `106` nhận **26 ảnh**, `127` nhận **27 ảnh**, `157` nhận **27 ảnh**. Mỗi ảnh có hai người gán, tổng **80 lượt**. Danh sách chung tại `submission/qc/assignment.csv`; ảnh của bạn đã nằm trong `work/127/images/`. Đây là bước chuẩn bị phân công; chưa xác nhận hoàn thành gán nhãn.

## 1. Mở đúng file cá nhân

- Guideline: [guideline_127.md](../submission/guidelines/individual/guideline_127.md).
- Ghi chú: [127.md](../submission/individual_notes/127.md).
- Ảnh: `data/images/img_001.jpg` đến `img_040.jpg`.

Guideline đã được soạn thành bản đề xuất `v0.2-proposal-127`, có đủ năm phần và bảng ca khó dẫn từ tài liệu lab. Bạn cần tự đối chiếu ảnh trước khi xác nhận nội dung. Các ô `[127 điền]` trong ghi chú cá nhân dành cho quan sát và trải nghiệm thực tế; chưa dùng hai file như bằng chứng đã hoàn thành các pha.

Đã có cả ba tài liệu 106 / 127 / 157 và [guideline chung TMT v1.0](../submission/guidelines/guideline_v1.0_agreed.md). Bản chung có bảng xử lý khác biệt, đi kèm taxonomy v1.0 và cấu hình CVAT tám lớp; chờ các thành viên đối chiếu ảnh và xác nhận trước khi khóa lượt gán độc lập.

## 2. Việc đầu tiên: khảo sát và ghi nhận

1. Đọc [quy tắc bài](../RULES.md), [guideline v0](../guideline/guideline_v0_starter.md).
2. Xem lần lượt 40 ảnh, chưa vẽ box, chưa xem bản cá nhân của người khác.
3. Với ca chưa rõ, ghi: tên ảnh → v0 chưa nói rõ điều gì → quyết định ban đầu → lý do / câu hỏi cần họp.
4. Đối chiếu năm phần của guideline đề xuất với ảnh, điều chỉnh nếu cần và ghi ba ca khó thực sự đã xem vào ghi chú. Thử quy tắc người đi xe máy trên hai ảnh khác nhau.
5. Gửi riêng bản cá nhân theo kênh coach quy định, rồi giữ nguyên để đối chiếu ở Pha 2.

Chỉ đánh dấu các lượt xem dưới đây sau khi thực sự mở ảnh:

- [ ] `img_001.jpg` đến `img_005.jpg`.
- [ ] `img_006.jpg` đến `img_010.jpg`.
- [ ] `img_011.jpg` đến `img_015.jpg`.
- [ ] `img_016.jpg` đến `img_020.jpg`.
- [ ] `img_021.jpg` đến `img_025.jpg`.
- [ ] `img_026.jpg` đến `img_030.jpg`.
- [ ] `img_031.jpg` đến `img_035.jpg`.
- [ ] `img_036.jpg` đến `img_040.jpg`.

## 3. Lệnh Python trên Windows

Thư mục đã có `.venv` với Pillow và jsonschema. Từ thư mục gốc, dùng đường dẫn Python này để khỏi cần kích hoạt môi trường. Bật UTF-8 trong phiên Terminal để xử lý tiếng Việt, kể cả các tiến trình Python con:

```powershell
$env:PYTHONUTF8 = '1'
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Nếu kiểm thử tạo symlink báo thiếu quyền Windows (`WinError 1314`), ghi nhận đây là trở ngại của kiểm thử symlink. Không coi lần chạy đó là 20/20 đạt; có thể bật Developer Mode trong Windows nếu chính sách máy cho phép rồi chạy lại. Các bước quan sát ảnh và viết guideline vẫn làm được.

## 4. Sau khi cả nhóm nộp bản cá nhân

Bản `submission/guidelines/guideline_v1.0_agreed.md` đã được tổng hợp và taxonomy đã nâng lên v1.0, giữ nguyên mục `rules`. Các thành viên kiểm bảng khác biệt ở Mục 5.2, đối chiếu ảnh, thống nhất điều chỉnh nếu có và ghi mốc khóa trong TEAM.md. Cấu hình CVAT đã được sinh; nếu sửa taxonomy sau khi duyệt, chạy lại:

```powershell
$env:PYTHONUTF8 = '1'
.\.venv\Scripts\python.exe scripts/make_cvat_labels.py
```

Lệnh chia ảnh dưới đây đã được chạy. Cả nhóm dùng chung kết quả hiện có; nếu cần tái tạo thì giữ nguyên ba mã và seed mặc định `42`. Không đổi phân công khi đã bắt đầu gán nhãn:

```powershell
.\.venv\Scripts\python.exe scripts/split_assign.py --members 106,157,127 --copy-images
```

Nhóm ba người: mỗi ảnh được hai người gán độc lập, tổng 80 lượt gán cho cả nhóm. Số ảnh cụ thể của 127 phải lấy từ `submission/qc/assignments/127.txt`, không tự chia bằng 40/3.

Sau khi phân công, tạo Task riêng từ `work/127/images/`. Hướng dẫn CVAT theo cấu hình của bài nằm tại [CVAT_SETUP.md](CVAT_SETUP.md). Xuất COCO 1.0, tắt Save images, lấy JSON annotation lưu thành `submission/labels/127.json`, rồi kiểm:

```powershell
.\.venv\Scripts\python.exe scripts/validate_labels.py submission/labels/127.json
```

Các pha IAA, calibration và QC tiếp theo làm theo [GUIDE.md](../GUIDE.md). Ghi kết quả vào `TEAM.md` và báo cáo sau khi có bằng chứng thực tế.

## Cập nhật sau bản xuất 127 mới

- COCO: đã nhập đủ 27 ảnh/90 annotation; validator đạt.
- Rà ảnh với hỗ trợ AI: đã đủ 27/27 ảnh, có lỗi cần sửa ở 23 ảnh. Mở [báo cáo và checklist](../submission/qc/review_127_ai.md) để làm tiếp.
- Ghi chú cá nhân đã được bổ sung bằng quan sát của lượt rà sau xuất; bản guideline cá nhân ban đầu được giữ nguyên, có phụ lục đối chiếu ảnh.
- Các ô xác nhận khảo sát Pha 1 ở trên dành cho việc thành viên thực sự đã làm; không đánh dấu thay từ lượt rà AI.
- Chưa có đủ đầu vào để đóng bài nhóm: thiếu nhãn 157, ghi chú 106/157 và xác nhận guideline, IAA/calibration và QC cuối.
