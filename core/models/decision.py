from core.models.dto.send_log import SendLog

class Decision:
    def __init__(self, user_id, template, channel, reason, event, should_send):
        self.user_id = user_id
        self.template = template
        self.channel = channel
        self.reason = reason
        self.event = event
        self.should_send = should_send

    def to_send_log(self):
        return SendLog(
            user_id = self.user_id,
            template_name = self.template,
            channel = self.channel,
            timestamp = self.event.event_timestamp,
            reason = self.reason,
            suppressed = False
        )

    def to_suppression_log(self):
        return SendLog(
            user_id = self.user_id,
            template_name = self.template,
            channel = self.channel,
            timestamp = self.event.event_timestamp,
            reason = self.reason,
            suppressed = True
        )
