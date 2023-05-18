import os


def save_audio(file):
    os.chdir("/usr/audio")
    try:
        audio = file.file.read()
        with open(file.filename, 'wb') as f:
            f.write(audio)
    except Exception:
        return {"message": "Ошибка при загрузке аудио"}
    finally:
        file.file.close()
    return file.filename


def audio_name(name):
    r = name.split('.')
    return r[0] + '.mp3'
