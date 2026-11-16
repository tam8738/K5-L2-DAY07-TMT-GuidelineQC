# Guideline gán nhãn — v0.1 — 157

- Phiên bản: v0.1-157
- Ngày: 16-11-2026
- Người viết / duyệt: 157

## 1. Mục tiêu

Tạo nhãn để huấn luyện mô hình phát hiện người và phương tiện trong cảnh đường phố. Đối tượng cần phát hiện là người thật và phương tiện thật có hình dạng nhận diện được, bao gồm xe đang chạy, đang đỗ hoặc đang được vận chuyển. Không suy ra khả năng vận hành, danh tính hay tình trạng pháp lý chỉ từ ảnh.

Ba rủi ro cần kiểm soát:

1. **Bỏ sót:** người bị xe che, người đi bộ trong bóng tối, phương tiện ở mép ảnh hoặc xe nằm trên xe vận chuyển.
2. **Gán thừa/sai lớp:** tượng, ma-nơ-canh, xe đồ chơi, hình in, phản chiếu; nhầm pickup với van; gộp người và xe.
3. **Sai biên/thuộc tính:** box ôm bóng đổ, vệt nhòe, hành lý dài hoặc phần bị che do suy đoán; nhầm cắt mép với che khuất.

Quy tắc phải cho phép hai người áp dụng độc lập trên cùng ảnh và có cùng cách chọn đối tượng, số box, lớp và phạm vi box. Không đặt mục tiêu số box cố định cho toàn ảnh khi chưa kiểm từng cá thể.

## 2. Lớp và thuộc tính

### 2.1. Các lớp

Giữ sáu tên lớp của v0. Một cá thể có tối đa một lớp đối tượng; người và phương tiện là các cá thể khác nhau nên box có thể chồng nhau.

| Lớp | Định nghĩa dùng trong bản đề xuất | Ví dụ trong bộ ảnh | Phản ví dụ / dễ nhầm |
|---|---|---|---|
| `car` | Ô tô con có thân và khoang hành khách đặc trưng sedan, hatchback, wagon hoặc SUV. | Xe trên xe vận chuyển ở img_002; SUV img_012; taxi img_040. | Pickup có thùng riêng là truck; xe đồ chơi img_038 không gán. |
| `truck` | Xe chở hàng có cabin và khu vực/thùng hàng phân biệt; gồm pickup, tải thùng, tải bạt và xe vận chuyển xe. | img_001, img_002, img_012, img_028, img_036, img_037. | Van thân hộp liền khối; tượng hình pickup img_027. |
| `van` | Xe thùng kín cỡ nhỏ có khoang lái và khoang hàng/khách nằm trong một thân hộp liền khối. | Xe màu bạc img_005, img_016. | Tải bạt img_036; pickup gắn nắp thùng img_037; bus img_009. |
| `motorcycle` | Xe máy hoặc mô tô có cấu trúc xe hai bánh gắn động cơ; bao gồm tổ hợp mô tô gắn sidecar cố định. | Xe tay ga img_008; xe img_022; xe bên trái img_029. | Xe đạp, xích lô và tuk-tuk không tự quy vào lớp này. |
| `person` | Người thật trong cảnh nhận diện được, bất kể đi bộ, đứng, ngồi, đi xe hoặc ở sau kính. | Người bán hàng img_003; người đi bộ img_014, img_034; người trên xe img_026. | Tượng img_017; ma-nơ-canh img_033; người in trên biển img_018. |
| `ignore_region` | Vùng có đối tượng cần bỏ khỏi đánh giá chi tiết vì quá nhỏ hoặc không thể tách/nhận diện ổn định. | Cụm người/xe xa dày đặc trong img_021, img_030 khi không thể tách. | Không bao cả ảnh chỉ vì đông; không dùng cho tượng hoặc đồ chơi rõ ràng. |

