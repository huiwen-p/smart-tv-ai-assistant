Tôi nghĩ bạn đang muốn xây dựng một khung Planning tổng quát (Universal Implementation Planning Framework) để AI có thể sử dụng trong nhiều tình huống:

- Phát triển một tính năng mới từ đầu.
- Mở rộng một module hiện có.
- Thay đổi nghiệp vụ hoặc kiến trúc.
- Refactor codebase.
- Tích hợp một công nghệ hoặc hệ thống bên ngoài.
- Sửa lỗi và cải thiện hệ thống.
- Xây dựng một sản phẩm hoặc một subsystem tương đối độc lập.

Điểm khác biệt quan trọng so với `CODEBASE CHANGE PLANNER` hiện tại là: không lấy Task/Acceptance Criteria làm trung tâm, mà lấy mục tiêu phát triển và trạng thái hệ thống mong muốn làm trung tâm.

Ví dụ, khi phát triển một module thanh toán mới, có thể chưa tồn tại codebase, chưa có task cụ thể, chưa có acceptance criteria. Nhưng vẫn cần lập kế hoạch từ mục tiêu, nghiệp vụ, kiến trúc, dữ liệu, bảo mật đến triển khai.

Tôi đề xuất khung dưới đây.

# 1. Cấu trúc tổng thể của một Implementation Plan

Tôi chia thành 12 phần. Đây là cấu trúc đầy đủ, nhưng không có nghĩa mọi dự án đều phải triển khai tất cả các mục với mức độ chi tiết như nhau.

| STT | Thành phần                             | Mục đích                                 |
| --- | -------------------------------------- | ---------------------------------------- |
| 1   | Context & Objectives                   | Xác định bối cảnh và mục tiêu phát triển |
| 2   | Scope & Constraints                    | Xác định phạm vi, giới hạn và ràng buộc  |
| 3   | Requirements & Expected Behavior       | Đặc tả hệ thống cần đạt được điều gì     |
| 4   | Technical Assessment                   | Đánh giá cơ sở kỹ thuật hiện tại         |
| 5   | Technical Solution & Design            | Xác định phương án kỹ thuật              |
| 6   | Work Breakdown & Phase Design          | Chia công việc và thiết kế các phase     |
| 7   | Detailed Phase Specification           | Đặc tả chi tiết từng phase               |
| 8   | Traceability Matrix                    | Xây dựng ma trận truy vết                |
| 9   | Verification & Cross-phase Integration | Xác định cách kiểm chứng                 |
| 10  | Risk & Dependency Management           | Quản lý rủi ro và dependency             |
| 11  | Execution Readiness                    | Xác định điều kiện sẵn sàng              |
| 12  | Plan Governance & Change Management    | Quản lý sự thay đổi của kế hoạch         |

Sau đây là nội dung cụ thể.

# 2. Khung chi tiết

## 1. Context & Objectives – Bối cảnh và mục tiêu

Xác định tại sao cần phát triển và kết quả cuối cùng mong muốn là gì.

### 1.1. Background

- Bối cảnh hình thành nhu cầu.
- Vấn đề hiện tại.
- Hạn chế của hệ thống hiện tại (nếu có).
- Cơ hội hoặc nhu cầu phát triển.

### 1.2. Objectives

Xác định mục tiêu theo các khía cạnh:

- Business Objective: Giá trị nghiệp vụ cần đạt.
- Functional Objective: Khả năng hệ thống cần có.
- Technical Objective: Mục tiêu về kiến trúc, hiệu năng, khả năng mở rộng...
- Quality Objective: Mức chất lượng mong muốn.

### 1.3. Success Criteria

Xác định bằng chứng để kết luận mục tiêu đã đạt.

Ví dụ:

| Mục tiêu                     | Tiêu chí thành công                      |
| ---------------------------- | ---------------------------------------- |
| Xây dựng hệ thống thanh toán | Người dùng có thể thanh toán thành công  |
| Đảm bảo tính nhất quán       | Không ghi nhận giao dịch trùng khi retry |
| Đảm bảo hiệu năng            | p95 latency dưới ngưỡng đã xác định      |

Lý do: Phân biệt giữa việc hoàn thành các đầu việc và thực sự đạt được mục tiêu phát triển.

## 2. Scope & Constraints – Phạm vi và ràng buộc

### 2.1. In Scope

Những gì sẽ được thực hiện.

### 2.2. Out of Scope

Những gì chủ động không thực hiện trong lần phát triển này.

### 2.3. Constraints

Các giới hạn:

- Công nghệ bắt buộc.
- Kiến trúc hiện có.
- Thời gian.
- Nhân lực.
- Hạ tầng.
- Tương thích ngược.
- Quy định bảo mật hoặc nghiệp vụ.

### 2.4. Assumptions & Open Questions

- Các giả định đang sử dụng.
- Thông tin chưa được xác minh.
- Câu hỏi cần làm rõ.
- Những giả định có thể ảnh hưởng đến phương án kỹ thuật.

