import streamlit as st
from streamlit_calendar import calendar
import pendulum

#st.set_page_config(layout="wide")
st.header('Club Schedule')

calendar_options = {
    "editable": True,
    "selectable": True,
    "headerToolbar": {
        "left": "today prev,next",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek,timeGridDay",
    },


    "slotMinTime": "06:00:00",
    "slotMaxTime": "24:00:00",
    "initialView": "dayGridMonth",
}

calendar_events = [
    {
        "title": "kickOff event",
        "start": "2025-10-31T08:30:00",
        "end": "2025-10-31T10:30:00",
        "className": ["kickoff-event"]
    },
    {
        "title": "Weekly meeting 2",
        "daysOfWeek":[6],
        'startTime':"18:00",
        'endTime': '19:30',
        'startRecur':"2025-10-11",
        "endRecur": "2025-12-31",
        "className": ["meeting-event"]



    },
    {
        "title": "Weekly meeting 1",
        "daysOfWeek": [4],
        'startTime': "18:00",
        'endTime': '19:30',
        'startRecur': "2025-10-16",
        "endRecur": "2025-12-31",
        "className": ["meeting-event"]

    },


]

custom_css = """
    .fc-event-past {
        opacity: 0.8;
    }
    
     .kickoff-event {
        background-color: #1E90FF !important;
        color: #ffffff !important;
        border: 2px solid #1E90FF !important;
    }
     .meeting-event {
        background-color: #28a745 !important;
        color: #ffffff !important;
        border: 2px solid #28a745 !important;
    }
    
    
    .fc-event{
        border: 2px solid #0066cc!important;
        border-radius: 4px;
    }
   
    
    .fc-event-time {
        font-style: italic;
    }
    .fc-event-title {
        font-weight: 700;
    }
    .fc-toolbar-title {
        font-size: 2rem;
    }
    
    
"""




calendar_result = calendar(
    events=calendar_events,
    options=calendar_options,
    custom_css=custom_css,
    key='calendar',
)




if calendar_result.get("eventClick"):
    title=calendar_result['eventClick']['event']['title']
    start=calendar_result['eventClick']['event']['start']
    end=calendar_result['eventClick']['event']['end']

    startDate=pendulum.parse(start).date()
    EndDate=pendulum.parse(end).date()
    startTime=pendulum.parse(start).format("hh:mm A")
    endTime=pendulum.parse(end).format("hh:mm A")
    if startDate==EndDate:
        st.write(f"You clicked on: {title}")
    else:
        st.write(f"You clicked on: {title}{startDate} - {EndDate}")
    st.write(f"**Start time**: {startTime}")
    st.write(f"**End time**: {endTime}")
    st.write("TEST message")