**Phương tiện ngoài năm lớp đối tượng:** xe đạp, xích lô đạp, xe buýt/minibus có thân xe buýt, tuk-tuk/xe ba bánh dạng cabin không được ép thành car, van hoặc motorcycle. Đề xuất bỏ qua bản thân phương tiện đó; người thật trên đó vẫn xét person. Không tạo lớp mới và không tự bọc ignore_region cho đối tượng ngoài phạm vi đã xác định rõ. Nếu nhóm muốn thu thập chúng, phải thống nhất lớp/định nghĩa và taxonomy trước lượt gán độc lập.

**Trường hợp chưa biết thuộc lớp nào:** không dùng ignore_region để che một quyết định phân lớp chưa được giải quyết. Ghi ảnh, vùng và lựa chọn đang phân vân để reviewer chốt; nếu có box ứng viên phù hợp thì tick can_review. Phân biệt rõ “ngoài phạm vi đã chốt” với “chưa xác định được”.

### 2.2. Thuộc tính và ngưỡng

Mỗi box đối tượng dùng các trường của v0. ignore_region là vùng loại trừ, không đánh giá mức che như một vật thể.

#### `occluded_level`

Giữ nghĩa mức 3 của v0 là **không rõ**, không dùng nó như một mức che nặng thứ ba.

| Giá trị | Nghĩa | Quy ước cụ thể đề xuất |
|---|---|---|
| `0` | Thấy rõ | Không thấy phần bị vật khác che; bỏ qua che cực nhỏ dưới khoảng 5% diện tích hình chiếu đối tượng. |
| `1` | Che ít | Ước lượng phần bị vật khác che từ 5% đến 30%, vẫn xác định rõ cá thể. |
| `2` | Che nhiều | Ước lượng trên 30% bị che, nhưng đủ bằng chứng xác định lớp và cá thể. Không tự loại ở một tỷ lệ 70% hay 85% tùy ý. |
| `3` | Không rõ | Xác định được đối tượng nhưng không đủ căn cứ ước lượng mức che, hoặc mức che không phân biệt được với nhòe/tối; tick can_review. |

Tỷ lệ này là ước lượng diện tích hình chiếu đối tượng trong ảnh, không phải phép đo đã được thực hiện. Ngưỡng 5% và 30% là quy ước bổ sung đề xuất, chưa có trong v0. Phần ngoài khung ảnh được xử lý bằng truncated, không cộng vào phần bị che. Không mặc định người đi xe luôn có mức 1 hoặc mức 2: xét từng người. Kính trong nhìn xuyên được không tự làm tăng mức che; phần thực sự bị khung xe, ghế hoặc vật khác chắn mới tính là che.

#### `truncated`

- `yes`: khung ảnh cắt mất một phần đối tượng, ví dụ người mất chân ở mép dưới hoặc xe mất đầu ở mép trái.
- `no`: không có bằng chứng đối tượng bị cắt bởi khung ảnh. Chạm mép nhưng không mất bộ phận chưa đủ để đặt yes.
- Một vật vừa bị che vừa bị cắt mép có thể đồng thời mang occluded_level=1/2 và truncated=yes.
- Không đặt truncated=yes chỉ vì đối tượng bị cây, xe hoặc người khác che ở giữa ảnh.

#### `can_review`

- Bỏ tick: quy tắc rõ, lớp và biên đủ chắc.
- Tick: nghi nhầm lớp, vật thật/vật giả, nhòe gây khó xác định biên, không rõ mức che hoặc ca mới ngoài quy tắc.
- Cờ này không cho phép chọn lớp tùy tiện. Nếu không thể tạo box có căn cứ, ghi vấn đề cấp ảnh thay vì tạo nhãn giả.

## 3. Quy tắc vẽ box

### R-01 — Biên phần nhìn thấy

Dùng hình chữ nhật nhỏ nhất bao các điểm ngoài cùng nhìn thấy của cùng đối tượng. Không thêm khoảng đệm cố ý. Làm ở độ phóng đại đủ thấy biên, kiểm lại ở tỷ lệ toàn ảnh. Không dùng sai số “đúng 2 px” như một cam kết đo đạc khi biên vốn mờ. Box không vượt khung ảnh, có chiều rộng và chiều cao dương.

### R-02 — Một cá thể, một box

