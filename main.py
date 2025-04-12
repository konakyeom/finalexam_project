import customtkinter as ctk
import time
from threading import Thread
from playsound import playsound
from PIL import Image, ImageTk
import os

# 테마 설정
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# 앱 창 생성
app = ctk.CTk()
app.geometry("400x500")
app.title("🥚 귀여운 계란 삶기 어플")

# 상단 타이틀
title_label = ctk.CTkLabel(app, text="🥚 삶기 모드를 골라주세요!", font=("Arial", 20, "bold"))
title_label.pack(pady=20)

# 남은 시간 출력 라벨
status_label = ctk.CTkLabel(app, text="🍳 삶을 모드를 선택하면 시작돼요!", font=("Arial", 16))
status_label.pack(pady=10)

# 달걀 이미지 초기화 (Image 객체 사용)
egg_image = ctk.CTkLabel(app, text="🥚", font=("Arial", 100))
egg_image.pack(pady=20)

# 프로그레스 바
progress = ctk.CTkProgressBar(app, width=300)
progress.pack(pady=20)

# 소리 재생 함수 (백그라운드)
def play_sound(filename):
    sound_path = os.path.join(os.path.dirname(__file__), filename)
    Thread(target=lambda: playsound(sound_path), daemon=True).start()

# 타이머 시작 함수
def start_timer(minutes):
    seconds = minutes * 60
    status_label.configure(text=f"⏳ {minutes}분 삶는 중...")
    egg_image.configure(text="🥚")  # 달걀 이미지 초기화
    play_sound(r"C:\finalterm\eggtimer\sound\start_beep1.wav")

    # 이미지 업데이트 함수
    def update_egg_image(state):
        #이모지 제거
        egg_image.configure(text="")

        if state == "raw":
            egg_img = Image.open(r"C:\finalterm\eggtimer\eggimage\4minegg.png")  # 'egg_raw.png'는 미리 준비된 이미지 파일
        elif state == "half":
            egg_img = Image.open(r"C:\finalterm\eggtimer\eggimage\6minegg.png")  # 'egg_half.png'
        elif state == "cooked":
            egg_img = Image.open(r"C:\finalterm\eggtimer\eggimage\10minegg.png")  # 'egg_cooked.png'
        egg_img = egg_img.resize((100, 100))  # 이미지 크기 조정
        egg_img = ImageTk.PhotoImage(egg_img)  # 이미지 Tkinter 형식으로 변환
        egg_image.configure(image=egg_img)  # Label에 이미지 설정
        egg_image.image = egg_img  # 이미지 참조를 유지하기 위해 설정

    def countdown():
        for t in range(seconds, 0, -1):
            m, s = divmod(t, 60)
            status_label.configure(text=f"⏳ 남은 시간: {m}:{s:02d}")
            progress.set(1 - t / seconds)  # 진행 바 업데이트

            # 달걀 이미지 변화 (시간에 따라 달걀 이미지 변경)
            if t > seconds * 0.7:
                update_egg_image("raw")  # 반숙 전
            elif t > seconds * 0.4:
                update_egg_image("half")  # 반숙
            else:
                update_egg_image("cooked")  # 완숙

            time.sleep(1)
        
        # 완료 시
        
        result = get_result_text(minutes)
        status_label.configure(text=f"✅ 완료! → {result}")
        play_sound(r"C:\finalterm\eggtimer\sound\done_beep1.wav")
        egg_image.configure(image=None, text="🥚")

    Thread(target=countdown, daemon=True).start()

# 결과 문구 반환
def get_result_text(mins):
    if mins <= 4:
        return "반숙 (노른자 흐름) 🥚"
    elif 5 <= mins <= 6:
        return "반숙 (노른자 거의 익음) 🥚"
    elif 7 <= mins <= 8:
        return "완숙 (적당히) 🍳"
    else:
        return "완숙 (꽉 익음) 🍳"

# 버튼 프레임
button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=20)

# 각 버튼 생성 (애니메이션 효과 포함)
def make_timer_button(label, mins, color="#FFD6E8"):
    button = ctk.CTkButton(button_frame, text=label, command=lambda: start_timer(mins), width=140, height=40, fg_color=color, hover_color="FFFFFF", text_color="black")
    return button

# 버튼 생성
btn1 = make_timer_button("🥚 노른자 흘러내림 4분", 4, "#FFD6E8")
btn2 = make_timer_button("🥚 노른자 거의 익음 6분", 6, "#FFF3B0")
btn3 = make_timer_button("🍳 노른자 부드러움 8분", 8, "#C2F0C2")
btn4 = make_timer_button("🍳 노른자 퍽퍽함 10분", 10, "#BDE0FE")

# 버튼 배치 (2줄)
btn1.grid(row=0, column=0, padx=10, pady=10)
btn2.grid(row=0, column=1, padx=10, pady=10)
btn3.grid(row=1, column=0, padx=10, pady=10)
btn4.grid(row=1, column=1, padx=10, pady=10)

# 앱 실행
app.mainloop()
