# OCode.js + Velclaw Ecosystem Registry

> Tài liệu tổng hợp từ README và metadata công khai của 11 repository. Đây là registry tài liệu/liên kết nguồn, chưa phải bản sao toàn bộ source code.

## Nguyên tắc
- Mỗi sản phẩm giữ repository, lịch sử Git, CI, quyền truy cập và vòng đời phát hành riêng.
- Repo này là điểm tập trung tài liệu, chỉ mục và hướng dẫn tích hợp.
- Không tự động gộp source code, ghi đè file, đổi production hoặc sao chép secrets.
- Không khẳng định tính năng production nếu chưa có bằng chứng runtime/CI.

## Danh mục repository

| Repository | Vai trò theo README đã xem |
|---|---|
| [VelCli](https://github.com/Velclaw/VelCli) | AI engineering workspace: agent, plan mode, editor, projects, chat history, hosting/deploy integrations. |
| [X-BO](https://github.com/zskbot/X-BO) | AI agent chat; React/Vite frontend và Node.js backend/provider routing. |
| [OCodejs/OCodejs](https://github.com/OCodejs/OCodejs) | Thư viện tiện ích JavaScript/TypeScript; README mô tả zero runtime dependencies, Node.js 18+ và giai đoạn phát triển sớm. |
| [Velclaw/OCodejs](https://github.com/Velclaw/OCodejs) | README và blob SHA khớp với OCodejs/OCodejs ở lần đọc này; xác minh quan hệ fork/đồng bộ trước khi chọn nguồn chuẩn. |
| [VelclawHost](https://github.com/Velclaw/VelclawHost) | Hosting/deployment control plane, domains, DNS, TLS, metrics và hạ tầng. |
| [velclaw-deploy](https://github.com/Velclaw/velclaw-deploy) | Next.js App Router deployment console tích hợp Vercel API phía server. |
| [Oauth](https://github.com/Velclaw/Oauth) | Ranh giới định danh OAuth; README nói hostname production chưa được gán, cần xác minh DNS/HTTPS trước callback công khai. |
| [docs.velclaw.ai](https://github.com/Velclaw/docs.velclaw.ai) | Next.js/MDX docs, Sandpack examples, Gemini assistant và semantic search qua Supabase pgvector. |
| [VELCLAW](https://github.com/Velclaw/VELCLAW) | Control Center/registry cho repositories, deployments, domains, databases, integrations, security và audit log. |
| [Docs UI Reference](https://github.com/Velclaw/Velclaw-velclaw-docs-ui-reference) | Chuẩn UI docs: dark/purple, góc vuông, responsive drawer, search, copy code và dark/light. |
| [Velclaw-OCodejs](https://github.com/Velclaw/Velclaw-OCodejs) | README đã đọc giống VELCLAW Control Center; tên repo và nội dung có vẻ lệch nhau, cần xác minh danh tính. |

## Sơ đồ tích hợp mục tiêu

```text
Developer / Mobile
  -> VelCli / X-BO (agent/chat interfaces)
  -> OCode.js (JS/TS utilities; scope must be verified)
  -> Velclaw OAuth -> Identity Provider
  -> Velclaw Deploy -> Vercel API -> Preview/Production
  -> VelclawHost -> hosting/domains/TLS/metrics
  -> VELCLAW Control Center -> repository/deployment registry
  -> Velclaw TechDocs -> MDX/examples/semantic search
  -> Docs UI Reference -> design-system source of truth
```

Sơ đồ là quan hệ kiến trúc mục tiêu, không chứng minh mọi kết nối đang chạy production. Xác minh từng kết nối bằng cấu hình, endpoint, CI và môi trường.

## Bảo mật và ranh giới triển khai
- Không commit API keys, OAuth secrets, access tokens, database URLs hoặc deployment tokens.
- Secrets chỉ nằm trong secret manager/environment server-side; không dùng tiền tố public cho secrets.
- Chỉ cấu hình OAuth callback sau khi xác nhận hostname, HTTPS, redirect URI và provider allowlist.
- Thay đổi tập trung phải qua branch/PR; không tự merge hoặc deploy production.
- Không chạy destructive migrations hoặc ghi đè database dựa trên tài liệu này.

## Trạng thái kiểm tra
| Hạng mục | Trạng thái |
|---|---|
| Metadata và README nguồn | Đã xem metadata và README của các repository được truy cập thành công |
| Recursive tree/file inventory | Chưa hoàn tất |
| Tải/giải nén toàn bộ source và binary | Chưa thực hiện |
| Runtime/endpoints/CI/build/test | Chưa xác minh |
| Trạng thái production integrations | Chưa xác minh |

Không tuyên bố đã đọc toàn bộ file khi chưa hoàn thành recursive file-level audit. Mọi tài liệu nhập sau này cần ghi nguồn, branch, commit SHA, path và ngày rà soát.