Không chia cùng một người hoặc xe thành nhiều box vì cột, cây hoặc xe khác che ngang. Khi có bằng chứng các phần rời nhau thuộc cùng một vật, một box bao các cực nhìn thấy của vật đó. Không nối hai người chỉ vì đứng sát nhau. Box có thể chứa khoảng trống hoặc vật che nằm giữa các phần của cùng cá thể.

### R-03 — Người và phương tiện tách riêng

Một xe máy có hai người: xét một box motorcycle và hai box person nếu từng người nhận diện được. Box motorcycle bao bánh, thân, tay lái, gương và bộ phận xe; không kéo lên đầu người. Box person bao phần cơ thể nhìn thấy và mũ đang đội, không bao cả xe. Người trên xe đạp/xích lô vẫn có person dù phương tiện ngoài phạm vi. Không tạo person cho xe trống như img_022.

### R-04 — Che khuất và người trong cabin

Chỉ gán khi đủ bằng chứng đó là cá thể thuộc lớp: có thể chỉ thấy đầu, thân trên hoặc phần đặc trưng khác, không bắt buộc đủ toàn thân. Không dựng chiều dài chân hoặc đuôi xe ở vùng bị che. Người thật nhận diện được qua kính vẫn được xét; không gán khuôn mặt in trên xe hay phản chiếu như người trong cabin. Với kính tối không đủ bằng chứng, ghi review, không suy đoán số người ngồi trong xe.

### R-05 — Cắt mép

Gán phần còn nhìn thấy của đối tượng đủ nhận diện, dừng box tại mép ảnh và đặt truncated=yes. Ví dụ xe tiền cảnh img_015, người/xe ở mép img_005 và img_040. Phần bị cắt không làm box vượt ra ngoài ảnh.

### R-06 — Phụ kiện, hành lý và hàng hóa

Bao quần áo, mũ đang đội, giày và túi/ba lô đeo sát cơ thể trong box person. Không kéo box người ra hết đòn gánh, thanh dài, thúng hàng, ô mở rộng hoặc xe đẩy. Với truck, bao kết cấu xe và thùng xe; không mở box theo khối hàng chất nhô cao hay vật rời. Nếu hàng che xe, ghi mức che theo vùng xe bị khuất. Đề xuất này phải giữ nhất quán ở img_003, img_012, img_029 và img_035.

### R-07 — Xe tải, pickup và van

Ưu tiên cấu trúc thân, không dựa vào kích thước đơn thuần hoặc tên hãng. Cabin tách khu vực hàng là truck dù xe nhỏ hoặc gắn nắp thùng kín. Thân hộp liền khối cỡ nhỏ là van. Pickup gắn nắp thùng img_037 không tự thành van; tải bạt img_036 không thành van vì thùng đã kín. Nếu không thấy khớp cấu trúc đủ rõ, can_review thay vì khẳng định từ màu xe.

### R-08 — Xe chở xe và phương tiện trưng bày

Xe thật đang đỗ/trưng bày vẫn thuộc lớp xe; trạng thái không chạy không phải lý do loại. Xe vận chuyển img_002 có truck cho xe chở và các box riêng cho xe được chở đủ rõ. Box xe chở bao khung vận chuyển nhưng không mở theo đầu/đuôi xe hàng vượt ra ngoài khung. Xe thật mang vật trang trí như img_028 vẫn gán truck, không bao tượng ngựa vào box truck.

Vỏ xe/mô hình không có đủ bằng chứng là phương tiện thật phải review. Với img_024, gán các ô tô thật rõ ràng; vật vàng trên nóc cần chốt loại trước khi tạo box car, không suy ra có động cơ hoặc chỉ là đồ chơi từ một ảnh.

### R-09 — Sidecar và xe ba bánh

Mô tô có sidecar gắn cố định là một tổ hợp motorcycle; box bao cả xe chính lẫn sidecar (img_022). Tuk-tuk, xe lam và xe hàng ba bánh dạng cabin không nằm trong định nghĩa motorcycle của bản này; đề xuất bỏ phương tiện, xét người riêng. Không tự tạo box car rồi thêm can_review để né quy tắc. Đây là lựa chọn phạm vi của bản đề xuất, cần nhóm chốt trước v1.0.