Lý do: Ngăn việc AI tự mở rộng phạm vi hoặc tự đưa ra quyết định dựa trên giả định chưa được xác nhận.

## 3. Requirements & Expected Behavior – Yêu cầu và hành vi mong muốn

Đây là phần quan trọng để chuyển mục tiêu thành những gì có thể triển khai.

### 3.1. Functional Requirements

- Các chức năng cần xây dựng.
- Luồng nghiệp vụ.
- Actor và quyền hạn.
- Business rules.
- Các trường hợp ngoại lệ.

### 3.2. Non-functional Requirements

Khi có liên quan:

- Performance.
- Security.
- Reliability.
- Scalability.
- Maintainability.
- Observability.
- Compatibility.
- Availability.

### 3.3. System Behavior

Mô tả hành vi mong muốn thông qua:

- Input / Output.
- State transitions.
- Data flow.
- Error handling.
- Boundary conditions.
- Failure scenarios.

### 3.4. Acceptance Criteria

Chuyển yêu cầu thành điều kiện có thể kiểm chứng.

Ví dụ:

Không nên ghi:

> Hệ thống xử lý thanh toán chính xác.

Nên ghi:

> Khi nhận hai request thanh toán có cùng idempotency key, hệ thống chỉ tạo một giao dịch và trả về kết quả nhất quán cho cả hai request.

Lý do: AI không thể lập kế hoạch triển khai tốt nếu chưa hiểu chính xác hệ thống cần hành xử như thế nào.

## 4. Technical Assessment – Đánh giá cơ sở kỹ thuật

Phần này áp dụng đặc biệt khi làm việc với codebase hiện có.

### 4.1. Current System State

- Kiến trúc hiện tại.
- Các module liên quan.
- Luồng xử lý hiện tại.
- Data model.
- API và integration contract.
- Các dependency quan trọng.

Nếu phát triển mới hoàn toàn, thay bằng đánh giá môi trường và hệ thống liên quan.

### 4.2. Reusable Components

- Các abstraction có thể tái sử dụng.
- Utilities.
- Existing services.
- Shared contracts.
- Design patterns đang được sử dụng.

### 4.3. Impact Assessment

Xác định các thành phần bị ảnh hưởng:

- Module.
- Layer.
- Database.
- API.
- Consumer.
- External services.
- Infrastructure.
- Deployment configuration.

### 4.4. Technical Gaps

Những khả năng hệ thống hiện tại chưa đáp ứng được mục tiêu.

Lý do: Tránh thiết kế dựa trên kiến thức chung về công nghệ thay vì tình trạng thực tế của hệ thống.

## 5. Technical Solution & Design – Phương án và thiết kế kỹ thuật

Đây là phần trả lời câu hỏi: Sẽ giải quyết vấn đề bằng cách nào?

### 5.1. Solution Overview

- Phương án tổng thể.
- Cơ chế hoạt động.
- Các thành phần tham gia.
- Luồng xử lý chính.

### 5.2. Architecture & Component Design

- Các module/component.
- Trách nhiệm từng thành phần.
- Ranh giới giữa các thành phần.
- Quan hệ dependency.
- Data flow và control flow.

### 5.3. Data Design

Nếu có thay đổi dữ liệu:

- Entity và relationship.
- Schema.
- Constraints.
- Indexes.
- Migration.
- Data transformation.
- Backward compatibility.
- Data integrity.

### 5.4. Interface & Contract Design

- API contract.
- Internal interfaces.
- Event/message schema.
- External integration.
- Error contract.
- Versioning.

### 5.5. Security & Reliability Design

- Authentication / Authorization.
- Input validation.
- Trust boundaries.
- Threat considerations.
- Transaction boundaries.
- Idempotency.
- Retry / Timeout.
- Failure recovery.

### 5.6. Alternatives & Trade-offs

| Phương án | Ưu điểm | Nhược điểm | Lý do chọn/loại |
| --------- | ------- | ---------- | --------------- |
| A         | ...     | ...        | ...             |
| B         | ...     | ...        | ...             |

Không cần đưa ra 5–10 phương án. Chỉ so sánh những lựa chọn thực sự có khả năng ảnh hưởng đến quyết định.

### 5.7. Design Decisions

Ghi lại các quyết định quan trọng:

- Quyết định.
- Lý do.
- Các phương án đã cân nhắc.
- Hệ quả kỹ thuật.

Có thể sử dụng ADR khi quyết định ảnh hưởng đáng kể đến kiến trúc.

Lý do: Nếu không có phương án kỹ thuật rõ ràng, AI rất dễ tự lựa chọn cách triển khai khác nhau trong từng phase.

## 6. Work Breakdown & Phase Design – Phân rã công việc và thiết kế phase

Đây là phần đặc biệt quan trọng đối với yêu cầu của bạn.

### 6.1. Work Breakdown

Phân rã mục tiêu lớn thành các nhóm công việc có quan hệ logic.

Ví dụ phát triển module thanh toán:

