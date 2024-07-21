import streamlit as st
import openai
import os
from dotenv import load_dotenv
import random
import pyodbc
import assemblyai as aai

load_dotenv()

openai.api_type = os.getenv("OPENAI_API_TYPE", "azure")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")
deployment_id = os.getenv("AZURE_DEPLOYMENT_ID")


aai.settings.api_key = "8bcec297f6c1463cb388aa52b7e121af"
transcriber = aai.Transcriber()

st.set_page_config(
    page_title="GapcloudAI - Conversations with your Data",
    page_icon="🤖",
    layout="wide"
)

logo_url = "https://media.licdn.com/dms/image/C560BAQGeCieaiSruPg/company-logo_200_200/0/1630669521343/gapcloud_logo?e=2147483647&v=beta&t=jFkQ6l0vG434rsZTMywindOO_6FkdrH4FYhE0W6Xj0Q"
logo_html = f"""
<div style="position: absolute; top: 10px; right: 10px; z-index: 1000;">
    <img src="{logo_url}" alt="Logo" style="width: 100px; height: 100px;">
</div>
"""
st.markdown(logo_html, unsafe_allow_html=True)

st.markdown('<h1 class="title" style="color: Black; display: inline;">GapcloudAI</h1>'
            '<h3 style="color: Pink; display: inline;">Actions on your Data</h3>', 
            unsafe_allow_html=True)

st.markdown("      ")

st.markdown('<h2 class="title" style="color: Black; display: inline;">BP Call Transcription</h2>', unsafe_allow_html=True)
st.markdown("      ")
st.write("Upload an audio file to get the transcription")

uploaded_file = st.file_uploader("Choose an audio file", type=["m4a", "mp3", "wav", "flac"])

def sidebar():
    global TEMP, MODEL
    with st.sidebar:
        with st.expander("Settings", expanded=True):
            TEMP = st.slider(label='LLM Temperature', min_value=0.0, max_value=1.0, value=0.7)
            MODEL = st.selectbox(label='LLM Model', options=['gpt-4', 'gpt-3.5-turbo'])

sidebar()

def get_database_connection():
    server = 'in-sqlsrvr-stg.database.windows.net,1433'
    database = 'IN-SQLDB-AU-DevDataset-01012023-STG'
    username = 'admin123'
    password = 'Abhishek123@#'  # Replace with your actual password
    driver = '{ODBC Driver 18 for SQL Server}'
    connection_string = f"""
        Server={server};
        Database={database};
        User Id={username};
        Password={password};
        Encrypt=yes;
        TrustServerCertificate=yes;
        Connection Timeout=30;
    """
    try:
        conn = pyodbc.connect("Driver={ODBC Driver 18 for SQL Server};Server=tcp:in-sqlsrvr-stg.database.windows.net,1433;Database=IN-SQLDB-AU-DevDataset-01012023-STG;Uid=admin123;Pwd=Abhishek123@#;Encrypt=yes;TrustServerCertificate=yes;Connection Timeout=30;")
        return conn
    except Exception as e:
        print(f"Error connecting to SQL Server: {str(e)}")
        return None

conn = get_database_connection()



def random_color():
    return f'rgb({random.randint(100, 200)}, {random.randint(100, 200)}, {random.randint(100, 200)})'

if not deployment_id:
    st.error("The AZURE_DEPLOYMENT_ID environment variable is not set.")