### R-10 — Tượng, mô hình, hình in và trang phục

Không gán cho tượng người/ngựa img_017, tượng hình bán tải img_027, ma-nơ-canh img_033, xe đồ chơi img_038 hoặc người in trên biển img_018. Không dùng ignore_region chỉ vì chúng trông giống lớp cần phát hiện.

Không kết luận “vật giả” từ dáng khác thường. Xe diễu hành img_019 có cấu trúc phương tiện rõ nên đề xuất car; người thật cạnh nhân vật chuột xét person. Nhân vật chuột chưa đủ bằng chứng xác định là người mặc đồ hay mô hình: ghi review riêng. Nếu sau đối chiếu xác nhận là người mặc trang phục thì xử lý person theo quy tắc trang phục; nếu mô hình thì loại.

### R-11 — Phản chiếu và xe chủ

Không gán bản sao của người/xe trong gương, mặt nước, kính hoặc thân xe bóng. Mặt gương và phần cửa xe gắn camera img_020 không gán như một xe độc lập; không gán cảnh chỉ xuất hiện trong gương. Đối tượng thật ngoài gương, nếu có và đủ rõ, vẫn xét bình thường. Không mặc định mọi xe sát mép dưới là xe chủ khi không có bằng chứng.

### R-12 — Kích thước nhỏ

Đề xuất chiều cao tối thiểu của box phần nhìn thấy là 20 px trên ảnh gốc; không đo theo kích thước hiển thị khi ảnh đã thu nhỏ. Từ 20 px trở lên vẫn phải nhận diện được lớp. Vật thuộc phạm vi nhưng nhỏ hơn ngưỡng dùng ignore_region sát vật hoặc cụm. Vật rõ là đồ chơi không được đưa vào ignore_region dù kích thước nhỏ.

20 px là quy ước bổ sung của bản này, không phải con số được nêu trong v0; khi triển khai phải đối chiếu ngưỡng đã được lab/nhóm khóa và không tự sửa cấu hình QC để hợp bản viết.

### R-13 — Đám đông và bãi xe

Đông không đồng nghĩa bỏ qua. Tách box cho mỗi cá thể đủ rõ; chỉ dùng ignore_region tại cụm không thể phân ranh giới hoặc quá nhỏ. Không đặt một vùng bỏ qua phủ cả các vật rõ ở tiền cảnh. Nếu box rõ chồng vùng ignore phía sau, điều chỉnh vùng để giảm loại trừ nhầm và ghi review khi không tránh được.

Áp dụng cả đám đông người img_019, img_021, img_032 và xe đỗ img_030. Xe đỗ vẫn là motorcycle nếu là xe thật. Không đặt điều kiện tùy ý “trên 3–4 vật thì gom”.

### R-14 — Nhòe, thiếu sáng, mưa và bóng

Có thể gán nếu còn bằng chứng lớp và biên chính. Không bao vệt phơi sáng, bóng đổ, phản sáng đèn hoặc mặt đường ướt. Nhòe chuyển động không tự là che khuất; truncated chỉ phụ thuộc mép ảnh. Với biên không đáng tin cậy, can_review và mô tả vùng; nếu không xác định được vật, ghi vấn đề cấp ảnh. Không bịa biên chính xác cho img_014/015 chỉ để có box.

### R-15 — Ca chưa chốt

Ghi tên ảnh, vị trí cụ thể, điều quan sát được, hai khả năng và câu hỏi cần quyết định. Trong lượt độc lập không xem nhãn người khác, không thay định nghĩa giữa chừng. Các ca thay đổi ý nghĩa phải đi qua calibration; phạm vi bị ảnh hưởng cần kiểm lại. Không sửa ngược bản cá nhân ban đầu sau họp để tạo cảm giác đã đồng thuận từ đầu.

## 4. Ca khó — đối chiếu đủ 40 ảnh

Bảng nêu quy tắc áp dụng và quyết định đề xuất, không phải danh sách đầy đủ mọi box hoặc kết quả đo pixel. Không gán sẵn tỷ lệ che, số box toàn ảnh hay thuộc tính khi chưa kiểm từng vật trên ảnh gốc.

