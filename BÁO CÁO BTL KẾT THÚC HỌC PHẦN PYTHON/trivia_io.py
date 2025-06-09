import tkinter as tk
from tkinter import messagebox

# Hàm đọc file (tái sử dụng từ Bước 1)
def open_file(filename):
    """
    Mở file câu hỏi và xử lý lỗi.
    Trả về đối tượng file hoặc None nếu có lỗi.
    """
    try:
        file = open(filename, 'r', encoding='utf-8')
        return file
    except FileNotFoundError:
        print(f"Lỗi: File '{filename}' không tồn tại!")
        return None
    except Exception as e:
        print(f"Lỗi khi mở file: {e}")
        return None

def next_block(file):
    """
    Đọc một khối câu hỏi từ file.
    Trả về dictionary chứa thông tin câu hỏi hoặc None nếu hết câu hỏi.
    """
    title = file.readline().strip()
    if not title:
        return None
    
    question = file.readline().strip()
    options = [file.readline().strip() for _ in range(4)]
    answer_line = file.readline().strip()
    explanation = file.readline().strip()
    
    if not answer_line.startswith("Đáp án: "):
        print(f"Lỗi định dạng: Dòng đáp án không đúng định dạng: {answer_line}")
        return None
    
    answer = answer_line.replace("Đáp án: ", "").strip()
    
    empty_line = file.readline().strip()
    if empty_line and empty_line != "":
        print(f"Lỗi định dạng: Dòng trống bị thiếu sau câu hỏi: {title}")
        return None
    
    return {
        "title": title,
        "question": question,
        "options": options,
        "answer": answer,
        "explanation": explanation
    }

# Class GUI
class TriviaGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Trivia Challenge")
        self.root.geometry("450x400")
        self.root.configure(bg="#f0f0f0")  # Màu nền xám nhạt

        # Khởi tạo biến
        self.score = 0
        self.current_question = None
        self.file = open_file("questions.txt")
        if not self.file:
            messagebox.showerror("Lỗi", "Không thể mở file questions.txt!")
            self.root.destroy()
            return
        
        # Frame chính
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(expand=True, padx=20, pady=20)

        # Tiêu đề
        self.title_label = tk.Label(self.main_frame, text="Trivia Challenge", font=("Arial", 16, "bold"), fg="#2c3e50", bg="#f0f0f0")
        self.title_label.pack(pady=(0, 20))

        # Label cho câu hỏi
        self.question_label = tk.Label(self.main_frame, text="", font=("Arial", 12), fg="#2c3e50", bg="#ffffff", wraplength=350, justify="left", padx=10, pady=10, relief="groove")
        self.question_label.pack(pady=10)

        # Entry cho đáp án
        self.answer_entry = tk.Entry(self.main_frame, font=("Arial", 12), width=20)
        self.answer_entry.pack(pady=10)

        # Button Nộp
        self.submit_button = tk.Button(self.main_frame, text="Nộp", font=("Arial", 12), bg="#3498db", fg="white", padx=10, pady=5, relief="raised", command=self.submit_answer)
        self.submit_button.pack(pady=10)

        # Label cho điểm
        self.score_label = tk.Label(self.main_frame, text=f"Điểm: {self.score}", font=("Arial", 12), fg="#2c3e50", bg="#ffffff", padx=10, pady=5, relief="groove")
        self.score_label.pack(pady=10)

        # Button Kết thúc
        self.end_button = tk.Button(self.main_frame, text="Kết thúc", font=("Arial", 12), bg="#e74c3c", fg="white", padx=10, pady=5, relief="raised", command=self.end_game)
        self.end_button.pack(pady=10)

        # Nạp câu hỏi đầu tiên
        self.load_next_question()

    def load_next_question(self):
        self.current_question = next_block(self.file)
        if self.current_question:
            # Tạo chuỗi văn bản với định dạng rõ ràng (thêm A, B, C, D)
            question_text = f"{self.current_question['question']}\n" \
                          f"{self.current_question['options'][0]}\n" \
                          f"{self.current_question['options'][1]}\n" \
                          f"{self.current_question['options'][2]}\n" \
                          f"{self.current_question['options'][3]}"
            self.question_label.config(text=question_text)
            self.answer_entry.delete(0, tk.END)
        else:
            messagebox.showinfo("Kết thúc", f"Trò chơi kết thúc! Điểm của bạn: {self.score}")
            self.root.destroy()

    def submit_answer(self):
        if self.current_question:
            user_answer = self.answer_entry.get().strip().upper()
            correct_answer = self.current_question['answer']
            if user_answer == correct_answer:
                self.score += 1
                messagebox.showinfo("Đúng", "Chúc mừng! Đáp án đúng!", parent=self.root)
            else:
                messagebox.showinfo("Sai", f"Đáp án sai! Đáp án đúng là: {correct_answer}", parent=self.root)
            self.score_label.config(text=f"Điểm: {self.score}")
            self.load_next_question()

    def end_game(self):
        messagebox.showinfo("Kết thúc", f"Trò chơi kết thúc! Điểm của bạn: {self.score}", parent=self.root)
        self.root.destroy()

# Khởi chạy ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    app = TriviaGame(root)
    root.mainloop()