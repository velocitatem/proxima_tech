from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st
import json
import pandas as pd
from io import StringIO
import plotly.express as px
import random


client = OpenAI()
assistant_id = "asst_gj9B12th1eSiyLGVU6Q9sC9T"


load_dotenv()


class Cache:
    def __init__(self):
        self.cache = "./cache.json"
        try:
            with open(self.cache, "r") as f:
                pass
        except:
            with open(self.cache, "w") as f:
                json.dump({}, f)


    def get(self, key):
        with open(self.cache, "r") as f:
            data = json.load(f)
        return data.get(key, None)


    def set(self, key, value):
        with open(self.cache, "r") as f:
            data = json.load(f)
        data[key] = value
        with open(self.cache, "w") as f:
            json.dump(data, f)


cache = Cache()


NEWS = [
    {"headline": "In 2023, Spain granted 1,154,263 residency documents, a 3% increase from the previous year.", "sentiment_score": 0.7},
    {"headline": "Venezuelan residents in Spain increased by 46% this year, reaching 140,214 approvals.", "sentiment_score": 0.8},
    {"headline": "There was a significant 75% decrease in residency approvals for Ukrainians, with only 43,463 documents issued.", "sentiment_score": -0.6},
    {"headline": "Colombia saw a surge in residency grants, climbing by 38% to 98,583 approvals.", "sentiment_score": 0.75},
    {"headline": "The most common reasons for residency approvals in 2023 were temporary work and exceptional circumstances.", "sentiment_score": 0.5},
    {"headline": "Catalonia and Madrid accounted for over 40% of all residency approvals in 2023.", "sentiment_score": 0.6},
    {"headline": "The average age of foreign residents granted documents in 2023 was 33 years, which has been increasing.", "sentiment_score": 0.3},
    {"headline": "In 2023, 731,946 of the approvals were for temporary residency, indicating a growing trend.", "sentiment_score": 0.6},
    {"headline": "Women constituted 50% of residency approvals, reflecting a balanced gender distribution.", "sentiment_score": 0.65},
    {"headline": "The age demographic among foreign residents shows a youthful trend with 27 years for Pakistanis.", "sentiment_score": 0.4},
    {"headline": "Honduran female residency approvals are notably high, with 70% being women.", "sentiment_score": 0.7},
    {"headline": "There were 12,721 approvals for international protection or statelessness, stable compared to the previous year.", "sentiment_score": 0.5},
    {"headline": "The fluctuation in residency approvals has highlighted the challenges faced by Ukrainians in Spain.", "sentiment_score": -0.7},
    {"headline": "New regulations have allowed an increased diversity of residency types in Spain this year.", "sentiment_score": 0.5},
    {"headline": "Chinese nationals show a 31% increase in residency approvals, indicating stronger ties.", "sentiment_score": 0.8},
    {"headline": "Nicaraguan residency approvals also grew, with a 23% increase noted in 2023.", "sentiment_score": 0.68},
    {"headline": "Madrid experienced the largest annual increase in approvals, with an 18% rise.", "sentiment_score": 0.7},
    {"headline": "The significant drop in approvals for Ukrainians has raised concerns among advocacy groups.", "sentiment_score": -0.8},
    {"headline": "A total of 203,969 residency approvals were granted under exceptional circumstances, marking a 52% increase.", "sentiment_score": 0.75},
    {"headline": "Documentation under the EU's free movement reduced slightly by 2%, continuing a downward trend.", "sentiment_score": -0.5}
]

@st.cache_data
def generate_data(k=50):
    data = {
        "Region": random.choices(["Madrid", "Catalonia", "Andalusia", "Valencia", "Basque Country"], k=k),
        "Demographic_Group": random.choices(
            ["Latin American Immigrants", "Low-income Workers", "Youth", "Elderly", "General Population"], k=k
        ),
        "Trust_in_Government (%)": [round(random.gauss(55, 10), 2) for _ in range(k)],  # Mean of 55 with a SD of 10
        "Corruption_Perception (%)": [round(random.gauss(60, 15), 2) for _ in range(k)],  # Mean of 60 with a SD of 15
        "Citizen_Participation (%)": [round(random.gauss(40, 10), 2) for _ in range(k)],  # Mean of 40 with a SD of 10
        "Policy_Impact_Score": [round(random.gauss(7, 1.5), 2) for _ in range(k)],  # Mean of 7 with a SD of 1.5
        "Social_Media_Sentiment_Score": [round(random.gauss(0, 0.3), 2) for _ in range(k)],  # Mean of 0 with a SD of 0.3
        "Survey_Year": random.choices([2022, 2023, 2024], k=k),
    }

    # Ensure values are within valid ranges
    data["Trust_in_Government (%)"] = [max(0, min(100, v)) for v in data["Trust_in_Government (%)"]]
    data["Corruption_Perception (%)"] = [max(0, min(100, v)) for v in data["Corruption_Perception (%)"]]
    data["Citizen_Participation (%)"] = [max(0, min(100, v)) for v in data["Citizen_Participation (%)"]]
    data["Policy_Impact_Score"] = [max(1, min(10, v)) for v in data["Policy_Impact_Score"]]
    data["Social_Media_Sentiment_Score"] = [max(-1, min(1, v)) for v in data["Social_Media_Sentiment_Score"]]


    synthetic_dataset = pd.DataFrame(data)
    return synthetic_dataset



