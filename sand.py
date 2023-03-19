from datetime import datetime

event_id = datetime.now().strftime("_%d.%m.%Y-%H:%M:%S")

print(event_id)