# Guideline chung — TMT — v1.1 (Calibrated)

> Bản đặc tả `v1.1` sau phiên họp Calibration của nhóm TMT (`106`, `127`, `157`), kế thừa và đính chính biên tập (`kind = editorial`) từ `guideline_v1.0_agreed.md`. Giữ nguyên bộ tám lớp và các ngưỡng QC trong `submission/taxonomy.json`.

- Nhóm: `TMT`; thành viên: `106`, `127`, `157`.
- Phiên bản đặc tả: `v1.1` (taxonomy giữ nguyên cấu trúc `v1.0`).
- Ngày cập nhật: `2026-11-17`.
- Người điều phối / chốt calibration: `106`; người review kiểm lại: `157`.
- Nguồn cá nhân: [106 — v0.1-draft-106](individual/guideline_106.md), [127 — v0.2-proposal-127](individual/guideline_127.md), [157 — v0.1-proposal-157](individual/guideline_157.md).
- Cấu hình đi kèm: [taxonomy.json](../taxonomy.json), [guideline_change.json](../guideline_change.json), [labels_generated.json](../../cvat/labels_generated.json).

## 1. Mục tiêu và phạm vi

Bộ nhãn dùng cho thực hành phát hiện người và phương tiện giao thông đường bộ trên ảnh 2D. Mỗi cá thể thuộc phạm vi có một lớp và một bounding box ôm sát phần nhìn thấy. Vùng không gán từng cá thể được xử lý riêng theo R-06.

Ưu tiên tránh bỏ sót người / phương tiện thật, gán nhầm vật giả hoặc phản chiếu, nhầm lớp và vẽ sai biên. Box không biểu diễn khoảng cách, vận tốc, phần vật bị che hoàn toàn hoặc phần nằm ngoài ảnh. Bộ 40 ảnh là dữ liệu thực hành, chưa có bằng chứng cho sử dụng thực tế.

- Phạm vi khảo sát guideline: cả 40 ảnh `img_001.jpg` đến `img_040.jpg`.
- Lượt gán độc lập: dùng [assignment.csv](../qc/assignment.csv), seed 42; 106 nhận 26 ảnh, 127 nhận 27 ảnh, 157 nhận 27 ảnh. Mỗi ảnh hai người gán, tổng 80 lượt.
- Ngoài phạm vi phương tiện: xe đạp / xích lô không động cơ, phương tiện không thuộc bảy lớp đối tượng, vật trang trí và hàng hóa rời. Người thật trên phương tiện ngoài phạm vi vẫn được xét riêng.
- Tượng, ma-nơ-canh, hình in, đồ chơi và phản chiếu là phản ví dụ; không tạo vùng ignore chỉ cho các vật đó.

## 2. Taxonomy và thuộc tính

### 2.1. Danh sách lớp

Taxonomy có **bảy lớp đối tượng và một lớp vùng**. Tên lớp phải trùng chính xác giữa guideline, taxonomy, Project CVAT và COCO.