1. Payment Domain & Data Model.
2. Payment Processing.
3. Payment Provider Integration.
4. Transaction Reconciliation.
5. Testing & Operational Readiness.

### 6.2. Phase Design

Mỗi phase cần xác định:

- Mục tiêu.
- Kết quả cần đạt.
- Phạm vi.
- Dependency.
- Đầu vào.
- Đầu ra.
- Điều kiện bắt đầu.
- Điều kiện hoàn thành.

### 6.3. Dependency Graph

Xác định thứ tự phụ thuộc.

Ví dụ:

\#chatgpt-mermaid-\_r_dc\_{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;fill:rgb(237, 237, 237);}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#chatgpt-mermaid-\_r_dc\_ .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_dc\_ .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_dc\_ .error-icon{fill:rgb(48, 48, 48);}#chatgpt-mermaid-\_r_dc\_ .error-text{fill:rgb(237, 237, 237);stroke:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_dc\_ .edge-thickness-normal{stroke-width:1px;}#chatgpt-mermaid-\_r_dc\_ .edge-thickness-thick{stroke-width:3.5px;}#chatgpt-mermaid-\_r_dc\_ .edge-pattern-solid{stroke-dasharray:0;}#chatgpt-mermaid-\_r_dc\_ .edge-thickness-invisible{stroke-width:0;fill:none;}#chatgpt-mermaid-\_r_dc\_ .edge-pattern-dashed{stroke-dasharray:3;}#chatgpt-mermaid-\_r_dc\_ .edge-pattern-dotted{stroke-dasharray:2;}#chatgpt-mermaid-\_r_dc\_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_dc\_ .marker.cross{stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_dc\_ svg{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;}#chatgpt-mermaid-\_r_dc\_ p{margin:0;}#chatgpt-mermaid-\_r_dc\_ .label{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_dc\_ .cluster-label text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_dc\_ .cluster-label span{color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_dc\_ .cluster-label span p{background-color:transparent;}#chatgpt-mermaid-\_r_dc\_ .label text,#chatgpt-mermaid-\_r_dc\_ span{fill:rgb(237, 237, 237);color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_dc\_ .node rect,#chatgpt-mermaid-\_r_dc\_ .node circle,#chatgpt-mermaid-\_r_dc\_ .node ellipse,#chatgpt-mermaid-\_r_dc\_ .node polygon,#chatgpt-mermaid-\_r_dc\_ .node path{fill:rgb(9, 23, 44);stroke:rgb(31, 78, 148);stroke-width:1px;}#chatgpt-mermaid-\_r_dc\_ .rough-node .label text,#chatgpt-mermaid-\_r_dc\_ .node .label text,#chatgpt-mermaid-\_r_dc\_ .image-shape .label,#chatgpt-mermaid-\_r_dc\_ .icon-shape .label{text-anchor:middle;}#chatgpt-mermaid-\_r_dc\_ .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#chatgpt-mermaid-\_r_dc\_ .rough-node .label,#chatgpt-mermaid-\_r_dc\_ .node .label,#chatgpt-mermaid-\_r_dc\_ .image-shape .label,#chatgpt-mermaid-\_r_dc\_ .icon-shape .label{text-align:center;}#chatgpt-mermaid-\_r_dc\_ .node.clickable{cursor:pointer;}#chatgpt-mermaid-\_r_dc\_ .root .anchor path{fill:rgb(175, 175, 175)!important;stroke-width:0;stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_dc\_ .arrowheadPath{fill:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_dc\_ .edgePath .path{stroke:rgb(175, 175, 175);stroke-width:1px;}#chatgpt-mermaid-\_r_dc\_ .flowchart-link{stroke:rgb(175, 175, 175);fill:none;}#chatgpt-mermaid-\_r_dc\_ .edgeLabel{background-color:rgb(0, 0, 0);text-align:center;}#chatgpt-mermaid-\_r_dc\_ .edgeLabel p{background-color:rgb(0, 0, 0);}#chatgpt-mermaid-\_r_dc\_ .edgeLabel rect{opacity:0.5;background-color:rgb(0, 0, 0);fill:rgb(0, 0, 0);}#chatgpt-mermaid-\_r_dc\_ .labelBkg{background-color:rgba(0, 0, 0, 0.5);}#chatgpt-mermaid-\_r_dc\_ .cluster rect{fill:rgb(48, 48, 48);stroke:rgba(255, 255, 255, 0.15);stroke-width:1px;}#chatgpt-mermaid-\_r_dc\_ .cluster text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_dc\_ .cluster span{color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_dc\_ div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:12px;background:rgb(48, 48, 48);border:1px solid rgba(255, 255, 255, 0.15);border-radius:2px;pointer-events:none;z-index:100;}#chatgpt-mermaid-\_r_dc\_ .flowchartTitleText{text-anchor:middle;font-size:18px;fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_dc\_ rect.text{fill:none;stroke-width:0;}#chatgpt-mermaid-\_r_dc\_ .icon-shape,#chatgpt-mermaid-\_r_dc\_ .image-shape{background-color:rgb(0, 0, 0);text-align:center;}#chatgpt-mermaid-\_r_dc\_ .icon-shape p,#chatgpt-mermaid-\_r_dc\_ .image-shape p{background-color:rgb(0, 0, 0);padding:2px;}#chatgpt-mermaid-\_r_dc\_ .icon-shape .label rect,#chatgpt-mermaid-\_r_dc\_ .image-shape .label rect{opacity:0.5;background-color:rgb(0, 0, 0);fill:rgb(0, 0, 0);}#chatgpt-mermaid-\_r_dc\_ .label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#chatgpt-mermaid-\_r_dc\_ .node .label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#chatgpt-mermaid-\_r_dc\_ .node .neo-node{stroke:rgb(31, 78, 148);}#chatgpt-mermaid-\_r_dc\_ [data-look="neo"].node rect,#chatgpt-mermaid-\_r_dc\_ [data-look="neo"].cluster rect,#chatgpt-mermaid-\_r_dc\_ [data-look="neo"].node polygon{stroke:url(#chatgpt-mermaid-\_r_dc\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_dc\_ [data-look="neo"].swimlane.cluster rect{filter:none;}#chatgpt-mermaid-\_r_dc\_ [data-look="neo"].node path{stroke:url(#chatgpt-mermaid-\_r_dc\_-gradient);stroke-width:1px;}#chatgpt-mermaid-\_r_dc\_ [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_dc\_ [data-look="neo"].node .neo-line path{stroke:rgb(31, 78, 148);filter:none;}#chatgpt-mermaid-\_r_dc\_ [data-look="neo"].node circle{stroke:url(#chatgpt-mermaid-\_r_dc\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_dc\_ [data-look="neo"].node circle .state-start{fill:#000000;}#chatgpt-mermaid-\_r_dc\_ [data-look="neo"].icon-shape .icon{fill:url(#chatgpt-mermaid-\_r_dc\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_dc\_ [data-look="neo"].icon-shape .icon-neo path{stroke:url(#chatgpt-mermaid-\_r_dc\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_dc\_ .node text{font-size:14px;font-weight:600;letter-spacing:normal;fill:rgb(153, 206, 255);}#chatgpt-mermaid-\_r_dc\_ .edgeLabels text{font-size:13px;font-weight:600;letter-spacing:-0.08px;fill:rgb(153, 206, 255);}#chatgpt-mermaid-\_r_dc\_ .node tspan[font-weight="normal"],#chatgpt-mermaid-\_r_dc\_ .edgeLabels tspan[font-weight="normal"]{font-weight:600;}#chatgpt-mermaid-\_r_dc\_ .edgeLabel .label rect{opacity:1;rx:13px;ry:13px;fill:rgb(0, 14, 26);stroke:rgb(26, 62, 95);stroke-width:1px;}#chatgpt-mermaid-\_r_dc\_ .node rect,#chatgpt-mermaid-\_r_dc\_ .node circle,#chatgpt-mermaid-\_r_dc\_ .node ellipse,#chatgpt-mermaid-\_r_dc\_ .node polygon,#chatgpt-mermaid-\_r_dc\_ .node path{fill:rgb(0, 40, 77);stroke:rgba(255, 255, 255, 0.1);stroke-width:1px;}#chatgpt-mermaid-\_r_dc\_ .node rect{rx:16px;ry:16px;}#chatgpt-mermaid-\_r_dc\_ .mermaid-decision .label-container{fill:rgb(0, 14, 26);stroke:rgb(26, 62, 95);stroke-dasharray:2,2;}#chatgpt-mermaid-\_r_dc\_ .edgePaths .flowchart-link{stroke:rgb(175, 175, 175);stroke-width:1px;stroke-linecap:round;stroke-linejoin:round;}#chatgpt-mermaid-\_r_dc\_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_dc\_ :root{--mermaid-font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";}Domain & Data DesignPayment CoreProvider IntegrationTransaction ManagementEnd-to-end IntegrationOperational Readiness