| Ảnh | Tình huống quan sát | Rule ID | Quyết định đề xuất | Lý do |
|---|---|---|---|---|
| img_001 | Pickup trắng ở tiền cảnh, người đứng và người ngồi sau bàn trong quán. | R-04, R-05, R-07 | truck cho pickup; person riêng cho người thật đủ rõ; xét cắt mép và bàn che từng vật. | Thùng hàng riêng; không bỏ người chỉ vì ngồi trong quán. |
| img_002 | Xe tải khung hai tầng chở nhiều ô tô. | R-02, R-08 | truck cho xe chở, car riêng cho xe được chở đủ rõ; pickup được chở nếu thấy rõ cấu trúc thì truck. | Xe hàng vẫn là phương tiện thật; không gộp cả đoàn thành một box. |
| img_003 | Người gánh hàng, người cạnh xe hai bánh, nền phố đông. | R-03, R-06, R-12 | person không ôm hết đòn gánh/thúng; phân biệt xe máy với xe đạp bằng cấu trúc thấy được. | Đồ mang dài không phải biên cơ thể. |
| img_004 | Hai tuk-tuk có mái và khoang hở. | R-04, R-09 | Bỏ phương tiện theo phạm vi đề xuất; person chỉ khi thực sự nhận diện người trong khoang; chốt nhóm cách xử lý tuk-tuk. | Không ép vào motorcycle chỉ vì có tay lái xe máy. |
| img_005 | Nhiều người đội mũ trên xe máy; van bạc phía sau; nhiều vật cắt mép. | R-03, R-04, R-05 | Tách người và xe; van cho xe bạc; không suy đoán phần thân dưới ngoài ảnh. | Chồng lấn và cắt mép là hai thuộc tính khác nhau. |
| img_006 | Người đi xe máy và người đi xe đạp, taxi bên trái. | R-03, R-09 | person cho người trên cả hai loại xe; motorcycle cho xe máy, car cho taxi; bỏ xe đạp. | Loại phương tiện không quyết định có gán người hay không. |
| img_007 | Pickup và tải thùng trong khu tối, nền ướt. | R-07, R-14 | truck riêng cho xe có cấu trúc cabin/thùng; kiểm vùng tối và gương, bỏ phản sáng nền. | Không biến pickup thành car hoặc van vì góc nhìn trước. |
| img_008 | Xe máy đỗ dày, người ngồi trên xe và đứng giữa dãy. | R-03, R-13 | Tách xe đỗ đủ rõ và người; chỉ ignore cụm thực sự không tách được. | Xe đỗ vẫn thuộc phạm vi. |
| img_009 | Xe có thân bus và nhiều cửa kính hành khách. | R-04, R-09 | Đề xuất ngoài phạm vi bus, không ép vào van; người trong xe chỉ gán khi đủ bằng chứng. | v0 không định nghĩa bus; cần nhóm thống nhất thay vì dựa cỡ xe. |
| img_010 | Người bán hàng giữa xe máy và xe chở rau. | R-03, R-06 | person riêng, motorcycle cho xe máy thật; không gộp rau/thúng vào người; xe hàng chưa rõ động cơ ghi review. | Không suy đoán phương tiện chỉ từ bánh lộ ra. |
| img_011 | Tượng sinh vật lớn, các vật trưng bày giống mô tô, người thật phía sau. | R-10, R-12, R-15 | Loại tượng; gán người thật đủ rõ; vật giống mô tô trưng bày cần chốt là xe thật hay tác phẩm/mô hình. | Chỉ hình dáng bánh/ghi-đông chưa chứng minh là xe thật. |
| img_012 | Thùng pickup mở chất hộp và túi; SUV trái; xe lớn phía trước. | R-06, R-07 | truck cho pickup; car cho SUV; box pickup theo xe, không kéo theo đỉnh túi hàng. | Hàng là vật rời, không phải kết cấu thân. |
| img_013 | Phố đêm, người dưới ánh đèn, xe xa và phản chiếu trên đường. | R-12, R-14 | Gán đối tượng đủ rõ; không gán vệt sáng/bóng đường ướt; kiểm vật nhỏ ở ảnh gốc. | Thiếu sáng không tự là che khuất. |
| img_014 | Hai người đứng rõ phía trước, người/xe di chuyển nhòe phía sau. | R-01, R-14 | Hai person rõ; nền nhòe chỉ gán vật nhận diện được và có biên đủ tin cậy, còn lại ghi review. | Không suy số xe từ một dải nhòe. |
| img_015 | Hai ô tô sát mép tiền cảnh, xe xa nhòe, mặt đường phản sáng. | R-05, R-14 | car riêng cho từng xe rõ, truncated theo mép; không bao bóng hoặc vệt chuyển động. | Không phải mọi mảng đen/trắng trên đường đều là xe độc lập. |
| img_016 | Tuk-tuk, mô tô, van bạc, người sát mép phải. | R-03, R-05, R-09 | motorcycle/person riêng; van cho xe bạc; tuk-tuk ngoài phạm vi đề xuất; person mép xét truncated. | Một ảnh cần áp dụng đồng thời nhiều quy tắc. |
| img_017 | Tượng người cưỡi ngựa, có cọc tiêu trên đầu. | R-10 | Không gán person cho tượng; không tạo ignore chỉ cho tượng. | Vật điêu khắc không phải người thật. |
| img_018 | Chân dung trên bảng quảng cáo, nhiều xe sau hàng rào. | R-04, R-10, R-12 | Bỏ chân dung; xét xe thật phía dưới, không mặc định cả bãi là ignore. | Hình in khác đối tượng bị hàng rào che. |
| img_019 | Xe vàng kiểu hoạt hình, người thật cạnh nhân vật chuột, khán giả sau rào. | R-04, R-10, R-13 | car cho phương tiện rõ; person cho người thật; nhân vật chuột ghi review; tách khán giả đủ rõ. | Không suy khả năng vận hành hoặc bản chất mascot chỉ từ ngoại hình. |
| img_020 | Gương chiếu hậu, cảnh phản chiếu và phần cửa xe chủ. | R-11 | Không gán cảnh chỉ trong gương hoặc bộ phận xe chủ. | Tránh tạo bản sao đối tượng. |
| img_021 | Rất nhiều người/xe máy chồng lớp từ gần tới xa. | R-03, R-12, R-13 | Tách từng người và xe đủ rõ; ignore giới hạn ở cụm xa không tách được. | Không gom cả ảnh đông thành một vùng. |
| img_022 | Mô tô kèm sidecar trên đường rừng, không thấy người ngồi. | R-03, R-09 | Một motorcycle bao cả tổ hợp; không tạo person từ ghế/sidecar. | Sidecar gắn cơ khí là một xe; xe có thể trống. |
| img_023 | Người đạp xích lô nhìn từ sau, ô tô và xe máy trên phố. | R-03, R-04, R-09 | person cho người đạp; người khác chỉ khi thực sự thấy rõ; bỏ khung xích lô. | Không mặc định có thêm hành khách nếu ảnh không đủ bằng chứng. |
| img_024 | Các xe trưng bày, vật dạng vỏ xe vàng trên nóc xe đen. | R-08, R-15 | car cho xe thật rõ; vật vàng cần review về bản chất và phạm vi gán. | Không khẳng định có/không động cơ khi ảnh không cho biết. |
| img_025 | Người trên lối đi ven biển, xe trên đường phía phải. | R-12, R-13 | person cho người đủ rõ; kiểm vật nhỏ trên ảnh gốc; phân loại từng xe nhận diện được. | Khoảng cách xa cần ngưỡng kích thước nhất quán. |
| img_026 | Hai người trên xe máy trong không gian có tranh tường và ánh sáng tối. | R-03, R-10, R-14 | Hai person và một motorcycle cho tổ hợp tiền cảnh; bỏ vật thể chỉ là hình trong tranh. | Tách người lái/ngồi sau; không gán nội dung hình vẽ. |
| img_027 | Vật hình pickup đặt trên bệ tại khu nghĩa trang. | R-10 | Không gán truck cho vật tưởng niệm hình xe. | Hình dạng phương tiện không đủ khi ngữ cảnh cho thấy tượng. |
| img_028 | Pickup thật mang hình ngựa trên thùng; car đỏ phía sau. | R-06, R-08 | truck cho pickup, car cho xe đỏ; không bao ngựa vào truck, không tạo lớp động vật. | Phân biệt kết cấu xe với hàng trang trí. |
| img_029 | Người trên xe máy và xe đạp mang các thanh dài. | R-03, R-06, R-09 | person riêng, motorcycle cho xe có động cơ nhìn thấy; bỏ xe đạp và không kéo person theo thanh. | Tách cơ thể, phương tiện và hàng mang. |
| img_030 | Bãi xe máy dày, người đứng giữa và chân dung trên poster. | R-10, R-13 | Gán xe thật đủ rõ và người thật; bỏ chân dung; ignore phần cụm không tách. | Không loại tất cả xe chỉ vì là bãi đỗ. |
| img_031 | Giao thông ban đêm, nhiều vệt đèn phản chiếu nền ướt. | R-12, R-14 | Gán xe/người đủ bằng chứng; biên theo vật, không theo vệt sáng. | Tránh false positive do phản sáng. |
| img_032 | Hàng người trên vỉa hè đối diện, car cắt mép trái. | R-02, R-05, R-13 | Tách người có biên cá thể; không gom cả hàng; car mép trái đặt truncated nếu bị cắt. | Đứng sát vẫn có thể tách được. |
| img_033 | Ma-nơ-canh trong cửa kính, rèm và phản chiếu. | R-10, R-11 | Không gán person cho ma-nơ-canh hoặc bản phản chiếu. | Đây là vật trưng bày. |
| img_034 | Người đi bộ băng đường, xe máy và car trong ánh sáng ngược. | R-03, R-05, R-14 | person tiền cảnh; tách người/xe; xét cắt mép xe máy phải. | Không bỏ người vì ngược sáng nếu hình thể rõ. |
| img_035 | Xe hàng ba bánh chất cao, mô tô tiền cảnh, car và phương tiện phía sau. | R-03, R-06, R-09 | motorcycle/person tiền cảnh; ba bánh ngoài phạm vi đề xuất; không gộp khối hàng vào người. | Không biến xe hàng ba bánh thành truck khi chưa chốt lớp. |
| img_036 | Xe tải nhỏ phủ bạt đỗ sát lề, các xe phía sau. | R-07 | truck cho xe xanh vì cabin và thùng tách; không gán van chỉ vì thùng kín. | Cấu trúc quan trọng hơn kích thước. |
| img_037 | Pickup trắng gắn nắp thùng cao, bus và người phía trái. | R-07, R-09 | truck cho pickup có nắp; person cho người thật; bus ngoài phạm vi đề xuất. | Nắp thùng không làm mất cấu trúc pickup. |
| img_038 | Tủ kính chứa nhiều xe và nhân vật đồ chơi. | R-10, R-11 | Không gán car/truck/person cho đồ chơi hoặc phản chiếu của chúng. | Vật thu nhỏ trưng bày không phải phương tiện thật trong cảnh. |
| img_039 | Phố có xe máy, xe đạp, người đi bộ và biển chữ. | R-03, R-09, R-12 | Tách người/xe máy, bỏ xe đạp; chỉ xét vật xa đạt tiêu chí. | Không gộp người dắt/đi xe đạp vào lớp xe. |
| img_040 | Người đội mũ sát taxi, tuk-tuk và bus phía sau; gương xe tiền cảnh. | R-03, R-05, R-09, R-15 | person và car rõ; phương tiện ngoài phạm vi bỏ theo quy tắc; gương tiền cảnh chỉ gán xe khi xác định được cá thể/lớp. | Không đoán xe chủ hoặc loại xe từ riêng một chiếc gương. |

