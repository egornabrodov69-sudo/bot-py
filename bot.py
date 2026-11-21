import telebot
import os

TOKEN = '8933466476:AAH5KuJvl-TfX9_IwlP5FKJwi6DstDSFNiE'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Здорово! Скинь ссылку на видео или само видео файлом.")

@bot.message_handler(func=lambda message: message.text and 'http' in message.text)
def handle_link(message):
    url = message.text.strip()
    bot.reply_to(message, "📥 Качаю и уникализирую...")
    input_p = 'input.mp4'
    output_p = 'output.mp4'
    try:
        os.system(f"yt-dlp -o {input_p} '{url}'")
        cmd = f"ffmpeg -y -i {input_p} -vf 'noise=c0s=4:all_flags=t,eq=brightness=0.002' -c:a copy {output_p}"
        os.system(cmd)
        with open(output_p, 'rb') as v:
            bot.send_video(message.chat.id, v)
        if os.path.exists(input_p): os.remove(input_p)
        if os.path.exists(output_p): os.remove(output_p)
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

@bot.message_handler(content_types=['video'])
def handle_video(message):
    bot.reply_to(message, "⏳ Обрабатываю файл...")
    input_p = 'input.mp4'
    output_p = 'output.mp4'
    try:
        file_info = bot.get_file(message.video.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(input_p, 'wb') as f:
            f.write(downloaded_file)
        cmd = f"ffmpeg -y -i {input_p} -vf 'noise=c0s=4:all_flags=t,eq=brightness=0.002' -c:a copy {output_p}"
        os.system(cmd)
        with open(output_p, 'rb') as v:
            bot.send_video(message.chat.id, v)
        if os.path.exists(input_p): os.remove(input_p)
        if os.path.exists(output_p): os.remove(output_p)
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

print("🚀 Бот запущен!")
bot.polling(none_stop=True)
