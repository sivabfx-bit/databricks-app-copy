import html

import streamlit as st

DOMAIN_PAGES = [
    ("Portfolio", "app.py", "🏠"),
    ("Markets", "pages/02_Market_Analytics.py", "🌎"),
    ("Properties", "pages/03_Property_Analytics.py", "🏢"),
    ("Maintenance", "pages/04_Maintenance.py", "🔧"),
]

THEME_CSS = """
<style>
.stApp {
    background: #f5f7fa;
    color: #334155;
    font-family: Inter, "Segoe UI", Roboto, Arial, sans-serif;
}

.main .block-container {
    max-width: 1440px;
    padding: 1.5rem 2rem 3rem 2rem;
}

section[data-testid="stSidebar"] { display: none; }
header[data-testid="stHeader"] { background: transparent; }

.stApp h1, .stApp h2, .stApp h3, .stApp h4 {
    color: #172b4d;
    letter-spacing: -0.01em;
    line-height: 1.2;
}

.stApp p, .stApp li, .stApp label {
    color: #334155;
    line-height: 1.5;
}

div[data-testid="stCaptionContainer"] p {
    color: #5b6678 !important;
}

/* Brand block */
.pi-brand { display: flex; align-items: center; gap: 12px; }
.pi-brand-mark {
    width: 40px; height: 40px; border-radius: 10px;
    background: #087f67; color: #ffffff;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; font-weight: 700;
}
.pi-brand-title { font-size: 22px; font-weight: 750; color: #172b4d; letter-spacing: -0.02em; line-height: 1.2; }
.pi-brand-sub { font-size: 12px; color: #5b6678; line-height: 1.4; }

/* Top-right actions */
.pi-nav-muted {
    color: #5b6678; font-size: 14px; font-weight: 600;
    text-align: center; padding: 8px 4px;
}
.pi-avatar {
    width: 36px; height: 36px; border-radius: 50%;
    background: #e2e8f0; color: #172b4d;
    display: flex; align-items: center; justify-content: center;
    font-size: 13px; font-weight: 700; margin: 0 auto;
}

/* Domain navigation */
.pi-section-label {
    color: #3f6b5f; font-size: 11px; font-weight: 750;
    letter-spacing: 1px; text-transform: uppercase;
    margin: 16px 0 8px 0;
}
div[class*="st-key-nav-"] a {
    display: flex; justify-content: center; align-items: center; gap: 6px;
    min-height: 40px; border-radius: 10px;
    border: 1px solid #dfe5ee; background: #ffffff;
    text-decoration: none; box-shadow: 0 1px 2px rgba(25, 40, 65, 0.04);
    transition: border-color 0.15s ease, background 0.15s ease;
}
div[class*="st-key-nav-"] a:hover { border-color: #087f67; }
div[class*="st-key-nav-"] a,
div[class*="st-key-nav-"] a p,
div[class*="st-key-nav-"] a span {
    color: #34445c !important; font-weight: 600; font-size: 14px;
}
div[class*="st-key-nav-active-"] a {
    background: #e8f4f0; border-color: #9fd3c3;
}
div[class*="st-key-nav-active-"] a,
div[class*="st-key-nav-active-"] a p,
div[class*="st-key-nav-active-"] a span {
    color: #066b56 !important;
}

/* Page header */
.pi-eyebrow {
    color: #3f6b5f; font-size: 11px; font-weight: 750;
    letter-spacing: 1px; text-transform: uppercase; margin-bottom: 4px;
}
.pi-page-header h1 {
    font-size: 30px; font-weight: 750; margin: 0 0 4px 0;
}
.pi-page-header p {
    color: #5b6678; font-size: 15px; margin: 0 0 24px 0;
}

.pi-section-header h3 {
    font-size: 18px; font-weight: 700; margin: 24px 0 2px 0;
}
.pi-section-header p {
    color: #5b6678; font-size: 13px; margin: 0 0 12px 0;
}

/* Metric cards */
div[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e3e8ef;
    border-radius: 14px;
    padding: 18px 20px;
    box-shadow: 0 2px 8px rgba(25, 40, 65, 0.04);
}
div[data-testid="stMetricLabel"], div[data-testid="stMetricLabel"] p {
    color: #5b6678 !important; font-size: 13px; font-weight: 600;
}
div[data-testid="stMetricValue"] {
    color: #172b4d; font-weight: 750;
}

/* Containers, charts and tables */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #ffffff;
    border-color: #e3e8ef;
    border-radius: 14px;
}
div[data-testid="stVegaLiteChart"],
div[data-testid="stArrowVegaLiteChart"],
div[data-testid="stDataFrame"] {
    background: #ffffff;
    border: 1px solid #e3e8ef;
    border-radius: 12px;
}
div[data-testid="stVegaLiteChart"],
div[data-testid="stArrowVegaLiteChart"] { padding: 12px; }
div[data-testid="stDataFrame"] { overflow: hidden; }

/* Buttons and inputs */
.stButton > button {
    border-radius: 10px; font-weight: 600;
    border: 1px solid #dce2ea; color: #34445c;
}
.stButton > button[kind="primary"] {
    background: #087f67; border-color: #087f67; color: #ffffff;
}
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    border-radius: 10px; border-color: #dce2ea; background: #ffffff;
}

/* Alerts */

import streamlit as st


def apply_theme():
    st.markdown("""
    <style>
    /* Main application */
    .stApp {
        background: #f7f8fa;
        color: #20242c;
        font-family: Inter, Arial, sans-serif;
    }

    .main .block-container {
        max-width: 1440px;
        padding-top: 1.2rem;
        padding-bottom: 3rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    /* Hide default sidebar */
    section[data-testid="stSidebar"] {
        display: none;
    }

    /* Top navigation */
    .brand-title {
        font-size: 23px;
        font-weight: 750;
        color: #172b4d;
        letter-spacing: -0.7px;
    }

    .brand-subtitle {
        font-size: 12px;
        color: #788397;
        margin-top: -5px;
    }

    .section-label {
        color: #52756d;
        font-size: 11px;
        font-weight: 750;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-top: 20px;
        margin-bottom: 8px;
    }

    .page-heading {
        font-size: 30px;
        font-weight: 750;
        color: #172b4d;
        letter-spacing: -1px;
        margin-top: 12px;
        margin-bottom: 3px;
    }

    .page-description {
        color: #697586;
        font-size: 14px;
        margin-bottom: 20px;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e7eaf0;
        border-radius: 13px;
        padding: 18px 20px;
        box-shadow: 0 2px 8px rgba(25, 40, 65, 0.035);
    }

    div[data-testid="stMetricLabel"] {
        color: #68758a;
        font-size: 13px;
    }

    div[data-testid="stMetricValue"] {
        color: #172b4d;
        font-weight: 750;
    }

    /* Containers and cards */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #ffffff;
        border-color: #e7eaf0;
        border-radius: 13px;
    }

    /* Buttons */
    .stButton > button,
    div[data-testid="stPageLink"] a {
        border-radius: 9px;
        font-weight: 600;
        border: 1px solid #e1e6ed;
    }

    .stButton > button[kind="primary"] {
        background: #087f67;
        border-color: #087f67;
        color: white;
    }

    /* Inputs */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        border-radius: 8px;
        border-color: #dce2ea;
        background: white;
    }

    /* Dataframes */
    div[data-testid="stDataFrame"] {
        border: 1px solid #e7eaf0;
        border-radius: 10px;
        overflow: hidden;
    }

    /* Charts */
    div[data-testid="stVegaLiteChart"],
    div[data-testid="stArrowVegaLiteChart"] {
        background: white;
        border: 1px solid #e7eaf0;
        border-radius: 12px;
        padding: 12px;
    }

    hr {
        border-color: #e8ebf0;
    }

    /* Remove excessive top padding */
    header[data-testid="stHeader"] {
        background: transparent;
    }

    
