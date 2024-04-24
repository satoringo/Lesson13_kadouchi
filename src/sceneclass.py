import tkinter as tk
import random
from pygame import mixer
import sys


class App():
    def __init__(self, root = None):
        StartScene(root)

        
class MainScene(tk.Frame):
    def __init__(self, parent = None):
        super().__init__(parent)
        mixer.init()
        self.parent = parent

        mixer.music.set_volume(0.3)
        mixer.music.load("../data/sound/tiktak_sound.mp3")
        mixer.music.play(loops=-1)
        
        self.correct_sound_effect = mixer.Sound("../data/sound/correct_sound.wav")
        self.incorrect_sound_effect = mixer.Sound("../data/sound/incorrect_sound.wav")

        self.pack()
        self.count = 31
        self.score = 0
        self.colors_en = ("white", "black", "red", "green", "blue", "yellow")
        self.colors_jp = ("しろ", "くろ", "あか", "みどり", "あお", "き")
        self.correct_index = 0
        self.correct_answer = ""
        
        self.set_image()
        self.set_instruction_label()
        self.set_time_label()
        self.set_promlem_label()
        self.set_answer_column()
        self.set_score_label()
        self.count_down()

    def set_image(self):
        # 時限爆弾の画像の設置
        self.image = tk.PhotoImage(file = "../data/image/time_bomb.png")
        self.canvas_w, self.canvas_h = self.image.width(), self.image.height()
        self.canvas = tk.Canvas(self, width = self.canvas_w, height = self.canvas_h)
        self.canvas.create_image(self.canvas_w//2, self.canvas_h//2, anchor="c", image=self.image)
        self.canvas.pack(pady = 5)

    def set_instruction_label(self):
        # 指示文を設置
        self.instruction_label = tk.Label(self.canvas, text = "１０問正解して時限爆弾を止めろ！", 
                                          width = 25, height = 2, 
                                          fg = "black", bg = "white", 
                                          font = ("メイリオ", 27, "bold", "underline"))
        self.canvas.create_window(self.canvas_w//2-3, self.canvas_h//2-160, window = self.instruction_label)
    
    def set_time_label(self):
        # 残り時間を設置
        self.time_label = tk.Label(self.canvas, text = self.count_to_time(), 
                                   borderwidth = 3, width = 7, height = 2, 
                                   bg = "black", fg = "red", font = ("Segoe UI", 25, "bold"))
        self.canvas.create_window(self.canvas_w//2-3, self.canvas_h//2+21, window = self.time_label)

    def count_to_time(self):
        # 秒数(count)から時限爆弾表示用の文字列へ
        minutes, seconds = divmod(self.count, 60)
        return f"00:{minutes:02d}:{seconds:02d}"

    def set_promlem_label(self):
        # 問題文を設置
        self.correct_index = random.randint(0, 5)
        self.correct_answer = self.colors_jp[self.correct_index]
        self.problem_label = tk.Label(self.canvas, 
                                      text = self.colors_jp[random.randint(0, 5)], 
                                      width = 10, height = 1, 
                                      fg = self.colors_en[self.correct_index], 
                                      font = ("メイリオ", 40, "bold"), 
                                      borderwidth = 5, relief = "raised")
        self.canvas.create_window(self.canvas_w//2-3, self.canvas_h//2+170, window = self.problem_label)

    def set_answer_column(self):
        #回答欄を設置
        self.answer_column = tk.Entry(self, width = 10,
                                      font = ("メイリオ", 40, "bold"), justify = "center")
        self.answer_column.bind("<Return>", self.answer_callback)
        self.answer_column.pack()
        self.answer_column.focus_set()

    def set_score_label(self):
        # 正解数ラベルを設置
        self.score_label = tk.Label(self, text = "正解数: 0/10", pady = 5,
                                    width = 10, height = 1, fg = "black", 
                                    font = ("メイリオ", 20, "bold"), 
                                    borderwidth = 3, relief = "groove")
        self.score_label.pack()

    def count_down(self):
        if self.count > 0:
            self.count -= 1
            self.time_label["text"] = self.count_to_time()
            self.after(1000, self.count_down)
        else:
            mixer.music.stop()
            mixer.music.load("../data/sound/explosion_sound.mp3")
            mixer.music.play()
            self.after(4000)
            self.delete_scene()
            self.destroy()
            GameOverScene(self.parent)


    def answer_callback(self, event):
        # 回答欄にてEnterを押したときのコールバック関数
        answer = self.answer_column.get()
        if answer == self.correct_answer:
            self.score += 1
            self.score_label["text"] = f"正解数: {self.score}/10"
            self.correct_sound_effect.play()
            if self.score == 10: 
                self.delete_scene()
                self.destroy()
                GameClearScene(self.parent)
                return
        else:
            if self.count >= 5:
                self.count -= 5
                self.time_label["text"] = self.count_to_time()
                self.incorrect_sound_effect.play()
            else:
                self.count = 0
                self.time_label["text"] = self.count_to_time()
            
        self.correct_index = random.randint(0, 5)
        self.correct_answer = self.colors_jp[self.correct_index]
        self.problem_label["text"] = self.colors_jp[random.randint(0, 5)]
        self.problem_label["fg"] = self.colors_en[self.correct_index]
        self.answer_column.delete(0, "end")
        
    def delete_scene(self):
        # 全てのウィジェットを消去する
        mixer.quit()
        for widget in self.winfo_children(): widget.destroy()
        


class StartScene(tk.Frame):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.pack()
        self.parent = parent
        mixer.init()
        mixer.music.set_volume(0.1)
        mixer.music.load("../data/sound/start_scene_bgm.wav")
        mixer.music.play(loops = -1)
        self.button_press_se = mixer.Sound("../data/sound/button_press_sound.wav")

        self.set_title_label()
        self.set_title_image()
        self.set_start_button()
        self.set_quit_button()


    def set_title_label(self):
        self.title_label = tk.Label(self, text = "爆弾解除ゲーム", 
                                        fg = "red", pady = 5,
                                        font = ("メイリオ", 32, "bold"))
        self.title_label.pack()

    def set_title_image(self):
        self.title_image = tk.PhotoImage(file = "../data/image/bomb_defuse.png")
        self.image_label = tk.Label(self, image = self.title_image)
        self.image_label.pack()

    def set_start_button(self):
        self.start_button = tk.Button(self, text = "スタート", 
                                      fg = "black", pady = 5, padx = 5, 
                                      font = ("メイリオ", 20, "bold"), 
                                      command = self.start_button_func)
        self.start_button.pack(side = "left")

    def set_quit_button(self):
        self.quit_button = tk.Button(self, text = "やめる", 
                                     fg = "black", pady = 5, padx = 5, 
                                     font = ("メイリオ", 20, "bold"), 
                                     command = self.quit_button_func)
        self.quit_button.pack(side = "right")

    def start_button_func(self):
        self.button_press_se.play()
        self.after(200)
        self.delete_scene()
        self.destroy()
        ExplainScene(self.parent)

    def quit_button_func(self):
        self.button_press_se.play()
        self.after(200)
        self.delete_scene()
        self.destroy()
        sys.exit(0)

    def delete_scene(self):
        # 全てのウィジェットを消去する
        mixer.quit()
        for widget in self.winfo_children(): widget.destroy()


class ExplainScene(tk.Frame):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.pack()
        self.parent = parent
        mixer.init()
        mixer.music.set_volume(0.1)

        mixer.music.load("../data/sound/explain_scene_bgm.wav")
        mixer.music.play()
        self.button_press_se = mixer.Sound("../data/sound/button_press_sound.wav")

        self.explain_image = tk.PhotoImage(file = "../data/image/explain.PNG")
        self.image_label = tk.Label(self, image = self.explain_image, pady = 5)
        self.image_label.pack()

        self.accept_button = tk.Button(self, text = "ゲームを始める", 
                                       fg = "red", 
                                       font = ("メイリオ", 30, "bold"),
                                       command = self.accept_button_func)
        self.accept_button.pack()

    def accept_button_func(self):
        self.button_press_se.play()
        self.after(200)
        self.delete_scene()
        self.destroy()
        MainScene(self.parent)

    def delete_scene(self):
        # 全てのウィジェットを消去する
        mixer.quit()
        for widget in self.winfo_children(): widget.destroy()


class GameClearScene(tk.Frame):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.pack()
        self.parent = parent

        mixer.init()
        self.button_press_se = mixer.Sound("../data/sound/button_press_sound.wav")
        mixer.music.set_volume(0.1)
        mixer.music.load("../data/sound/gameclear_sound.mp3")
        mixer.music.play()

        self.clear_message = tk.Label(self, text = "クリアおめでとう！", 
                                      fg = "black", height = 1, 
                                      font = ("メイリオ", 30, "bold"))
        self.clear_message.pack()

        self.gameclear_image = tk.PhotoImage(file = "../data/image/gameclear_image.png")
        self.gameclear_image_label = tk.Label(self, image = self.gameclear_image)
        self.gameclear_image_label.pack()

        self.retry_button = tk.Button(self, text = "リトライ", 
                                      fg = "black", 
                                      font = ("メイリオ", 20, "bold"), 
                                      command = self.retry_func)
        self.retry_button.pack(side = "left")

        self.quit_button = tk.Button(self, text = "やめる", 
                                      fg = "black", 
                                      font = ("メイリオ", 20, "bold"), 
                                      command = self.quit_func)
        self.quit_button.pack(side = "right")
        
    def retry_func(self):
        self.button_press_se.play()
        self.after(200)
        self.delete_scene()
        self.destroy()
        MainScene(self.parent)

    def quit_func(self):
        self.button_press_se.play()
        self.after(200)
        self.delete_scene()
        self.destroy()
        sys.exit(0)

    def delete_scene(self):
        # 全てのウィジェットを消去する
        mixer.quit()
        for widget in self.winfo_children(): widget.destroy()


class GameOverScene(tk.Frame):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.pack()
        self.parent = parent

        mixer.init()
        self.button_press_se = mixer.Sound("../data/sound/button_press_sound.wav")
        mixer.music.set_volume(0.1)
        mixer.music.load("../data/sound/gameover_sound.mp3")
        mixer.music.play()

        self.clear_message = tk.Label(self, text = "残念！爆弾処理に失敗した！",  
                                      fg = "black", height = 1, 
                                      font = ("メイリオ", 30, "bold"))
        self.clear_message.pack()

        self.gameover_image = tk.PhotoImage(file = "../data/image/gameover_image.png")
        self.gameover_image_label = tk.Label(self, image = self.gameover_image)
        self.gameover_image_label.pack()

        self.retry_button = tk.Button(self, text = "リトライ", 
                                      fg = "black", 
                                      font = ("メイリオ", 20, "bold"), 
                                      command = self.retry_func)
        self.retry_button.pack(side = "left")

        self.quit_button = tk.Button(self, text = "やめる", 
                                      fg = "black", 
                                      font = ("メイリオ", 20, "bold"), 
                                      command = self.quit_func)
        self.quit_button.pack(side = "right")
        
    def retry_func(self):
        self.button_press_se.play()
        self.after(200)
        self.delete_scene()
        self.destroy()
        MainScene(self.parent)

    def quit_func(self):
        self.button_press_se.play()
        self.after(200)
        self.delete_scene()
        self.destroy()
        sys.exit(0)

    def delete_scene(self):
        # 全てのウィジェットを消去する
        mixer.quit()
        for widget in self.winfo_children(): widget.destroy()