## 5. QC và phiên bản

### 5.1. Kiểm tra trước khi giao nhãn

1. **Phạm vi:** đúng ảnh được giao; ảnh không có đối tượng vẫn phải tồn tại trong tập xuất. Không tự bỏ img_017/020/027/033/038 chỉ vì ít hoặc không có nhãn hợp lệ.
2. **Đối tượng:** không bỏ người/xe đủ rõ; không gán đồ chơi, tượng, hình in hoặc phản chiếu. Xe đỗ và xe được chở vẫn được xét.
3. **Lớp:** đúng định nghĩa; đặc biệt kiểm truck/van, tuk-tuk/bus, mô tô-sidecar và vật trưng bày.
4. **Hình học:** ôm sát phần thấy được, không suy phần khuất; không ôm vệt sáng/hàng rời; box trong khung và không trùng cùng cá thể.
5. **Thuộc tính:** kiểm che khuất và cắt mép độc lập; mức 3 giữ nghĩa không rõ; cờ review có mô tả vấn đề.
6. **Bằng chứng:** ca chưa chắc có ảnh và vùng tìm lại được; không ghi số đo, người duyệt, kết quả sửa hoặc Release chưa thực hiện.

### 5.2. Ngưỡng và cách báo cáo

V0 không cung cấp ngưỡng IoU, tỷ lệ đồng thuận hoặc tỷ lệ lỗi nghiệm thu. Vì bản này chỉ xây từ ảnh, v0 và TEMPLATE, không gán các con số đó thành yêu cầu có sẵn của v0. Khi nhóm triển khai, áp dụng đúng cấu hình QC chính thức của lab, giữ nguyên các ngưỡng đã khóa và ghi chúng trong guideline chung.

