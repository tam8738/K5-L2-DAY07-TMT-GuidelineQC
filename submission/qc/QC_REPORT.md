# Báo cáo QC — TMT

> **Trạng thái hiện tại: `HOLD`** · **Ngày báo cáo:** 17-11-2026 · **Thành viên:** `106` · `127` · `157`
>
> Chưa có nhãn cuối được nghiệm thu; báo cáo ghi kết quả gán độc lập và IAA, không thay thế bằng chứng calibration hoặc QC toàn lô.

---

## 1. Mục đích, dữ liệu và phiên bản

| Hạng mục | Ghi nhận |
| --- | --- |
| **Mục đích và giới hạn sử dụng** | Thực hành xây dựng đặc tả, gán bounding box 2D và kiểm soát chất lượng nhãn người/phương tiện trên 40 ảnh đường phố. Bộ ảnh thực hành không đủ căn cứ khẳng định tính đại diện hoặc dùng cho hệ thống thực tế. Chưa cho phép sử dụng nhãn như bộ dữ liệu đã được nghiệm thu. |
| **Nguồn và phép sử dụng dữ liệu** | Theo hồ sơ nguồn và giấy phép từng ảnh tại `data/ATTRIBUTION.csv` và hướng dẫn `data/README.md` của starter repo. Giữ thông tin ghi công và tuân thủ điều kiện từng nguồn; báo cáo này không xác nhận bổ sung việc rà giấy phép riêng cho từng ảnh. |
| **Manifest và checksum nhãn cuối** | Chưa có `batch_manifest.json` và SHA-256 của bộ nhãn cuối được xác nhận. `build_final.py` chưa hoàn tất do bảng quyết định chưa đầy đủ và thiếu guideline sau calibration; không ghi checksum giả hoặc dùng checksum bản độc lập thay nhãn cuối. |
| **Guideline và taxonomy khi gán / khi bàn giao** | Các bản gán độc lập được thực hiện theo guideline chung v1.0 và taxonomy v1.0, gồm bảy lớp đối tượng và `ignore_region`. Tham chiếu `submission/guidelines/guideline_v1.0_agreed.md`, `submission/taxonomy.json`. Chưa hoàn thiện `guideline_v1.1_calibrated.md`; chưa xác nhận phiên bản dùng bàn giao nhãn cuối. Giữ nguyên rules QC. Mốc xác nhận và khóa v1.0 của cả nhóm chưa có bằng chứng bổ sung trong báo cáo này. |

---

## 2. Phân công và đồng thuận trước calibration

| Hạng mục | Ghi nhận |
| --- | --- |
| **Lượt hoàn thành / được giao** | 80/80 lượt (100%), bao phủ 40/40 ảnh; mỗi ảnh hai người gán theo `submission/qc/assignment.csv`. Thành viên 106: 26/26 ảnh; 127: 27/27 ảnh; 157: 27/27 ảnh. `validate_labels.py --all` xác nhận ba file hợp lệ về cấu trúc; chưa xác nhận độ đúng thị giác. |
| **Số cặp box ghép, IoU TB, đồng thuận lớp và mẫu số** | 123 cặp, IoU TB **0,749** (yêu cầu ≥ 0,85), cùng lớp **96,7%** trên 123 cặp (yêu cầu ≥ 95%). Đồng thuận `occluded_level` **68,3%**, `truncated` **90,2%**, cùng mẫu số 123 cặp. Chỉ tính trên box ghép 1–1 có IoU ≥ 0,5, không phụ thuộc lớp khi ghép. IAA tổng thể **chưa đạt** vì IoU trung bình dưới ngưỡng. Tỷ lệ được giữ theo số làm tròn của script, không suy ngược thành số đếm chính xác. |
| **Box chưa ghép, loại do ignore, bất đồng vùng ignore** | Báo cáo tổng ghi chưa ghép A/B là **171/215** theo thứ tự các cặp so sánh; đây là số đếm theo cặp, không phải số vật duy nhất. Loại do ignore: **0**. Có **59** ca bất đồng ignore. Tổng **541** ca cần xem trên 35/40 ảnh (chi tiết ở bảng dưới). Không cộng số box chưa ghép với số ca để suy ra tổng lỗi; 541 là ca cần kiểm, chưa phải lỗi đã được người review xác nhận. Bằng chứng: `submission/qc/iaa_summary.md`, `iaa_summary.json`, `calibration_candidates.csv`, `flagged_images.txt`. |
| **Ca hai người có thể cùng sai sau khi đối chiếu tham chiếu** | Chưa hoàn thành đối chiếu ca tham chiếu của coach nên chưa xác nhận ca cùng sai. Cần đối chiếu ảnh gốc, guideline v1.0 và tham chiếu, đặc biệt vật giả/phản chiếu theo R-05 và vùng ignore theo R-06. Các chủ đề này là kế hoạch kiểm, không phải phát hiện đã được xác nhận. IAA cao hoặc cùng lớp không chứng minh cả hai cùng đúng. |

### 2.1. Chi tiết theo cặp người gán

