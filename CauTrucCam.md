# CÁC LỖI CẤU TRÚC CẦN TRÁNH (ANTI-PATTERNS)

Đây là những khuôn mẫu tường thuật tồi mà AI rất dễ rơi vào khi viết tiểu thuyết dài hơi. Hãy dùng các mục này làm tiêu chí để **đánh giá** (trong `evaluate.py`) và **chỉnh sửa** (trong `adversarial_edit.py`).

## 1. Nhân vật nói quá nhiều, hành động quá ít
**Triệu chứng**:
- Một cuộc trò chuyện kéo dài 3 trang liền, không có sự thay đổi về vị trí, ngôn ngữ cơ thể, hoặc xung đột leo thang.
- Nhân vật dùng lời nói để "giải thích" mọi thứ thay vì tự hành động để thể hiện.

**Chữa trị**:
- Sau mỗi 3-4 dòng đối thoại, hãy chèn một hành động, một chi tiết cảnh vật, hoặc một biểu cảm vi tế.
- Áp dụng quy tắc "Mỗi câu thoại phải có mục đích" – hoặc đẩy cốt truyện, hoặc bộc lộ tính cách, hoặc tạo xung đột.

## 2. Giải quyết xung đột quá dễ dàng (Deus Ex Machina)
**Triệu chứng**:
- Ở thời điểm khó khăn nhất, một nhân vật phụ ghé qua và vô tình mang đến giải pháp.
- Nhân vật chính chợt "nhận ra" một sức mạnh mới chưa từng được giới thiệu trước đó.
- Kẻ thù đột nhiên trở nên ngu ngốc hoặc có thay đổi lòng dạ vô lý.

**Chữa trị**:
- Trong giai đoạn **dàn ý (outline)**, hãy đảm bảo mọi giải pháp đều được "gieo mầm" ít nhất 3 chương trước khi xảy ra.
- Nếu một khó khăn không thể giải quyết một cách thuyết phục, hãy để nhân vật **thất bại** hoặc **trả giá** – điều đó còn hay hơn.

## 3. Nhân vật phẳng (không thay đổi sau hành trình)
**Triệu chứng**:
- Cuối sách, nhân vật vẫn có cùng niềm tin, thói quen, và cách ứng xử như đầu sách.
- Nhân vật vượt qua thử thách nhưng không hề bị tổn thương hoặc trưởng thành.

**Chữa trị**:
- Xác định một **cung bậc cảm xúc** (emotional arc) cho nhân vật chính: từ sợ hãi đến dũng cảm, từ ích kỷ đến vị tha, từ ngây thơ đến cay đắng.
- Trong mỗi chương, có ít nhất một hành động hoặc lời nói cho thấy sự thay đổi dần dần đó.

## 4. Lạm dụng hồi tưởng (flashback) để lấp lỗ hổng
**Triệu chứng**:
- Quá nhiều đoạn hồi tưởng (hơn 2 mỗi chương) khiến dòng thời gian bị đứt đoạn.
- Hồi tưởng được dùng để "kể" quá khứ một cách lười biếng thay vì để thông tin xuất hiện tự nhiên qua hành động hiện tại.

**Chữa trị**:
- Mỗi flashback phải có một **tác nhân kích thích** rõ ràng trong hiện tại (một mùi hương, một câu nói, một đồ vật).
- Ưu tiên dùng **hội thoại gián tiếp** hoặc **phát hiện dần dần** hơn là cắt một khối quá khứ nguyên miếng.

## 5. Độc giả biết trước mọi thứ, nhân vật thì không
**Triệu chứng**:
- Đoạn trần thuật toàn tri tiết lộ quá sớm danh tính kẻ phản diện, hoặc âm mưu phía sau.
- Sự mỉa mai kịch tính (dramatic irony) bị dùng quá đà đến mức nhân vật trông ngu ngốc.

**Chữa trị**:
- Giới hạn điểm nhìn: chỉ biết những gì nhân vật chính biết (hoặc tối đa 2-3 nhân vật).
- Nếu cần dùng toàn tri, hãy làm điều đó qua một **người kể chuyện có cá tính** (ví dụ: một nhân vật chứng kiến câu chuyện và kể lại với giọng riêng).

## 6. Mở đầu bằng cảnh báo thức, kết thúc bằng đoạn kết sến súa
**Triệu chứng**:
- Chương 1: "Chuông báo thức reo. Nhân vật ngồi dậy, nhìn ra cửa sổ, và nghĩ về cuộc đời mình." – Cực kỳ sáo.
- Chương cuối: "Vậy là câu chuyện kết thúc. Họ nhìn nhau và mỉm cười." – Thiếu sức nặng.

**Chữa trị**:
- Mở đầu bằng một **hành động bất thường** hoặc **xung đột ngay lập tức**.
- Kết thúc không nhất thiết phải "happy ever after" – hãy để lại một câu hỏi nhỏ, một mất mát, hoặc một sự mỉa mai.

## Cách sử dụng trong pipeline
- Trong giai đoạn **đánh giá (evaluate.py)**, mỗi chương sẽ bị trừ điểm nếu phát hiện các pattern trên.
- Trong giai đoạn **chỉnh sửa đối kháng (adversarial_edit.py)**, AI được yêu cầu đọc lại chương và cắt bỏ hoàn toàn bất kỳ đoạn nào thuộc 6 loại trên.
- Ngưỡng loại bỏ: nếu một chương vi phạm từ 3 pattern khác nhau → **đánh dấu cần viết lại từ đầu**.