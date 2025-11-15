# Deduplication helpers
def has_sent_template_ever(user_id, template, get_sends_func):
    return any(s.template_name == template and not s.suppressed for s in get_sends_func(user_id))