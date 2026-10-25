# The Agent Skills Directory

**Mục tiêu:** cung cấp điểm bắt đầu để khám phá các skills có thể tái sử dụng cho AI agents, được giới thiệu trên [Skills.sh](https://skills.sh/).

> Đây là danh mục hướng dẫn và tham khảo trong OCode.js Documentation Hub. Nó không phải bản mirror của Skills.sh, không phát hành các skill liệt kê bên dưới và không xác nhận độc lập tính tương thích của từng skill.

## Skills là gì?

Skills là các gói hướng dẫn/quy trình có thể tái sử dụng, giúp AI agent thực hiện những tác vụ chuyên biệt theo một quy trình nhất quán. Tùy repository, một skill có thể chứa tệp hướng dẫn như `SKILL.md`, ví dụ, tài nguyên hoặc script. Hãy kiểm tra cấu trúc và yêu cầu của từng repository trước khi dùng.

## Cài đặt nhanh

Cú pháp được giới thiệu:

```bash
npx skills add <owner/repo>
```

Thay `<owner/repo>` bằng repository chứa skill mà bạn đã chọn. Đọc hướng dẫn cài đặt tại [Skills.sh](https://skills.sh/) và repository nguồn để xác nhận cú pháp, tùy chọn và agent đích trước khi thực thi.

## Nền tảng và công cụ

Danh mục người dùng cung cấp nêu các công cụ như Claude Code, Cursor, GitHub Copilot, Windsurf, Gemini, VS Code và Zed. Khả năng tương thích thực tế phụ thuộc vào định dạng skill, phiên bản công cụ, cấu hình và hướng dẫn của repository; đừng coi danh sách này là kết quả kiểm thử của OCode.js.

## Bộ sưu tập theo nhóm

### Tối ưu codebase, kiến trúc và kiểm thử

- `find-skills` — tìm/khám phá skills phù hợp.
- `diagnosing-bugs` — quy trình chẩn đoán lỗi.
- `improve-codebase-architecture` — rà soát và cải thiện kiến trúc.
- `domain-modeling` — mô hình hóa miền nghiệp vụ.
- `tdd` — phát triển theo hướng kiểm thử trước.

### Thiết kế giao diện và UI/UX

- `frontend-design` — thiết kế giao diện web.
- `design-mobile-apps` — thiết kế trải nghiệm ứng dụng di động.
- `vercel-react-best-practices` — thực hành React/Next.js.

### Sáng tạo và đa phương tiện

- `ai-video-generation` — quy trình tạo video bằng AI.
- `hyperframes`
- `hyperframes-animation`
- `hyperframes-creative`

Tên gọi và mô tả trên đây là nhãn tham khảo dựa trên danh sách được cung cấp; hãy kiểm tra repository nguồn để xác nhận maintainer, chức năng và điều kiện sử dụng.

### Tự động hóa và điều phối công việc

- `agent-browser` — tự động hóa tương tác trình duyệt.
- `reddit-automation` — quy trình tự động hóa Reddit.
- `lark-doc` — hỗ trợ quy trình tài liệu Lark.
- `triage` — phân loại và ưu tiên yêu cầu.
- `handoff` — bàn giao tác vụ và ngữ cảnh.

## Chủ đề để khám phá

Bắt đầu từ chủ đề gắn với nhu cầu thực tế, chẳng hạn React, Next.js, AI, Testing, code quality, thiết kế giao diện, browser automation hoặc tài liệu. Dùng trang [Skills.sh](https://skills.sh/) để tra cứu danh sách và thứ hạng hiện hành thay vì dựa vào bản tóm tắt tĩnh trong tài liệu này.

## Checklist an toàn trước khi cài

1. Mở repository nguồn, kiểm tra chủ sở hữu, lịch sử và giấy phép.
2. Đọc `SKILL.md` và mọi script/tệp được yêu cầu chạy.
3. Kiểm tra quyền truy cập, biến môi trường, thao tác mạng và thay đổi tệp.
4. Không đưa API key, token, mật khẩu hoặc dữ liệu riêng tư vào prompt/tệp skill.
5. Thử nghiệm trong repository hoặc môi trường sandbox không chứa secrets trước khi dùng trong dự án chính.
6. Ghi lại nguồn, commit/tag và kết quả thử nghiệm nếu dùng trong quy trình của nhóm.

## Ranh giới dự án

- Trang này chỉ liên kết và mô tả danh mục tham khảo; không tự động tải hay thực thi skills.
- Không có mã nguồn skill bên thứ ba nào được sao chép vào repository bởi thay đổi tài liệu này.
- Không có production deploy, thay đổi database hoặc secrets nào thuộc phạm vi tính năng.
- Mọi tích hợp tự động trong tương lai cần thiết kế quyền hạn, xác nhận của người dùng và kiểm thử bảo mật riêng.

**Nguồn chính:** [Skills.sh — The Agent Skills Directory](https://skills.sh/).