### 6.4. Phase Ordering Strategy

Giải thích tại sao chia phase theo thứ tự này.

Các nguyên tắc:

- Dependency trước, consumer sau.
- Xử lý rủi ro lớn trước khi đầu tư quá nhiều.
- Xây dựng vertical slice khi có thể.
- Ưu tiên kết quả có thể kiểm chứng.
- Không chia phase chỉ để mỗi phase có số lượng file tương đương nhau.

Lý do: Phase là đơn vị quản lý tiến độ và tính đúng đắn, không phải đơn vị phân chia file.

## 7. Detailed Phase Specification – Đặc tả chi tiết từng phase

Đây là phần cần chi tiết nhất để AI có thể thực sự triển khai.

Tôi đề xuất mỗi phase sử dụng cấu trúc sau.

### 7.1. Phase Overview

- Phase ID / Name.
- Objective.
- Scope.
- Expected Outcome.
- Dependencies.
- Estimated Complexity (nếu cần).

### 7.2. Preconditions

Điều kiện cần có trước khi bắt đầu:

- Phase trước đã hoàn thành.
- Contract đã thống nhất.
- Migration hoặc dependency cần thiết đã sẵn sàng.
- Môi trường cần thiết đã hoạt động.

### 7.3. Implementation Tasks

Phân rã các đầu việc trong phase.

