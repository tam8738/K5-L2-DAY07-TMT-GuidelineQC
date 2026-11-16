# Guideline gán nhãn — v0.1-draft — 106

> Bản dự thảo guideline cá nhân (Pha 1) của thành viên `106`, mở rộng từ `guideline_v0_starter.md` sau khi khảo sát 40 ảnh trong `data/images/`.

- Phiên bản: `v0.1-draft-106`
- Ngày: `2026-11-16`
- Người viết / duyệt: `106`
- Loại nhãn: Bounding box 2D trên ảnh đường phố (CVAT, xuất COCO 1.0)

---

## 1. Mục tiêu

Bộ nhãn dùng để huấn luyện và đánh giá mô hình thị giác máy tính **phát hiện người và phương tiện giao thông đường bộ trên ảnh 2D** (ứng dụng cho camera giám sát giao thông và hệ thống hỗ trợ lái / xe tự lái ADAS).

- **Sai sót nguy hiểm nhất (False Negative — Bỏ sót):** Bỏ sót người đi bộ, người đi xe máy hoặc phương tiện đang lưu thông thật trên đường (dẫn đến nguy cơ va chạm trực tiếp hoặc đếm thiếu lưu lượng).
- **Sai sót gây nhiễu hệ thống (False Positive — Gán thừa vật giả):** Gán nhầm tượng, ma-nơ-canh, hình ảnh in trên biển quảng cáo/thân xe, hoặc bóng phản chiếu qua kính/gương thành người/xe thật (dẫn đến phanh gấp giả hoặc cảnh báo sai).
- **Sai lệch hình học (IoU thấp):** Box quá lỏng (ôm cả bóng đổ, khói bụi) hoặc quá hẹp (cắt mất bánh xe, đầu người) làm giảm độ chính xác định vị khoảng cách 2D/3D.

---

## 2. Lớp và thuộc tính

### 2.1. Định nghĩa các lớp (mỗi đối tượng chỉ thuộc đúng 1 lớp)

| Lớp | Định nghĩa (một câu) | Ví dụ | Phản ví dụ / dễ nhầm với |
|---|---|---|---|
| `car` | Ô tô chở người cỡ nhỏ đến trung bình (4–7 chỗ), có khoang hành khách gắn liền thân xe. | Sedan, hatchback, SUV, crossover, coupe, taxi 4–7 chỗ. | Xe bán tải có thùng hở phía sau (`truck`), minivan/xe thùng kín (`van`), xe lam/tuk-tuk 3 bánh. |
| `truck` | Xe chuyên chở hàng hóa có thùng hàng tách biệt với cabin (thùng hở, thùng kín cỡ lớn, xe bồn, xe chuyên dụng) hoặc xe bán tải (pickup). | Xe tải thùng kín/thùng bạt, xe ben, xe đầu kéo, xe cứu hộ chở xe khác, xe bán tải (pickup truck). | Xe van có khoang lái và khoang hàng liền khối nhỏ (`van`), SUV 7 chỗ (`car`). |
| `van` | Xe thùng kín cỡ nhỏ/trung bình có cabin và khoang chở hàng/chở khách liền một khối dạng hộp, cửa trượt hoặc cửa mở sau. | Minivan, xe tải van giao hàng nội đô, xe khách cỡ nhỏ (12–16 chỗ dạng Ford Transit, HiAce). | SUV (`car`), xe tải có cabin rời với thùng hàng (`truck`), xe buýt cỡ lớn (>24 chỗ). |
| `motorcycle` | Phương tiện cơ giới 2 bánh hoặc 3 bánh nhỏ gắn động cơ (tay ga, xe số, mô tô phân khối lớn). | Xe máy tay ga, xe số, mô tô, scooter có gắn máy. *(Ghi chú: Cần thống nhất nhóm về xe 3 bánh / tuk-tuk).* | Xe đạp không động cơ (bỏ qua), người đang ngồi trên xe máy (`person` gán box riêng). |
| `person` | Con người thật (còn sống) xuất hiện trong cảnh, bất kể tư thế (đi bộ, đứng, ngồi, lái xe, ngồi sau xe). | Người đi bộ, người điều khiển xe máy, người ngồi sau xe máy, công nhân ven đường, người ngồi quán vỉa hè thấy rõ thân người. | Tượng, ma-nơ-canh, ảnh người trên poster/biển quảng cáo, bóng phản chiếu trong gương/kính. |
| `ignore_region` | Vùng ảnh chứa các đối tượng quá nhỏ, quá mờ/tối, đám đông/bãi xe chồng lấn dày đặc không thể tách rời từng vật, hoặc phương tiện ngoài phạm vi chưa chắc chắn. | Cụm xe/người ở rất xa có chiều cao `< 20 px`, đám đông chợ/ngã tư dính liền nhau. | Không dùng `ignore_region` cho vật giả (tượng, phản chiếu) vì vật giả đơn giản là **không vẽ box**. |

