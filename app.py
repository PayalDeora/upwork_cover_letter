import streamlit as st
import random
import re

# ─────────────────────────────────────────────
# COVER LETTER GENERATION ENGINE
# ─────────────────────────────────────────────

OPENINGS = [
    "I'm genuinely excited to put myself forward for this role.",
    "Your project caught my attention straight away — it's exactly the kind of work I love doing.",
    "This opportunity is a strong match for what I specialise in, and I'd love to help you get results.",
    "After reading through your post, I'm confident I can deliver exactly what you're looking for.",
    "I've been doing this kind of work for years and your project is right in my wheelhouse.",
]

INTROS = {
    "Google Ads": "I specialize in building full-funnel Google Ads campaigns — from search and shopping to display and remarketing — that drive measurable growth while keeping cost per acquisition tight.",
    "Meta Ads": "I specialize in running Meta (Facebook/Instagram) campaigns focused on the full customer journey, from cold audience awareness all the way through to conversion and retention.",
    "SEO": "I specialize in SEO strategy that drives sustainable organic growth — covering technical audits, on-page optimization, content strategy, and link building.",
    "SMM": "I specialize in social media management that builds real engagement and brand presence, not just vanity metrics — crafting content that connects with the right audience.",
    "SEM": "I specialize in search engine marketing across Google and Bing, building data-driven campaigns that maximize visibility and return on ad spend.",
    "GEO": "I specialize in geo-targeted digital marketing strategies that connect local businesses with the right customers in the right locations at the right time.",
    "Digital Marketing": "I specialize in building full-funnel digital marketing strategies across paid media, SEO, and social — everything working together to drive measurable, sustainable growth.",
    "default": "I specialize in full-stack digital marketing — paid ads, SEO, social media, and strategy — handling everything personally to drive real, measurable results for my clients.",
}

SERVICES = {
    "Google Ads": "I run paid campaigns across Google Search, Shopping, Display, and YouTube — focusing on the complete customer journey to deliver strong returns. I guide brand messaging and ad creative to keep everything consistent and on-brand. I also review landing pages to spot and fix friction points that hurt conversions. To keep everything accurate, I set up proper tracking and provide clear weekly reports covering the metrics that matter most: return on ad spend, customer lifetime value, and cost per acquisition.",
    "Meta Ads": "I run paid campaigns across Facebook and Instagram, building audiences from cold traffic through to loyal customers. I manage ad creative strategy, copywriting, and visuals to make sure ads connect with the right people. I test constantly — creatives, audiences, placements — and refine based on what the data shows. You'll get clear weekly reports on ROAS, CPM, CPA, and any other metrics relevant to your goals.",
    "SEO": "I handle the full SEO picture — technical audits to fix crawlability and site speed issues, on-page optimisation to make every page work harder, and content strategy to build topical authority. I build quality backlinks through ethical outreach and keep you informed with monthly reports showing keyword rankings, organic traffic growth, and conversion data.",
    "SMM": "I manage your social media presence end to end — content creation, scheduling, community management, and growth strategy. I craft posts that reflect your brand voice and actually drive engagement. I track what's working and adjust the strategy regularly, keeping you updated with clear performance reports covering reach, engagement, and follower growth.",
    "default": "I run paid campaigns across Google and Meta, focusing on the full customer journey to deliver strong results. Alongside this, I guide brand messaging and visuals so ads feel consistent and connect with the right audience. I review landing pages to spot and fix friction points, helping improve conversions. To keep everything accurate, I ensure proper tracking is in place, and I provide clear weekly reports that highlight the metrics that matter most — return on ad spend, customer lifetime value, and cost per acquisition.",
}

APPROACHES = [
    "I believe in a collaborative, transparent workflow — testing, refining, and scaling campaigns while keeping you informed with clear, actionable reporting. My goal is to maximise efficiency of your ad spend, strengthen your brand presence, and generate sustainable growth.",
    "My approach is built on transparency and results. I test constantly, share what I find, and make data-driven decisions at every step. Everything I do is focused on making your budget work harder and your brand grow stronger.",
    "I work closely with my clients, not just for them. You'll always know what's happening, why I'm doing it, and what results it's producing. I combine creative thinking with solid data to drive campaigns that scale.",
]

