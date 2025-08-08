import streamlit as st
from langchain import PromptTemplate
from langchain_openai import OpenAI


template = """
    Below is a draft text that may be poorly worded.
    Your goal is to:
    - Properly redact the draft text
    - Convert the draft text to a specified tone
    - Convert the draft text to a specified dialect

    Here are some examples different Tones:
    - Formal: Greetings! OpenAI has announced that Sam Altman is rejoining the company as its Chief Executive Officer. After a period of five days of conversations, discussions, and deliberations, the decision to bring back Altman, who had been previously dismissed, has been made. We are delighted to welcome Sam back to OpenAI.
    - Informal: Hey everyone, it's been a wild week! We've got some exciting news to share - Sam Altman is back at OpenAI, taking up the role of chief executive. After a bunch of intense talks, debates, and convincing, Altman is making his triumphant return to the AI startup he co-founded.  

    Here are some examples of words in different dialects:
    - American: French Fries, cotton candy, apartment, garbage, \
        cookie, green thumb, parking lot, pants, windshield
    - British: chips, candyfloss, flag, rubbish, biscuit, green fingers, \
        car park, trousers, windscreen

    Example Sentences from each dialect:
    - American: Greetings! OpenAI has announced that Sam Altman is rejoining the company as its Chief Executive Officer. After a period of five days of conversations, discussions, and deliberations, the decision to bring back Altman, who had been previously dismissed, has been made. We are delighted to welcome Sam back to OpenAI.
    - British: On Wednesday, OpenAI, the esteemed artificial intelligence start-up, announced that Sam Altman would be returning as its Chief Executive Officer. This decisive move follows five days of deliberation, discourse and persuasion, after Altman's abrupt departure from the company which he had co-established.

    Please start the redaction with a warm introduction. Add the introduction \
        if you need to.
    
    Below is the draft text, tone, and dialect:
    DRAFT: {draft}
    TONE: {tone}
    DIALECT: {dialect}

    YOUR {dialect} RESPONSE:
"""

#PromptTemplate variables definition
prompt = PromptTemplate(
    input_variables=["tone", "dialect", "draft"],
    template=template,
)


#LLM and key loading function
def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm


#Page title and header
st.set_page_config(page_title="Re-write your text")
st.header("Re-Write Your Text")


#Intro: instructions
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Re-write your text in different styles**")

with col2:
    st.write("Contact [*William Sun*](omniai.labs4ever@gmail.com) for any issues")


#Input OpenAI API Key
st.markdown("## Enter Your OpenAI API Key")

# "key" makes this widget tied to st.session_state["openai_api_key_input"].

def get_openai_api_key():
    input_text = st.text_input(label="Your OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input", type="password")
    return input_text

openai_api_key = get_openai_api_key()



# Input
st.markdown("## Enter the text you want to re-write")

def get_draft():
    draft_text = st.text_area(label="Text", label_visibility='collapsed', placeholder="Your Text...", key="draft_input")
    return draft_text

draft_input = get_draft()

if len(draft_input.split(" ")) > 700:
    st.write("Please enter a shorter text. The maximum length is 700 words.")
    st.stop()

# Prompt template tunning options
col1, col2 = st.columns(2)
with col1:
    option_tone = st.selectbox(
        'Which tone would you like your redaction to have?',
        ('Formal', 'Informal'))
    
with col2:
    option_dialect = st.selectbox(
        'Which English Dialect would you like?',
        ('American', 'British'))
    
    
# Output
st.markdown("### Your Re-written text:")

if draft_input:
    if not openai_api_key:
        st.warning('Please insert OpenAI API Key. \
            Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', 
            icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_draft = prompt.format(
        tone=option_tone, 
        dialect=option_dialect, 
        draft=draft_input
    )

    improved_redaction = llm(prompt_with_draft)

    st.write(improved_redaction)

note1 = '''
Example where key matters:
st.text_input("Name")
st.text_input("Name")  # ❌ Will crash — same label, no unique key

# Correct:
st.text_input("Name", key="name1")
st.text_input("Name", key="name2")

Example using session state:
input_text = st.text_input("OpenAI API Key", key="api_key")

# Access it later:
if st.button("Print Key"):
    st.write(st.session_state["api_key"])

Values inside st.session_state persist across user actions.
1, Track user input values

st.text_input("Enter name", key="username")

# Access the value
st.write("You typed:", st.session_state["username"])

2, Manually store variables

st.session_state["count"] = st.session_state.get("count", 0)

if st.button("Add 1"):
    st.session_state["count"] += 1

st.write("Counter:", st.session_state["count"])

3,  Initialize only once- Use if "key" not in st.session_state to initialize state variables:

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

4, Control widgets programmatically

st.session_state["username"] = "William"
st.text_input("Enter name", key="username")  # Shows "William" prefilled

Remember:
You must use a key to connect a widget with st.session_state.
Avoid using the same key across multiple widgets unless you're intentionally reusing values.
Session state is not permanent; it's wiped when the session ends (e.g., page reload).
| Feature                       | Description                                            |
| ----------------------------- | ------------------------------------------------------ |
| `st.session_state["var"]`     | Access a stored value                                  |
| `st.session_state.get("var")` | Safer way to access, returns `None` if not found       |
| `st.session_state["var"] = x` | Store a value manually                                 |
| `key="var"` in widget         | Automatically binds widget value to `st.session_state` |
| Widget → `st.session_state`   | Happens automatically when `key` is used               |

'''