**Xử lý vật KHÔNG thuộc lớp nào ở trên:**
- **Vật không thật** (tượng, ma-nơ-canh, đồ chơi, mô hình trang trí, hình in 2D, bóng phản chiếu): **Tuyệt đối không gán box** (không gán lớp đối tượng và cũng không bọc `ignore_region`).
- **Phương tiện ngoài danh sách cơ bản** (xe đạp, xe kéo tay, xe buýt lớn, tuk-tuk/xe ba gác, tàu hỏa...): Ghi nhận vào bảng Ca khó để chốt ở Pha 2 (không gán hoặc quy về lớp gần nhất / `ignore_region`).

---

### 2.2. Thuộc tính (Attributes) và ngưỡng đo được

Mọi box thuộc các lớp đối tượng (`car`, `truck`, `van`, `motorcycle`, `person`) đều phải gán đủ 3 thuộc tính sau. Riêng `ignore_region` giữ giá trị mặc định (`occluded_level=0`, `truncated=no`, `can_review=false`).

#### 1) `occluded_level` (Mức độ bị vật khác che khuất)
Tính theo **tỷ lệ diện tích phần thân vật bị che khuất** bởi vật cản phía trước (xe khác, người khác, cây cối, biển báo, cột điện...). *Không tính phần bị mất do chạm mép ảnh vào `occluded_level` (phần đó tính ở `truncated`).*

| Giá trị | Ý nghĩa | Ngưỡng đo lường cụ thể (% diện tích bị che) |
|---|---|---|
| `0` | Thấy rõ hoàn toàn | **0% – < 5%** bị che (nhìn thấy trọn vẹn hoặc chỉ bị vướng chi tiết rất nhỏ như dây điện, cành cây mảnh). |
| `1` | Bị che ít | **5% – 30%** diện tích vật bị che khuất; vẫn nhận diện rõ ràng hình dáng chính (ví dụ: người ngồi trên xe máy bị ghi-đông/thân xe che một phần chân). |
| `2` | Bị che nhiều | **> 30% – 70%** diện tích vật bị che khuất (ví dụ: ô tô đỗ sau xe khác chỉ thấy nửa thân trên hoặc nửa đầu xe). |
| `3` | Bị che rất nặng / Khó nhận diện | **> 70% – 85%** diện tích bị che khuất, chỉ lộ một phần nhỏ (như đầu/vai người hoặc góc đuôi xe) nhưng vẫn khẳng định chắc chắn được lớp. *(Nếu che > 85% không nhận diện nổi thì không gán riêng).* |

#### 2) `truncated` (Bị cắt ở mép khung hình)

