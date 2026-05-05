import openai
import json
import os
import time

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

def call_llm_history(messages, temperature=0.7):
    """Hàm gọi API giữ nguyên cấu trúc lịch sử trò chuyện để đảm bảo văn bản liền mạch"""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[LỖI API]: {e}"

def write_chapter(chapter_num, target_chunks=7):
    print(f"\n================ BẮT ĐẦU VIẾT CHƯƠNG {chapter_num} (CẤU TRÚC 7 GIAI ĐOẠN) ================")
    
    with open(FILE_SETTINGS, 'r', encoding='utf-8') as f:
        settings = json.load(f)
    
    chars = load_file(f"{DIR_WORLD}/2_Nhan_vat.md")
    world = load_file(f"{DIR_WORLD}/3_The_gioi_va_Phep_thuat.md")
    outlines = load_file(f"{DIR_WORLD}/5_Dan_y_tung_chuong.md")
    
    past_summary = load_file(f"{DIR_SUMM}/Sum_Chuong_{chapter_num - 1}.md") if chapter_num > 1 else "Mở đầu truyện."

    system_prompt = (
        f"Bạn là tiểu thuyết gia {settings['reference_author']}. NHIỆM VỤ: Viết CHƯƠNG {chapter_num} bám sát phong cách và bối cảnh đã thiết lập.\n\n"
        f"[Dữ liệu thế giới & Nhân vật]:\n{world}\n{chars}\n\n"
        f"[Dàn ý chương {chapter_num} & Tóm tắt trước đó]:\n{outlines}\n- Trước đó: {past_summary}\n\n"
        f"QUY TẮC CỐT LÕI:\n"
        f"1. Viết bằng {settings['lang_main']}. Văn phong 'Show, Don't Tell', miêu tả sâu sắc cảm quan (âm thanh, mùi vị, cảm giác).\n"
        f"2. Áp dụng Định luật Sanderson: Chú trọng giới hạn và cái giá phải trả khi nhân vật sử dụng công nghệ/năng lực.\n"
        f"3. TUYỆT ĐỐI LIỀN MẠCH: Không mào đầu, viết nối tiếp trực tiếp đoạn trước."
    )

    messages = [{"role": "system", "content": system_prompt}]
    chapter_text = ""

    # Cấu trúc 7 giai đoạn
    stage_prompts = {
        1: "Thiết lập bối cảnh hiện tại của chương. Đưa ra 'Lời hứa' (Promise) về xung đột sắp tới. Miêu tả tâm trạng nhân vật.",
        2: "Mở rộng tương tác giữa nhân vật và môi trường. Xây dựng không khí đặc trưng (ví dụ: sự lạnh lẽo của vùng cao, ánh đèn neon cyberpunk).",
        3: "Bắt đầu xuất hiện vật cản hoặc xung đột đầu tiên. Nhân vật phải đưa ra quyết định hoặc sử dụng năng lực/công nghệ.",
        4: "Đẩy cao trào. Miêu tả chi tiết sự khó khăn, các 'giới hạn' và 'chi phí' mà nhân vật phải gánh chịu (Định luật 2).",
        5: "Đỉnh điểm của chương (Payoff). Sự kiện bùng nổ hoặc một khám phá chấn động diễn ra.",
        6: "Hệ quả tức thì của cao trào. Phản ứng cảm xúc của nhân vật sau khi sự việc xảy ra.",
        7: "Kết thúc chương. Giải quyết xong vấn đề hiện tại nhưng phải tạo ra một 'nút thắt' (Cliffhanger) để kéo người đọc sang chương sau."
    }

    for chunk in range(1, target_chunks + 1):
        instruction = stage_prompts[chunk]
        
        if chunk == 1:
            user_msg = f"BẮT ĐẦU CHƯƠNG {chapter_num}: {instruction}"
        else:
            user_msg = f"VIẾT TIẾP PHẦN {chunk}/7: {instruction} Hãy bắt đầu ngay bằng câu văn nối tiếp đoạn trước."

        messages.append({"role": "user", "content": user_msg})
        
        print(f"\n[Đang viết phân đoạn {chunk}/{target_chunks} - {instruction[:40]}...]")
        
        response = call_llm_history(messages, temperature=0.6)
        print("\n" + response)
        
        messages.append({"role": "assistant", "content": response})
        chapter_text += response + "\n\n"

    # Lưu và tóm tắt
    save_file(f"{DIR_CHAP}/Chuong_{chapter_num}.md", chapter_text)
    
    # Tạo tóm tắt chất lượng cao để làm context cho chương sau
    sum_instruction = "Tóm tắt chương này thành 3 câu: 1. Sự kiện chính. 2. Thay đổi quan trọng của nhân vật. 3. Nút thắt cuối cùng."
    summary = call_llm("Bạn là trợ lý biên tập.", f"Nội dung:\n{chapter_text}\n\n{sum_instruction}", temperature=0.3)
    save_file(f"{DIR_SUMM}/Sum_Chuong_{chapter_num}.md", summary)

# ==========================================
# MENU ĐIỀU KHIỂN
# ==========================================
def main():
    while True:
        print("\n=== HỆ THỐNG VIẾT TIỂU THUYẾT SANDERSON ===")
        print("1. Khởi tạo Dự án & Settings")
        print("2. Chạy Pipeline Xây dựng Thế giới & Dàn ý (Bước 1-6)")
        print("3. Viết 1 Chương lẻ (Thủ công)")
        print("4. Viết LIÊN TỤC nhiều chương (Auto Mode - Treo máy)")
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
        elif choice == '4':
            try:
                start_c = int(input("Nhập số chương BẮT ĐẦU (VD: 1): "))
                end_c = int(input("Nhập số chương KẾT THÚC (VD: 10): "))
                
                if start_c > end_c:
                    print("Lỗi: Chương bắt đầu phải nhỏ hơn hoặc bằng chương kết thúc.")
                    continue
                
                print(f"\n[CẢNH BÁO] Hệ thống sẽ tự động viết từ chương {start_c} đến {end_c}.")
                print("VGA của bạn sẽ chạy 100% công suất trong thời gian dài. Vui lòng đảm bảo tản nhiệt tốt!")
                input("Nhấn Enter để xác nhận BẮT ĐẦU treo máy...")
                
                for c_num in range(start_c, end_c + 1):
                    write_chapter(c_num)
                    print(f"\n>>> ĐÃ HOÀN THÀNH CHƯƠNG {c_num} <<<")
                    
                    if c_num < end_c:
                        print("Tạm nghỉ 10 giây để làm mát GPU trước khi chạy chương tiếp theo...\n")
                        time.sleep(10)
                        
                print(f"\n[THÀNH CÔNG] Đã hoàn tất chiến dịch viết tự động từ chương {start_c} đến {end_c}!")
                
            except ValueError:
                print("Vui lòng nhập số nguyên hợp lệ!")
                
        elif choice == '0':
            break

if __name__ == "__main__":
    main()