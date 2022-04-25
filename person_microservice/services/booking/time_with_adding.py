from datetime import time, timedelta


def time_adding(start_time, duration, coefficient=1):
    start_time = timedelta(
        hours=start_time.hour, minutes=start_time.minute, seconds=start_time.second
    )
    add_time = timedelta(
        hours=duration.hour, minutes=duration.minute, seconds=duration.second
    )
    add_time *= coefficient
    res = start_time + add_time
    hour = res // timedelta(hours=1)
    res -= timedelta(hours=hour)
    minute = res // timedelta(minutes=1)
    second = (res - timedelta(minutes=minute)).seconds
    return time(hour=hour, minute=minute, second=second)


def get_start_time_appointments(start_time, finish_time, duration):
    count_appointment = (
        timedelta(
            hours=finish_time.hour,
            minutes=finish_time.minute,
            seconds=finish_time.second,
        )
        - timedelta(
            hours=start_time.hour, minutes=start_time.minute, seconds=start_time.second
        )
    ) // timedelta(
        hours=duration.hour, minutes=duration.minute, seconds=duration.second
    )
    return [
        time_adding(start_time, duration, coefficient)
        for coefficient in range(count_appointment)
    ]