| ID    | Công việc                    | Thành phần     | Dependency | Kết quả               |
| ----- | ---------------------------- | -------------- | ---------- | --------------------- |
| P1-T1 | Xây dựng domain model        | Payment Domain | Không      | Domain model          |
| P1-T2 | Xây dựng repository contract | Repository     | P1-T1      | Repository interface  |
| P1-T3 | Implement persistence        | Infrastructure | P1-T2      | Persistence hoạt động |

### 7.4. File-level Change Specification

Đây chính là phần bạn đang nhấn mạnh: AI cần biết cụ thể sẽ thêm, sửa, xóa những gì.

| File / Symbol           | Action | Nội dung thay đổi                                 | Mục đích                    |
| ----------------------- | ------ | ------------------------------------------------- | --------------------------- |
| `payment.entity.ts`     | CREATE | Định nghĩa Payment entity và trạng thái giao dịch | Xây dựng domain model       |
| `payment.repository.ts` | CREATE | Định nghĩa các thao tác persistence cần thiết     | Tách biệt domain và storage |
| `payment.service.ts`    | CREATE | Triển khai nghiệp vụ tạo và xử lý thanh toán      | Điều phối nghiệp vụ         |
| `app.module.ts`         | MODIFY | Đăng ký PaymentModule                             | Tích hợp module             |

Quy ước:

- `CREATE`: Tạo file mới.
- `MODIFY`: Thay đổi file hiện có.
- `DELETE`: Loại bỏ file.
- `MOVE/RENAME`: Di chuyển hoặc đổi tên.
- `NO CHANGE`: Chỉ đọc hoặc kiểm chứng, không sửa.

Với mỗi file, phải nêu:

1. Đường dẫn.
2. Symbol liên quan.
3. Nội dung hiện tại (nếu cần).
4. Nội dung cần thêm, sửa hoặc loại bỏ.
5. Lý do.
6. Thành phần phụ thuộc hoặc consumer bị ảnh hưởng.

Nếu chưa biết chính xác file, ghi rõ `TO BE DETERMINED` và điều kiện cần xác minh. Không tự bịa đường dẫn.

### 7.5. Implementation Sequence

Thứ tự triển khai bên trong phase.

Ví dụ:

1. Define domain contract.
2. Implement domain logic.
3. Implement persistence.
4. Integrate service.
5. Expose API.
6. Add tests.

Thứ tự này phải dựa trên dependency thực tế, không áp dụng máy móc cho mọi dự án.

### 7.6. Verification

Xác định kiểm tra ngay trong phase:

- Unit tests.
- Integration tests.
- Contract tests.
- Manual verification.
- Static analysis.
- Security checks (khi liên quan).

Nêu rõ test case hoặc behavior cần kiểm tra, không chỉ ghi chung chung "viết unit test".

### 7.7. Definition of Done

Phase chỉ hoàn thành khi:

- Các behavior thuộc phase hoạt động đúng.
- Contract và invariant được giữ.
- Các test bắt buộc đạt.
- Không có lỗi nghiêm trọng chưa xử lý.
- Tài liệu và cấu hình liên quan đã được cập nhật.
- Kết quả có bằng chứng kiểm chứng.

### 7.8. Risks & Rollback

- Failure modes.
- Regression risks.
- Compatibility risks.
- Biện pháp giảm thiểu.
- Cách khôi phục nếu thay đổi gây lỗi.

Không phải phase nào cũng cần rollback plan riêng. Nhưng các phase liên quan đến dữ liệu, migration, external integration hoặc deployment phải xem xét nghiêm túc.

## 8. Traceability Matrix – Ma trận truy vết

Đảm bảo không có yêu cầu nào bị bỏ quên khi chuyển thành implementation.

Tôi đề xuất không chỉ truy vết yêu cầu → phase, mà truy vết cả mục tiêu → yêu cầu → thiết kế → implementation → verification.

| Objective / Requirement  | Design Component      | Phase / Task | File / Symbol           | Verification            |
| ------------------------ | --------------------- | ------------ | ----------------------- | ----------------------- |
| Tạo thanh toán           | Payment Service       | P2 / T1      | `payment.service.ts`    | Unit test               |
| Chống giao dịch trùng    | Idempotency mechanism | P2 / T2      | `payment.service.ts`    | Concurrent request test |
| Lưu trạng thái giao dịch | Payment persistence   | P1 / T3      | `payment.repository.ts` | Integration test        |
| Đồng bộ với provider     | Provider adapter      | P3 / T1      | `provider.adapter.ts`   | Contract test           |

Các quy tắc:

