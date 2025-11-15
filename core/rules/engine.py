import os
from datetime import timedelta
from typing import List, Callable

import yaml

from core.models.decision import Decision
from core.models.dto.event import Event
from core.models.match_condition_result import MatchConditionResult

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RULES_PATH = os.path.join(BASE_DIR, "config", "rules.yaml")

with open(RULES_PATH, "r") as f:
    print(f"Loading rules from: {RULES_PATH}")
    rules_data = yaml.safe_load(f)
    print("Loaded rules:", rules_data)


# class RuleEngine:
#     def apply_rules(self, event: Event):
#         rules: List[Callable[[Event], Optional[Decision]]] = [
#             self.signup_welcome,
#             self.bank_link_nudge,
#             self.insufficient_funds_email,
#             self.high_risk_alert
#         ]
#
#         decisions: List[Decision] = []
#         for rule in rules:
#             decision = rule(event)
#             if decision:
#                 decisions.append(decision)
#         return decisions
#
#     @staticmethod
#     def signup_welcome(event: Event):
#         if event.event_type != EventType.SIGNUP_COMPLETED:
#             return None
#
#         if not event.user_traits.get("marketing_opt_in", False):
#             return None
#
#         if has_sent_template_ever(event.user_id, "WELCOME_EMAIL", get_user_sends):
#             return Decision(event.user_id, "WELCOME_EMAIL", "email",
#         "skipped: already sent", event, should_send = False)
#         return Decision(event.user_id, "WELCOME_EMAIL", "email",
#                         "signup completed, user opted in", event, should_send = True)
#
#     @staticmethod
#     def bank_link_nudge(event: Event):
#         if event.event_type != EventType.LINK_BANK_SUCCESS:
#             return None
#
#         events = get_user_events(event.user_id)
#         signup_events = [signup_event for signup_event in events
#                          if signup_event.event_type == EventType.SIGNUP_COMPLETED]
#
#         if not signup_events:
#             return None
#
#         last_signup = signup_events[-1]
#
#         if event.event_timestamp - last_signup.event_timestamp > timedelta(hours = 24):
#             return None
#
#         if has_sent_template_ever(event.user_id, "BANK_LINK_NUDGE_SMS", get_user_sends):
#             return Decision(event.user_id, "BANK_LINK_NUDGE_SMS", "sms",
#                             "skipped: already sent", event, should_send = False)
#
#         return Decision(event.user_id, "BANK_LINK_NUDGE_SMS", "sms",
#                         "bank linked within 24h of signup", event, should_send = True)
#
#     @staticmethod
#     def insufficient_funds_email(event: Event):
#         if event.event_type != EventType.PAYMENT_FAILED:
#             return None
#
#         if event.properties.get("failure_reason") != "INSUFFICIENT_FUNDS":
#             return None
#
#         if has_sent_template_today(event.user_id, "INSUFFICIENT_FUNDS_EMAIL", event.event_timestamp,
#                                    get_user_sends):
#             return Decision(event.user_id, "INSUFFICIENT_FUNDS_EMAIL", "email",
#                             "skipped: already sent today", event, should_send = False)
#         return Decision(event.user_id, "INSUFFICIENT_FUNDS_EMAIL", "email",
#                         "payment failed: insufficient funds", event, should_send = True)
#
#     @staticmethod
#     def high_risk_alert(event: Event):
#         if event.event_type != EventType.PAYMENT_FAILED:
#             return None
#
#         if event.properties.get("attempt_number", 0) >= 3:
#             return Decision(event.user_id, "HIGH_RISK_ALERT", "internal_alert",
#                             "payment failed 3+ times", event, should_send = True)
#
#         return None
#
#
# rule_engine = RuleEngine()

class RuleEngine:
    def __init__(self, rules):
        self.rules = rules

    def apply_rules(self, event: Event, get_user_events: Callable, get_user_sends: Callable,
                    has_sent_template_today: Callable, has_sent_template_ever: Callable):
        decisions: List[Decision] = []

        for rule in self.rules:
            match_condition_result: MatchConditionResult = self.match_condition(rule["condition"], event, get_user_events,
                                                                              get_user_sends, has_sent_template_today,
                                                                              has_sent_template_ever, rule)
            if match_condition_result.is_success:
                decision = self.create_decision(rule["action"], event)
                decisions.append(decision)
            else:
                if match_condition_result.should_create_decision:
                    decision = self.create_decision(rule["action"], event, reason = match_condition_result.reason,
                                                    should_send = False)
                    decisions.append(decision)

        return decisions

    @staticmethod
    def match_condition(
            cond,
            event,
            get_user_events,
            get_user_sends,
            has_sent_template_today,
            has_sent_template_ever,
            rule) -> MatchConditionResult:

        # Check event_type
        if "event_type" in cond and event.event_type.value.lower() != cond["event_type"].lower():
            return MatchConditionResult(False)

        # Check user_traits
        if "user_traits" in cond:
            for k, v in cond["user_traits"].items():
                user_trait = event.user_traits.get(k);

                if user_trait != v:
                    return MatchConditionResult(False)

        # Check properties
        if "properties" in cond:
            for k, v in cond["properties"].items():
                if isinstance(v, dict):
                    if "gte" in v and event.properties.get(k, 0) < v["gte"]:
                        return MatchConditionResult(False)
                else:
                    if event.properties.get(k) != v:
                        return MatchConditionResult(False)

        # Check once_per_day for deduplication
        if cond.get("once_per_day", False):
            if has_sent_template_today(event.user_id, rule["action"]["send_template"], event.event_timestamp,
                                       get_user_sends):
                return MatchConditionResult(False, True, "skipped: already sent today")

        # Check once for deduplication
        if cond.get("once", False):
            if has_sent_template_ever(event.user_id, rule["action"]["send_template"],
                                     get_user_sends):
                return MatchConditionResult(False, True, "skipped: already sent")

        # check condition within_hours_of
        if "within_hours_of" in cond:
            ref_events = get_user_events(event.user_id)
            target = cond["within_hours_of"]
            ref_evts = [e for e in ref_events if e.event_type.value == target["event_type"]]

            if not ref_evts:
                return MatchConditionResult(False)
            last_evt = ref_evts[-1]

            if event.event_timestamp - last_evt.event_timestamp > timedelta(hours=target["hours"]):
                return MatchConditionResult(False)

        return MatchConditionResult(True)

    @staticmethod
    def create_decision(action, event, *, should_send: bool = None, reason: str = None):
        final_reason = reason if reason is not None else action.get("reason", "")
        final_should_send = should_send if should_send is not None else True

        if "send_template" in action:
            return Decision(event.user_id, action["send_template"], action["channel"], final_reason, event,
                            final_should_send)

        if "escalate" in action:
            return Decision(event.user_id, action["escalate"], action["channel"], final_reason, event,
                            final_should_send)

        return None

rule_engine = RuleEngine(rules_data["rules"])