Quy ước bổ sung đề xuất của bản cá nhân gồm chiều cao tối thiểu 20 px và ranh giới che 5%/30%; cần đối chiếu cấu hình và thảo luận trước khi dùng. Không chỉnh ngưỡng để làm kết quả đạt.

Báo cáo lỗi theo ảnh và theo đối tượng phải có tử số/mẫu số. Độ đồng thuận giữa hai người không chứng minh nhãn đúng nếu cả hai cùng bỏ sót hoặc hiểu sai. Kiểm lại ảnh gốc và quy tắc ngay cả khi kết quả so sánh tốt. Không xác nhận chất lượng biên chỉ bằng việc file JSON hợp lệ.

### 5.3. Chốt ca và thay đổi

- Thành viên 157 xác nhận đề xuất cá nhân; nhóm chốt guideline/taxonomy ở Pha 2 trước lượt gán độc lập.
- Trong lượt gán, giữ nguyên phiên bản đã khóa; dùng can_review hoặc ghi vấn đề cấp ảnh.
- Khi calibration, ghi người chốt bằng mã, quyết định, Rule ID, ảnh/box được sửa, người kiểm lại và phạm vi ảnh/cả lô. Không điền tên người hay kết quả kiểm thay cho việc thực hiện.
- Đổi lớp/phạm vi, cách bao box hoặc cách dùng thuộc tính là thay đổi ý nghĩa; tăng phiên bản và rà mọi ảnh bị ảnh hưởng. Sửa chính tả không đổi nhãn thì ghi là sửa câu chữ.
- Sau họp lưu guideline chung phiên bản mới; không sửa ngược bản cá nhân đã nộp để che khác biệt ban đầu.

### 5.4. Lịch sử phiên bản

| Phiên bản | Thay đổi | Lý do / ca liên quan |
|---|---|---|
| v0 | Bản khởi đầu: sáu lớp, ba thuộc tính, quy tắc ngắn. | Chưa giải quyết ca biên của bộ ảnh. |
| v0.2-157 | Viết lại theo năm phần của TEMPLATE sau khi xem trực tiếp đủ 40 ảnh; bổ sung định nghĩa, 15 quy tắc và bảng 40 ca ảnh. | Người/xe chồng lấn; xe chở xe img_002; mô tô-sidecar img_022; tượng/đồ chơi img_017/027/033/038; phản chiếu img_020; lớp chưa có img_004/009/035; vỏ xe img_024. |

Ghi chú nguồn và hỗ trợ: nội dung được hỗ trợ biên soạn bằng AI từ bộ ảnh và hai tài liệu nêu ở đầu. Chưa có nhãn, số liệu QC hoặc xác nhận reviewer được tạo trong quá trình soạn tài liệu này.