- Mọi requirement phải được truy vết tới ít nhất một implementation task.
- Mọi requirement có thể kiểm chứng phải có verification tương ứng.
- Mọi thành phần quan trọng trong thiết kế phải có implementation hoặc giải thích rõ lý do chưa triển khai.
- Những thay đổi không truy ngược được về mục tiêu hoặc requirement phải được xem xét lại phạm vi.

## 9. Verification & Cross-phase Integration – Kiểm chứng và tích hợp xuyên phase

Đây là phần nhiều plan thường bỏ sót.

Hoàn thành các phase riêng lẻ không đồng nghĩa hệ thống hoạt động đúng khi tích hợp.

### 9.1. Cross-phase Contract Verification

- Contract giữa các module có đồng nhất không?
- Input/output mapping có chính xác không?
- Error contract có nhất quán không?
- State transition có đúng không?

### 9.2. End-to-end Flow Verification

Kiểm tra các luồng hoàn chỉnh:

- Happy path.
- Validation failure.
- Authorization failure.
- Duplicate request.
- Concurrent request.
- External service failure.
- Retry.
- Partial failure.

Chỉ chọn các trường hợp liên quan đến hệ thống đang xây dựng.

### 9.3. Regression Verification

- Luồng cũ có bị ảnh hưởng không?
- Consumer cũ có còn tương thích không?
- API contract cũ có thay đổi không?
- Database migration có ảnh hưởng dữ liệu hiện tại không?

### 9.4. Non-functional Verification

Kiểm tra các yêu cầu phi chức năng có liên quan:

- Performance.
- Security.
- Reliability.
- Resource consumption.
- Observability.

### 9.5. Final Acceptance

Tổng hợp bằng chứng để kết luận mục tiêu ban đầu đã đạt hay chưa.

Phân biệt quan trọng:

- Phase Verification: Xác minh một phase.
- Cross-phase Verification: Xác minh các phase phối hợp đúng.
- Final Acceptance: Xác minh sản phẩm đạt mục tiêu tổng thể.

Ba cấp độ này không thay thế nhau.

## 10. Risk & Dependency Management – Quản lý rủi ro và dependency

### 10.1. Technical Risks

- Sai kiến trúc.
- Sai data model.
- Tích hợp không tương thích.
- Performance bottleneck.
- Regression.

### 10.2. External Dependencies

- Third-party API.
- Infrastructure.
- Database.
- Authentication provider.
- External libraries.
- Team hoặc hệ thống khác.

### 10.3. Risk Assessment

| Risk                     | Probability | Impact   | Mitigation                   | Detection        |
| ------------------------ | ----------- | -------- | ---------------------------- | ---------------- |
| Payment provider timeout | Medium      | High     | Timeout, retry policy        | Integration test |
| Duplicate transaction    | Medium      | Critical | Idempotency                  | Concurrency test |
| Schema migration failure | Low         | High     | Backup, migration validation | Staging test     |

### 10.4. Unknowns & Contingency

Với mỗi unknown quan trọng:

- Điều chưa biết.
- Tại sao quan trọng.
- Cách xác minh.
- Phương án nếu giả định ban đầu sai.

Không cần biến mọi uncertainty nhỏ thành risk item. Tập trung vào những thứ có thể làm thay đổi thiết kế, tiến độ hoặc tính đúng đắn.

## 11. Execution Readiness – Điều kiện sẵn sàng triển khai

Đây là checkpoint trước khi AI bắt đầu sửa code.

### 11.1. Planning Completeness

- Mục tiêu rõ ràng.
- Phạm vi xác định.
- Requirements có thể kiểm chứng.
- Phương án kỹ thuật được lựa chọn.
- Dependency đã được xác minh.
- Các phase có đầu vào và đầu ra rõ ràng.
- File-level specification đủ cơ sở.

### 11.2. Environment Readiness

- Repository và branch đã xác định.
- Working tree đã được kiểm tra.
- Dependencies cần thiết đã xác định.
- Database/environment đã sẵn sàng.
- Các lệnh kiểm tra đã được xác minh.

### 11.3. Risk Readiness

- Rủi ro quan trọng đã được đánh giá.
- Các vấn đề cần quyết định đã được làm rõ.
- Có phương án cho những dependency chưa chắc chắn.

### 11.4. Readiness Decision

| Trạng thái            | Ý nghĩa                                                                |
| --------------------- | ---------------------------------------------------------------------- |
| READY TO IMPLEMENT    | Có đủ cơ sở triển khai                                                 |
| READY WITH CONDITIONS | Có thể triển khai nếu đáp ứng các điều kiện cụ thể                     |
| NEED CLARIFICATION    | Thiếu thông tin quan trọng                                             |
| BLOCKED               | Không thể triển khai do dependency hoặc ràng buộc chưa được giải quyết |

Điểm cần lưu ý: không nên bắt buộc xác định toàn bộ file và symbol ngay từ đầu đối với dự án mới. Những thành phần chỉ có thể xác định sau khi hoàn thành một phase cần được ghi nhận là điểm cần khám phá có kiểm soát.

