import re
import speech_recognition as sr
import streamlit as st

st.set_page_config(
    page_title="Calculator",
    layout="centered",
    menu_items={
        "About": "Note: Mic input can only be used for numbers, not operators (+, -, etc.)."
    },
)

def add(a, b):
    return a + b

def sub(a, b):
    return a - b

def mul(a, b):
    return a * b

def div(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b

def power(a, b):
    return a ** b

def sqrt(a):
    if a < 0:
        raise ValueError("Cannot take square root of a negative number")
    return a ** 0.5



if "num1" not in st.session_state:
    st.session_state.num1 = ""
if "num2" not in st.session_state:
    st.session_state.num2 = ""
if "operation" not in st.session_state:
    st.session_state.operation = None
if "typing_second" not in st.session_state:
    st.session_state.typing_second = False
if "display" not in st.session_state:
    st.session_state.display = "0"


def press_number(digit):
    if not st.session_state.typing_second:
        st.session_state.num1 += digit
        st.session_state.display = st.session_state.num1
    else:
        st.session_state.num2 += digit
        st.session_state.display = st.session_state.num2


def press_operator(op):
    if st.session_state.num1 == "":
        return
    st.session_state.operation = op
    st.session_state.typing_second = True


def press_clear():
    st.session_state.num1 = ""
    st.session_state.num2 = ""
    st.session_state.operation = None
    st.session_state.typing_second = False
    st.session_state.display = "0"


def press_sqrt():
    target = st.session_state.num2 if st.session_state.typing_second else st.session_state.num1
    if target == "":
        return
    try:
        result = sqrt(float(target))
        result = format_result(result)
        if st.session_state.typing_second:
            st.session_state.num2 = str(result)
        else:
            st.session_state.num1 = str(result)
        st.session_state.display = str(result)
    except ValueError as e:
        st.session_state.display = str(e)


def press_equals():
    s = st.session_state
    if s.num1 == "" or s.num2 == "" or s.operation is None:
        return
    try:
        n1, n2 = float(s.num1), float(s.num2)
        if s.operation == "add":
            result = add(n1, n2)
        elif s.operation == "sub":
            result = sub(n1, n2)
        elif s.operation == "mul":
            result = mul(n1, n2)
        elif s.operation == "div":
            result = div(n1, n2)
        elif s.operation == "pow":
            result = power(n1, n2)

        result = format_result(result)
        s.display = str(result)
        s.num1 = str(result)
        s.num2 = ""
        s.operation = None
        s.typing_second = False
    except ZeroDivisionError as e:
        s.display = str(e)


def format_result(result):
    if isinstance(result, float) and result.is_integer():
        return int(result)
    return round(result, 8)


def process_voice_input(audio_value):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_value) as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        st.warning("Couldn't understand that. Try speaking the digits clearly.")
        return
    except sr.RequestError:
        st.warning("Speech recognition service unavailable. Check your internet connection.")
        return

    digits_only = re.sub(r"[^0-9.]", "", text)
    if digits_only == "":
        st.warning(f"Heard \"{text}\" — no numbers found in that.")
        return

    for char in digits_only:
        press_number(char)
    st.rerun()


# ---- UI ----
st.title("Calculator")
st.text_input("Display", value=st.session_state.display, disabled=True, label_visibility="collapsed")

audio_value = st.audio_input("Speak a number (digits only)")
if audio_value is not None:
    process_voice_input(audio_value)

rows = [
    [("C", "clear"), ("\u221A", "sqrt"), ("^", "pow"), ("/", "div")],
    [("7", "num"), ("8", "num"), ("9", "num"), ("*", "mul")],
    [("4", "num"), ("5", "num"), ("6", "num"), ("-", "sub")],
    [("1", "num"), ("2", "num"), ("3", "num"), ("+", "add")],
    [("0", "num"), (".", "num"), ("=", "equals")],
]

for row in rows:
    cols = st.columns(len(row))
    for col, (label, kind) in zip(cols, row):
        if col.button(label, key=f"btn_{label}_{kind}", use_container_width=True):
            if kind == "num":
                press_number(label)
            elif kind == "clear":
                press_clear()
            elif kind == "sqrt":
                press_sqrt()
            elif kind == "equals":
                press_equals()
            else:
                press_operator(kind)
            st.rerun()