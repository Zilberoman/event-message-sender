# Deduplication helpers
def has_sent_template_ever(user_id, template, get_sends_func):
    return any(s.template_name == template and not s.suppressed for s in get_sends_func(user_id))

def has_sent_template_today(user_id, template, ts, get_sends_by_user):
    day = ts.date()
    return any(s.template_name == template
               and not s.suppressed
               and s.timestamp.date() == day for s in get_sends_by_user(user_id))