/* ===== TEXT CONTRAST FIX ===== */

.stApp,
.stApp p,
.stApp label,
.stApp span,
.stApp li {
    color: #263449;
}

/* Headings */
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4 {
    color: #172b4d !important;
}

/* Markdown text */
div[data-testid="stMarkdownContainer"] p {
    color: #526176 !important;
}

/* Navigation links */
div[data-testid="stPageLink"] a {
    color: #34445c !important;
    background: #ffffff;
}

div[data-testid="stPageLink"] a p {
    color: #34445c !important;
}

/* Selected navigation */
div[data-testid="stPageLink"] a[aria-current="page"] {
    background: #e8f2ef !important;
    border-color: #b8d9ce !important;
    color: #087f67 !important;
}

/* KPI labels */
div[data-testid="stMetricLabel"],
div[data-testid="stMetricLabel"] p {
    color: #64748b !important;
}

/* Success and information messages */
div[data-testid="stAlert"] p,
div[data-testid="stAlert"] span {
    color: #245b45 !important;
}

hr { border-color: #e3e8ef; }

@media (max-width: 768px) {
    .main .block-container { padding: 1rem 1rem 2rem 1rem; }
    .pi-page-header h1 { font-size: 24px; }
}
</style>
"""


def apply_theme():
    st.markdown(THEME_CSS, unsafe_allow_html=True)


def render_header(active_page="Portfolio"):
    brand_col, actions_col = st.columns([3, 2], vertical_alignment="center")

    with brand_col:
        st.markdown(
            """
            <div class="pi-brand">
                <div class="pi-brand-mark">◈</div>
                <div>
                    <div class="pi-brand-title">Property Intelligence</div>
                    <div class="pi-brand-sub">AI Studio · Enterprise Data Intelligence Platform</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with actions_col:
        today_col, products_col, agents_col, avatar_col = st.columns(
            [1.2, 1.4, 1, 0.5], vertical_alignment="center"
        )

        with today_col:
            st.page_link("app.py", label="Today", icon="🏠")

        with products_col:
            st.markdown('<div class="pi-nav-muted">Data products</div>', unsafe_allow_html=True)

        with agents_col:
            st.markdown('<div class="pi-nav-muted">Agents</div>', unsafe_allow_html=True)

        with avatar_col:
            st.markdown('<div class="pi-avatar">PI</div>', unsafe_allow_html=True)

    st.divider()

    st.markdown('<div class="pi-section-label">Data domain</div>', unsafe_allow_html=True)

    columns = st.columns(len(DOMAIN_PAGES))

    for column, (label, path, icon) in zip(columns, DOMAIN_PAGES):
        state = "active" if label == active_page else "idle"
        with column:
            with st.container(key=f"nav-{state}-{label.lower()}"):
                st.page_link(path, label=label, icon=icon)


def page_header(title, description, eyebrow=None):
    eyebrow_html = (
        f'<div class="pi-eyebrow">{html.escape(eyebrow)}</div>' if eyebrow else ""
    )
    st.markdown(
        f"""
        <div class="pi-page-header">
            {eyebrow_html}
            <h1>{html.escape(title)}</h1>
            <p>{html.escape(description)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title, caption=None):
    caption_html = f"<p>{html.escape(caption)}</p>" if caption else ""
    st.markdown(
        f'<div class="pi-section-header"><h3>{html.escape(title)}</h3>{caption_html}</div>',
        unsafe_allow_html=True,
    )
/* Buttons */
.stButton button {
    color: #34445c !important;
}

/* Captions */
div[data-testid="stCaptionContainer"] p {
    color: #788397 !important;
}

    </style>
    """, unsafe_allow_html=True)


def render_header(active_page="Portfolio"):

    # Brand and primary navigation
    left, right = st.columns([2.2, 3])

    with left:
        st.markdown(
            """
            <div class="brand-title">◈ Property Intelligence</div>
            <div class="brand-subtitle">
                AI Studio · Enterprise Data Intelligence Platform
            </div>
            """,
            unsafe_allow_html=True
        )

    with right:
        nav1, nav2, nav3 = st.columns(3)

        with nav1:
            st.page_link(
                "app.py",
                label="Today",
                icon="🏠"
            )

        with nav2:
            st.markdown(
                "<div style='padding:8px;color:#64748b;"
                "font-size:14px;text-align:center'>Data products</div>",
                unsafe_allow_html=True
            )

        with nav3:
            st.markdown(
                "<div style='padding:8px;color:#64748b;"
                "font-size:14px;text-align:center'>Agents</div>",
                unsafe_allow_html=True
            )

    st.divider()

    # Domain navigation
    st.markdown(
        '<div class="section-label">DATA DOMAIN</div>',
        unsafe_allow_html=True
    )

    pages = [
        ("Portfolio", "app.py", "🏠"),
        ("Markets", "pages/02_Market_Analytics.py", "🌎"),
        ("Properties", "pages/03_Property_Analytics.py", "🏢"),
        ("Maintenance", "pages/04_Maintenance.py", "🔧"),
    ]

    columns = st.columns(len(pages))

    for column, (label, path, icon) in zip(columns, pages):
        with column:
            st.page_link(
                path,
                label=label,
                icon=icon
            )

    st.divider()
