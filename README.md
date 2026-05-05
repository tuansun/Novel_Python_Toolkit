# 🖋️ Toolkit viết lovel bằng Local LLM

Bộ công cụ Python hỗ trợ viết tiểu thuyết dài hơi (đủ tiêu chuẩn xuất bản) sử dụng mô hình ngôn ngữ lớn (LLM) chạy cục bộ qua **LM Studio**. Hệ thống được xây dựng dựa trên các kỹ thuật viết và định luật của **Brandon Sanderson**.

## ✨ Tính năng nổi bật
- **Worldbuilding Pipeline:** Tự động xây dựng thế giới, hệ thống sức mạnh (Hard/Soft Magic), nhân vật và dàn ý 20-30 chương liên kết chặt chẽ.
- **Sanderson's Laws Integration:** Ép AI tuân thủ các quy tắc về giới hạn sức mạnh, chi phí sử dụng và tính logic trong hành động.
- **Seamless Chapter Writing:** Cơ chế chia nhỏ chương thành 7 phân đoạn (7-stage arc) giúp đạt độ dài ~3000 từ/chương mà không bị đứt gãy mạch văn.
- **Auto-Summarization:** Tự động tóm tắt "cuốn chiếu" để duy trì ngữ cảnh cho các chương sau mà không làm tràn bộ nhớ VRAM.
- **AI Editor:** Công cụ biên tập riêng biệt giúp gọt giũa câu từ, sửa lỗi lủng củng và tối ưu hóa văn phong sau khi viết nháp.

## 🛠️ Yêu cầu hệ thống
- **LM Studio:** Đã tải và chạy mô hình (Khuyên dùng Llama-3-8B hoặc Qwen-2-7B).
- **Python 3.10+**
- **Hardware:** Khuyến nghị 8GB VRAM trở lên.

## 🚀 Hướng dẫn cài đặt

1. **Khởi động LM Studio:**
   - Chọn model và Start Server tại `http://localhost:1234`.
   - Thiết lập Context Length tối thiểu 8192.

2. **Cài đặt thư viện:**
   ```bash
   pip install openai

3. **Chạy dự án:**

    Bắt đầu tạo thế giới: python Viettieuthuyet.py (Chọn menu 1 và 2).

    Viết truyện: Chọn menu 3 hoặc 4.

    Biên tập lại: python Bien_Tap.py

##📁 Cấu trúc thư mục

    Viettieuthuyet_Sanderson.py: Script điều khiển chính.

    BienTap_Sanderson.py: Script hậu kỳ, biên tập.

    Data_Worldbuilding/: Chứa các tài liệu về thiết lập thế giới.

    Data_Summaries/: Chứa tóm tắt các chương để nạp ngữ cảnh.

    Chapters/: Chứa bản thảo thô.

    Chapters_Edited/: Chứa bản thảo đã qua biên tập.

##📜 Giấy phép

Dự án được chia sẻ dưới giấy phép MIT. Tự do sử dụng và tùy biến cho mục đích sáng tác cá nhân.