def extract_data(message_string):
    # get all between ```csv...```
    # multiple blocks like this can be present
    # return a list of csv strings
    data = []
    start = 0
    while True:
        start = message_string.find("```csv", start)
        if start == -1:
            break
        end = message_string.find("```", start+1)
        data.append(message_string[start:end][6:].strip())
        start = end
    return data



def generate_plot(data):
    columns = data.columns
    if len(columns) == 2:
        fig = px.bar(data, x=columns[0], y=columns[1])
    elif len(columns) == 3:
        fig = px.bar(data, x=columns[0], y=columns[1], color=columns[2])
    else:
        fig = px.bar(data, x=columns[0], y=columns[1], color=columns[2], barmode='group')
    return fig





def get_data(question):

    question = "What is the demographic distrubution of immigrants?" if not question else question
    hit = cache.get(question)
    if hit:
        return True, hit


    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=question
    )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    if run.status == "completed":
        messages = client.beta.threads.messages.list(
        thread_id=thread.id
        )
        print(messages.data[0].content[0])
        cache.set(question, messages.data[0].content[0].text.value)
        return True, messages.data[0].content[0].text.value
    else:
        print(run.status)
        return None, run.status


def left_column(col):
    data = generate_data()
    with col[0]:
        # Bar Chart: Trust in Government vs Corruption Perception
        fig = px.scatter(data, x="Trust_in_Government (%)", y="Corruption_Perception (%)", color="Region", title="Trust in Government vs Corruption Perception")
        st.plotly_chart(fig)
        # Heatmap: Trust in Government by Region and Year
        fig = px.density_heatmap(data, x="Survey_Year", y="Region", z="Trust_in_Government (%)", title="Trust in Government by Region and Year")
        st.plotly_chart(fig)
        # Scatter Plot: Social Media Sentiment vs Policy Impact Score
        fig = px.scatter(data, x="Social_Media_Sentiment_Score", y="Policy_Impact_Score", color="Region", title="Social Media Sentiment vs Policy Impact Score")
        st.plotly_chart(fig)
        # Violin Plot: Policy Impact Score by Demographic Group
        fig = px.violin(data, x="Demographic_Group", y="Policy_Impact_Score", title="Policy Impact Score by Demographic Group")
        st.plotly_chart(fig)

def right_column(col):
    # this shoould be a synthetic news feed that is generated by the AI
    with col[2]:
        st.title("News Feed")
        for news in NEWS:
            # color it based on the sentiment score
            st.markdown(f"<span style='color: {'green' if news['sentiment_score'] > 0 else 'red'};'>{news['headline']}</span>", unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Proxima Tech",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded")
    col = st.columns((2.5, 2.5, 2), gap='medium')
    left_column(col)
    right_column(col)
    with col[1]:
        st.title("Proxima Tech Smart Dashboard")
        st.write("This is a smart dashboard that can answer your questions")
    with st.sidebar:
        st.title("Proxima Tech")
        question = st.text_input("Enter your question", "What is the demographic distrubution of immigrants?")
    # show some example questions
        if st.button("Submit"):
            placeholder = st.snow()
            status, messages = get_data(question)
            if status:
                #st.write("Here is the response")
                #st.write(messages)
                data = extract_data(messages)
                figs = []
                for dat in data:
                    df = pd.read_csv(StringIO(dat))
                    #st.write(df)
                    fig = generate_plot(df)
                    figs.append(fig)
                # create an organid dashboard with all the plots in a grid
                with col[1]:
                    for fig in figs:
                        st.plotly_chart(fig)
        else:
            st.write("Something went wrong")

if __name__ == "__main__":
    main()
