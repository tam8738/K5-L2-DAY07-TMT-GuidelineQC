# Rà soát ảnh và nhãn 127 — có hỗ trợ AI

Ngày: **2026-11-17**. Đối tượng kiểm: bản xuất `127.zip`, 27 ảnh, 90 annotation. Đây là rà soát bổ sung sau xuất nhãn; không thay cho lượt gán độc lập hoặc vòng QC do thành viên 157 thực hiện.

Nguồn `submission/labels/127.json`, SHA-256: `c7e2bf3be1d32a1a3b308b92d53a0584eb9dd2314a3a3163224c9874946ef35d`. Nhãn nguồn được giữ nguyên để truy vết. ID trong báo cáo là **ID COCO của bản 127 mới**; có thể khác số hiển thị trong CVAT và bản xuất trước.

## Kết quả và giới hạn

- Validator: đạt; đủ 27/27 ảnh, lớp/thuộc tính/hình học hợp lệ, không còn box vượt biên.
- Đã mở ảnh gốc và overlay cho đủ **27/27 ảnh**. Ghi **79 phát hiện/nhóm vấn đề** trên **23 ảnh**; một phát hiện có thể liên quan nhiều box hoặc nhiều vật bỏ sót.
- 4 ảnh `017`, `027`, `033`, `038`: không xác định thêm mục tiêu thật trong lượt rà; tượng, ma-nơ-canh, đồ chơi được loại theo R-05. Đây không phải phiếu QC sạch do người review ký.
- **Bản 127 cần sửa thêm** trước khi bàn giao. Sửa 7 đáy vượt biên trước đây chỉ giải quyết tính hợp lệ tọa độ; nhiều box vẫn không ôm vật thật.
- Các tọa độ trong JSON là đề xuất nhìn ảnh, cần đối chiếu lại và xác định đúng cá thể trước khi dùng. Không tự áp dụng đề xuất còn nghi vấn vào bản độc lập.
- Chưa có IAA, calibration, nhãn cuối hoặc quyết định Release. Đã đồng bộ COCO độc lập 106 từ GitHub; còn thiếu COCO 157 và xác nhận nhóm.

## Mở bằng chứng

- [Ảnh gốc/overlay và liên kết tới từng frame CVAT](../../docs/reviews/127/index.html).
- [Checklist 27 ảnh](review_127_ai_checklist.csv).
- [Phát hiện và tọa độ đề xuất](review_127_ai_findings.json).
- [Phụ lục đối chiếu guideline từ ảnh](../guidelines/individual/guideline_127_review.md).

## Danh sách theo ảnh

