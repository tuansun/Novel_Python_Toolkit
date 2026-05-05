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

    print("\n--- ĐANG CHẠY PIPELINE TẠO THẾ GIỚI LIÊN KẾT ---")
    
    # System prompt chung cho toàn bộ quá trình setup
    sys_setup = f"Bạn là nhà văn mô phỏng phong cách {author_style}. Ngôn ngữ đầu ra BẮT BUỘC là {lang}."

    # Bước 1: Cốt truyện chính
    print("1/5: Đang phác thảo Cốt truyện chính...")
    prompt_plot = (
        f"[Ý TƯỞNG CỐT LÕI]: {idea}\n\n"
        f"[NHIỆM VỤ]: Phác thảo cốt truyện chính (Main Plot) theo cấu trúc 3 hồi. "
        f"Bắt buộc thể hiện rõ: Promise (Hứa hẹn ban đầu) -> Progress (Thử thách tiến triển) -> Payoff (Cao trào và đền đáp)."
    )
    plot = call_llm(sys_setup, prompt_plot)
    save_file(f"{DIR_WORLD}/1_Cot_truyen_chinh.md", plot)

    # Bước 2: Nhân vật (Ép liên kết với Cốt truyện)
    print("2/5: Đang tạo Tóm tắt Nhân vật...")
    prompt_char = (
        f"[DỮ LIỆU NỀN - CỐT TRUYỆN]:\n{plot}\n\n"
        f"[NHIỆM VỤ]: Tạo 3 nhân vật chính XUẤT HIỆN TRONG CỐT TRUYỆN TRÊN. "
        f"Mỗi nhân vật phải nêu rõ: Tên, Động lực, Xung đột nội tâm, và Vai trò của họ trong cốt truyện này."
    )
    chars = call_llm(sys_setup, prompt_char)
    save_file(f"{DIR_WORLD}/2_Nhan_vat.md", chars)

    # Bước 3: Thế giới & Phép thuật (Ép liên kết với Ý tưởng, Nhân vật và Cốt truyện)
    print("3/5: Đang xây dựng Thế giới & Hệ thống...")
    prompt_world = (
        f"[DỮ LIỆU NỀN]:\n- Cốt truyện: {plot}\n- Nhân vật: {chars}\n\n"
        f"[NHIỆM VỤ]: Xây dựng Hệ thống năng lượng/công nghệ/phép thuật cho thế giới này.\n"
        f"BẮT BUỘC TUÂN THỦ SANDERSON'S LAWS:\n"
        f"1. Xác định rõ loại hệ thống (Cứng hay Mềm).\n"
        f"2. Nêu rõ GIỚI HẠN (thứ không thể làm) và CÁI GIÁ PHẢI TRẢ (Cost) khi các nhân vật trên sử dụng năng lực này.\n"
        f"3. Hệ thống này định hình kinh tế/xã hội trong cốt truyện thế nào?"
    )
    world = call_llm(sys_setup, prompt_world)
    save_file(f"{DIR_WORLD}/3_The_gioi_va_Phep_thuat.md", world)

    # Bước 4: Điểm cốt truyện (Khóa chặt vào Nhân vật & Thế giới)
    print("4/5: Đang xây dựng các Điểm cốt truyện (Beats)...")
    prompt_beats = (
        f"[DỮ LIỆU NỀN]:\n- Nhân vật: {chars}\n- Giới hạn Thế giới: {world}\n- Cốt truyện tổng quát: {plot}\n\n"
        f"[NHIỆM VỤ]: Liệt kê 10-15 sự kiện quan trọng nhất (Plot Beats) theo trình tự thời gian.\n"
        f"QUY TẮC TỐI THƯỢNG:\n"
        f"- CÁC SỰ KIỆN PHẢI SỬ DỤNG ĐÚNG CÁC NHÂN VẬT VÀ BỐI CẢNH TRÊN.\n"
        f"- KHÔNG ĐƯỢC TỰ BỊA THÊM nhân vật mới, phe phái mới hay phép thuật mới ngoài [DỮ LIỆU NỀN]."
    )
    beats = call_llm(sys_setup, prompt_beats)
    save_file(f"{DIR_WORLD}/4_Diem_cot_truyen.md", beats)

    # Bước 5: Dàn ý chi tiết từng chương (Ép bám sát Plot Beats)
    print("5/5: Đang lập Dàn ý từng chương...")
    prompt_outlines = (
        f"[DỮ LIỆU NỀN - TIẾN TRÌNH SỰ KIỆN]:\n{beats}\n\n"
        f"[NHIỆM VỤ]: Chuyển đổi chính xác các sự kiện trên thành DÀN Ý 20 CHƯƠNG. "
        f"Mỗi chương gồm 2-3 câu tóm tắt nội dung. KHÔNG THÊM THẮT SỰ KIỆN NGOÀI TIẾN TRÌNH."
    )
    outlines = call_llm(sys_setup, prompt_outlines)
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
        f"Bạn là tác giả mô phỏng {settings['reference_author']}. NHIỆM VỤ CỦA BẠN: BÁM SÁT DỮ LIỆU VÀ VIẾT CHƯƠNG {chapter_num}.\n\n"
        f"--- DỮ LIỆU NỀN BẮT BUỘC ---\n"
        f"[Thế giới & Giới hạn năng lực]:\n{world}\n\n"
        f"[Tuyến Nhân Vật]:\n{chars}\n\n"
        f"[Dàn ý Toàn truyện]:\n{outlines}\n"
        f"-> CHÚ Ý: ĐỐI CHIẾU DÀN Ý TRÊN, BẠN HIỆN CHỈ ĐƯỢC PHÉP VIẾT NỘI DUNG CỦA CHƯƠNG {chapter_num}. KHÔNG VIẾT VƯỢT QUÁ CHƯƠNG NÀY.\n\n"
        f"[Tóm tắt diễn biến ngay trước Chương {chapter_num}]:\n{past_summary}\n"
        f"---------------------------\n\n"
        f"BỘ QUY TẮC VIẾT (SANDERSON'S LAWS):\n"
        f"1. Định luật 1 & 3: Bám sát [DỮ LIỆU NỀN]. Tuyệt đối KHÔNG bịa thêm nhân vật, địa danh hay phép thuật mới. Không có 'phép màu' từ trên trời rơi xuống để cứu nhân vật.\n"
        f"2. Định luật 2 (Giới hạn): Miêu tả rõ điểm yếu, cái giá phải trả (Cost) về thể chất/tài nguyên khi nhân vật hành động.\n"
        f"3. Cấu trúc: Thúc đẩy cốt truyện tiến lên theo đúng dàn ý của CHƯƠNG {chapter_num}, giải quyết xung đột hoặc tạo bí ẩn mới.\n\n"
        f"ĐỊNH DẠNG ĐẦU RA:\n"
        f"- Viết bằng {settings['lang_main']}. Miêu tả chi tiết, văn phong điện ảnh.\n"
        f"- Cuối bài viết, BẮT BUỘC DỪNG LẠI và đưa ra 3 lựa chọn diễn biến tiếp theo cho đoạn kế tiếp, đánh số 1, 2, 3."
    )

    chapter_file = f"{DIR_CHAP}/Chuong_{chapter_num}.md"
    chapter_text = ""

    for chunk in range(1, target_chunks + 1):
        if chunk == 1:
            current_context = f"Dàn ý tổng:\n{outlines}\n\nHãy bắt đầu viết phân đoạn đầu tiên của Chương {chapter_num} dựa trên dàn ý này. Nhớ đưa ra 3 lựa chọn 1, 2, 3 ở cuối."
        else:
            current_context = (
                f"Bạn đang viết phân đoạn {chunk} của Chương {chapter_num}.\n"
                f"Nhân vật quyết định chọn hướng đi số: [{choice}]. Viết tiếp diễn biến một cách logic và hấp dẫn. Cuối đoạn đưa ra 3 lựa chọn 1, 2, 3 mới."
            )
            
        print(f"\n[Đang viết phân đoạn {chunk}...] (Chờ LM Studio xử lý)")
        response = call_llm(system_prompt, current_context, temperature=0.6)
        print("\n" + response)
        
        chapter_text += response + "\n\n"
        
        if chunk < target_chunks:
            # Thay đổi A/B/C thành 1/2/3
            choice = input("\n>> Nhập lựa chọn (1/2/3) hoặc nhập diễn biến tùy chỉnh: ")
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