## 12. Plan Governance & Change Management – Quản lý kế hoạch

Đây là phần tôi khuyên nên bổ sung nếu bạn muốn AI sử dụng plan xuyên suốt quá trình phát triển, thay vì chỉ tạo plan một lần rồi thực hiện máy móc.

### 12.1. Plan Versioning

- Plan ID.
- Version.
- Created date.
- Current status.
- Last updated.
- Reason for update.

### 12.2. Progress Tracking

Theo dõi từng phase:

- NOT STARTED.
- IN PROGRESS.
- BLOCKED.
- COMPLETED.
- NEEDS REVISION.

Theo dõi task tương tự.

### 12.3. Change Impact Assessment

Khi phát hiện yêu cầu mới hoặc bằng chứng mới:

- Có ảnh hưởng đến mục tiêu không?
- Có thay đổi scope không?
- Có cần thay đổi architecture/design không?
- Có ảnh hưởng phase khác không?
- Có cần cập nhật file-level specification không?
- Có cần cập nhật traceability matrix không?
- Có làm mất hiệu lực verification trước đó không?

### 12.4. Plan Update Rules

- Không tự ý mở rộng scope.
- Không tiếp tục thực hiện plan đã lỗi thời khi phát hiện mâu thuẫn quan trọng.
- Không đánh dấu hoàn thành nếu chưa có bằng chứng.
- Mọi thay đổi ảnh hưởng đến thiết kế phải được phản ánh vào plan.
- Không giữ nguyên phase chỉ vì đã bắt đầu triển khai nếu dependency hoặc phương án đã thay đổi.

Lý do: Plan là tài liệu sống, cần được đồng bộ với trạng thái thực tế của codebase.

# 3. Những tiêu chí đánh giá một plan chất lượng

12 phần trên là cấu trúc nội dung. Nhưng để đánh giá chất lượng, tôi đề xuất sử dụng 10 tiêu chí độc lập.

| Tiêu chí                    | Câu hỏi đánh giá                                                |
| --------------------------- | --------------------------------------------------------------- |
| 1. Goal Clarity             | Mục tiêu có rõ ràng và đo lường được không?                     |
| 2. Scope Control            | Phạm vi và giới hạn có được xác định không?                     |
| 3. Technical Grounding      | Phương án có dựa trên bằng chứng kỹ thuật không?                |
| 4. Design Consistency       | Các thành phần, contract và data flow có nhất quán không?       |
| 5. Phase Quality            | Phase có mục tiêu, dependency và kết quả độc lập đủ rõ không?   |
| 6. Implementation Precision | AI có biết cần thêm, sửa, xóa gì và tại sao không?              |
| 7. Traceability             | Có thể truy ngược từ mục tiêu đến implementation và test không? |
| 8. Verifiability            | Có cách chứng minh từng kết quả đạt được không?                 |
| 9. Risk Management          | Các failure mode và dependency quan trọng đã được xem xét chưa? |
| 10. Adaptability            | Plan có thể cập nhật khi phát hiện thông tin mới không?         |

Đây là khung đánh giá đề xuất, không phải một tiêu chuẩn chấm điểm chính thức.

Tôi đặc biệt nhấn mạnh 4 tiêu chí:

- Technical Grounding: Không bịa file, không thiết kế dựa trên suy đoán.
- Phase Quality: Không chia phase tùy tiện.
- Implementation Precision: Phải đủ cụ thể để AI thực hiện mà không tự phát minh quá nhiều.
- Verifiability: Không lấy việc code chạy được hoặc không có lỗi compile làm bằng chứng hoàn thành.

# 4. Cấu trúc rút gọn nên sử dụng trong thực tế

12 phần trên phù hợp làm khung chuẩn. Tuy nhiên, nếu bắt AI viết đầy đủ cả 12 phần cho mọi công việc thì sẽ tạo ra tài liệu rất dài, nhiều nội dung hình thức và tốn context.

Tôi đề xuất cấu trúc thực tế gồm 9 phần chính:

## Universal Implementation Plan

Cấu trúc khuyến nghị để xây dựng skill lập kế hoạch

1. Context & Objectives

   Bối cảnh, vấn đề, mục tiêu, success criteria.
2. Scope & Requirements

   In scope, out of scope, functional/non-functional requirements, business rules, acceptance criteria.
3. Technical Assessment

   Hiện trạng, dependency, thành phần tái sử dụng, impact và technical gaps.
4. Solution & Design

   Phương án kỹ thuật, kiến trúc, data, interface, security, trade-offs và design decisions.
5. Phase Architecture

   Work breakdown, phase objectives, dependency graph, thứ tự triển khai và expected outcomes.
6. Detailed Phase Specifications

   Preconditions, tasks, file-level changes, implementation sequence, verification, DoD và risks.
7. Traceability Matrix

   Objective → Requirement → Design → Phase/Task → Implementation → Verification.
