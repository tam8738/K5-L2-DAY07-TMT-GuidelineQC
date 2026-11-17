# Phụ lục đối chiếu ảnh — guideline 127

Ngày 2026-11-17. Rà bổ sung có hỗ trợ AI, sau khi xuất nhãn. Giữ nguyên bản `guideline_127.md` và không đổi `taxonomy.json/rules`. Phụ lục ghi cách áp dụng các quy tắc đã có, không phải bản v1.1 sau calibration hoặc bằng chứng khảo sát độc lập trước gán.

## Phạm vi

Đã khảo sát tổng quan đủ 40 ảnh trên 7 bảng ảnh; riêng 27 ảnh được giao 127 đã mở ảnh gốc và overlay nhãn để kiểm chi tiết. Các quan sát tổng quan ở [survey_40_ai.csv](../../../docs/reviews/127/survey_40_ai.csv) có đánh dấu phạm vi xem. Không gán nhãn thêm cho 13 ảnh ngoài phân công.

## Bằng chứng ba ca khó

- **R-04, img_002.jpg:** 8 xe được chở vẫn là các cá thể riêng; bản hiện tại có 7 nhãn car. Cần kiểm đủ vật và ôm đúng từng xe trước khi chọn mức che.
- **R-05, img_018.jpg:** chân dung trên biển không phải person, còn các xe thật sau hàng rào phải xét riêng. Loại một vật giả không có nghĩa loại cả ảnh.
- **R-03/R-08, img_023.jpg:** xích lô đạp bị loại khỏi lớp phương tiện cơ giới nhưng người vẫn được gán. Không dùng motorcycle để ôm xích lô; kiểm lại xe máy thật ở nền.

## Thử quy tắc người–xe trên hai ảnh

| Ảnh / vùng thử | Cá thể được xét | Cách đếm và phạm vi |
|---|---|---|
| `img_005.jpg`, người áo xanh đội mũ trắng bên phải và xe tay ga đang cầm lái | 1 người và 1 xe máy | 2 box thuộc 2 lớp person/motorcycle; người gồm phần cơ thể nhìn thấy, xe gồm bộ phận cơ khí/gương gắn xe. Không kéo box xe theo đầu người. Đây là vùng thử, không phải tổng số box của cả ảnh đông người. |
| `img_029.jpg`, người mặc đồ tối đang ngồi trên xe máy ở giữa ảnh | 1 người và 1 xe máy | 2 box person/motorcycle. Thanh dài là hàng rời nên không kéo biên xe theo thanh. Người đi xe đạp ở bên phải vẫn cần person nhưng không có box phương tiện cơ giới cho xe đạp. |

Phép thử do lượt rà AI thực hiện, không ghi như kết quả người 127 đã tự thử trước Pha 2.

## Những bẫy cần sửa trong nhãn

- R-01/R-02: clipping box về mép ảnh chỉ sửa giới hạn số học. Với người đi bộ ở img_034, chân kết thúc gần y=439, không phải y=540; phải ôm lại vật và giữ truncated theo phần vật thật.
- R-05: loại tượng ở img_017/img_027, mannequin ở img_033, đồ chơi ở img_038; không dùng ignore cho chính vật giả.
- R-06: không dùng một dải ignore rộng để phủ cả người/xe rõ ở img_021; tách cá thể tiền cảnh trước khi xử lý vùng xa.
- R-09: pickup lắp nắp thùng vẫn truck khi thấy kết cấu thùng tách cabin (img_037); pickup ở img_007 cần phân biệt car/truck.
- R-10/R-11: không ôm hàng rời hoặc vệt phản sáng trên mặt đường vào box xe (img_028/img_029/img_031).

## Trạng thái còn chờ

Bản nhãn cần sửa theo [báo cáo 127](../../qc/review_127_ai.md): 23/27 ảnh có phát hiện. Các thành viên phải ghi nhận xác nhận bản chung theo thực tế; đã có nhãn 106/127 nhưng còn thiếu nhãn 157 để làm IAA/calibration, chưa có người review xác nhận. Không đổi tên phụ lục này thành bản calibrated để bỏ qua các bước còn thiếu.
