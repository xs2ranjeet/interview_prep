'''
1889. Design Event Management System
https://enginebogie.com/public/question/design-event-management-system/1889
Medium
You are asked to design and implement a simple Event Management system. The company needs to manage events, track registrations, and generate reports.

You need to create the following classes:

Person

Implements an interface IPerson.
Constructor takes two strings firstName and lastName.
Properties: firstName, lastName.
EventInfo

Implements an interface IEventInfo.

Constructor initializes:

string eventName
Date eventDate
int capacity
boolean canceled
Two lists:

Registration (list of registered people)
Attendees (list of attendees)
Methods:

Register(IPerson person) → Adds person to Registration list only if:

Event is not canceled
Capacity not full
Person not already registered
Attend(IPerson person) → Adds person to Attendees list only if:

Event is not canceled
Person is already registered
Person not already marked as attendee
EventManager

Implements an interface IEventManager.

Constructor initializes Events list.

Methods:

AddEvent(IEventInfo event) → Adds new event if not already present.
Register(eventName, IPerson person) → Registers a person for given event if it exists.
Attend(eventName, IPerson person) → Marks person as attendee for given event if it exists.
GetEventCountByYears() → Returns list of strings showing total number of events grouped by year.
GetEventRegistrationCountByYears() → Returns list of strings showing total registrations grouped by year.
GetEventAttendeesCountByYears() → Returns list of strings showing total attendees grouped by year.
Example:

People: Jane Smith, John Doe, Richard Roe Events: Event1 in 2021, Event2 in 2020

Actions:

John Doe registered for Event1
John Doe registered for Event2
Richard Roe registered for Event1
Jane Smith registered for Event1
Jane Smith registered for Event2
John Doe attended Event1
Richard Roe attended Event1
Output:

Event Count:
2020 - 1
2021 - 1

Registrations:
2020 - 2
2021 - 3

Attendees:
2020 - 0
2021 - 2
'''

