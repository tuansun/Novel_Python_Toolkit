import openai
import json
import os

client = openai.OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
MODEL_NAME = "local-model"

DIR_WORLD = "Data_Worldbuilding"
DIR_SUMM = "Data_Summaries"
DIR_CHAP = "Chapters"
FILE_SETTINGS = "Project_Settings.json"

for d in [DIR_WORLD, DIR_SUMM, DIR_CHAP]:
    os.makedirs(d, exist_ok=True)

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
        return f"[LỖI]: {e}"

def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f">> Đã lưu: {filepath}")

def load_file(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

# ==========================================
# GIAI ĐOẠN 1: KHỞI TẠO DỰ ÁN THEO SANDERSON
# ==========================================

def init_project():
    print("\n--- BƯỚC 1: THIẾT LẬP DỰ ÁN ---")
    settings = {
        "title": input("Tên sách: "),
        "lang_main": input("Ngôn ngữ chính (VD: Tiếng Việt): "),
        "lang_sub": input("Ngôn ngữ phụ (nếu có, VD: Tiếng Anh cho thuật ngữ): "),
        "genre": input("Thể loại (VD: Epic Fantasy, Sci-Fi): "),
        "reference_author": input("Tác giả tham khảo (VD: Brandon Sanderson): "),
        "core_idea": input("Ý tưởng cốt lõi (1-2 câu): ")
    }
    with open(FILE_SETTINGS, 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)
    return settings

def generate_worldbuilding_pipeline():
    with open(FILE_SETTINGS, 'r', encoding='utf-8') as f:
        settings = json.load(f)
    
    author_style = settings['reference_author']
    idea = settings['core_idea']
    lang = settings['lang_main']

    print("\n--- ĐANG CHẠY PIPELINE TẠO THẾ GIỚI TỰ ĐỘNG ---")

    # Bước 2: Cốt truyện chính
    print("1/5: Đang phác thảo Cốt truyện chính...")
    sys_plot = f"Bạn là nhà văn mô phỏng phong cách {author_style}. Viết bằng {lang}."
    prompt_plot = f"Dựa trên ý tưởng '{idea}', hãy phác thảo một cốt truyện chính (Main Plot) theo cấu trúc 3 hồi. Tập trung vào lời hứa của câu chuyện (Promises), quá trình (Progress) và sự đền đáp (Payoff)."
    plot = call_llm(sys_plot, prompt_plot)
    save_file(f"{DIR_WORLD}/1_Cot_truyen_chinh.md", plot)

    # Bước 3: Nhân vật
    print("2/5: Đang tạo Tóm tắt Nhân vật...")
    prompt_char = f"Dựa trên cốt truyện sau:\n{plot}\nHãy tạo 3 nhân vật chính. Mỗi nhân vật phải có Động lực, Xung đột nội tâm, và Năng lực đặc biệt."
    chars = call_llm(sys_plot, prompt_char)
    save_file(f"{DIR_WORLD}/2_Nhan_vat.md", chars)

    # Bước 4: Thế giới & Phép thuật (Sanderson's Laws)
    print("3/5: Đang xây dựng Thế giới & Hệ thống (Áp dụng Sanderson's Laws)...")
    prompt_world = (
        f"Dựa trên ý tưởng '{idea}'. Hãy xây dựng Lịch sử, Địa lý, Văn hóa, và Hệ thống năng lượng (công nghệ/phép thuật).\n"
        "BẮT BUỘC áp dụng 3 Định luật của Brandon Sanderson:\n"
        "1. Năng lực phải có quy tắc vật lý/logic rõ ràng để người đọc hiểu.\n"
        "2. Điểm yếu, chi phí (Cost) và giới hạn (Limitations) của năng lực quan trọng hơn sức mạnh.\n"
        "3. Lồng ghép năng lực này sâu vào kinh tế, văn hóa và quân sự của thế giới."
    )
    world = call_llm(sys_plot, prompt_world)
    save_file(f"{DIR_WORLD}/3_The_gioi_va_Phep_thuat.md", world)

    # Bước 5: Điểm cốt truyện (Plot Beats)
    print("4/5: Đang xây dựng các Điểm cốt truyện (Beats)...")
    prompt_beats = f"Dựa trên cốt truyện và thế giới, hãy liệt kê 10-15 sự kiện quan trọng nhất (Plot Beats) từ đầu đến cuối truyện."
    beats = call_llm(sys_plot, prompt_beats)
    save_file(f"{DIR_WORLD}/4_Diem_cot_truyen.md", beats)

    # Bước 6: Dàn ý chi tiết từng chương
    print("5/5: Đang lập Dàn ý từng chương...")
    prompt_outlines = f"Dựa trên các sự kiện sau:\n{beats}\nHãy chia chúng thành 20 chương. Mỗi chương viết 2-3 câu tóm tắt nội dung chính sẽ xảy ra."
    outlines = call_llm(sys_plot, prompt_outlines)
    save_file(f"{DIR_WORLD}/5_Dan_y_tung_chuong.md", outlines)

# ==========================================
# GIAI ĐOẠN 2: VIẾT CHƯƠNG (WORKFLOW CUỐN CHIẾU)
# ==========================================

def write_chapter(chapter_num, target_chunks=4):
    print(f"\n================ BẮT ĐẦU VIẾT CHƯƠNG {chapter_num} ================")
    
    with open(FILE_SETTINGS, 'r', encoding='utf-8') as f:
        settings = json.load(f)
    
    # Nạp dữ liệu cốt lõi (Worldbuilding)
    chars = load_file(f"{DIR_WORLD}/2_Nhan_vat.md")
    world = load_file(f"{DIR_WORLD}/3_The_gioi_va_Phep_thuat.md")
    
    # Kỹ thuật chia nhỏ dàn ý: Chỉ lấy đoạn liên quan đến chương hiện tại (giả định dùng AI để trích xuất hoặc anh tự copy paste)
    # Để đơn giản và an toàn cho token, ta nạp dàn ý tổng nhưng dặn AI chỉ chú ý chương hiện tại
    outlines = load_file(f"{DIR_WORLD}/5_Dan_y_tung_chuong.md")
    
    if chapter_num > 1:
        past_summary = load_file(f"{DIR_SUMM}/Sum_Chuong_{chapter_num - 1}.md")
    else:
        past_summary = "Đây là chương mở đầu."

    system_prompt = (
        f"Bạn là tác giả mô phỏng phong cách của {settings['reference_author']}. "
        f"NHIỆM VỤ DUY NHẤT: Viết CHƯƠNG {chapter_num}.\n\n"
        f"[Hệ thống Thế giới & Giới hạn năng lực]:\n{world}\n\n"
        f"[Nhân vật]:\n{chars}\n\n"
        f"[Tóm tắt chương {chapter_num - 1}]:\n{past_summary}\n\n"
        f"Quy tắc viết:\n"
        f"1. Viết bằng {settings['lang_main']}. Sử dụng văn phong rõ ràng như cửa sổ (windowpane prose), tập trung miêu tả hành động và suy nghĩ nội tâm.\n"
        f"2. Tuân thủ nghiêm ngặt các 'chi phí' và 'giới hạn' của năng lực/công nghệ.\n"
        f"3. Viết khoảng 250 từ, sau đó dừng lại và đưa ra 3 lựa chọn (A, B, C) cho diễn biến tiếp theo."
    )

    chapter_file = f"{DIR_CHAP}/Chuong_{chapter_num}.md"
    chapter_text = ""

    for chunk in range(1, target_chunks + 1):
        if chunk == 1:
            # Gửi kèm Dàn ý vào lượt viết đầu tiên của chương để định hướng
            current_context = f"Dàn ý tổng:\n{outlines}\n\nHãy bắt đầu viết phân đoạn đầu tiên của Chương {chapter_num} dựa trên dàn ý này."
        else:
            current_context = (
                f"Bạn đang viết phân đoạn {chunk} của Chương {chapter_num}.\n"
                f"Nhân vật quyết định: [{choice}]. Viết tiếp diễn biến."
            )
            
        print(f"\n[Đang viết phân đoạn {chunk}...] (Chờ LM Studio xử lý)")
        response = call_llm(system_prompt, current_context, temperature=0.6) # Nhiệt độ 0.6 cho Hard Magic
        print("\n" + response)
        
        chapter_text += response + "\n\n"
        
        if chunk < target_chunks:
            choice = input("\n>> Nhập lựa chọn (A/B/C) hoặc tùy chỉnh: ")
        else:
            print("\n[Đã hoàn thành chương]")

    save_file(chapter_file, chapter_text)

    # Tạo tóm tắt cuốn chiếu
    print(f"\n--- Đang tạo tóm tắt Chương {chapter_num} ---")
    sys_sum = "Bạn là trợ lý. Tóm tắt nội dung sau thành 3 câu, tập trung vào những thay đổi trạng thái của nhân vật và cốt truyện."
    summary = call_llm(sys_sum, f"Tóm tắt:\n{chapter_text}", temperature=0.3)
    save_file(f"{DIR_SUMM}/Sum_Chuong_{chapter_num}.md", summary)

# ==========================================
# MENU ĐIỀU KHIỂN
# ==========================================
def main():
    while True:
        print("\n=== HỆ THỐNG VIẾT TIỂU THUYẾT SANDERSON ===")
        print("1. Khởi tạo Dự án & Settings")
        print("2. Chạy Pipeline Xây dựng Thế giới & Dàn ý (Bước 1-6)")
        print("3. Viết Chương mới (Bước 7)")
        print("0. Thoát")
        
        choice = input("Chọn chức năng: ")
        
        if choice == '1':
            init_project()
        elif choice == '2':
            if not os.path.exists(FILE_SETTINGS):
                print("Vui lòng chạy Bước 1 trước!")
            else:
                generate_worldbuilding_pipeline()
        elif choice == '3':
            c_num = int(input("Nhập số chương muốn viết: "))
            write_chapter(c_num)
        elif choice == '0':
            break

if __name__ == "__main__":
    main()