| Giá trị | Ý nghĩa | Ngưỡng đo lường cụ thể |
|---|---|---|
| `no` | Không bị cắt mép | Toàn bộ phần nhìn thấy của đối tượng nằm trọn bên trong 4 cạnh khung ảnh (cách mép ảnh `>= 2 px` hoặc chạm sát mép nhưng không bị mất bộ phận nào). |
| `yes` | Bị cắt bởi mép ảnh | Đối tượng nằm ở rìa khung hình (trái, phải, trên, dưới) khiến **bất kỳ bộ phận nào của vật bị cắt mất ra ngoài biên ảnh** (dù chỉ mất một phần bánh xe, bàn chân hay đầu xe). |

#### 3) `can_review` (Cờ đánh dấu cần xem lại)

| Giá trị | Ý nghĩa | Khi nào sử dụng |
|---|---|---|
| `false` (bỏ tick) | Chắc chắn | Đối tượng rõ ràng, đã có quy tắc khớp hoàn toàn trong guideline. |
| `true` (tick) | Cần họp / review | Khi người gán phân vân giữa 2 lớp (vd: SUV vs Van, Pickup vs Car), phân vân mức che khuất ở ranh giới (xấp xỉ 30% hoặc 70%), hoặc gặp ca biên mới phát sinh. |

---

## 3. Quy tắc vẽ box (Rule IDs)

- **R-01 (Biên giới box — Ôm sát phần nhìn thấy / Visible Box):**
  - Box phải **ôm sát phần diện tích thực tế nhìn thấy được (visible part)** của đối tượng với sai số biên `<= 2 px`.
  - **Không** tự suy đoán và kéo rộng box ra vùng bị vật khác che khuất hoàn toàn ở một phía.
  - Nếu một đối tượng bị vật mỏng (cột đèn, thân cây nhỏ, người đi ngang) chia làm 2 phần rời nhau nhưng vẫn thấy rõ 2 đầu của cùng 1 vật, vẽ **1 box duy nhất** bao trùm toàn bộ phần nhìn thấy từ cực trái sang cực phải, cực trên xuống cực dưới của vật đó và đặt `occluded_level` tương ứng (`1`, `2` hoặc `3`).
  - Bao gồm gương chiếu hậu (với xe) và chân/tay/mũ bảo hiểm đang đội (với người). Không bao gồm bóng đổ dưới mặt đường, khói xe, hay tia sáng đèn pha.

- **R-02 (Người đi xe máy / Người trên phương tiện khoang hở vs khoang kín):**
  - Gán **tách biệt 2 box độc lập**: 1 box `person` cho mỗi người ngồi trên xe và 1 box `motorcycle` cho chiếc xe máy.
  - Box `motorcycle` chỉ ôm phần thân xe máy (bánh xe, khung xe, tay lái, gương), **không** kéo cao lên để bao trùm đầu người lái.
  - Box `person` ôm toàn bộ cơ thể người ngồi (từ đỉnh đầu/mũ bảo hiểm đến hết bàn chân nhìn thấy). Do một phần chân/thân dưới bị xe che hoặc khuất sau thân xe, đặt `occluded_level = 1` (hoặc `2` nếu bị người ngồi trước/xe che > 30%).
  - **Phương tiện khoang hở (Tuk-tuk, xe lam, xích lô, xe ba gác, thùng xe tải hở):** Vì không có cửa và vách kín, nếu nhìn thấy rõ cơ thể tài xế hoặc hành khách bên trong (`>= 20 px`, bị che `<= 85%`) thì **CÓ gán box `person`** và đặt `occluded_level = 1` hoặc `2` tương ứng với phần bị khung xe che.
  - **Phương tiện khoang kín (`car`, `truck`, `van`, xe buýt đóng kính):** Người ngồi trong cabin kín chỉ lộ mờ đầu/vai qua kính chắn gió hoặc cửa sổ thì **KHÔNG gán `person`**, trừ khi người đó mở cửa thò hẳn nửa người ra ngoài.

- **R-03 (Vật không thật — Tượng, Ma-nơ-canh, Hình in, Phản chiếu, Đồ chơi):**
  - **Không vẽ box** cho tượng điêu khắc hình người/xe, ma-nơ-canh trưng bày ở cửa hàng, hình người/xe in trên biển quảng cáo, pano, hoặc dán trên thân xe buýt/xe tải.
  - **Không vẽ box** cho hình ảnh phản chiếu của người hoặc xe trong gương, cửa kính tòa nhà, mặt nước hoặc thân xe bóng.

