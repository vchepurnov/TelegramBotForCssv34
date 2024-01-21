def check_spam(last_send_datetime, need_seconds, current_time):
    if not last_send_datetime:
        return True
    else:
        # Разница в секундах между текущим временем и временем последнего сообщения
        delta_seconds = (current_time - last_send_datetime).total_seconds()
        # Осталось ждать секунд перед отправкой
        seconds_left = int(need_seconds - delta_seconds)
        # Если время ожидания не закончилось
        if seconds_left > 0:
            return False
        else:
            return True