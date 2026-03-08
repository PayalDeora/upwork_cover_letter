import streamlit as st
import streamlit.components.v1 as components
import random
import re
import html

st.set_page_config(
    page_title="Upwork Cover Letter Generator",
    page_icon="⚡",
    layout="centered"
)

st.markdown(
    """
    <style>
    .stButton button:disabled {
        opacity: 0.55 !important;
        cursor: not-allowed !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

DEFAULTS = {
    "client_name": "",
    "service": "",
    "job_post": "",
    "portfolio": "",
    "drive_url": "",
    "tone": "Confident & Direct",
    "length": "Medium (~180 words)",
    "include_results": False,
    "generated_letter": "",
    "first_draft_done": False,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

OPENINGS = [
    "I'm genuinely excited to put myself forward for this role.",
    "Your project caught my attention straight away, it's exactly the kind of work I love doing.",
    "This opportunity is a strong match for what I specialise in, and I'd love to help you get results.",
    "After reading through your post, I'm confident I can deliver exactly what you're looking for.",
    "I've been doing this kind of work for years and your project is right in my wheelhouse.",
]

INTROS = {
    "Google Ads": "I specialize in building full-funnel Google Ads campaigns, from search and shopping to display and remarketing, with a strong focus on clean structure, tracking, and conversion quality.",
    "Meta Ads": "I specialize in running Meta campaigns across the full customer journey, from audience discovery through to conversion-focused optimisation.",
    "SEO": "I specialize in SEO strategy built around technical audits, on-page refinement, content improvements, and link building work that supports long-term organic visibility.",
    "SMM": "I specialize in social media management that builds real engagement and brand presence, with content planned around the audience rather than vanity metrics.",
    "SEM": "I specialize in search engine marketing across Google and Bing, with a focus on campaign structure, search intent, and ongoing optimisation.",
    "GEO": "I specialize in geo-targeted digital marketing strategies that help local businesses strengthen their visibility across the areas that matter most to them.",
    "Digital Marketing": "I specialize in building full-funnel digital marketing strategies across paid media, SEO, and social, with each channel aligned to the wider business goals.",
    "default": "I specialize in full-stack digital marketing, paid ads, SEO, social media, and strategy, with a hands-on, practical approach tailored to each project.",
}

SERVICES = {
    "Google Ads": "I work across Google Search, Shopping, Display, and YouTube, shaping campaigns around intent, conversion tracking, messaging, and landing page relevance.",
    "Meta Ads": "I manage Meta campaigns across Facebook and Instagram with close attention to audience segmentation, creative direction, testing structure, and landing page alignment.",
    "SEO": "I handle SEO as a whole, including technical review, on-page refinement, content alignment, internal linking, and off-page support where it makes sense.",
    "SMM": "I manage social media with a focus on content quality, posting consistency, brand voice, and audience engagement.",
    "SEM": "I work across paid search with close attention to keyword intent, account structure, ad messaging, landing page relevance, and tracking accuracy.",
    "GEO": "I handle local SEO with a focus on Google Business Profile refinement, local keyword mapping, citation consistency, review management, and location page improvements.",
    "Digital Marketing": "I work across paid media, SEO, and digital strategy depending on what the brief actually needs most, with a practical and structured approach.",
    "default": "I work across paid media, SEO, and digital strategy depending on what the brief actually needs most, with a practical and structured approach.",
}

APPROACHES = [
    "My approach is collaborative and transparent. I like to keep the work structured, explain what's being done, and make decisions based on what the data and the project needs are actually showing.",
    "I prefer to work in a practical and methodical way, where the setup is cleaned up first, the priorities are clear, and each next step has a reason behind it.",
    "I tend to work closely with clients rather than in isolation, so there's always clarity around what I'm doing, what I'm seeing, and how I'd prioritize the next phase of work.",
]

NEXT_STEPS = [
    "If the fit feels right, I'd be happy to discuss the brief further and share how I'd prioritize the first phase of work.",
    "Happy to talk through your goals and current setup, then outline the areas I'd focus on first.",
    "I'd be glad to learn a bit more about the project and share a practical roadmap based on what you need most right now.",
    "I'm happy to jump on a quick call to discuss the brief and how I'd approach it.",
]

RESULT_EXAMPLES = {
    "Google Ads": [
        "In a recent Google Ads project, I helped restructure the account, improve tracking clarity, and make the setup much easier to manage and optimise.",
        "I recently worked on a paid search account that needed cleaner segmentation, better messaging alignment, and a more practical reporting setup.",
    ],
    "Meta Ads": [
        "I recently supported a Meta Ads account by refining the audience setup, improving creative testing structure, and making the funnel easier to evaluate.",
        "For one campaign, I focused on account organisation, creative direction, and a more reliable testing process across different audience stages.",
    ],
    "SEO": [
        "For one SEO project, I worked through the technical setup, content structure, and internal linking so the site had a much clearer foundation to build on.",
        "I recently supported an SEO campaign by cleaning up page targeting, improving content alignment, and addressing the technical issues that were getting in the way.",
    ],
    "default": [
        "In a recent cross-channel project, I helped bring the paid and organic work into a more consistent structure so the business had a clearer marketing roadmap.",
        "For a growing brand, I supported the marketing setup through better targeting, cleaner reporting, and a more organised testing process.",
    ],
}

def normalize_output(text):
    text = text.replace("—", ",")
    text = text.replace("–", ",")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"\s+,", ",", text)
    text = re.sub(r",\s*,", ",", text)
    return text.strip()

def count_words(text):
    return len(text.split())

def get_length_range(length_label):
    if length_label == "Very Short (~80 words)":
        return 80, 90
    if length_label == "Short (~120 words)":
        return 120, 130
    return 180, 200

def detect_service(job_text, service_input):
    text = (job_text + " " + service_input).lower()

    if any(w in text for w in ["google ads", "google ad", "ppc", "adwords", "search ads", "performance max", "shopping"]):
        return "Google Ads"
    if any(w in text for w in ["meta ads", "facebook ads", "instagram ads", "fb ads", "reels", "stories"]):
        return "Meta Ads"
    if any(w in text for w in ["social media", "smm", "instagram", "linkedin", "tiktok"]):
        return "SMM"
    if any(w in text for w in ["sem", "search engine marketing", "bing ads"]):
        return "SEM"
    if any(w in text for w in ["local", "geo", "location", "local seo", "google business profile", "gmb", "gbp", "maps", "citations"]):
        return "GEO"
    if any(w in text for w in ["seo", "search engine optim", "organic", "ranking", "backlink", "technical seo", "schema", "on-page", "off-page"]):
        return "SEO"

    return "Digital Marketing"

def build_strategy_preview(service_name, job_post):
    ads_openers = [
        "For paid campaigns, I usually like to start with the account structure, tracking accuracy, and landing page alignment before making bigger optimisation decisions.",
        "With ads, the first thing I'd want to review is how the campaigns are structured, whether conversion tracking is reliable, and how closely the messaging matches the landing page.",
    ]

    seo_openers = [
        "For SEO work like this, I'd normally begin by reviewing the site structure, page targeting, and any technical friction that may be getting in the way.",
        "With SEO, I prefer to start by understanding how the pages are currently mapped, where the content gaps are, and whether the technical setup is helping or holding things back.",
    ]

    local_openers = [
        "For a local project like this, I'd begin by refining the business profile and checking how consistently the business appears across the main listings.",
        "With local SEO, I usually start by improving the core local signals first, especially the profile setup, citation consistency, and location relevance.",
    ]

    social_openers = [
        "For social media work, I'd usually start by understanding the brand voice, content direction, and where the current engagement gaps are.",
        "With social, my first step would be to look at the content style, posting rhythm, and how the brand is currently connecting with its audience.",
    ]

    general_openers = [
        "From the way your project is described, I'd start by tightening the foundations and getting the core setup into better shape first.",
        "After reading through the brief, my first step would be to review the current setup and sort the immediate priorities from the longer-term work.",
    ]

    if service_name in ["Google Ads", "SEM", "Meta Ads"]:
        return random.choice(ads_openers)
    if service_name == "SEO":
        return random.choice(seo_openers)
    if service_name == "GEO":
        return random.choice(local_openers)
    if service_name == "SMM":
        return random.choice(social_openers)
    return random.choice(general_openers)

def unique_letters(sequence):
    seen = set()
    output = []
    for item in sequence:
        if item not in seen:
            seen.add(item)
            output.append(item)
    return output

def generate_candidate_letters(client_name, job_post, service_input, portfolio_url, drive_url, tone, length, include_results):
    service_name = detect_service(job_post, service_input)
    name = client_name.strip() if client_name.strip() else "there"
    greeting = f"Hello {name},"

    if tone == "Bold & Punchy":
        opening_choices = [
            "Your project is exactly what I do best. Let me show you.",
            "This role has my name on it, and here's why.",
            "I'll cut to the chase. I can deliver exactly what you're asking for.",
        ]
    elif tone == "Friendly & Warm":
        opening_choices = [
            "Your project really caught my eye and I'd love to be part of it.",
            "I came across your post and felt genuinely excited about the opportunity.",
            "This looks like a brilliant project and I think we'd work really well together.",
        ]
    elif tone == "Professional":
        opening_choices = [
            "I'm pleased to present myself as a strong candidate for this role.",
            "Your requirements are closely aligned with my core areas of expertise.",
            "I'm confident my background in digital marketing makes me an excellent fit for this position.",
        ]
    else:
        opening_choices = OPENINGS

    intro = INTROS.get(service_name, INTROS["default"])
    services_para = SERVICES.get(service_name, SERVICES["default"])
    next_steps_choices = NEXT_STEPS
    approach_choices = APPROACHES
    results_choices = RESULT_EXAMPLES.get(service_name, RESULT_EXAMPLES["default"])

    links_para = ""
    if portfolio_url.strip() or drive_url.strip():
        parts = []
        if portfolio_url.strip():
            parts.append(portfolio_url.strip())
        if drive_url.strip():
            parts.append(drive_url.strip())
        links_para = "Here are my portfolio and work samples for reference: " + " and ".join(parts)

    min_words, max_words = get_length_range(length)
    candidates = []

    for _ in range(80):
        opening_line = random.choice(opening_choices)
        opening_para = f"{opening_line} {intro}"
        strategy_para = build_strategy_preview(service_name, job_post)
        next_steps_para = random.choice(next_steps_choices)
        approach_para = random.choice(approach_choices)
        results_para = random.choice(results_choices)

        if length == "Very Short (~80 words)":
            paragraph_sets = [
                [greeting, opening_para, strategy_para, "Best regards,"],
                [greeting, opening_para, next_steps_para, "Best regards,"],
                [greeting, opening_para, strategy_para, next_steps_para, "Best regards,"],
            ]
        elif length == "Short (~120 words)":
            paragraph_sets = [
                [greeting, opening_para, services_para, next_steps_para, "Best regards,"],
                [greeting, opening_para, strategy_para, next_steps_para, "Best regards,"],
                [greeting, opening_para, services_para, strategy_para, "Best regards,"],
                [greeting, opening_para, services_para, strategy_para, next_steps_para, "Best regards,"],
            ]
        else:
            paragraph_sets = [
                [greeting, opening_para, services_para, strategy_para, approach_para, next_steps_para, "Best regards,"],
                [greeting, opening_para, services_para, strategy_para, results_para, next_steps_para, "Best regards,"],
                [greeting, opening_para, services_para, strategy_para, results_para, approach_para, next_steps_para, "Best regards,"],
            ]

            if include_results:
                paragraph_sets.append(
                    [greeting, opening_para, services_para, strategy_para, results_para, approach_para, next_steps_para, "Best regards,"]
                )

            if links_para:
                paragraph_sets.append(
                    [greeting, opening_para, services_para, strategy_para, approach_para, next_steps_para, links_para, "Best regards,"]
                )

        for pset in paragraph_sets:
            letter = normalize_output("\n\n".join(pset))
            candidates.append(letter)

    candidates = unique_letters(candidates)
    valid = [c for c in candidates if min_words <= count_words(c) <= max_words]

    if valid:
        return valid

    target = (min_words + max_words) / 2
    closest = sorted(candidates, key=lambda x: abs(count_words(x) - target))
    return closest[:10]

def build_cover_letter(client_name, job_post, service_input, portfolio_url, drive_url, tone, length, include_results, previous_letter=None):
    candidates = generate_candidate_letters(
        client_name,
        job_post,
        service_input,
        portfolio_url,
        drive_url,
        tone,
        length,
        include_results
    )

    if previous_letter and len(candidates) > 1:
        filtered = [c for c in candidates if c != previous_letter]
        if filtered:
            candidates = filtered

    return random.choice(candidates)

def generate_letter(previous_letter=None):
    return build_cover_letter(
        st.session_state.client_name,
        st.session_state.job_post,
        st.session_state.service,
        st.session_state.portfolio,
        st.session_state.drive_url,
        st.session_state.tone,
        st.session_state.length,
        st.session_state.include_results,
        previous_letter=previous_letter
    )

def reset_form():
    for key, value in DEFAULTS.items():
        st.session_state[key] = value

def render_output_box_with_copy(text):
    safe_text = html.escape(text)
    formatted_paragraphs = []
    for p in safe_text.split("\n\n"):
        if p.strip():
            formatted_paragraphs.append(f"<p>{p.replace(chr(10), '<br>')}</p>")
    formatted_html = "".join(formatted_paragraphs)

    js_text = (
        text.replace("\\", "\\\\")
        .replace("`", "\\`")
        .replace("${", "\\${")
    )

    html_code = f"""
    <div class="cover-wrapper">
        <button class="copy-icon" onclick="copyCoverLetter()" title="Copy cover letter">📋</button>
        <div class="cover-box">
            {formatted_html}
        </div>
        <div id="copy-toast" class="copy-toast">Your cover letter has been copied successfully</div>
    </div>

    <style>
    .cover-wrapper {{
        position: relative;
        margin-top: 8px;
    }}
    .cover-box {{
        background: #ffffff;
        color: #000000;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        font-size: 0.95rem;
        line-height: 1.75;
        cursor: text;
        user-select: text;
        box-shadow: 0 0 0 1px rgba(0,0,0,0.02);
        max-height: 420px;
        overflow-y: auto;
        overflow-x: hidden;
    }}
    .cover-box p {{
        margin: 0 0 1rem 0;
        color: #000000;
    }}
    .cover-box p:last-child {{
        margin-bottom: 0;
    }}
    .cover-box::-webkit-scrollbar {{
        width: 8px;
    }}
    .cover-box::-webkit-scrollbar-thumb {{
        background: #cfcfcf;
        border-radius: 10px;
    }}
    .cover-box::-webkit-scrollbar-track {{
        background: transparent;
    }}
    .copy-icon {{
        position: absolute;
        top: 12px;
        right: 12px;
        border: 1px solid #d9d9d9;
        background: #ffffff;
        border-radius: 8px;
        padding: 6px 9px;
        cursor: pointer;
        font-size: 16px;
        line-height: 1;
        z-index: 2;
    }}
    .copy-icon:hover {{
        background: #f5f5f5;
    }}
    .copy-toast {{
        position: fixed;
        left: 50%;
        bottom: 24px;
        transform: translateX(-50%);
        background: rgba(17, 17, 17, 0.92);
        color: white;
        padding: 12px 18px;
        border-radius: 10px;
        font-size: 14px;
        z-index: 9999;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.25s ease;
    }}
    .copy-toast.show {{
        opacity: 1;
    }}
    </style>

    <script>
    function copyCoverLetter() {{
        const text = `{js_text}`;
        navigator.clipboard.writeText(text).then(function() {{
            const toast = document.getElementById("copy-toast");
            toast.classList.add("show");
            setTimeout(function() {{
                toast.classList.remove("show");
            }}, 2200);
        }});
    }}
    </script>
    """
    components.html(html_code, height=500, scrolling=False)

st.markdown("## ⚡ Upwork Cover Letter Generator")
st.caption("Fill details below for instant professional cover letters for your job post.")

st.subheader("Job Details")
col1, col2 = st.columns(2)
col1.text_input("Client Name", placeholder="e.g. Kamal, Sarah...", key="client_name")
col2.text_input("Service/Niche", placeholder="e.g. Google Ads, SEO...", key="service")

st.text_area(
    "Job Post/Description *",
    height=180,
    placeholder="Paste Upwork job here...",
    key="job_post"
)

st.subheader("Your Links (optional)")
st.text_input("Portfolio URL", placeholder="https://yourportfolio.com", key="portfolio")
st.text_input("Drive/Video Link", placeholder="https://drive.google.com/...", key="drive_url")

st.subheader("Tone & Style")
col3, col4, col5 = st.columns(3)
col3.selectbox(
    "Tone",
    ["Confident & Direct", "Friendly & Warm", "Professional", "Bold & Punchy"],
    key="tone"
)
col4.selectbox(
    "Length",
    ["Very Short (~80 words)", "Short (~120 words)", "Medium (~180 words)"],
    key="length"
)
col5.checkbox("Include Results Example?", key="include_results")

col_btn1, col_btn2, col_btn3 = st.columns(3)

generate_disabled = st.session_state.first_draft_done
rewrite_disabled = not st.session_state.first_draft_done

generate_btn = col_btn1.button(
    "Generate Cover Letter →",
    use_container_width=True,
    type="primary",
    disabled=generate_disabled,
    key="generate_btn"
)

rewrite_btn = col_btn2.button(
    "🔄 Rewrite",
    use_container_width=True,
    disabled=rewrite_disabled,
    key="rewrite_btn"
)

col_btn3.button(
    "🗑️ New Project",
    use_container_width=True,
    key="new_project_btn",
    on_click=reset_form
)

if generate_btn:
    if not st.session_state.job_post.strip():
        st.error("Paste job description first.")
    else:
        st.session_state.generated_letter = generate_letter()
        st.session_state.first_draft_done = True
        st.rerun()

if rewrite_btn:
    if not st.session_state.job_post.strip():
        st.error("Paste job description first.")
    else:
        st.session_state.generated_letter = generate_letter(
            previous_letter=st.session_state.generated_letter
        )
        st.rerun()

if st.session_state.generated_letter:
    st.markdown("### ✦ Generated Letter")
    render_output_box_with_copy(st.session_state.generated_letter)

    st.caption(
        f"{len(st.session_state.generated_letter.split())} words · {len(st.session_state.generated_letter)} chars"
    )

    st.download_button(
        "📥 Download TXT",
        st.session_state.generated_letter,
        "cover_letter.txt"
    )