NEXT_STEPS = [
    "I'd be glad to discuss your current marketing goals and challenges, and then outline a tailored roadmap for immediate improvements and long-term success.",
    "Let's have a quick conversation about where you are now and where you want to go — I'll put together a clear plan to get you there.",
    "I'd love to learn more about your business and share some initial ideas specific to your goals. Drop me a message and let's talk.",
    "If you'd like to explore working together, I'm happy to jump on a quick call to discuss your goals and how I can help achieve them.",
]

RESULT_EXAMPLES = {
    "Google Ads": [
        "In a recent project, I helped an e-commerce client grow their ROAS from 1.8x to 4.3x within 60 days by restructuring their campaign architecture and tightening audience targeting.",
        "For a SaaS client, I reduced their cost per lead by 42% while increasing monthly lead volume by 3x through aggressive A/B testing on ad copy and landing pages.",
        "I recently took a struggling Google Ads account from a 1.2x ROAS to 3.8x in under 8 weeks by rebuilding the campaign structure from the ground up.",
    ],
    "Meta Ads": [
        "For a fashion brand, I scaled their Meta Ads spend from $3k to $15k/month while maintaining a 3.5x ROAS — achieved through rigorous creative testing and audience segmentation.",
        "I recently helped a local service business generate 180 qualified leads in 30 days through a targeted Meta Ads funnel, cutting their cost per lead in half.",
        "For an online course creator, I built a cold-to-warm Meta funnel that delivered a 4.1x ROAS on a $10k monthly budget within the first 45 days.",
    ],
    "SEO": [
        "For an e-commerce store, I grew organic traffic from 200 to 2,400 monthly visitors in 5 months through a focused content and technical SEO strategy.",
        "I helped a B2B SaaS company rank on page 1 for 14 high-intent keywords within 6 months, resulting in a 60% increase in organic demo requests.",
        "After a full technical SEO audit and content overhaul, a client's organic sessions grew by 180% in 4 months without a single paid ad.",
    ],
    "default": [
        "In a recent full-stack project, I helped a client grow their monthly revenue by 65% in 90 days through a combination of Google Ads optimisation, SEO improvements, and social media strategy.",
        "For a growing e-commerce brand, I reduced blended CAC by 38% while scaling overall digital marketing spend — all through better targeting, creative testing, and funnel optimisation.",
        "I recently took on a client whose digital marketing was underperforming across every channel and turned it around within 3 months, growing their ROAS by 2.4x and organic traffic by 120%.",
    ],
}

def detect_service(job_text, service_input):
    text = (job_text + " " + service_input).lower()

    if any(w in text for w in ["google ads", "google ad", "ppc", "adwords", "search ads"]):
        return "Google Ads"
    if any(w in text for w in ["meta ads", "facebook ads", "instagram ads", "fb ads"]):
        return "Meta Ads"
    if any(w in text for w in ["seo", "search engine optim", "organic", "ranking", "backlink"]):
        return "SEO"
    if any(w in text for w in ["social media", "smm", "instagram", "linkedin", "tiktok"]):
        return "SMM"
    if any(w in text for w in ["sem", "search engine marketing", "bing ads"]):
        return "SEM"
    if any(w in text for w in ["local", "geo", "location", "local seo"]):
        return "GEO"

    return "Digital Marketing"

def extract_keywords(job_text):
    keywords = []
    patterns = [
        r'\b(increase|grow|scale|improve|boost|drive|generate)\b[^.]{0,40}',
        r'\b(brand|audience|traffic|leads|sales|revenue|conversions)\b',
        r'\b(e-?commerce|saas|local business|startup|agency)\b',
    ]

    for pattern in patterns:
        matches = re.findall(pattern, job_text.lower())
        keywords.extend(matches[:2])

    return keywords[:3]

