import streamlit as st

from main import generate_love_quotes


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Love Quote Generator",
    page_icon="💖",
    layout="centered"
)


# =========================================================
# SESSION STATE
# =========================================================

if "generated" not in st.session_state:
    st.session_state.generated = False

if "result" not in st.session_state:
    st.session_state.result = None


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* Main Background */
    .stApp {
        background: linear-gradient(
            135deg,
            #ff758c,
            #ff7eb3,
            #ffb199
        );
        overflow:hidden;
    }

    /* Hide Streamlit Menu/Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Title */
    .main-title {
        text-align:center;
        font-size:65px;
        font-weight:bold;
        color:white;
        margin-top:20px;
        text-shadow: 0px 0px 20px rgba(255,255,255,0.8);
    }

    /* Subtitle */
    .sub-title {
        text-align:center;
        font-size:24px;
        color:white;
        margin-bottom:40px;
    }

    /* Quote Card */
    .quote-card {
        background: rgba(255,255,255,0.18);
        backdrop-filter: blur(18px);

        border-radius:30px;

        padding:40px;

        margin-top:40px;

        box-shadow: 0px 8px 32px rgba(0,0,0,0.25);

        animation: fadeIn 1.2s ease-in-out;

        color:black;

        font-size:34px;

        font-weight:700;

        line-height:1.8;

        text-align:center;

        font-family: cursive;

        text-shadow:0px 0px 12px rgba(255,255,255,0.5);
    }

    /* Floating Hearts */
    .heart {
        position: fixed;
        color: rgba(255,255,255,0.8);
        animation: floatUp 6s linear infinite;
        font-size:30px;
    }

    @keyframes floatUp {
        0% {
            transform: translateY(100vh);
            opacity:0;
        }

        10% {
            opacity:1;
        }

        100% {
            transform: translateY(-120vh);
            opacity:0;
        }
    }

    @keyframes fadeIn {

        from {
            opacity:0;
            transform: translateY(40px);
        }

        to {
            opacity:1;
            transform: translateY(0px);
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# FLOATING HEARTS
# =========================================================

hearts_html = ""

positions = [5, 15, 25, 35, 45, 55, 65, 75, 85, 95]

delays = [0, 1, 2, 3, 4, 5, 1.5, 2.5, 3.5, 4.5]

for i in range(10):

    hearts_html += f"""
    <div class="heart"
         style="
         left:{positions[i]}%;
         animation-delay:{delays[i]}s;">
         ❤️
    </div>
    """

st.markdown(hearts_html, unsafe_allow_html=True)


# =========================================================
# SHOW FORM ONLY BEFORE GENERATION
# =========================================================

if not st.session_state.generated:

    st.markdown(
        """
        <div class="main-title">
            💖 AI Love Quote Generator 💖
        </div>

        <div class="sub-title">
            Create magical romantic quotes using AI ✨
        </div>
        """,
        unsafe_allow_html=True
    )

    lover_name = st.text_input(
        "💘 Enter Lover Name"
    )

    flower_name = st.text_input(
        "🌹 Enter Flower Name"
    )

    food_name = st.text_input(
        "🍫 Enter Favorite Food"
    )

    if st.button("✨ Generate Love Quotes ✨"):

        if lover_name and flower_name and food_name:

            result = generate_love_quotes(

                lover_name=lover_name,

                flower_name=flower_name,

                food_name=food_name
            )

            st.session_state.generated = True

            st.session_state.result = result

            st.rerun()


# =========================================================
# SHOW ONLY QUOTES AFTER GENERATION
# =========================================================

else:

    result = st.session_state.result

    st.markdown(
        """
        <div class="main-title">
            💖 Your Love Quotes 💖
        </div>
        """,
        unsafe_allow_html=True
    )

    # Quote 1
    st.markdown(
        f"""
        <div class="quote-card">
                💌 {result["quote_1"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Quote 2
    st.markdown(
        f"""
        <div class="quote-card">
                ❤️ {result["quote_2"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Generate Again Button
    if st.button("💞 Generate Again"):

        st.session_state.generated = False

        st.rerun()