8. Integration, Risk & Readiness

   Cross-phase verification, regression, risks, unknowns và điều kiện sẵn sàng.
9. Plan Governance

   Progress tracking, versioning, change impact và quy tắc cập nhật plan.

## 5. Một số nguyên tắc tôi muốn bổ sung vào skill của bạn

Có 5 điểm tôi cho rằng cần đưa thành quy tắc bắt buộc.

1\. Không bắt buộc mọi phase phải biết trước 100% file sẽ thay đổi.

Đây là một lỗi thiết kế plan khá phổ biến.

Ví dụ, khi phát triển một module mới, AI có thể cần khám phá codebase trong Phase 1 trước khi biết chính xác các file cần sửa ở Phase 2.

Giải pháp: cho phép `Discovery Task` hoặc `Implementation Refinement` có giới hạn. Nhưng phải xác định rõ đầu ra và điều kiện kết thúc của việc khám phá.

2\. Không đồng nhất phase với layer.

Không nên mặc định:

- Phase 1: Database.
- Phase 2: Backend.
- Phase 3: Frontend.
- Phase 4: Testing.

Cách chia này đôi khi khiến mỗi phase không tạo ra được kết quả nghiệp vụ có thể kiểm chứng.

Nên chia theo các capability hoặc trạng thái hệ thống đạt được, có xét đến dependency.

3\. Phải phân biệt Design Decision và Implementation Detail.

Ví dụ:

- Design Decision: Sử dụng transactional outbox để đảm bảo đồng bộ event.
- Implementation Detail: Thêm `outbox.entity.ts`, sửa `order.service.ts`.

Quyết định thiết kế cần được xác định trước. Chi tiết file có thể được hoàn thiện sau khi xác minh codebase.

4\. Mọi phase phải có đầu ra có thể kiểm chứng.

Không dùng các mục tiêu mơ hồ như:

- Hoàn thiện backend.
- Xây dựng database.
- Tối ưu hệ thống.

Thay bằng kết quả cụ thể, ví dụ:

- API tạo đơn hàng hoạt động với validation và transaction.
- Hai request đồng thời không tạo ra hai đơn hàng trùng idempotency key.
- Consumer có thể xử lý event và khôi phục sau khi gặp lỗi.

5\. Phân biệt Implementation Plan và Execution Log.

Đây là hai tài liệu khác nhau:

| Implementation Plan   | Execution Log            |
| --------------------- | ------------------------ |
| Dự định làm gì        | Thực tế đã làm gì        |
| File dự kiến thay đổi | File thực tế thay đổi    |
| Kết quả mong đợi      | Kết quả thực tế          |
| Test cần chạy         | Test đã chạy             |
| Rủi ro dự kiến        | Vấn đề thực tế phát sinh |

Không nên để AI liên tục sửa plan thành nhật ký triển khai, khiến mất dấu thiết kế ban đầu.

# 6. Kết luận: Tôi khuyên bạn xây dựng skill theo hướng nào?

Tôi không khuyên bạn chỉ mở rộng `CODEBASE CHANGE PLANNER` bằng cách thêm vài mục. Nên tách thành hai tầng:

Tầng 1

UNIVERSAL IMPLEMENTATION PLANNER

Khung lập kế hoạch tổng quát, áp dụng cho cả phát triển mới và thay đổi hệ thống hiện có.

- Objectives & Requirements.
- Scope.
- Technical Solution.
- Phase Design.
- Detailed Implementation.
- Traceability.
- Verification.
- Risk & Readiness.
- Governance.

Tầng 2

SPECIALIZED PLANNING MODULES

Các hướng dẫn chuyên biệt được kích hoạt tùy loại công việc.

- Codebase Change Planning.
- Greenfield Development Planning.
- Architecture Evolution Planning.
- Refactoring Planning.
- Database Migration Planning.
- External Integration Planning.
- Security Improvement Planning.

Lý do là các loại công việc có những yêu cầu lập kế hoạch khác nhau. Ví dụ:

- Greenfield cần chú trọng domain discovery, kiến trúc nền tảng và thiết lập môi trường.
- Codebase Change cần chú trọng impact analysis, backward compatibility và regression.
- Refactoring cần chú trọng behavioral equivalence và kiểm soát thay đổi hành vi.
- Database Migration cần chú trọng data integrity, rollout và rollback.

Một lưu ý cuối cùng: Plan tốt không phải là plan mô tả càng nhiều file, càng nhiều task càng tốt. Nó là plan giúp AI trả lời được 5 câu hỏi mà không phải tự suy đoán quá nhiều:

1. Tại sao phải làm?
2. Hệ thống cần đạt trạng thái nào?
3. Sẽ thay đổi những gì và bằng cách nào?
4. Thực hiện theo thứ tự nào, phụ thuộc vào đâu?
5. Dựa vào bằng chứng nào để biết đã làm đúng?

Đây nên là tiêu chuẩn cốt lõi để bạn thiết kế và đánh giá skill Planning.