else:
    if uploaded_file is not None:
        try:
            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Perform transcription using OpenAI or Whisper
            with open(uploaded_file.name, "rb") as audio_file:
                transcript = openai.audio.transcriptions.create(
                    model=deployment_id,
                    file=audio_file,
                    response_format="srt"
                )
            

            # Display audio file in the Streamlit app
            st.audio(uploaded_file, format='audio/mp3')


            FILE_URL = uploaded_file.name



            config = aai.TranscriptionConfig(speaker_labels=True).set_redact_pii(
                         policies=[
                                     aai.PIIRedactionPolicy.medical_condition,
                                     aai.PIIRedactionPolicy.email_address,
                                     aai.PIIRedactionPolicy.phone_number,
                                     aai.PIIRedactionPolicy.banking_information,
                                     aai.PIIRedactionPolicy.credit_card_number,
                                     aai.PIIRedactionPolicy.credit_card_cvv,
                                     aai.PIIRedactionPolicy.date_of_birth,
                                     aai.PIIRedactionPolicy.person_name,
                                  ]
                                                                            )

            transcriber = aai.Transcriber()
            transcript = transcriber.transcribe(
            FILE_URL,
            config=config
                                              )
            st.markdown(f'<div style="background-color: {random_color()}; padding: 10px; border-radius: 5px;"><h3>Transcript:</h3></div>', unsafe_allow_html=True)
            for utterance in transcript.utterances:
               st.write(f"Speaker {utterance.speaker}: {utterance.text}")

            summary = openai.chat.completions.create(
            model="gpt35",
            messages=[
                  {"role": "system", "content": transcript.text},
                  {"role": "user", "content": "Summarize the call in 50 words"}
                     ]
                                           )

            st.markdown(f'<div style="background-color: {random_color()}; padding: 10px; border-radius: 5px;"><h3>Summarized Transcript:</h3></div>', unsafe_allow_html=True)
            st.write(summary.choices[0].message.content)

            keywords = openai.chat.completions.create(
            model="gpt35",
            messages=[
                  {"role": "system", "content": transcript.text},
                  {"role": "user", "content": "Point Out 5 Keywords from the call separated by Comma."}
                     ]
                                           )

            st.markdown(f'<div style="background-color: {random_color()}; padding: 10px; border-radius: 5px;"><h3>Keywords:</h3></div>', unsafe_allow_html=True)
            st.write(keywords.choices[0].message.content)


            senti = openai.chat.completions.create(
            model="gpt35",
            messages=[
                  {"role": "system", "content": transcript.text},
                  {"role": "user", "content": "Give a one line long sentiment of the caller along with a happy,sad or neutral emoji.The sentiment sentence should be around 8-10 words"}
                     ]
                                           )

            st.markdown(f'<div style="background-color: {random_color()}; padding: 10px; border-radius: 5px;"><h3>Sentiment:</h3></div>', unsafe_allow_html=True)
            st.write(senti.choices[0].message.content)

            sentiscore = openai.chat.completions.create(
            model="gpt35",
            messages=[
                  {"role": "system", "content": transcript.text},
                  {"role": "user", "content": "Give a sentiment score from 0 to 100 where 0 is minimum happiness of the caller and 100 is the maximum.The output should just be a number without any text or special character"}
                     ]
                                           )


            st.markdown(f'<div style="background-color: {random_color()}; padding: 10px; border-radius: 5px;">'
            f'<h4 style="font-size: 20px;">Sentiment Score (0-100%)</h4>'
            f'<p style="font-size: 16px;">Sentiment Score = ((Positive Word Count) - (Negative Word Count)) Expressed as % of difference.</p>'
            f'</div>', unsafe_allow_html=True)
            st.write(sentiscore.choices[0].message.content)



            listentotalkratio = openai.chat.completions.create(
            model="gpt35",
            messages=[
                  {"role": "system", "content": transcript.text},
                  {"role": "user", "content":"Calculate the listen to talk ratio as a percentage.Don't show any calculation in the steps.The final answer should be a percentage without any text or any special charecter.if you don't know the answer or unable to perform calculations , give the output as 50.Do not include the percentage symbol.Any text self generated and containing the phrase- text-based AI, I don't have the ability to- should default to 50"}

                     ]
                                           )

            st.markdown(f'<div style="background-color: {random_color()}; padding: 10px; border-radius: 5px;">'
            f'<h4 style="font-size: 20px;">Listen to Talk Ratio (0-100%)</h4>'
            f'<p style="font-size: 16px;">Talk-Listen Ratio = (Rep\'s Talking Time / Prospect\'s Talking Time) * 100</p>'
            f'</div>', unsafe_allow_html=True)
            st.write(listentotalkratio.choices[0].message.content)


            engagementrate = openai.chat.completions.create(
            model="gpt35",
            messages=[
                  {"role": "system", "content": transcript.text},
                  {"role": "user", "content":"Calculate the engagement rate as a percentage which gives a rough estimate of the percentage of words the caller speakes in the entire conversation against the callee in the above generated transcription.The output should just be a number without any text or special character. If you don't know the answer or are unable to calculate it, provide output as 50.Do not show any calculation steps. Just give the number as final output."}

                     ]
                                           )

            st.markdown(f'<div style="background-color: {random_color()}; padding: 10px; border-radius: 5px;">'
            f'<h4 style="font-size: 20px;">Engagement Rate (0-100%)</h4>'
            f'<p style="font-size: 16px;">Engagement Rate = Total Customers / Number of Engagements * 100</p>'
            f'</div>', unsafe_allow_html=True)

            st.write(engagementrate.choices[0].message.content)

            positivenegativeratio = openai.chat.completions.create(
            model="gpt35",
            messages=[
                  {"role": "system", "content": transcript.text},
                  {"role": "user", "content":"Calculate the percentage of positive phrases against negative phrases in the above generated summary.The output should just be a number without any text or special character. If you don't know the answer or are unable to calculate it, provide output as 50.Do not show any calculation steps. Just give the number as final output. "}

                     ]
                                           )

            st.markdown(f'<div style="background-color: {random_color()}; padding: 10px; border-radius: 5px;">'
            f'<h4 style="font-size: 20px;">Positive Interaction Rate (0-100%)</h4>'
            f'<p style="font-size: 16px;">Positive-Negative Ratio = (Number of Negative Interactions / Number of Positive Interactions) * 100</p>'
            f'</div>', unsafe_allow_html=True)

            st.write(positivenegativeratio.choices[0].message.content)

           

            problem = openai.chat.completions.create(
            model="gpt35",
            messages=[
                  {"role": "system", "content": transcript.text},
                  {"role": "user", "content": "Give the problem statement of the caller"}
                     ]
                                           )

            st.markdown(f'<div style="background-color: {random_color()}; padding: 10px; border-radius: 5px;"><h3>Problem Statement:</h3></div>', unsafe_allow_html=True)
            st.write(problem.choices[0].message.content)


            intent = openai.chat.completions.create(
            model="gpt35",
            messages=[
                  {"role": "system", "content": transcript.text},
                  {"role": "user", "content": "Give the Intent of the caller for calling"}
                     ]
                                           )

            st.markdown(f'<div style="background-color: {random_color()}; padding: 10px; border-radius: 5px;"><h3>Caller Intent:</h3></div>', unsafe_allow_html=True)
            st.write(intent.choices[0].message.content)


            Emapthy = openai.chat.completions.create(
            model="gpt35",
            messages=[
                  {"role": "system", "content": transcript.text},
                  {"role": "user", "content": "Give the Emapthy involved between the caller and callee. Limit it to one sentence only of 8-10 words."}
                     ]
                                           )

            st.markdown(f'<div style="background-color: {random_color()}; padding: 10px; border-radius: 5px;"><h3>Empathy:</h3></div>', unsafe_allow_html=True)
            st.write(Emapthy.choices[0].message.content)

            empathyscore = openai.chat.completions.create(
            model="gpt35",
            messages=[
                  {"role": "system", "content": transcript.text},
                  {"role": "user", "content": """
{
Based on the Empathy generated between the caller and callee, generate an Emapthy Score between 0 to 100.If you are unsure generate 40.Print only the number without any text or special characters."""}

                     ]
                                           )

            st.markdown(f'<div style="background-color: {random_color()}; padding: 10px; border-radius: 5px;">'
            f'<h4 style="font-size: 20px;">Empathy Score (0-100%)</h4>'
            f'<p style="font-size: 16px;">Identify specific behaviors or attributes that demonstrate empathy in customer interactions. This may include active listening, acknowledging emotions, showing understanding, offering personalized solutions, etc.</p>'
            f'</div>', unsafe_allow_html=True)

            st.write(empathyscore.choices[0].message.content)


            category = openai.chat.completions.create(
            model="gpt35",
            messages=[
                  {"role": "system", "content": transcript.text},
                  {"role": "user", "content": "Categorize the call giving it a tag"}
                     ]
                                           )

            st.markdown(f'<div style="background-color: {random_color()}; padding: 10px; border-radius: 5px;"><h3>Category:</h3></div>', unsafe_allow_html=True)
            st.write(category.choices[0].message.content)
            uploaded_file_name = uploaded_file.name[:255] if uploaded_file.name else ''
            transcript_text = transcript.text[:4000] if transcript.text else ''
            senti_content = senti.choices[0].message.content[:255] if senti.choices else ''
            keywords_content = keywords.choices[0].message.content[:255] if keywords.choices else ''
            intent_content = intent.choices[0].message.content[:255] if intent.choices else ''
            problem_content = problem.choices[0].message.content[:255] if problem.choices else ''
            empathy_content = Emapthy.choices[0].message.content[:255] if Emapthy.choices else ''
            category_content = category.choices[0].message.content[:255] if category.choices else ''

            cursor = conn.cursor()
            cursor.execute('''
                          INSERT INTO TranscriptionResults 
                                    (AudioFile, Transcription, Sentiment, KeyPhrases, Intent, ProblemStatement, Empathy, CallCategory,
                                         SentimentScore, ListenToTalkRatio, EngagementRatio, PositiveInteractionRatio, EmpathyScore)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                          ''', (
            uploaded_file_name,
            transcript_text,
            senti_content,
            keywords_content,
            intent_content,
            problem_content,
            empathy_content,
            category_content,
            sentiscore.choices[0].message.content if sentiscore.choices else 0,  # SentimentScore
            listentotalkratio.choices[0].message.content if listentotalkratio.choices else 0,  # ListenToTalkRatio
            engagementrate.choices[0].message.content if engagementrate.choices else 0,  # EngagementRatio
            positivenegativeratio.choices[0].message.content if positivenegativeratio.choices else 0,  # PositiveInteractionRatio
            empathyscore.choices[0].message.content if empathyscore.choices else 0  # EmpathyScore
            ))
            conn.commit()
            cursor.close()


        except Exception as e:
            st.error(f"An error occurred: {e}")
            if conn:
                conn.rollback()  # Rollback changes if an error occurs
            raise  # Raise the error to see details in Streamlit or logs

        finally:
            if conn:
                conn.close()  # Close the database connection
