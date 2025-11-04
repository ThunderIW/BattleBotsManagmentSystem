import orjson
import streamlit as st
from networkx.algorithms.operators.binary import difference
from streamlit_calendar import calendar
import pendulum
import database_backend as db

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

calendar_events=db.get_events()


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
    with st.container(border=True):
        title=calendar_result['eventClick']['event']['title']
        start=calendar_result['eventClick']['event']['start']
        end=calendar_result['eventClick']['event']['end']
        event_description=calendar_result['eventClick']['event']['extendedProps'].get('description')

        startDate=pendulum.parse(start).date()
        EndDate=pendulum.parse(end).date()
        startTime=pendulum.parse(start).time()
        endTime=pendulum.parse(end).time()
        if startDate==EndDate:
            st.write(f"You clicked on: {title}")
        else:
            st.write(f"You clicked on: {title}{startDate} - {EndDate}")
        difference=endTime-startTime
        st.write(f"- **Duration**: {startTime.format('hh:mm A')} - {endTime.format('hh:mm A')} (**{difference.in_words()}**)")
        st.write(f"- **Event Details**: {event_description}")
st.page_link(page="MainGUIStreamlit.py",label="Click here to add more events",icon=":material/calendar_add_on:")