- **R-04 (Xe chở xe / Hàng hóa là phương tiện):**
  - Nếu một phương tiện (`car`, `motorcycle`, `truck`, `van`) đang được chở bên trên thùng xe tải / xe cứu hộ mà vẫn nhìn thấy rõ hình khối (`>= 20 px`), **vẫn gán box riêng** cho phương tiện được chở (kèm `occluded_level` theo phần bị thành thùng xe che), và gán 1 box `truck` riêng cho xe chở bên dưới (chỉ ôm phần xe tải chở, hoặc bao gồm khung thùng xe). *(Cần thảo luận chốt thêm ở Pha 2).*

- **R-05 (Kích thước tối thiểu & Vùng bỏ qua `ignore_region`):**
  - Đối tượng đơn lẻ có chiều cao box **`< 20 px`**: **Không gán lớp đối tượng** (`car`, `person`...). Hãy dùng box `ignore_region` bao phủ đối tượng hoặc cụm đối tượng nhỏ đó.
  - Đám đông người đi bộ hoặc dãy xe đỗ/di chuyển ở xa bị chồng lấn dày đặc (> 3–4 vật dính liền, che khuất > 70%, không thể tách ranh giới từng cá thể): Vẽ **1 box `ignore_region`** bao quanh toàn bộ cụm đó. Nếu có cá thể đứng tách biệt rõ ràng ở phía trước cụm (`>= 20 px`), gán box đối tượng cho cá thể phía trước và vẽ `ignore_region` cho phần đám đông phía sau.

- **R-06 (Vật hành lý / Phụ kiện mang theo của `person`):**
  - Box `person` bao gồm quần áo, mũ bảo hiểm, ba lô/túi xách đeo sát người.
  - Không kéo rộng box `person` để ôm cả xe đẩy hàng, xe đạp dắt tay, ô (dù) xòe rộng hay kiện hàng lớn đặt rời dưới đất.

- **R-07 (Xe chủ / Ego-vehicle và vật cắt mép `truncated`):**
  - Nếu một phần nắp capo, gương hoặc bảng điều khiển của chính chiếc xe gắn camera (ego-vehicle) xuất hiện ở mép dưới ảnh: **Không gán** phần xe chủ đó.
  - Các phương tiện/người khác bị cắt ở rìa ảnh nhưng phần còn lại vẫn `>= 20 px` chiều cao và nhận diện được lớp: Gán bình thường và đặt `truncated = yes`.

- **R-08 (Phương tiện ngoại lai — Tuk-tuk, Xe 3 bánh, Xe buýt, Xe đạp):**
  - **Xe đạp (bicycle), xích lô đạp, xe kéo tay:** Không có động cơ → **Không gán** (bỏ qua).
  - **Tuk-tuk / Xe lam 3 bánh có động cơ / Xe ba gác máy:** Đề xuất cá nhân `106` là đưa vào `ignore_region` (hoặc tạo quy ước xếp vào lớp cố định khi họp nhóm Pha 2) và tick `can_review` nếu chưa rõ.
  - **Xe buýt cỡ lớn (Bus):** Đề xuất cá nhân `106` là không gán vào `van`/`truck` mà dùng `ignore_region` (hoặc bổ sung định nghĩa trong Pha 2).

---

## 4. Ca khó (Khảo sát thực tế trên 40 ảnh `data/images/`)

| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| `img_001` | Xe bán tải (Suzuki pickup truck) có thùng hàng hở phía sau và nhóm người ngồi trong quán bị bàn ghế che khuất | `R-01` | Gán xe bán tải là `truck` (`truncated=yes`). Gán `person` cho người đứng ngoài (`occluded_level=0`) và các khách ngồi trong quán (`occluded_level=2`) | Theo `taxonomy.json`, xe có thùng hàng riêng tách với cabin thuộc lớp `truck` (không phải `car`). Người ngồi trong quán bị bàn che khoảng 40–60% thân dưới nên chọn mức `2`. |
| `img_004`, `img_016` | Xe 3 bánh Tuk-tuk có mái che và tài xế/khách ngồi bên trong khoang hở | `R-08`, `R-02` | **Chưa chốt về Tuk-tuk, cần họp Pha 2** (Đề xuất cá nhân `106`: không gán Tuk-tuk vào `motorcycle`/`car` để tránh nhiễu hoặc bọc `ignore_region`; còn người ngồi trong khoang Tuk-tuk hở thấy rõ thân người thì vẫn gán `person` với `occluded_level=2`) | Tuk-tuk là xe cơ giới 3 bánh có mái, nằm ở ranh giới giữa `motorcycle` và `car`/`van`. Cần cả nhóm thống nhất 1 quy tắc duy nhất ở Pha 2. |
| `img_009` | Xe khách cỡ nhỏ / minibus (dạng Hyundai County) có hành khách ngồi bên trong chỉ lộ đầu qua ô cửa kính | `R-02`, `R-08` | Gán chiếc xe là `van` (hoặc họp chốt ranh giới `van` vs bus ở Pha 2). **Không gán `person`** cho hành khách ngồi trong khoang kính kín | Theo `R-02`, người ngồi trong cabin kín của ô tô/xe khách chỉ lộ mờ qua cửa kính không được gán `person` để tránh nhiễu đặc trưng người đi bộ/đi xe máy. |
| `img_010` | Xe đạp thồ bán hàng rong (chỉ lộ bánh xe đạp bên dưới thúng hàng) | `R-08` | **Không gán box** cho chiếc xe đạp thồ; chỉ gán `person` và `motorcycle` cho người và xe máy thật xung quanh | Xe đạp (không động cơ) nằm ngoài 5 lớp đối tượng của taxonomy. Phần hàng hóa/thúng tre che trên xe đạp cũng không phải phương tiện cơ giới. |
| `img_011` | Tượng mô hình quái vật Predator khổng lồ bằng nhựa/kim loại, mô hình xe 3 bánh độ trang trí triển lãm và đám đông ở xa | `R-03`, `R-05` | **Không vẽ box** cho tượng Predator. Với xe 3 bánh độ trưng bày: tick `can_review` / đề xuất họp nhóm. Đám đông người ở xa `< 20 px` hoặc chồng lấn dày đặc gom vào `ignore_region` | Tượng Predator là vật vô tri giả hình người (`R-03`). Đám đông ở hậu cảnh quá nhỏ và chồng lấn không thể tách từng box (`R-05`). |
| `img_012` | Xe bán tải (pickup truck) chụp từ phía sau với thùng xe hở chất đầy thùng carton và túi hàng | `R-01` | Gán 1 box `truck` (`truncated=yes`) bao trọn phần nhìn thấy của thân xe bán tải (không cắt rời phần thùng hàng) | Xe bán tải có thùng hàng riêng thuộc lớp `truck`. Hàng hóa nằm gọn trong lòng thùng xe nên box ôm theo biên ngoài của xe. |
| `img_015` | Hai ô tô (1 đen, 1 trắng) chạy ngược chiều bị nhòe chuyển động (motion blur) làm vệt mờ nối liền đầu/đuôi nhau | `R-01` | Gán **2 box `car` riêng biệt** cho xe đen và xe trắng; biên box ước lượng tại ranh giới thân xe thực tế, không kéo box ôm hết vệt nhòe (tick `can_review` ở vùng giao nhau) | Vệt mờ là hiệu ứng phơi sáng của camera, không phải kích thước vật lý của xe. Hai xe vẫn phân biệt rõ 2 khối màu đen và trắng. |
| `img_017` | Tượng đồng người cưỡi ngựa trên bệ đá | `R-03` | **Không vẽ box** cho bức tượng | Tượng điêu khắc không phải người thật; gán `person` sẽ gây lỗi False Positive nghiêm trọng cho mô hình. |
| `img_019` | Xe ô tô vàng phong cách hoạt hình (Dangermouse car) có biển số đang chạy diễu hành trên phố, bên trong có 1 tài xế thật và 1 mascot chuột trắng | `R-01`, `R-03` | Gán chiếc xe vàng là `car` (tick `can_review` để chốt ở Pha 2); gán tài xế người thật là `person` (`occluded_level=2`); **không gán** mascot chuột trắng; đám đông khán giả dày đặc sau rào chắn gom vào `ignore_region` | Chiếc xe là phương tiện cơ giới thật có bánh, đèn, biển số và người lái thật trên đường. Mascot chuột không phải người thật (`R-03`). |
| `img_021` | Cảnh tắc đường rất đông người đi xe máy và ô tô xếp lớp dày đặc từ gần tới xa | `R-02`, `R-05` | Gán từng box `person`, `motorcycle`, `car` cho các xe ở tiền cảnh/trung cảnh thấy rõ (`>= 20 px`, che `<= 85%`). Phần hậu cảnh phía xa nơi xe/người dính đặc và `< 20 px` thì vẽ 1 box `ignore_region` | Đảm bảo tách bạch vùng gán chi tiết và vùng quá dày đặc/quá nhỏ ở xa theo đúng ngưỡng `min_box_height_px = 20`. |
| `img_022` | Xe mô tô cổ có gắn thùng thuyền bên hông (motorcycle with sidecar) và người ngồi trong thùng xe | `R-02`, `R-08` | Gán `person` cho người ngồi (`occluded_level=2`). Với xe mô tô kèm sidecar: gán `motorcycle` và tick `can_review` để nhóm thống nhất ở Pha 2 xem box `motorcycle` ôm cả phần sidecar hay chỉ thân xe chính | Sidecar gắn liền thành một khối cơ khí với xe mô tô; cần thống nhất quy tắc biên box để hai người không bị lệch IoU. |
| `img_023` | Xe xích lô đạp (cyclo) chở khách du lịch trên phố | `R-08`, `R-02` | **Không gán** khung xe xích lô đạp (vì là phương tiện thô sơ dùng sức người, không động cơ). Chỉ gán 2 box `person` riêng biệt cho người đạp xích lô và hành khách ngồi trên ghế | Taxonomy chỉ thu thập phương tiện cơ giới (`car`, `truck`, `van`, `motorcycle`); người ngồi trên xích lô vẫn là người thật trên đường nên gán `person`. |
| `img_024` | Khung vỏ ô tô màu vàng (bản trưng bày cắt khung không kính/động cơ) đặt trên nóc một chiếc ô tô thật màu đen (`AMC Pacer`) | `R-03`, `R-04` | Gán chiếc xe đen bên dưới là `car`. Với khung xe vàng trên nóc: đề xuất **không gán** (hoặc tick `can_review` bàn ở Pha 2) vì chỉ là vỏ mô hình trưng bày rỗng ruột, bánh xe nhỏ kiểu xe đẩy, không phải xe lưu thông thật | Phân biệt giữa "xe chở xe thật" (`img_002` — gán cả xe trên thùng) với "khung mô hình/vỏ xe trưng bày đặt trên nóc" (`img_024` — vật trưng bày). |
| `img_026` | Hai người ngồi sát ôm nhau trên 1 xe máy đang chạy trong hầm (người ngồi sau che một phần lưng người lái trước) | `R-02` | Gán **3 box riêng biệt**: 1 box `person` cho người lái phía trước (`occluded_level=1`), 1 box `person` cho người ngồi sau (`occluded_level=1`), và 1 box `motorcycle` cho chiếc xe máy (`occluded_level=1`). Không gán tàu thuyền in trên tranh tường phía sau | Mỗi cá thể người phải có 1 box `person` riêng ôm sát phần cơ thể nhìn thấy của người đó. Tranh vẽ tàu thuyền trên tường hầm là hình in 2D (`R-03`). |
| `img_029` | Một người đi xe tay ga nhỏ/xe máy điện vác thanh kim loại dài, đi cạnh một người đi xe đạp thường | `R-02`, `R-06`, `R-08` | Người bên trái: gán 1 box `person` (không ôm thanh kim loại dài vào box `person`) và 1 box `motorcycle` cho chiếc xe ga/xe máy điện (có sàn để chân, yếm xe, đèn pha, động cơ). Người bên phải: chỉ gán 1 box `person`, **không gán** chiếc xe đạp bàn đạp | Xe hai bánh có kết cấu thân vỏ scooter/xe máy điện được xếp vào `motorcycle`; xe đạp có bàn đạp và khung gióng mảnh không có động cơ thì bỏ qua (`R-08`). Vật vác dài không tính vào box người (`R-06`). |
| `img_037` | Xe bán tải (pickup truck) gắn thêm thùng kín cao phía sau (`Master 75 Truck Cap`) và có xe buýt ở phía xa | `R-01`, `R-08` | Gán chiếc xe trắng tiền cảnh là `truck` (box ôm trọn cả phần cabin và phần thùng cap gắn trên bệ bán tải). Gán người đi bộ là `person`. Với 2 xe buýt xanh-trắng: đề xuất họp Pha 2 để thống nhất cách xử lý xe buýt cỡ lớn | Thực chất xe trắng là xe bán tải (pickup truck) lắp nắp thùng chuyên dụng rời trên thùng sau (vẫn thấy rõ khớp nối giữa cabin pickup và thùng hàng), nên bản chất là `truck`, không phải `van` liền khối. |

