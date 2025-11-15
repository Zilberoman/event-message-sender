from collections import defaultdict

from core.models.dto.send_log import SendLog

sends_by_user = defaultdict(list)

def store_send_log(log: SendLog):
    sends_by_user[log.user_id].append(log)

def get_user_sends(user_id):
    return sends_by_user[user_id]