| Ảnh | Số nhóm vấn đề | Quan sát và việc cần sửa |
|---|---:|---|
| [img_001.jpg](http://localhost:8080/tasks/1/jobs/1?frame=0) | 3 | Box truck #1 bỏ phần thùng xe bên trái; box người #5 lệch khỏi người phụ nữ đứng và chưa ghi nhận phần chân bị cắt ở mép dưới. Cần ôm lại từng cá thể, đặc biệt #6 đang chứa nhiều phần xe thay vì người đàn ông tóc bạc; rà các box #2–#4 để tách đúng người ngồi. |
| [img_002.jpg](http://localhost:8080/tasks/1/jobs/1?frame=1) | 3 | Ảnh có tám xe con được chở nhưng hiện chỉ có bảy box car #8–#14; thiếu xe trắng cuối tầng trên. Các box xe bị lệch hoặc dư nền, đặc biệt #11 và #14; người #15 cần thu nhỏ theo người đứng cạnh đuôi và đổi truncated thành no sau khi kiểm lại. |
| [img_004.jpg](http://localhost:8080/tasks/1/jobs/1?frame=2) | 2 | Hai lớp tuk_tuk #16–#17 phù hợp với hình xe, nhưng box #16 bỏ biển TAXI trên mái và #17 dư nhiều nền. Cần thêm box person riêng cho người ngồi trong mỗi xe, rồi kiểm các phần cơ thể bị che trước khi chốt biên. |
| [img_005.jpg](http://localhost:8080/tasks/1/jobs/1?frame=3) | 4 | Box van #18 bỏ phần thân dưới và chưa thể hiện việc xe ra khỏi mép phải. Ba box người #20–#22 đang bao nhiều cá thể; cần tách người tiền cảnh, người áo xanh và những người phía sau, đồng thời bổ sung các xe máy nhìn thấy riêng biệt. |
| [img_007.jpg](http://localhost:8080/tasks/1/jobs/1?frame=4) | 2 | Xe pickup chở thùng giữa ảnh #24 phải được rà đổi từ car sang truck theo kết cấu cabin và thùng tách biệt. Cả #23 và #24 đều dư nền hoặc bỏ phần xe nhìn thấy, nên cần ôm lại box; #23 bị cắt ở mép phải. |
| [img_008.jpg](http://localhost:8080/tasks/1/jobs/1?frame=5) | 5 | Box person #30 phủ mũ và xe đỗ mà không thấy người tương ứng, cần xác minh để bỏ nhãn thừa. Box #26 bỏ tay/chân người lái và #28 phủ nhiều cá thể; cần ôm lại từng người, rà các xe #27–#29 và bổ sung người rõ ở phía sau. |
| [img_010.jpg](http://localhost:8080/tasks/1/jobs/1?frame=6) | 5 | Box person #32 đang gộp người lớn ngồi xe, trẻ đội mũ đỏ và người bán; cần tách thành các cá thể. Các box xe #31, #33, #35 và người #34 lệch hoặc dư nền; kiểm lại truncated của #33/#35 và bổ sung xe tay ga đỗ phía phải. |
| [img_012.jpg](http://localhost:8080/tasks/1/jobs/1?frame=7) | 4 | Box car #36 kéo xuống nền; box truck #37 đặt lên biển/tường và hàng hóa thay vì xe tải nền, cần chuyển về xe thật. Với pickup tiền cảnh #38, cần kiểm tiêu chí xe chủ và ghi truncated=yes nếu giữ nhãn vì xe ra mép ảnh; rà xe con nhỏ ở giữa đường. |
| [img_013.jpg](http://localhost:8080/tasks/1/jobs/1?frame=8) | 4 | Box #39 gộp hai người đi bộ và phần phản chiếu dưới đường, cần tách hai person theo phần cơ thể thật. Box person #40 phủ tượng/cây, cần xác minh để loại; thu hẹp hoặc bỏ các vùng ignore #41–#42 không có căn cứ và rà bổ sung car trắng bên trái. |
| [img_014.jpg](http://localhost:8080/tasks/1/jobs/1?frame=9) | 3 | Box người #43 cắt mất đỉnh đầu và bàn tay trái; #44 kéo quá rộng và quá thấp xuống nền đường. Cần ôm lại phần cơ thể nhìn thấy và kiểm riêng những người/xe máy bị nhòe ở hai bên, không loại chỉ vì ảnh mờ. |
| [img_017.jpg](http://localhost:8080/tasks/1/jobs/1?frame=10) | 0 | Chủ thể là tượng người cưỡi ngựa, nên không tạo nhãn person hoặc vùng ignore cho tượng theo R-05. Ảnh hiện không có annotation; nhận xét này là hỗ trợ AI, không thay cho phiếu QC của người kiểm. |
| [img_018.jpg](http://localhost:8080/tasks/1/jobs/1?frame=11) | 1 | Ảnh hiện trống nhãn dù còn ít nhất năm xe thật phía dưới, sau hàng rào. Loại chân dung in trên biển quảng cáo là đúng, nhưng cần gán riêng các xe; kiểm cắt mép trái/phải và mức che bởi hàng rào. |
| [img_019.jpg](http://localhost:8080/tasks/1/jobs/1?frame=12) | 3 | Box người #45 ôm cả thân xe thay vì chỉ phần đầu/vai tài xế nhìn thấy; cần thu box và kiểm lại mức che khuất. Nhiều khán giả rõ, cao hơn 20 px đang bị bỏ sót; con chuột trang trí phải loại. Xe diễu hành có bánh, biển số và người lái cần được nhóm xác nhận cách phân lớp trước khi thêm nhãn. |
| [img_021.jpg](http://localhost:8080/tasks/1/jobs/1?frame=13) | 2 | Các cặp box #46–#51 không bám sát từng người và xe; có box trộn hai người hoặc kéo ra vỉa hè. Dải ignore #52 phủ cả nhiều cá thể lớn, tách được nên cần thu hẹp sau khi rà từng người/xe. Đây là ảnh đông đối tượng, cần kiểm lại toàn cảnh ở độ phân giải gốc. |
| [img_022.jpg](http://localhost:8080/tasks/1/jobs/1?frame=14) | 1 | Box motorcycle #53 bao nhiều cây và nền đường, đồng thời cắt tay lái bên trái. Cần thu box theo cả xe máy và sidecar gắn liền, kiểm lại occluded_level; không thấy người thật trên xe. |
| [img_023.jpg](http://localhost:8080/tasks/1/jobs/1?frame=15) | 4 | Box #54 và #57 quá rộng, quá thấp, không ôm đúng người lái xích lô và ô tô. #55 không bao một người riêng ở vị trí hiện tại; #56 cần kiểm lại vì xích lô đạp không thuộc lớp motorcycle. Còn người và xe máy thật ở vỉa hè/nền sau chưa được gán; không tự đặt truncated=yes chỉ vì box cũ từng vượt đáy ảnh. |
| [img_025.jpg](http://localhost:8080/tasks/1/jobs/1?frame=16) | 5 | Box người #59, #60 lệch xa phần cơ thể nhìn thấy và chứa nhiều nền. #58, #61 đang bao vỉa hè hoặc nhiều vật thay vì một xe; cần xác nhận đúng cá thể rồi sửa biên/lớp. Còn taxi xanh-vàng, người đi bộ và người lái xe có thể nhận diện chưa được gán. |
| [img_027.jpg](http://localhost:8080/tasks/1/jobs/1?frame=17) | 0 | Chiếc pickup là tượng đài đặt trên bệ trong nghĩa trang, không phải xe thật để gán truck. Ảnh hiện không có annotation phù hợp với việc loại chủ thể theo R-05; chưa xác nhận QC người thật. |
| [img_028.jpg](http://localhost:8080/tasks/1/jobs/1?frame=18) | 2 | Box truck #62 bỏ mất phần đuôi và đáy bánh, đồng thời bao lên tượng ngựa; cần vẽ lại theo kết cấu xe thật. Box car #63 lệch sang phải và xuống dưới so với SUV đỏ phía sau; thu sát phần SUV còn nhìn thấy và kiểm lại mức che khuất. |
| [img_029.jpg](http://localhost:8080/tasks/1/jobs/1?frame=19) | 5 | Cả bốn box #64–67 còn sai vị trí dù tọa độ đáy đã nằm trong ảnh: box người bỏ đầu/thân và bao nhiều mặt đường, box motorcycle bỏ biên xe. Cần khớp lại #66 với đúng cá thể, tách người đi xe đạp khỏi xe ngoài phạm vi và bổ sung những người thật còn thiếu. Các vật chính kết thúc trước y414 nên không ép box xuống mép ảnh hoặc tự bật truncated. |
| [img_031.jpg](http://localhost:8080/tasks/1/jobs/1?frame=20) | 2 | Các box #68–72 đều kéo xuống vùng đường và phản sáng phía dưới xe; cần thu sát phần thân, bánh và biên xe thực. Thiếu motorcycle/người ở tiền cảnh trái cùng một số người đi đường và người lái; phóng to ảnh tối để tách cá thể trước khi thêm box. |
| [img_033.jpg](http://localhost:8080/tasks/1/jobs/1?frame=21) | 0 | Đã xem ảnh gốc và bản không có box: mannequin và hình thời trang in không thuộc person theo R-05. Chưa xác định thêm người hoặc phương tiện thật cần gán; đây là quan sát có AI hỗ trợ, không phải phiếu QC sạch của người review. |
| [img_034.jpg](http://localhost:8080/tasks/1/jobs/1?frame=22) | 6 | Người #73 có bàn chân kết thúc gần y439, còn box hiện xuống y540 và cắt mất tay trái; car #74 cũng nằm thấp hơn xe thật. Các cặp #75/#78 và #76/#79 phần lớn phủ đường trống, cần khớp lại đúng người và motorcycle; kiểm riêng motorcycle #77 với người tiền cảnh sát mép phải. Còn nhiều cặp người/xe đủ lớn chưa được gán. |
| [img_036.jpg](http://localhost:8080/tasks/1/jobs/1?frame=23) | 3 | Truck #81 thiếu phần sau, nóc khung và đáy bánh; xe nằm trọn ảnh nên cần đổi truncated từ yes sang no sau khi đối chiếu biên. Hai vùng ignore #80/#82 bao nhiều mặt đường và phủ cả phần xe rõ; tách motorcycle nhận diện được, chỉ giữ ignore cho phần thực sự không tách được. Kiểm thêm người bị truck che ở phía sau. |
| [img_037.jpg](http://localhost:8080/tasks/1/jobs/1?frame=24) | 4 | Person #83, truck #84 và bus #85 đều sai biên, bỏ phần trên và bao nhiều đường phía dưới. Truck có kết cấu pickup gắn khoang nên giữ lớp truck; bus trái bị cắt ở mép ảnh nên cần truncated=yes. Có bus thứ hai phía sau pickup chưa có box riêng, cần gán phần còn nhìn thấy. |
| [img_038.jpg](http://localhost:8080/tasks/1/jobs/1?frame=25) | 0 | Đã xem ảnh gốc và bản không có box: các xe, nhân vật và xe lăn trong tủ đều là đồ chơi/mô hình, được loại theo R-05. Chưa xác định mục tiêu thật cần thêm; không dùng quan sát này thay cho QC độc lập của người review. |
| [img_040.jpg](http://localhost:8080/tasks/1/jobs/1?frame=26) | 6 | Person #86 thiếu đỉnh mũ và tay, đồng thời bị cắt ở đáy ảnh nên cần kiểm lại truncated=yes; car #87 bỏ nóc và biển taxi. Các box SUV #88, bus #89 và tuk_tuk #90 đều cần thu lại theo biên thực; bus bị cắt ở mép trên và không thể giữ mức che khuất 0. Kiểm thêm tuk-tuk phía trái, người thật qua kính và phần motorcycle tiền cảnh; tránh gán hình người in trên quảng cáo. |

## Trình tự xử lý tiếp

1. Giữ bản độc lập hiện tại và bản ZIP nguồn; dùng checklist để sửa đúng từng vật trên CVAT. Đối chiếu số ID theo ảnh/lớp/vị trí, không ghép theo số ID đơn lẻ.
2. Kiểm lại các vật bị bỏ sót, box gộp cá thể và lớp phương tiện trước; sau đó rà occluded_level/truncated/can_review. Không gán motorcycle cho xe đạp/xích lô đạp; không đặt truncated=yes chỉ vì box cũ bị cắt về mép ảnh.
3. Xuất bản sửa theo tên phiên bản mới, chạy lại validator và đối chiếu ảnh. Chưa thay bản độc lập bằng bản sửa calibration khi nhóm chưa chốt quy trình lưu phiên bản.
4. Khi nhận thêm bản độc lập 157 để đủ nhóm 106/127/157, chạy IAA rồi calibration/QC theo GUIDE.md. Người chốt/người kiểm lại phải được ghi theo thực tế.
5. Lượt kiểm bài nộp sau đồng bộ báo 5 lỗi: thiếu nhãn 157, thiếu ghi chú 106/157, tập thành viên nhãn chưa đủ và thiếu bằng chứng QC_REPORT. Log tại [evidence_127](evidence_127/status.json). Không sửa script/ngưỡng để làm kết quả đạt.