---

## 5. QC và phiên bản

### 5.1. Ngưỡng QC áp dụng (theo `taxonomy.json`)
- **Chiều cao box tối thiểu:** `min_box_height_px = 20` px.
- **Ngưỡng IoU đạt chuẩn:**
  - Box lớn (chiều cao `>= 50 px`): `IoU >= 0.85`.
  - Box nhỏ (chiều cao từ `20 px` đến `< 50 px`): `IoU >= 0.70`.
- **Ngưỡng đồng thuận liên người gán (IAA):**
  - IoU trung bình trên các cặp box ghép (`match_iou >= 0.5`): `>= 0.85`.
  - Tỷ lệ đồng thuận lớp (Class Agreement): `>= 95%`.
- **Ngưỡng nghiệm thu lô (Release):** Tỷ lệ ảnh có lỗi `<= 2%` (với lô 40 ảnh, phải đạt `0/40` ảnh lỗi khi duyệt toàn bộ lô mới được `Release`).
- **Quy trình xử lý ca mơ hồ:** Trong lúc gán độc lập (Pha 3), tuyệt đối không tự ý đổi quy tắc mà tick `can_review = true` hoặc ghi vào `image_issues.csv`. Người điều phối (`106`) và người review (`157`) sẽ họp chốt ở Pha 5 (Calibration).

### 5.2. Lịch sử phiên bản

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| `v0` | Bản khởi đầu của giảng viên | Chỉ có tên 6 lớp và 3 thuộc tính sơ sài, chưa có ngưỡng đo và quy tắc xử lý ca khó. |
| `v0.1-draft-106` | Bổ sung mục tiêu rủi ro FN/FP, bảng ví dụ/phản ví dụ cho 6 lớp, ngưỡng `%` cho `occluded_level` (0/5/30/70%), bộ quy tắc `R-01` đến `R-08` và bảng ca khó thực tế. | Giải quyết sự mơ hồ của `v0` đối với người đi xe máy, tượng/ma-nơ-canh, phản chiếu, xe bán tải, tuk-tuk, xe chở xe và vật nhỏ `< 20 px`. |
