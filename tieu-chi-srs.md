Một tài liệu SRS (Software Requirements Specification) chất lượng cần mô tả rõ hệ thống phải làm gì, hoạt động trong những điều kiện nào và tiêu chí nào được dùng để xác định hệ thống đã đáp ứng yêu cầu.

Có thể tham khảo cấu trúc dưới đây, dựa trên tinh thần của chuẩn IEEE 29148.

## 1. Cấu trúc đề xuất cho một SRS

| STT | Mục                             | Nội dung và lý do cần có                                                                                   |
| --- | ------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| 1   | Introduction                    | Giới thiệu tài liệu, mục đích, phạm vi và đối tượng đọc. Giúp mọi người hiểu tài liệu được viết để làm gì. |
| 1.1 | Purpose                         | Mục đích của tài liệu SRS.                                                                                 |
| 1.2 | Scope                           | Phạm vi sản phẩm, hệ thống giải quyết vấn đề gì và không giải quyết vấn đề gì.                             |
| 1.3 | Definitions, Acronyms           | Giải thích thuật ngữ, từ viết tắt để tránh hiểu sai.                                                       |
| 1.4 | References                      | Tài liệu, tiêu chuẩn, quy định được tham chiếu.                                                            |
| 2   | Overall Description             | Mô tả bức tranh tổng thể của hệ thống trước khi đi vào từng yêu cầu.                                       |
| 2.1 | Product Perspective             | Hệ thống độc lập hay là một phần của hệ thống khác.                                                        |
| 2.2 | Product Functions               | Tóm tắt các chức năng chính.                                                                               |
| 2.3 | User Classes                    | Các nhóm người dùng và đặc điểm của họ.                                                                    |
| 2.4 | Operating Environment           | Môi trường vận hành: OS, trình duyệt, thiết bị, server...                                                  |
| 2.5 | Constraints                     | Các ràng buộc về công nghệ, pháp lý, ngân sách, thời gian...                                               |
| 2.6 | Assumptions & Dependencies      | Các giả định và phụ thuộc có thể ảnh hưởng đến hệ thống.                                                   |
| 3   | Functional Requirements         | Mô tả chi tiết hệ thống phải thực hiện những chức năng gì. Đây là phần cốt lõi của SRS.                    |
| 4   | External Interface Requirements | Xác định cách hệ thống giao tiếp với người dùng và các hệ thống bên ngoài.                                 |
| 4.1 | User Interface                  | Yêu cầu giao diện và tương tác người dùng.                                                                 |
| 4.2 | Software Interface              | API, dịch vụ bên thứ ba, hệ thống tích hợp.                                                                |
| 4.3 | Hardware Interface              | Yêu cầu tương tác với phần cứng nếu có.                                                                    |
| 4.4 | Communication Interface         | Giao thức, phương thức giao tiếp, định dạng dữ liệu.                                                       |
| 5   | Non-functional Requirements     | Mô tả chất lượng hệ thống cần đạt được, không chỉ chức năng.                                               |
| 5.1 | Performance                     | Thời gian phản hồi, throughput, số lượng người dùng đồng thời.                                             |
| 5.2 | Security                        | Xác thực, phân quyền, mã hóa, bảo vệ dữ liệu.                                                              |
| 5.3 | Reliability & Availability      | Độ tin cậy, khả năng hoạt động liên tục, phục hồi lỗi.                                                     |
| 5.4 | Usability                       | Khả năng sử dụng, tính dễ hiểu, dễ thao tác.                                                               |
| 5.5 | Scalability                     | Khả năng mở rộng khi tải tăng.                                                                             |
| 5.6 | Maintainability                 | Khả năng bảo trì, sửa lỗi và nâng cấp.                                                                     |
| 6   | Data Requirements               | Mô tả dữ liệu hệ thống quản lý: cấu trúc, quan hệ, lưu trữ, vòng đời và tính toàn vẹn.                     |
| 7   | Business Rules                  | Các quy tắc nghiệp vụ mà hệ thống phải tuân thủ.                                                           |
| 8   | Acceptance Criteria             | Tiêu chí nghiệm thu để xác định yêu cầu đã được đáp ứng hay chưa.                                          |
| 9   | Appendices                      | Phụ lục như sơ đồ, bảng thuật ngữ, biểu mẫu, tài liệu bổ sung.                                             |

