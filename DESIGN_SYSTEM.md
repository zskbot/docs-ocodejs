# OCode.js — Giao diện mặc định và quy tắc bảo vệ

**Trạng thái:** Chuẩn giao diện chính thức  
**Phạm vi:** OCode.js và toàn bộ hệ sinh thái Velclaw/zskbot sử dụng giao diện OCode.js  
**Nguồn chuẩn:** Trang chủ và tài liệu OCode.js trong repository này

## Quy tắc bắt buộc

1. Giao diện OCode.js đang được duy trì tại `index.html` là **giao diện mặc định, giao diện chính và nguồn tham chiếu thiết kế**.
2. Không tự ý sửa, thay thế, làm mới, tái cấu trúc, đổi bố cục, màu sắc, typography, logo GIF, khoảng cách, điều hướng hoặc responsive của giao diện chuẩn này.
3. Chỉ được thay đổi giao diện chuẩn khi chủ dự án yêu cầu rõ ràng và trực tiếp cho thay đổi cụ thể đó. Yêu cầu sửa chức năng, tài liệu, API hoặc nội dung không được hiểu là cho phép thay đổi giao diện.
4. Mọi dự án, website, trang tài liệu, dashboard và thành phần trong hệ sinh thái Velclaw/zskbot phải tuân theo ngôn ngữ thiết kế OCode.js làm mặc định khi áp dụng hệ giao diện này. Không tự tạo một hệ giao diện cạnh tranh hoặc lệch chuẩn.
5. Khi tích hợp vào dự án khác, giữ nguyên các đặc điểm nhận diện cốt lõi: nền tối/đen, chữ sáng, điểm nhấn xanh/tím tinh tế, phong cách tối giản, logo OCode.js đúng tài sản, nhịp khoảng cách gọn và responsive cho điện thoại.
6. Không được dùng việc đồng bộ tài liệu, cập nhật nội dung, sửa lỗi chức năng hoặc tự động hóa làm lý do ghi đè CSS/HTML giao diện chuẩn.
7. Trước mọi thay đổi có thể ảnh hưởng giao diện, phải kiểm tra quy tắc này và dừng lại nếu chưa có yêu cầu trực tiếp cho phép. Không tự suy diễn sự cho phép.
8. Các dự án tích hợp nên liên kết hoặc tham chiếu tài liệu này thay vì sao chép rồi tự ý biến đổi giao diện. Những tùy chỉnh riêng của dự án phải được tách biệt, không sửa ngược nguồn chuẩn OCode.js.

## Quy trình thay đổi được phép

- Chỉ thay đổi khi có yêu cầu cụ thể, trực tiếp từ chủ dự án.
- Giới hạn thay đổi đúng phạm vi đã yêu cầu.
- Không gộp chỉnh sửa giao diện không liên quan.
- Xác minh trên màn hình điện thoại và desktop nếu thay đổi tác động đến giao diện.
- Ghi rõ file, phạm vi và kết quả kiểm tra trong báo cáo.

## Bản hiện hành

Trang chuẩn: https://zskbot.github.io/docs-ocodejs/  
Repository: https://github.com/zskbot/docs-ocodejs  
Logo động: https://github.com/zskbot/pages_logo/blob/main/OCode.js/ocode-js-logo-animated.gif

Quy tắc này là chỉ dẫn bảo vệ dự án; nó không tự tạo cơ chế khóa kỹ thuật trên các repository khác. Mỗi repository/automation cần tham chiếu và tuân thủ quy tắc này.