| Lớp | Định nghĩa | Ví dụ / dấu hiệu | Phản ví dụ / ranh giới |
|---|---|---|---|
| `car` | Ô tô con dạng sedan, hatchback, SUV hoặc crossover; không có thùng chở hàng tách biệt với cabin. | Xe con chở người, SUV; phân biệt bằng kết cấu nhìn thấy. | Pickup là truck; thân van là van; đồ chơi / tượng xe không gán. |
| `truck` | Xe chở hàng có cabin và thùng hoặc kết cấu chở hàng tách biệt, gồm pickup và xe chuyên dụng chở xe. | Xe chở ô tô trong `img_002.jpg`; pickup có nắp thùng ở `img_037.jpg`. | Van liền khối; SUV; tượng pickup tại `img_027.jpg`. |
| `van` | Xe có thân dạng hộp liền khối giữa cabin và khoang chở hàng hoặc hành khách, không có thùng hàng riêng như pickup. | Panel van hoặc minibus dùng thân van. | Xe buýt chuyên dụng là bus; pickup lắp nắp thùng vẫn là truck. |
| `bus` | Xe buýt hoặc xe khách có thân và khoang hành khách chuyên dụng kéo dài, phân biệt với minibus dùng thân van. | Các ca xe buýt ở `img_009.jpg`, `img_037.jpg`. | Không dựa vào số ghế suy đoán hoặc kích thước tương đối trong ảnh để phân lớp. |
| `tuk_tuk` | Xe cơ giới ba bánh dạng tuk-tuk, xe lam hoặc xe ba gác máy có khoang chở người hoặc sàn chở hàng. | Ca tuk-tuk tại `img_004.jpg`, `img_016.jpg`, `img_035.jpg`. | Xích lô đạp không động cơ; mô tô có sidecar; mô hình trưng bày. |
| `motorcycle` | Xe máy hoặc mô tô hai bánh có động cơ, gồm scooter; sidecar gắn liền được tính cùng một phương tiện. | Xe số, tay ga, mô tô có sidecar cố định (`img_022.jpg`). | Tuk-tuk không thuộc lớp này; người ngồi trên xe gán riêng; xe đạp không động cơ ngoài phạm vi. |
| `person` | Người thật nhận diện được trong cảnh, kể cả người trên phương tiện hoặc nhìn rõ qua kính. | Người đi bộ, người lái / ngồi sau xe máy; người thật đủ rõ sau kính. | Tượng, ma-nơ-canh, người trong hình in, phản chiếu; không suy đoán người sau kính tối. |
| `ignore_region` | Vùng chứa đối tượng trong phạm vi có phần nhìn thấy cao dưới 20 px hoặc cụm không thể tách từng cá thể đáng tin cậy. | Vật quá nhỏ, phần đám đông không tách được theo R-06. | Không dùng thay cho việc chưa chọn được lớp, không gom vật rõ, không dùng để giấu lỗi. |

### 2.2. Thuộc tính

Mọi box thuộc bảy lớp đối tượng có đủ ba thuộc tính dưới đây. `ignore_region` không cần thuộc tính trong cấu hình CVAT.

| Giá trị `occluded_level` | Tỉ lệ bị che `p` | Tiêu chí |
|---|---|---|
| `0` | `p = 0%` | Không thấy dấu hiệu bị vật khác che. |
| `1` | `0% < p <= 30%` | Bị che ít, còn thấy phần lớn hình dạng. |
| `2` | `30% < p <= 70%` | Bị che nhiều nhưng vẫn xác định được cá thể và lớp. |
| `3` | `70% < p < 100%` | Còn phần nhìn thấy cao ít nhất 20 px và vẫn nhận diện chắc chắn. |

| Thuộc tính | Giá trị | Cách áp dụng |
|---|---|---|
| `truncated` | `yes` / `no` | `yes` khi một phần vật thật sự nằm ngoài khung; chỉ chạm mép mà vẫn trọn vẹn chưa đủ để chọn yes. |
| `can_review` | `true` / `false` | `true` khi có box tạm trong Pha 3; sau khi đã họp chốt ở Pha 5 (Calibration), mọi box trong nhãn cuối đặt `can_review = false`. |

## 3. Quy tắc vẽ box (R-01 đến R-12)

