import openai
import os

# Cấu hình LM Studio
client = openai.OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
MODEL_NAME = "local-model"

DATA_DIR = "Data"
CHAP_DIR = "Chapters"
FILE_DANY = f"{DATA_DIR}/Dan_Y.md"
FILE_CHAR = f"{DATA_DIR}/Nhan_Vat.md"
FILE_SUMMARY = f"{DATA_DIR}/Tom_tat_cac_chuong.md"

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(CHAP_DIR, exist_ok=True)

def read_file(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

def append_to_file(filepath, content):
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write(content + "\n")

def call_llm(system_prompt, user_prompt, temperature=0.7):
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[LỖI API HOẶC QUÁ GIỚI HẠN TOKEN]: {e}"

def summarize_chapter(chapter_num, chapter_content):
    """
    Tối ưu: Chỉ gửi mỗi nội dung chương vào để tóm tắt, không kẹp thêm dàn ý
    để tránh tràn Context Length.
    """
    print(f"\n--- Đang tạo tóm tắt cho Chương {chapter_num} (Tiết kiệm Token) ---")
    
    # Rút gọn System Prompt tối đa cho tác vụ tóm tắt
    system_prompt = "Bạn là trợ lý. Hãy tóm tắt văn bản người dùng cung cấp thành 3-4 câu cực kỳ ngắn gọn."
    
    # Nếu chapter_content quá dài (> 3000 từ), ta có thể phải cắt chuỗi (string slicing) ở đây
    # Nhưng với 4 chunks, thường vẫn an toàn ở mức 8K context.
    summary = call_llm(system_prompt, f"Tóm tắt nội dung sau:\n\n{chapter_content}", temperature=0.3)
    
    append_to_file(FILE_SUMMARY, f"**Tóm tắt Chương {chapter_num}:**\n{summary}\n")
    print(">> Đã lưu tóm tắt.")

def write_chapter(chapter_num, target_chunks=4):
    print(f"\n================ BẮT ĐẦU VIẾT CHƯƠNG {chapter_num} ================")
    
    dan_y = read_file(FILE_DANY)
    characters = read_file(FILE_CHAR)
    past_summaries = read_file(FILE_SUMMARY)
    
    chapter_file = f"{CHAP_DIR}/Chuong_{chapter_num}.md"
    chapter_full_text = ""
    
    # TỐI ƯU 1: Nhắc nhở CỰC MẠNH về việc chỉ viết chương hiện tại
    system_prompt = (
        f"Bạn là một tiểu thuyết gia. NHIỆM VỤ DUY NHẤT CỦA BẠN LÀ VIẾT CHƯƠNG {chapter_num}.\n"
        "TUYỆT ĐỐI KHÔNG chuyển sang chương khác, KHÔNG đề cập đến các chương sau, KHÔNG tự ý kết thúc truyện.\n\n"
        f"--- DỮ LIỆU NỀN ---\n"
        f"Nhân vật:\n{characters}\n\n"
        f"Sự kiện đã qua:\n{past_summaries}\n\n"
        f"Dàn ý tổng thể:\n{dan_y}\n"
        "------------------\n\n"
        "Quy tắc viết:\n"
        "1. Viết thật chi tiết, miêu tả sâu sắc hành động, bối cảnh và cảm xúc. Kéo dài nhịp độ câu chuyện một cách tự nhiên.\n"
        "2. Không lặp lại nội dung đã viết.\n"
        "3. Ở cuối đoạn, DỪNG LẠI và đưa ra 3 lựa chọn (1, 2, 3) cho diễn biến tiếp theo."
    )

    for chunk in range(1, target_chunks + 1):
        print(f"\n[Đang viết phân đoạn {chunk}/{target_chunks} của Chương {chapter_num}...]")
        
        # TỐI ƯU 2: Neo (Anchor) lại số chương ở mỗi lượt
        if chunk == 1:
            current_context = f"Hãy bắt đầu viết phần đầu tiên của Chương {chapter_num}."
        else:
            # Nhắc lại mạnh mẽ để chống ảo giác (Hallucination)
            current_context = (
                f"CHÚ Ý: BẠN ĐANG VIẾT DỞ CHƯƠNG {chapter_num}. ĐÂY LÀ PHÂN ĐOẠN {chunk}.\n"
                f"Dựa trên nội dung vừa viết, nhân vật quyết định: [{choice}].\n"
                "Hãy viết tiếp diễn biến chi tiết dựa trên lựa chọn này, nhớ giữ đúng tuyến thời gian hiện tại và đưa ra 3 lựa chọn mới ở cuối."
            )
            
        response_text = call_llm(system_prompt, current_context)
        print("\n" + response_text)
        
        chapter_full_text += response_text + "\n\n"
        
        if chunk < target_chunks:
            choice = input("\n>> Nhập lựa chọn của bạn (1/2/3) hoặc tùy chỉnh: ")
        else:
            print("\n[Đã đạt đủ số phân đoạn của chương]")
            break

    with open(chapter_file, 'w', encoding='utf-8') as f:
        f.write(chapter_full_text)
    print(f"\n>> Đã lưu file: {chapter_file}")

    # Gọi hàm tóm tắt
    summarize_chapter(chapter_num, chapter_full_text)

def main():
    for file in [FILE_DANY, FILE_CHAR, FILE_SUMMARY]:
        if not os.path.exists(file):
            with open(file, 'w', encoding='utf-8') as f:
                f.write("")

    while True:
        try:
            chap_num = int(input("\nNhập số chương bạn muốn viết (ví dụ: 1) hoặc '0' để thoát: "))
            if chap_num == 0:
                break
            write_chapter(chap_num)
        except ValueError:
            print("Vui lòng nhập một số nguyên.")

if __name__ == "__main__":
    main()