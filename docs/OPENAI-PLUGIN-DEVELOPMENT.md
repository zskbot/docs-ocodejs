# Phát triển Plugin cho ChatGPT và Codex

Tài liệu tham khảo tiếng Việt dựa trên hướng dẫn chính thức của OpenAI Developers: [Plugin development for ChatGPT and Codex](https://developers.openai.com/plugins).

> Đây là hướng dẫn tổng hợp độc lập trong OCode.js Documentation Hub, không phải tài liệu do OpenAI phát hành và không hàm ý OpenAI chứng thực OCode.js.

## 1. Plugin là gì?

Plugin là gói năng lực mà người dùng có thể khám phá, cài đặt và sử dụng trong ChatGPT hoặc Codex. Danh mục plugin được chia sẻ giữa hai sản phẩm, nhưng một số năng lực có thể chỉ hoạt động trên những bề mặt hoặc môi trường thực thi nhất định.

Một plugin có thể bao gồm:

- **Skills:** hướng dẫn, quy trình và tài nguyên tái sử dụng để mô hình biết khi nào và cách thực hiện một workflow. Skill thường là thư mục chứa `SKILL.md`, có thể kèm scripts, references, templates hoặc assets.
- **MCP server:** dịch vụ cung cấp tools có schema đầu vào/đầu ra, kết nối tới API, dữ liệu hoặc hệ thống bên ngoài và áp dụng xác thực/phân quyền.
- **UI tùy chọn:** giao diện tương tác để xem, so sánh, chỉnh sửa, xác nhận hoặc điều hướng dữ liệu có cấu trúc. Không phải plugin nào cũng cần UI.
- **Lifecycle hooks (khi phù hợp):** lệnh được chạy tại các thời điểm cấu hình trong môi trường Codex hỗ trợ; cần xem xét môi trường thực thi và yêu cầu tin cậy riêng.

Sơ đồ khái quát:

```text
Plugin
├── Skills (workflow guidance)
├── MCP server (optional)
│   ├── Tools + structured results
│   └── UI resources (optional)
└── Lifecycle hooks (when supported/needed)
```

## 2. Chọn kiến trúc nhỏ nhất phù hợp

| Hình thức | Khi nên dùng |
| --- | --- |
| Skills-only | Hướng dẫn và các công cụ sẵn có đã đủ để hoàn thành workflow. |
| MCP-only | Cần gọi công cụ, API hoặc dữ liệu từ dịch vụ bên ngoài nhưng không cần hướng dẫn workflow riêng. |
| Skills + MCP | Skill điều phối quy trình và MCP cung cấp hành động/dữ liệu có kiểm soát. |
| MCP + UI | Người dùng cần tương tác trực quan với dữ liệu có cấu trúc; UI không nên là điều kiện để tool hoạt động. |

Bắt đầu từ use case nhỏ nhất; chỉ bổ sung MCP server, UI hoặc hooks khi chúng giải quyết một nhu cầu cụ thể.

## 3. Quy trình phát triển

### Bước 1 — Plan

1. Xác định người dùng, vấn đề và workflow cụ thể cần giải quyết.
2. Viết các ví dụ yêu cầu (prompts) và tiêu chí thành công có thể kiểm thử.
3. Xác định mỗi bước cần skill, tool MCP hay UI; tránh tạo tool không cần thiết.
4. Định nghĩa quyền truy cập, dữ liệu được gửi đi, tác động phụ và hành động cần xác nhận.

### Bước 2 — Build

- **Build Skills:** viết chỉ dẫn rõ ràng về thời điểm sử dụng, đầu vào, từng bước, kết quả mong đợi và cách xử lý lỗi. Đưa scripts/tài nguyên phụ trợ vào khi cần và kiểm tra nguồn gốc của chúng.
- **Build MCP server:** định nghĩa tools với tên dễ hiểu, mô tả chính xác, schema chặt chẽ, kết quả rõ ràng và giới hạn hành vi. Server chỉ nên xử lý dữ liệu được chủ đích cung cấp cho tool.
- **Authentication & authorization:** nếu truy cập dữ liệu riêng tư hoặc thực hiện thao tác ghi, yêu cầu đăng nhập và kiểm tra quyền. Hướng dẫn hiện hành mô tả OAuth 2.1 theo MCP authorization spec; kiểm tra token, issuer, audience, thời hạn và scopes ở phía server. Không xem token nhận được là đáng tin chỉ vì client đã gửi nó.
- **Optional UI:** chỉ xây khi tương tác trực quan mang lại giá trị. Tuân theo UI guidelines, giới hạn iframe origin và giải thích rõ nhu cầu nhúng khi gửi duyệt.
- **Package:** đóng gói skills, MCP server, metadata và UI/hooks cần thiết thành plugin theo định dạng, cấu trúc và quy trình hiện hành của OpenAI.

### Bước 3 — Test

1. Kiểm thử từng skill/tool và các trường hợp lỗi, dữ liệu thiếu, quyền bị từ chối, token hết hạn, timeout và phản hồi không hợp lệ.
2. Kiểm tra hành vi an toàn cho các hành động ghi, xóa, thanh toán hoặc gửi dữ liệu ra ngoài; yêu cầu xác nhận ở nơi phù hợp.
3. Kiểm thử trải nghiệm end-to-end trên ChatGPT và Codex ở các bề mặt được hỗ trợ, bao gồm desktop và mobile khi có UI.
4. Kiểm tra hiệu năng, độ tin cậy, thông báo lỗi và phương án dự phòng.
5. Với plugin có xác thực, chuẩn bị tài khoản demo đầy đủ tính năng và dữ liệu mẫu theo yêu cầu submission hiện hành.

### Bước 4 — Submit & publish

- Kết nối và thử plugin trong môi trường phát triển.
- Kiểm tra metadata, prompts gợi ý, chính sách quyền riêng tư và các yêu cầu đánh giá.
- Gửi plugin qua quy trình submission để OpenAI xem xét; chỉ coi là phát hành sau khi quy trình được chấp thuận và listing xuất hiện đúng nơi.
- Theo dõi lỗi, cập nhật bảo mật, duy trì dịch vụ và kiểm tra lại sau mỗi thay đổi quan trọng.

Tên bước và yêu cầu cụ thể có thể thay đổi; luôn đối chiếu tài liệu chính thức trước khi gửi duyệt.

## 4. Ví dụ plugin trong tài liệu OpenAI

Trang hướng dẫn chính thức giới thiệu các ví dụ như:

- **Computer Use:** điều khiển ứng dụng Mac.
- **Chrome Control:** điều khiển Chrome.
- **Spreadsheets:** tạo và chỉnh sửa tệp bảng tính.
- **Presentations:** tạo và chỉnh sửa slide.
- **Data Analytics:** trả lời câu hỏi về dữ liệu sản phẩm và kinh doanh.
- **GitHub:** triage issues, pull requests và CI.

Đây là các ví dụ minh họa trong hệ sinh thái tài liệu OpenAI; khả năng có sẵn và quyền truy cập phụ thuộc sản phẩm, tài khoản, cấu hình và trạng thái hiện hành.

## 5. Metadata, UI và khả năng khám phá

- Tên và mô tả phải rõ ràng, chính xác, phản ánh hành vi thực tế; không dùng tuyên bố quảng bá không kiểm chứng.
- Mỗi tool cần tên duy nhất, ưu tiên động từ dễ hiểu; mô tả phải nói rõ tool làm gì, khi nào dùng, giới hạn và tác động phụ.
- Cung cấp prompts ví dụ hữu ích để người dùng bắt đầu.
- Nếu có UI, tuân thủ hướng dẫn bố cục, tương tác, khả năng tiếp cận và bảo mật; UI là tùy chọn, không thay thế tool phía server.
- Chỉ yêu cầu quyền cần thiết và giải thích minh bạch vì sao cần quyền đó.

## 6. Bảo mật và quyền riêng tư

Checklist trước khi phát hành:

- [ ] Chỉ yêu cầu quyền tối thiểu cần cho use case.
- [ ] Kiểm tra xác thực, scopes, audience, expiry và quyền ở phía server mỗi lần gọi tool.
- [ ] Không commit API keys, OAuth secrets, access tokens, dữ liệu cá nhân hoặc tệp môi trường có bí mật.
- [ ] Rà soát scripts, dependencies, nguồn skill và mọi hành động có thể chạy mã.
- [ ] Gắn nhãn và bảo vệ đúng các thao tác ghi/phá hủy; xác nhận trước hành động có hậu quả đáng kể.
- [ ] Hạn chế dữ liệu được gửi ra ngoài theo đúng mục đích, có thông báo quyền riêng tư rõ ràng.
- [ ] Kiểm tra lỗi, log và dữ liệu đầu ra để tránh rò rỉ secrets hoặc thông tin người dùng.
- [ ] Kiểm thử an toàn, độ tin cậy và giao diện trên các bề mặt được hỗ trợ.
- [ ] Đọc lại [Plugin guidelines](https://developers.openai.com/plugins/plugin-guidelines) và các yêu cầu bảo mật liên quan trước khi gửi.

## 7. Tài liệu chính thức

- [Plugin development for ChatGPT and Codex](https://developers.openai.com/plugins)
- [Plugin architecture](https://developers.openai.com/plugins/concepts/plugins)
- [Plugin guidelines](https://developers.openai.com/plugins/plugin-guidelines)
- [Authentication](https://developers.openai.com/plugins/build/auth)
- [OpenAI Developers plugin UI](https://developers.openai.com/plugins) — xem phần UI guidelines và UI reference từ trang tài liệu chính.

## Phạm vi tài liệu

Đây là bản tóm lược và liên kết tới nguồn chính thức, không phải bộ SDK hay plugin đang hoạt động. Việc thêm hướng dẫn này vào repository không tạo, cài đặt, gửi duyệt hoặc xuất bản plugin tự động.
