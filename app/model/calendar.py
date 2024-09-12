from dataclasses import dataclass, field
from datetime import datetime, date, time
from email.policy import default
from platform import system
from typing import ClassVar

from app.services.util import generate_unique_id, date_lower_than_today_error, event_not_found_error, \
    reminder_not_found_error, slot_not_available_error


# TODO: Implement Reminder class here
@dataclass
class Reminder:
    date_time: datetime
    EMAIL: str = "email"
    SYSTEM: str = "system"
    type: str = EMAIL

    def __str__(self):
        return f"Reminder on {self.date_time} of type {self.type}"


# TODO: Implement Event class here
@dataclass
class Event:
    title: str
    description: str
    date_: date
    start_at: time
    end_at: time
    reminders: list[Reminder] = field(default_factory = list)
    id: str = field(default_factory = generate_unique_id)

    def add_reminder(self,date_time: datetime, type: str):
        new_object = Reminder(date_time, type)
        self.reminders.append(new_object)

    def delete_reminder(self, reminder_index: int):
        for e in self.reminders:
            if e in self.reminders:
                self.reminders.remove(e)
            else:
                reminder_not_found_error()

    def _str_(self) -> str:
        return (f"ID: {self.id}\n"
                f"Event title: {self.title}\n"
                f"Description: {self.description}\n"
                f"Time: {self.start_at} - {self.end_at}")

# TODO: Implement Day class here
class Day:

    def __init__(self, date_: date):
        self.date_: date
        self.slots: dict[time, str | None] = {}
        self._init_slots()

    def _init_slots(self):
        for hour in range(24):
            for minute in range(0, 60 ,15):
                self.slots[time(hour, minute)] = None

    def add_event(self, event_id: str, start_at: time, end_at: time):
        for slot_time in self.slots:
            if start_at <= slot_time < end_at:
                if self.slots[slot_time] is not None:
                    slot_not_available_error()
                self.slots[slot_time] = event_id

    def delete_event(self, event_id: str):
        deleted = False
        for slot, saved_id in self.slots.items():
            if saved_id == event_id:
                self.slots[slot] = None
                deleted = True
        if not deleted:
            event_not_found_error()

    def update_event(self, event_id: str, start_at: time, end_at: time):
        for slot in self.slots:
            if self.slots[slot] == event_id:
                self.slots[slot] = None

        for slot in self.slots:
            if start_at <= slot < end_at:
                if self.slots[slot]:
                    slot_not_available_error()
                else:
                    self.slots[slot] = event_id
# TODO: Implement Calendar class here

class Calendar:

    def __init__(self):
        self.days: dict[date, Day] = {}
        self.events: dict[str, Event] = {}
        self.today = None

    def add_event(self, title: str, description: str, date_: date, start_at: time, end_at: time):
        self.today = datetime.now().date()
        if date_ < self.today:
            date_lower_than_today_error()

        if date_ not in self.days:
            other_object_day = Day(date_)
            self.days[date_] = other_object_day

        other_object_event = Event(title, description, date_, start_at, end_at)
        Day.add_event(other_object_event) #revisar esto
        self.events[Event.id] = other_object_event
        return Event.id















