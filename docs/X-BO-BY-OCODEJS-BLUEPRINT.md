# x-bo by OCODE.js — Product & Design Blueprint

**Trạng thái:** đề xuất thiết kế và lộ trình sản phẩm; không phải xác nhận rằng mọi tính năng đã được triển khai.  
**Liên quan:** [repository X-BO](https://github.com/zskbot/X-BO) · [OCode.js](https://github.com/Velclaw/OCodejs)

## 1. Định vị sản phẩm

**x-bo by OCODE.js** được định hướng là trợ lý phát triển web bằng AI: chuyển mô tả văn bản, ảnh tham khảo và yêu cầu thiết kế thành giao diện cùng mã nguồn có thể xem xét, kiểm thử và phát triển tiếp.

- **Đối tượng:** lập trình viên, UI/UX designer và product manager.
- **Đầu ra mục tiêu:** mã nguồn có cấu trúc, bản xem trước, danh sách tác vụ và hướng dẫn chạy/kiểm thử.
- **Nguyên tắc:** không gọi mã sinh ra là “production-ready” trước khi vượt qua kiểm thử, rà soát bảo mật, xác minh cấu hình và quy trình phát hành.
- **Phân định thương hiệu:** X-BO hiện là một web-based AI agent với frontend React/Vite và backend Node.js/provider-ready. Các năng lực builder được mô tả ở đây là hướng phát triển, không khẳng định đã có sẵn trong repository.

## 2. Bộ khung kiến trúc

```text
x-bo by OCODE.js
├── 1. Input & Conversation
│   ├── Prompt / chat (text first; voice when supported)
│   ├── Image and file attachments
│   └── Templates + design-system references
├── 2. AI Orchestration
│   ├── Planner → task list and acceptance criteria
│   ├── Code generation → files, components, tests
│   └── Integration adapters → API / database (permission-gated)
├── 3. Interactive Workspace
│   ├── Live preview / responsive viewport
│   ├── Design mode (select, inspect, refine)
│   ├── Code view / diff / undo
│   └── Test results and diagnostics
└── 4. Export & Release
    ├── GitHub branch + reviewable diff / pull request
    ├── Preview environment and health checks
    └── Deploy only after explicit approval and release gates
```

### Lớp 1 — Input & conversation

- Chat prompt với ví dụ gợi ý như “Tạo dashboard doanh thu Dark Mode”.
- Đính kèm hình ảnh/mẫu UI; nhập file thiết kế chỉ khi adapter tương ứng được xây dựng và kiểm thử.
- Template khởi đầu như SaaS landing page, dashboard, contact form và calculator.
- Hệ thống thiết kế dùng tokens tập trung: màu sắc, typography, spacing, border, breakpoints và component states.

### Lớp 2 — AI / orchestration

- **Planner:** phân tích yêu cầu, tạo task, xác định phụ thuộc và tiêu chí nghiệm thu.
- **Code generator:** sinh component, styles, logic, tests và ghi rõ file được thêm/sửa.
- **Integration engine:** kết nối API/database qua adapter được cấp quyền; không tự ý tạo hoặc thay đổi dữ liệu production.
- **Context and provider layer:** tách nhà cung cấp mô hình khỏi workflow, giữ secrets ở môi trường server-side và hỗ trợ timeout/error handling.

### Lớp 3 — Interactive editor

- **Live Preview:** xem trạng thái giao diện ở mobile/tablet/desktop và tương tác với controls.
- **Design Mode:** chọn phần tử, điều chỉnh tokens/layout và hiển thị thay đổi dự kiến.
- **Code Mode:** xem file, diff và kết quả sinh mã; cho phép hoàn tác thay đổi.
- **Quality panel:** hiển thị lint/test/build/accessibility/security findings; không che giấu lỗi hoặc tự đánh dấu pass khi chưa chạy.

### Lớp 4 — GitHub & release

- Tạo branch riêng, hiển thị diff, chạy kiểm tra và mở pull request.
- Preview/staging là bước xác minh trước khi phát hành.
- Production deploy phải là thao tác có chủ đích, được bảo vệ bằng quyền và release gates; không tự động deploy chỉ vì AI sinh xong mã.
- Báo cáo trạng thái rõ ràng: **PASS / FAIL / PENDING / NOT VERIFIED**.

## 3. Luồng làm việc đề xuất

```text
Prompt / Image / Template
          ↓
   Plan + Acceptance Criteria
          ↓
 Generate Files + Tests + Diff
          ↓
 Preview ↔ Design Mode ↔ Code Mode
          ↓
 Lint / Test / Build / Security Checks
          ↓
 GitHub Branch + Pull Request
          ↓
 Preview / Staging Verification
          ↓
 Explicit Approval → Release
```

1. **Khởi tạo:** nhập prompt hoặc chọn template, chỉ rõ mục tiêu, framework, dữ liệu giả lập và tiêu chí hoàn thành.
2. **Lập kế hoạch:** AI đề xuất tasks, file dự kiến thay đổi và các câu hỏi còn thiếu trước khi thực thi tác động lớn.
3. **Sinh mã:** tạo thay đổi theo từng nhóm nhỏ; giữ diff có thể đọc và không ghi đè file ngoài phạm vi.
4. **Xem trước:** chạy ứng dụng trong sandbox/preview được cô lập; hiển thị lỗi và trạng thái responsive.
5. **Tinh chỉnh:** dùng Design Mode hoặc prompt tiếp theo; cập nhật diff và chạy lại các kiểm tra liên quan.
6. **Đồng bộ:** đẩy branch và mở PR; không commit secrets hoặc dữ liệu người dùng.
7. **Phát hành:** chỉ sau khi checks xanh, review hoàn tất, cấu hình/health được xác minh và người có thẩm quyền phê duyệt.

## 4. Hướng dẫn sử dụng — giao diện mục tiêu

### Chat prompt

Ví dụ prompt:

> Tạo dashboard quản lý doanh thu bằng React, giao diện Dark Mode, có biểu đồ theo tháng, bộ lọc ngày, trạng thái loading/error và dữ liệu demo. Tách component, thêm test và không kết nối database thật.

Prompt tốt nên nêu:
- Mục tiêu và người dùng.
- Các màn hình/component cần có.
- Framework và design constraints.
- Hành vi, trạng thái lỗi/empty/loading.
- Nguồn dữ liệu (demo hay API thật).
- Tiêu chí nghiệm thu và giới hạn quyền.

### Templates

Mỗi template nên có preview, mô tả, framework, các component chính, dữ liệu demo, khả năng tiếp cận và trạng thái kiểm thử. Không ghi “đã xác minh” nếu chưa chạy test thực tế.

### Design Mode và Code Mode

Design Mode chỉnh tokens/bố cục; Code Mode xem diff và logic. Hai chế độ cần đồng bộ, có undo và không làm mất thay đổi chưa lưu. Preview phải được cô lập khỏi secrets và dữ liệu production.

### GitHub / Deploy

Kết nối GitHub bằng quyền tối thiểu. Mặc định tạo branch/PR để review. Nút Deploy chỉ xuất hiện khi có provider đã cấu hình, môi trường đích rõ ràng và kiểm tra bắt buộc đã đạt; nếu chưa, giải thích bước còn thiếu thay vì giả vờ deploy thành công.

## 5. Design system đề xuất

- **Visual direction:** nền đen than, bề mặt tối phân lớp, viền mảnh, chữ sáng và điểm nhấn xanh điện/tím; giữ góc vuông theo ngôn ngữ giao diện OCODE.js.
- **Layout desktop:** thanh điều hướng dự án; workspace ba vùng có thể đổi kích thước — chat/tasks, preview, code/inspector.
- **Layout mobile:** chat và preview là các tab/stack; toolbar gọn, vùng chạm đủ lớn; tránh nhồi editor desktop vào màn hình nhỏ.
- **Components:** prompt composer, attachment tray, task checklist, preview toolbar, viewport switcher, file tree, diff viewer, test/status panel, GitHub connection state, release confirmation.
- **States:** idle, planning, generating, preview-ready, checking, failed, awaiting-approval, published.
- **Accessibility:** keyboard navigation, focus-visible, contrast phù hợp, nhãn cho controls, thông báo trạng thái cho screen reader.

## 6. Phân kỳ triển khai

| Giai đoạn | Phạm vi | Điều kiện hoàn thành |
| --- | --- | --- |
| 0 — Foundation | Audit X-BO hiện tại, architecture note, design tokens, threat model | Scope được duyệt; không có secret bị lộ |
| 1 — Prompt → artifact | Prompt, task list, sinh file theo diff, dữ liệu demo | Output có thể tái lập; kiểm tra file/path; test cơ bản |
| 2 — Preview & refine | Sandbox preview, responsive viewport, lỗi/build output | Preview cô lập; timeout/cleanup hoạt động |
| 3 — Design/Code modes | Inspector, token edits, code diff, undo | Chỉnh sửa không mất dữ liệu; diff chính xác |
| 4 — GitHub workflow | OAuth/app permissions, branch, PR, checks | Quyền tối thiểu; không push thẳng main; secrets scan |
| 5 — Integrations | API/database adapters và quản lý credentials | AuthZ, audit, schema validation, migrations an toàn |
| 6 — Release gates | Staging, health checks, explicit approval | Rollback plan, observability và xác nhận release |

## 7. Bảo mật và độ tin cậy

- Không đưa API keys, OAuth tokens hoặc biến môi trường bí mật vào frontend, prompt logs, generated files hay Git.
- Đối với repository, chỉ cho phép thao tác trong phạm vi đã phê duyệt; branch/PR trước, không xóa/ghi đè hàng loạt.
- Chạy code do AI tạo trong sandbox có giới hạn mạng, CPU, bộ nhớ, thời gian và quyền truy cập tệp.
- Kiểm tra đường dẫn để ngăn path traversal; kiểm soát dependency, scripts và lệnh shell trước khi thực thi.
- Với database, dùng dữ liệu demo mặc định; thao tác ghi/migration yêu cầu quyền, backup/rollback và phê duyệt riêng.
- Chống prompt injection từ file/ảnh/nội dung repo; xem tài liệu đầu vào là dữ liệu không đáng tin, không phải chỉ thị hệ thống.
- Ghi nhận logs tối thiểu cần thiết; che secrets và thông tin cá nhân.
- Không tuyên bố hỗ trợ Figma import, iOS app, one-click OCODE.js deploy, shadcn/ui hay subscription ChatGPT integration cho đến khi từng tích hợp được xây dựng và xác minh.

## 8. Tài liệu và dự án liên quan

- [X-BO repository](https://github.com/zskbot/X-BO) — ứng dụng AI agent hiện có.
- [OCode.js repository](https://github.com/Velclaw/OCodejs) — dự án OCODE.js liên quan.
- [OCode.js Documentation Hub](https://zskbot.github.io/docs-ocodejs/) — tài liệu và kế hoạch kỹ thuật.

## Phạm vi và trạng thái

Tài liệu này xác định định hướng sản phẩm, UX và kiến trúc mục tiêu. Nó không tự thêm tính năng vào ứng dụng X-BO, không xác nhận mọi tích hợp đang hoạt động, và không triển khai production. Mỗi giai đoạn cần PR, kiểm thử và bằng chứng xác minh riêng.
