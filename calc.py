import streamlit as st

st.set_page_config(
    page_title="Calculator",
    layout="centered",
)

# ---- Responsive CSS: smaller keys on mobile, unchanged on laptop/desktop ----
st.markdown(
    """
    <style>
    /* Force column rows to stay horizontal on mobile instead of Streamlit's
       default behavior of stacking columns vertically on narrow screens */
    @media (max-width: 640px) {
        div[data-testid="stHorizontalBlock"] {
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            gap: 0.3rem !important;
        }
        div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
            width: auto !important;
            flex: 1 1 0 !important;
            min-width: 0 !important;
        }
    }

    /* Mobile: screens narrower than 480px get compact buttons */
    @media (max-width: 480px) {
        div[data-testid="stButton"] button {
            padding: 0.25rem 0.4rem !important;
            font-size: 0.85rem !important;
            min-height: 2.2rem !important;
            height: 2.2rem !important;
        }
        /* Number keys (0-9, .) are extra small on mobile */
        div[class*="st-key-num_"] div[data-testid="stButton"] button {
            padding: 0.15rem 0.25rem !important;
            font-size: 0.75rem !important;
            min-height: 1.8rem !important;
            height: 1.8rem !important;
        }
        div[data-testid="stTextInput"] input {
            font-size: 1.1rem !important;
            padding: 0.3rem !important;
        }
    }

    /* Desktop / laptop (>= 481px): keep default Streamlit sizing */
    @media (min-width: 481px) {
        div[data-testid="stButton"] button {
            font-size: 1rem;
            padding: 0.5rem 1rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
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
if "history" not in st.session_state:
    st.session_state.history = []
if "show_history" not in st.session_state:
    st.session_state.show_history = False

OP_SYMBOLS = {"add": "+", "sub": "-", "mul": "*", "div": "/", "pow": "^"}


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
        st.session_state.history.append(f"\u221A({format_operand(float(target))}) = {result}")
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
        symbol = OP_SYMBOLS.get(s.operation, s.operation)
        s.history.append(f"{format_operand(n1)} {symbol} {format_operand(n2)} = {result}")
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


def format_operand(n):
    return int(n) if float(n).is_integer() else n


def press_clear_history():
    st.session_state.history = []


# ---- UI ----
st.title("Calculator")

if st.button("📜 History", key="btn_toggle_history", use_container_width=True):
    st.session_state.show_history = not st.session_state.show_history
    st.rerun()

if st.session_state.show_history:
    with st.container(border=True):
        if st.button("Clear History", key="btn_clear_history", use_container_width=True):
            press_clear_history()
            st.rerun()

        if st.session_state.history:
            for item in reversed(st.session_state.history):
                st.text(item)
        else:
            st.caption("No calculations yet.")

st.text_input("Display", value=st.session_state.display, disabled=True, label_visibility="collapsed")

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
        # Number buttons get wrapped in a keyed container so mobile CSS
        # can target them separately from operator/function buttons.
        if kind == "num":
            target = col.container(key=f"num_{label}")
        else:
            target = col

        if target.button(label, key=f"btn_{label}_{kind}", use_container_width=True):
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