## 2. Những yếu tố quyết định chất lượng SRS

Không phải cứ có đủ các mục trên là SRS tốt. Một SRS chất lượng cần đảm bảo:

| Tiêu chí    | Ý nghĩa                                                                                |
| ----------- | -------------------------------------------------------------------------------------- |
| Correct     | Yêu cầu phản ánh đúng nhu cầu thực tế.                                                 |
| Unambiguous | Không có nhiều cách hiểu khác nhau.                                                    |
| Complete    | Không bỏ sót yêu cầu quan trọng.                                                       |
| Consistent  | Các yêu cầu không mâu thuẫn nhau.                                                      |
| Verifiable  | Có thể kiểm thử hoặc đo lường để xác nhận.                                             |
| Traceable   | Có thể truy ngược yêu cầu về nguồn gốc và theo dõi đến thiết kế, triển khai, kiểm thử. |
| Modifiable  | Dễ dàng cập nhật khi yêu cầu thay đổi.                                                 |
| Prioritized | Có mức độ ưu tiên để kiểm soát phạm vi triển khai.                                     |

## 3. Cách viết một Functional Requirement tốt

Đây là phần rất quan trọng. Không nên viết yêu cầu theo kiểu mô tả chung chung.

Ví dụ:

Không tốt

FR-01: Hệ thống hỗ trợ đăng nhập.

Không rõ đăng nhập bằng cách nào, điều kiện gì, xử lý lỗi ra sao.

Tốt hơn

FR-01: Đăng nhập hệ thống

- Actor: Người dùng đã đăng ký.
- Input: Email và mật khẩu.
- Preconditions: Tài khoản đã tồn tại và chưa bị khóa.
- Main Flow:
  1. Người dùng nhập email và mật khẩu.
  2. Hệ thống kiểm tra thông tin xác thực.
  3. Nếu hợp lệ, hệ thống tạo phiên đăng nhập.
  4. Người dùng được chuyển đến trang phù hợp với quyền hạn.
- Alternative Flow: Nếu thông tin không hợp lệ, hệ thống thông báo lỗi phù hợp.
- Postconditions: Người dùng được xác thực thành công.
- Priority: High.
- Acceptance Criteria: Có thể kiểm thử các trường hợp đăng nhập thành công, sai mật khẩu, tài khoản bị khóa.

## 4. Một số tài liệu nên đi cùng SRS

SRS không nên gánh toàn bộ tài liệu dự án. Nên phân chia trách nhiệm:

| Tài liệu                             | Trả lời câu hỏi                     |
| ------------------------------------ | ----------------------------------- |
| SRS                                  | Hệ thống cần làm gì?                |
| SDD (Software Design Description)    | Hệ thống được thiết kế như thế nào? |
| SAD (Software Architecture Document) | Kiến trúc tổng thể ra sao?          |
| Database Design                      | Dữ liệu được tổ chức như thế nào?   |
| Test Plan / Test Cases               | Kiểm thử hệ thống như thế nào?      |
| Deployment Document                  | Triển khai hệ thống ra sao?         |

Lưu ý: Không nhất thiết phải tạo tất cả thành các file riêng. Có thể gộp một số tài liệu tùy quy mô dự án.

## 5. Khuyến nghị thực tế

Nếu viết SRS cho một đồ án hoặc dự án phần mềm có quy mô vừa, tôi khuyên nên ưu tiên 6 phần:

1. Introduction – Xác định mục tiêu và phạm vi.
2. Overall Description – Hiểu bối cảnh và đối tượng sử dụng.
3. Functional Requirements – Đặc tả từng chức năng.
4. External Interface Requirements – Xác định giao tiếp và tích hợp.
5. Non-functional Requirements – Xác định chất lượng cần đạt.
6. Acceptance Criteria & Traceability – Xác định cách nghiệm thu và theo dõi yêu cầu.

Một nguyên tắc quan trọng: Mỗi yêu cầu nên có ID duy nhất, mô tả rõ ràng, mức ưu tiên và cách xác minh.

Như vậy, SRS không chỉ là tài liệu để đọc mà còn là cơ sở để thiết kế kiến trúc, chia task, triển khai và kiểm thử.