def build_cover_letter(client_name, job_post, service_input, portfolio_url,
                       drive_url, tone, length, include_results):
    service = detect_service(job_post, service_input)

    name = client_name.strip() if client_name.strip() else "there"
    greeting = f"Hello {name},"

    if tone == "Bold & Punchy":
        opening_line = random.choice([
            "Your project is exactly what I do best — let me show you.",
            "This role has my name on it, and here's why.",
            "I'll cut to the chase: I can deliver exactly what you're asking for.",
        ])
    elif tone == "Friendly & Warm":
        opening_line = random.choice([
            "Your project really caught my eye and I'd love to be part of it.",
            "I came across your post and felt genuinely excited about the opportunity.",
            "This looks like a brilliant project and I think we'd work really well together.",
        ])
    elif tone == "Professional":
        opening_line = random.choice([
            "I'm pleased to present myself as a strong candidate for this role.",
            "Your requirements are closely aligned with my core areas of expertise.",
            "I'm confident my background in digital marketing makes me an excellent fit for this position.",
        ])
    else:
        opening_line = random.choice(OPENINGS)

    intro = INTROS.get(service, INTROS["default"])
    opening_para = f"{opening_line} {intro}"

    services_para = SERVICES.get(service, SERVICES["default"])
    keywords = extract_keywords(job_post)
    if keywords:
        kw = str(keywords[0]).strip()
        if len(kw) > 4:
            services_para = services_para + f" I've reviewed your post carefully and I'm well-positioned to help you {kw} effectively."

    results_para = ""
    if include_results:
        results_pool = RESULT_EXAMPLES.get(service, RESULT_EXAMPLES["default"])
        results_para = random.choice(results_pool)

    approach_para = random.choice(APPROACHES)
    next_steps_para = random.choice(NEXT_STEPS)

    links_para = ""
    if portfolio_url.strip() or drive_url.strip():
        parts = []
        if portfolio_url.strip():
            parts.append(portfolio_url.strip())
        if drive_url.strip():
            parts.append(drive_url.strip())
        links_para = "Here are my portfolio and some videos for your reference: " + " and ".join(parts)

    paragraphs = [greeting, "", opening_para, ""]

    if results_para:
        if length == "Medium (~180 words)":
            paragraphs.append(services_para)
            paragraphs.append("")
            paragraphs.append(results_para)
            paragraphs.append("")
        else:
            paragraphs.append(services_para + " " + results_para)
            paragraphs.append("")
    else:
        paragraphs.append(services_para)
        paragraphs.append("")

    paragraphs.append(approach_para)
    paragraphs.append("")
    paragraphs.append(next_steps_para)
    paragraphs.append("")

    if links_para:
        paragraphs.append(links_para)
        paragraphs.append("")

    paragraphs.append("Best regards,")

    letter = "\n".join(paragraphs)

    if length == "Very Short (~80 words)":
        short = "\n".join([
            greeting,
            "",
            opening_para,
            "",
            next_steps_para,
            "",
        ])
        if links_para:
            short += links_para + "\n\n"
        short += "Best regards,"
        return short

    return letter

# ─────────────────────────────────────────────
# STREAMLIT PAGE
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Upwork Cover Letter Generator",
    page_icon="⚡",
    layout="centered"
)

st.markdown("## ⚡ Upwork Cover Letter Generator")
st.caption("Fill details below for instant professional letters — no API needed.")

# Job Details
st.subheader("Job Details")
col1, col2 = st.columns(2)
client_name = col1.text_input("Client Name", placeholder="e.g. Kamal, Sarah...")
service = col2.text_input("Service/Niche", placeholder="e.g. Google Ads, SEO...")
job_post = st.text_area(
    "Job Post/Description *",
    height=180,
    placeholder="Paste Upwork job here..."
)

# Links
st.subheader("Your Links (optional)")
portfolio = st.text_input("Portfolio URL", placeholder="https://yourportfolio.com")
drive_url = st.text_input("Drive/Video Link", placeholder="https://drive.google.com/...")

# Style
st.subheader("Tone & Style")
col3, col4, col5 = st.columns(3)
tone = col3.selectbox("Tone", ["Confident & Direct", "Friendly & Warm", "Professional", "Bold & Punchy"])
length = col4.selectbox("Length", ["Very Short (~80 words)", "Short (~120 words)", "Medium (~180 words)"])
include_results = col5.checkbox("Include Results Example?", value=True)

if st.button("Generate Cover Letter →", type="primary"):
    if not job_post.strip():
        st.error("Paste job description first.")
    else:
        letter = build_cover_letter(
            client_name,
            job_post,
            service,
            portfolio,
            drive_url,
            tone,
            length,
            include_results
        )

        st.markdown("### ✦ Generated Letter")
        st.text_area("Generated Output", value=letter, height=350)
        st.caption(f"{len(letter.split())} words · {len(letter)} chars")
        st.download_button("📥 Download TXT", letter, "cover_letter.txt")

# Sidebar
with st.sidebar:
    st.info("💡 Push to GitHub and deploy on Streamlit Community Cloud for public URL.")