- **R-01 — Box theo phần nhìn thấy:** Rectangle song song hai trục ảnh, ôm sát điểm ngoài cùng nhìn thấy của cùng một cá thể. Nếu vật bị vật mỏng chia thành nhiều mảnh nhưng xác định được là cùng vật, vẽ một box bao các phần nhìn thấy. Không bao bóng đổ, khói, phản sáng hoặc vệt sáng rời.
- **R-02 — Cắt mép ảnh:** Gán phần còn thấy nếu xác định được lớp và chiều cao ít nhất 20 px, đặt `truncated=yes`, dừng box tại biên ảnh.
- **R-03 — Người và phương tiện riêng biệt:** Một người trên một xe máy đủ điều kiện tương ứng hai box: `person` và `motorcycle`. Hai người trên một xe tương ứng ba box khi tách được từng cá thể. Không kéo box xe ôm đầu / thân người hoặc kéo box người ôm cả xe. Sidecar gắn cố định thuộc cùng một box `motorcycle`, người trong sidecar vẫn là cá thể riêng.
- **R-04 — Xe chở xe:** Gán xe chở theo kết cấu của xe chở và từng phương tiện được chở đủ điều kiện thành các box riêng (`img_002.jpg`). Nếu vật trên xe chỉ là tượng, mô hình hoặc vỏ trang trí (`img_024.jpg`, `img_028.jpg`) thì áp dụng R-05.
- **R-05 — Vật giả, hình in và phản chiếu:** Không gán đối tượng hoặc vùng ignore cho tượng (`img_011.jpg`, `img_017.jpg`, `img_027.jpg`, `img_028.jpg`), ma-nơ-canh (`img_033.jpg`), đồ chơi (`img_038.jpg`), hình in (`img_018.jpg`, `img_026.jpg`) hoặc vật chỉ xuất hiện trong phản chiếu (`img_020.jpg`, `img_033.jpg`).
- **R-06 — Vật nhỏ và vùng ignore:** Dưới 20 px chiều cao nhìn thấy: dùng vùng `ignore_region` vừa đủ cho vật / cụm vật thuộc phạm vi. Với đám đông / cụm xe không tách được cá thể đáng tin cậy ở hậu cảnh, vùng `ignore_region` chỉ bao phần không tách được; **tuyệt đối không dùng `ignore_region` trùm lên các cá thể rõ `>= 20 px` ở tiền cảnh và trung cảnh**.
- **R-07 — Xe chủ / ego-vehicle:** Bỏ phần xe gắn camera khi có đủ dấu hiệu là xe chủ (như vỏ gương chiếu hậu ở `img_020.jpg`).
- **R-08 — Phạm vi và bộ lớp đã khóa:** Dùng đúng tám tên trong taxonomy. Xe đạp / xích lô không động cơ ngoài phạm vi phương tiện, nhưng người thật trên đó gán `person` theo R-03.
- **R-09 — Pickup, van, bus và xe ba bánh:** Pickup lắp nắp thùng vẫn là `truck` (`img_037.jpg`). Van có thân liền khối; `bus` có kết cấu xe buýt / xe khách chuyên dụng; Tuk-tuk / xe lam / ba gác máy thuộc `tuk_tuk`.
- **R-10 — Hàng hóa, phụ kiện và vật mang theo:** Box phương tiện gồm bánh, gương, khung, mái và thùng gắn cố định; không kéo theo hàng rời nhô ra (`img_035.jpg`). Box `person` không kéo theo thanh sắt dài (`img_029.jpg`), quang gánh hay kiện hàng rời (`img_003.jpg`, `img_010.jpg`).
- **R-11 — Nhòe chuyển động:** Vẽ theo phần thân còn nhận biết, không ôm hết vệt nhòe (`img_014.jpg`, `img_015.jpg`). Không gộp các cá thể chỉ vì vệt nhòe nối nhau.
- **R-12 — Ca chưa chắc và truy vết:** Giải quyết dứt điểm các cờ `can_review` và các ca bất đồng trong bảng `calibration_decisions.csv`.

## 4. Ca khó đã chốt sau Calibration

