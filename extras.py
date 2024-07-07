from azure.core.credentials import AzureKeyCredential  
from azure.ai.textanalytics import TextAnalyticsClient
from sumy.parsers.plaintext import PlaintextParser  
from sumy.nlp.tokenizers import Tokenizer  
from sumy.summarizers.lsa import LsaSummarizer  
  
  
key = "c9f513aaa4284d618231df57b555117d"  
endpoint = "https://prodstats.cognitiveservices.azure.com/"  
  
def analyze_sentiment(text):  
    credential = AzureKeyCredential(key)  
    client = TextAnalyticsClient(endpoint=endpoint, credential=credential)  
      
    response = client.analyze_sentiment(documents=[{"id": "1", "text": text}])  
    sentiment = response[0].sentiment  
    return sentiment   
  

  
def analyze_key_phrases(text):  
    credential = AzureKeyCredential(key)  
    client = TextAnalyticsClient(endpoint=endpoint, credential=credential)  
      
    response = client.extract_key_phrases(documents=[{"id": "1", "text": text}])  
    key_phrases = response[0].key_phrases  
    return key_phrases  


def infer_intent(text):  
  
  
    if "buy" in text or "purchase" in text:  
        return "purchase of products"  
      
 
    if "cancel" in text or "return" in text:  
        return "cancellation of products"  
      
 
    return "unknown" 

def extract_problem_statement(key_phrases):  
 
      
  
    for phrase in key_phrases:  
        if "problem" in phrase or "issue" in phrase:  
            return phrase  
      
  
    return "No problem statement identified"  
  
  
transcription = "I'm having trouble with my laptop. It keeps freezing and crashing."  
key_phrases = analyze_key_phrases(transcription)  
problem_statement = extract_problem_statement(key_phrases)  



def calculate_empathy(sentiment):  
   
    if sentiment == "mixed":  
        return "Medium Empathy"  
    else:  
        return "Low Empathy"  


def categorization(key_phrases):  
    category1_keywords = ["sms", "email", "call"]  
    category2_keywords = ["cancel", "upgrade", "switch"]  
      
    for phrase in key_phrases:  
        if any(keyword in phrase for keyword in category1_keywords):  
            return "Category 1: SMS/Email/Call"  
        elif any(keyword in phrase for keyword in category2_keywords):  
            return "Category 2: Sales/Churn"  
      
    return "Not Available" 

 
  
