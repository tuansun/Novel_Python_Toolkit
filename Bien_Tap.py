import openai
import os
import time

# Cấu hình LM Studio
client = openai.OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
MODEL_NAME = "local-model"

# Thư mục
DIR_CHAP = "Chapters"
DIR_EDITED = "Chapters_Edited"

# Đảm bảo thư mục đầu ra tồn tại
os.makedirs(DIR_EDITED, exist_ok=True)

def read_file(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f">> Đã lưu bản biên tập: {filepath}")

def call_llm(system_prompt, user_prompt, temperature=0.3): # Nhiệt độ thấp để AI giữ nguyên cốt truyện, chỉ sửa lỗi
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
        return f"[LỖI API]: {e}"

def split_into_blocks(text, words_per_block=300):
    """Chia toàn bộ chương thành các đoạn nhỏ dựa trên dấu xuống dòng để không cắt ngang câu."""
    paragraphs = text.split('\n\n')
    blocks = []
    current_block = ""
    
    for p in paragraphs:
        if len(current_block.split()) + len(p.split()) < words_per_block:
            current_block += p + "\n\n"
        else:
            if current_block.strip():
                blocks.append(current_block.strip())
            current_block = p + "\n\n"
            
    if current_block.strip():
        blocks.append(current_block.strip())
        
    return blocks

def edit_chapter(chapter_num):
    input_file = f"{DIR_CHAP}/Chuong_{chapter_num}.md"
    output_file = f"{DIR_EDITED}/Chuong_{chapter_num}_Edited.md"
    
    if not os.path.exists(input_file):
        print(f"Lỗi: Không tìm thấy file {input_file}")
        return

    print(f"\n================ ĐANG BẮT ĐẦU BIÊN TẬP CHƯƠNG {chapter_num} ================")
    
    original_text = read_file(input_file)
    blocks = split_into_blocks(original_text, words_per_block=350)
    
    print(f"Chương {chapter_num} đã được chia thành {len(blocks)} khối văn bản để tối ưu VRAM.")
    
    system_prompt = (
        "Bạn là một Biên tập viên văn học chuyên nghiệp, lão luyện trong việc gọt giũa ngôn từ.\n"
        "NHIỆM VỤ CỦA BẠN: Sửa lỗi và nâng cấp đoạn văn bản do tác giả cung cấp.\n\n"
        "QUY TẮC BIÊN TẬP:\n"
        "1. TUYỆT ĐỐI KHÔNG thay đổi cốt truyện, không bịa thêm sự kiện hay nhân vật.\n"
        "2. Sửa các lỗi chính tả, ngữ pháp, câu lủng củng.\n"
        "3. Loại bỏ các từ ngữ lặp đi lặp lại (ví dụ: 'sau đó', 'bất ngờ', 'anh ta').\n"
        "4. Tăng cường tính gợi hình ('Show, don't tell'). Làm cho các đoạn miêu tả cảm xúc và hành động mượt mà hơn.\n"
        "5. Giữ nguyên định dạng phân đoạn, trả về CHỈ văn bản đã sửa, KHÔNG bình luận thêm."
    )

    edited_chapter = ""
    prev_edited_block = "Đây là phần mở đầu chương." # Ngữ cảnh mỏ neo cho khối đầu tiên

    for i, block in enumerate(blocks):
        print(f"\n[Đang biên tập khối {i+1}/{len(blocks)}...]")
        
        user_prompt = (
            f"[Ngữ cảnh đoạn văn NGAY TRƯỚC ĐÓ để đảm bảo văn phong nối tiếp mượt mà]:\n"
            f"...{prev_edited_block[-150:]}...\n\n" # Chỉ lấy 150 ký tự cuối của đoạn trước để mớm nhịp điệu
            f"[ĐOẠN VĂN CẦN BIÊN TẬP]:\n{block}\n\n"
            f"Hãy biên tập lại [ĐOẠN VĂN CẦN BIÊN TẬP] theo đúng các quy tắc. Phải đảm bảo nó nối tiếp hoàn hảo với câu cuối cùng của ngữ cảnh."
        )
        
        edited_block = call_llm(system_prompt, user_prompt, temperature=0.3)
        print(">> Hoàn thành.")
        
        edited_chapter += edited_block + "\n\n"
        prev_edited_block = edited_block # Cập nhật đoạn vừa sửa để làm mỏ neo cho vòng lặp tiếp theo
        
        # Nghỉ 2s để model xả bộ nhớ
        time.sleep(2)

    save_file(output_file, edited_chapter)
    print(f"\n[THÀNH CÔNG] Đã biên tập xong Chương {chapter_num}!")

def main():
    while True:
        print("\n=== HỆ THỐNG BIÊN TẬP (PROOFREADING) ===")
        print("1. Biên tập 1 Chương cụ thể")
        print("2. Biên tập hàng loạt (Từ chương A -> B)")
        print("0. Thoát")
        
        choice = input("Chọn chức năng: ")
        
        if choice == '1':
            try:
                c_num = int(input("Nhập số chương cần biên tập: "))
                edit_chapter(c_num)
            except ValueError:
                print("Vui lòng nhập số hợp lệ.")
        elif choice == '2':
            try:
                start_c = int(input("Từ chương: "))
                end_c = int(input("Đến chương: "))
                for c in range(start_c, end_c + 1):
                    edit_chapter(c)
                    time.sleep(5) # Nghỉ làm mát GPU giữa các chương
            except ValueError:
                print("Vui lòng nhập số hợp lệ.")
        elif choice == '0':
            break

if __name__ == "__main__":
    main()