| Ảnh | Tình huống | Rule ID | Quyết định chốt (v1.1) | Lý do |
|---|---|---|---|---|
| `img_002.jpg` | Xe tải chở 7 ô tô con và người đứng cạnh | `R-04` | Gán 1 box `truck` cho xe chở, 7 box `car` riêng cho các ô tô được chở, 1 box `person` | Tách cá thể xe chở và từng xe thật được chở theo đúng biên thực tế của `157`. |
| `img_004.jpg`, `img_016.jpg`, `img_035.jpg` | Tuk-tuk và người ngồi bên trong | `R-08`, `R-09`, `R-03` | Gán xe là `tuk_tuk` (không ôm hàng chất lố trên nóc ở `img_035.jpg`), gán người nhìn rõ bên trong là `person` | Thống nhất biên box `tuk_tuk` và tách cá thể `person` trong khoang hở. |
| `img_015.jpg` | Hai ô tô bị nhòe chuyển động nối nhau (`C197`, `C198`, `C203`) | `R-11`, `R-09` | Chốt lớp `car` cho cả 2 xe (không phải `van`), biên cắt tại ranh giới thân xe thực tế, tắt `can_review=false` | Cả hai đều là hatchback 5 cửa cỡ nhỏ; vệt mờ do phơi sáng không tính vào thân xe. |
| `img_017.jpg`, `img_020.jpg`, `img_027.jpg`, `img_033.jpg`, `img_038.jpg` | Tượng, phản chiếu gương, tượng đài pickup, ma-nơ-canh, cửa hàng đồ chơi | `R-05` | Không gán vật giả / phản chiếu (`img_017`, `img_020`, `img_033`, `img_038` có 0 box; `img_027` chỉ gán các xe thật đỗ phía xa, không gán tượng pickup trên bệ) | Loại bỏ hoàn toàn False Positive từ vật biểu diễn/vô tri. |
| `img_001.jpg`, `img_005.jpg`, `img_008.jpg`, `img_010.jpg`, `img_011.jpg`, `img_013.jpg`, `img_021.jpg`, `img_025.jpg`, `img_030.jpg`, `img_032.jpg`, `img_036.jpg` | Bất đồng số lượng box và vùng `ignore_region` giữa `127` và `106`/`157` | `R-01`, `R-03`, `R-06` | Giữ bộ box đối tượng chi tiết của `106` và `157` cho mọi cá thể nhìn rõ `>= 20 px`; loại bỏ các vùng `ignore_region` bao trùm quá rộng của `127` | Đảm bảo không bỏ sót cá thể thật (`>= 20 px`) và chỉ dùng `ignore_region` đúng cho cụm nhỏ/không tách được ở hậu cảnh. |

## 5. QC, hợp nhất và lịch sử phiên bản

### 5.1. Tám ngưỡng cố định (giữ nguyên trong `submission/taxonomy.json`)
- `min_box_height_px = 20`, `large_px = 50`, `iou_thr_large = 0.85`, `iou_thr_small = 0.70`, `match_iou = 0.50`, `iaa_iou = 0.85`, `iaa_class = 0.95`, `error_rate_img_max = 0.02`.

### 5.2. Lịch sử phiên bản

| Phiên bản | Thay đổi | Căn cứ |
|---|---|---|
| `v0` | Bản khởi đầu của giảng viên (5 lớp đối tượng + `ignore_region`). | Tài liệu gốc. |
| `v0.1` / `v0.2` (106, 127, 157) | Ba bản khảo sát độc lập trên 40 ảnh. | `submission/guidelines/individual/`. |
| `v1.0` | Hợp nhất 8 lớp (`car`, `truck`, `van`, `bus`, `tuk_tuk`, `motorcycle`, `person`, `ignore_region`), 3 thuộc tính và 12 quy tắc `R-01`..`R-12`. | `guideline_v1.0_agreed.md`. |
| `v1.1` | Đính chính biên tập (`kind=editorial`) sau khi giải quyết 541 ca IAA trên 35 ảnh bị cờ trong `calibration_decisions.csv`: làm rõ không lạm dụng `ignore_region` cho vật rõ `>= 20 px` (`R-06`), chốt lớp `car` và biên nhòe ở `img_015.jpg` (`R-11`), chuẩn hóa thuộc tính `occluded_level` và `truncated`. | `guideline_v1.1_calibrated.md`, `calibration_decisions.csv`. |