| Cặp | Ảnh chung | Cặp box ghép | IoU TB | Cùng lớp | Cùng `occluded_level` | Cùng `truncated` | Chưa ghép A/B | Đạt IAA |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | :---: | :--- |
| 106 và 127 | 13 | 13 | 0,635 | 84,6% | 61,5% | 53,8% | 118/31 | Chưa đạt |
| 106 và 157 | 13 | 100 | 0,767 | 98,0% | 70,0% | 97,0% | 22/78 | Chưa đạt |
| 127 và 157 | 14 | 10 | 0,719 | 100,0% | 60,0% | 70,0% | 31/106 | Chưa đạt |
| **Tổng** | **40** | **123** | **0,749** | **96,7%** | **68,3%** | **90,2%** | **171/215** | **Chưa đạt** |

> **Lưu ý về cách tính:** IoU tổng là trung bình trên toàn bộ 123 cặp box, không phải trung bình đơn giản của ba IoU theo cặp người.

### 2.2. Phân rã 541 ca cần xem (trên 35/40 ảnh)

| Mã ca | Số ca |
| :--- | ---: |
| `bo_sot_thua` | 341 |
| `iou_thap` | 89 |
| `sai_thuoc_tinh` | 46 |
| `bat_dong_ignore` | 59 |
| `sai_lop` | 4 |
| `co_can_review` | 2 |
| **Tổng** | **541** |

> 541 là số **ca cần kiểm**, chưa phải số lỗi đã được người review xác nhận. Không cộng số box chưa ghép với số ca để suy ra tổng lỗi.

---

## 3. Calibration và kiểm lại

**Ca đã xử lý, rule ID, bản sửa và người xác nhận**
Chưa có ca được ghi nhận hoàn tất trong bảng quyết định đã cung cấp. `submission/qc/calibration_decisions.csv` có 541 dòng `C001`–`C541`; các trường quyết định, quy tắc, phiên bản, người chốt, dấu vết sửa và kiểm lại còn trống. `pham_vi` đang là `anh`, chưa thay thế quyết định thực tế. Chưa có bản sửa hoặc người xác nhận để dẫn như kết quả hoàn thành.

**Tác động v1.1 lên nhãn và ảnh**
Chưa hoàn thành v1.1, chưa có thay đổi hoặc mapping sau calibration được xác nhận. Không tự khai `editorial`/`semantic` khi nhóm chưa chốt thay đổi thật. Nếu đổi cách chọn vật, lớp, box hoặc thuộc tính, phải ghi `semantic`, xác định phạm vi cả lô và rà lại các ảnh bị ảnh hưởng theo quy trình lab.

**Tham chiếu bằng chứng khi Rework**
Chưa có vòng sửa và vòng QC sau sửa. Giữ ba bản độc lập `submission/labels/106.json`, `127.json`, `157.json`, báo cáo IAA và danh sách ca làm đầu vào. Chưa có bằng chứng hoàn tất Rework; trạng thái hiện tại là **Hold** do thiếu calibration và QC.

---

## 4. Kết quả duyệt

| Hạng mục | Ghi nhận |
| --- | --- |
| **Vòng QC** | Chưa thực hiện vòng QC nhãn cuối; không ghi số vòng giả chỉ để đáp ứng kiểm tra tự động. |
| **Người review và ngày** | Chưa có người thực hiện duyệt nhãn cuối được xác nhận. Mã 157 là reviewer theo phân công `TEAM.md`, không phải bằng chứng đã duyệt. Ngày lập báo cáo 17-11-2026 không phải ngày hoàn tất review. |
| **Đã duyệt / cả lô** | **0/40** ảnh ở bước QC nhãn cuối theo bằng chứng hiện có; việc tạo 35 overlay IAA không được tính là đã duyệt QC. |
| **Ảnh lỗi / ảnh đã duyệt** | **N/A** — chưa có mẫu duyệt nhãn cuối (mẫu số 0). Không ghi 0% lỗi; 35 ảnh bị cờ IAA không đồng nghĩa 35 ảnh đã được xác nhận lỗi nghiệm thu. |
| **Annotation đối tượng hiện có bị lỗi / annotation đối tượng đã duyệt** | **N/A** — chưa duyệt annotation nhãn cuối (mẫu số 0); chưa có số lỗi đã xác nhận. |
| **Vật bỏ sót, ảnh và vùng** | Chưa có danh sách vật bỏ sót được xác nhận bằng review ảnh. Có 341 ca `bo_sot_thua` cần kiểm trong `calibration_candidates.csv`; không tự coi toàn bộ là bỏ sót. Ví dụ `C001` tại `img_001.jpg`: box person của 106 `[403,114,126,198]` chưa ghép với 127; phải đối chiếu ảnh và các box khác trước khi kết luận thiếu/thừa hay lệch biên. |
| **Ca khó / phần còn lại, lỗi lặp và ví dụ** | Còn 541 ca trên 35 ảnh chưa được chốt. Chưa có phiếu QC nhãn cuối nên chưa xác nhận lỗi lặp. Ảnh chồng nhãn đã sinh cục bộ trong `work/viz/` phục vụ đối chiếu; thư mục `work/` không thuộc gói nộp. Danh sách chính thức: `submission/qc/calibration_candidates.csv` và `flagged_images.txt`. |

### 4.1. Hai loại lỗi đại diện

- **Lỗi cần người đọc ảnh** — Ví dụ `C012` tại `img_001.jpg`, hai box truck có IoU 0,62; máy báo lệch nhưng không quyết định được biên nào ôm đúng xe. Cần ảnh gốc và R-01 để kết luận.

---
