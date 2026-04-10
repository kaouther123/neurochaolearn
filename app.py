
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import sys
sys.path.append('/content/drive/MyDrive/neurochaolearn')
from modules.hodgkin_huxley import simulate, get_regime, bifurcation_data
from modules.nlp_feedback import analyze_response, QUESTIONS, KNOWLEDGE_BASE

st.set_page_config(
    page_title="NeuroChaoLearn",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
<style>
.regime-badge {
    padding: 6px 16px; border-radius: 20px;
    font-weight: 600; font-size: 15px;
    display: inline-block; margin-bottom: 12px;
}
.feedback-box {
    padding: 16px; border-radius: 10px;
    margin-top: 10px; font-size: 14px;
}
.block-container { padding-top: 2rem; }
</style>
""", unsafe_allow_html=True)

# ── Navigation ──────────────────────────────────────────────────────
st.sidebar.title("🧠 NeuroChaoLearn")
page = st.sidebar.radio("Navigation", [
    "Simulation",
    "Feedback & Quiz"
])
st.sidebar.divider()
st.sidebar.caption("NeuroChaoLearn v0.2 — Conference prototype")

# ══════════════════════════════════════════════════════════════════
# PAGE 1 : SIMULATION
# ══════════════════════════════════════════════════════════════════
if page == "Simulation":

    st.title("🧠 NeuroChaoLearn")
    st.caption("Interactive platform for teaching chaotic systems in neuroscience")
    st.divider()

    with st.sidebar:
        st.header("Simulation parameters")
        I_ext = st.slider("External current I_ext (µA/cm²)",
            min_value=0.0, max_value=50.0, value=10.0, step=0.5)
        t_max = st.slider("Duration (ms)",
            min_value=50, max_value=500, value=100, step=50)
        show_gates       = st.checkbox("Show gate variables",      value=False)
        show_phase       = st.checkbox("Show phase portrait",      value=False)
        show_bifurcation = st.checkbox("Show bifurcation diagram", value=False)

    regime_label, regime_color = get_regime(I_ext)
    st.markdown(
        f'<span class="regime-badge" '
        f'style="background:{regime_color}22;color:{regime_color};'
        f'border:1.5px solid {regime_color}55;">'
        f'Regime : {regime_label}</span>',
        unsafe_allow_html=True
    )

    with st.spinner("Running simulation..."):
        sol = simulate(I_ext=I_ext, t_max=t_max)

    V, m, h, n, t = sol.y[0], sol.y[1], sol.y[2], sol.y[3], sol.t

    fig_V = go.Figure()
    fig_V.add_trace(go.Scatter(x=t, y=V, mode='lines',
        line=dict(color='#378ADD', width=1.8), name='Membrane potential'))
    fig_V.add_hline(y=-65, line_dash="dash", line_color="gray",
        line_width=0.8, annotation_text="Resting potential")
    fig_V.update_layout(
        title=f"Membrane potential — I_ext = {I_ext} µA/cm²",
        xaxis_title="Time (ms)", yaxis_title="Voltage (mV)",
        height=350, margin=dict(l=40,r=20,t=50,b=40),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_V, use_container_width=True)

    if show_gates:
        fig_g = go.Figure()
        fig_g.add_trace(go.Scatter(x=t, y=m, mode='lines',
            line=dict(color='#D85A30',width=1.5), name='m (Na activation)'))
        fig_g.add_trace(go.Scatter(x=t, y=h, mode='lines',
            line=dict(color='#1D9E75',width=1.5), name='h (Na inactivation)'))
        fig_g.add_trace(go.Scatter(x=t, y=n, mode='lines',
            line=dict(color='#7F77DD',width=1.5), name='n (K activation)'))
        fig_g.update_layout(title="Gate variables",
            xaxis_title="Time (ms)", yaxis_title="Probability",
            height=300, margin=dict(l=40,r=20,t=50,b=40),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_g, use_container_width=True)

    if show_phase:
        dV = np.gradient(V, t)
        fig_p = go.Figure()
        fig_p.add_trace(go.Scatter(x=V, y=dV, mode='lines',
            line=dict(color='#7F77DD',width=1.2), name='Phase trajectory'))
        fig_p.update_layout(title="Phase portrait (V vs dV/dt)",
            xaxis_title="V (mV)", yaxis_title="dV/dt (mV/ms)",
            height=350, margin=dict(l=40,r=20,t=50,b=40),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_p, use_container_width=True)

    if show_bifurcation:
        st.info("Computing bifurcation diagram — this may take 20–30 seconds...")
        with st.spinner("Scanning parameter space..."):
            peaks_I, peaks_V = bifurcation_data()
        fig_b = go.Figure()
        fig_b.add_trace(go.Scatter(x=peaks_I, y=peaks_V, mode='markers',
            marker=dict(color='#378ADD',size=2,opacity=0.6), name='Peaks'))
        fig_b.add_vline(x=I_ext, line_dash="dash", line_color="#D85A30",
            annotation_text=f"Current I = {I_ext}")
        fig_b.update_layout(title="Bifurcation diagram",
            xaxis_title="I_ext (µA/cm²)", yaxis_title="Peak potential (mV)",
            height=350, margin=dict(l=40,r=20,t=50,b=40),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_b, use_container_width=True)

    st.divider()
    with st.expander("What am I observing?", expanded=True):
        if I_ext < 2:
            st.markdown("**Resting state** — The neuron is below threshold. "
                "No action potential is generated.")
        elif I_ext < 10:
            st.markdown("**Threshold region** — Small changes in current "
                "produce large qualitative changes in behavior.")
        elif I_ext < 30:
            st.markdown("**Periodic firing** — The neuron fires regular "
                "action potentials. The phase portrait shows a stable limit cycle.")
        else:
            st.markdown("**High-frequency / chaotic regime** — Irregular "
                "firing patterns. The phase portrait no longer forms a clean loop.")

# ══════════════════════════════════════════════════════════════════
# PAGE 2 : FEEDBACK & QUIZ
# ══════════════════════════════════════════════════════════════════
elif page == "Feedback & Quiz":

    st.title("📝 Conceptual Feedback")
    st.caption("Answer the question below — the AI will analyze your understanding")
    st.divider()

    # Sélection du sujet
    topic = st.selectbox(
        "Choose a topic",
        options=list(QUESTIONS.keys()),
        format_func=lambda x: x.replace("_", " ").title()
    )

    # Afficher la question
    st.markdown(f"### Question")
    st.info(QUESTIONS[topic])

    # Zone de réponse
    student_answer = st.text_area(
        "Your answer",
        height=150,
        placeholder="Write your answer here in your own words..."
    )

    # Bouton d'analyse
    if st.button("Analyze my answer", type="primary"):
        if len(student_answer.strip()) < 10:
            st.warning("Please write a more complete answer before submitting.")
        else:
            with st.spinner("Analyzing your response..."):
                result = analyze_response(topic, student_answer)

            # Afficher le score
            score = result["score"]
            if score >= 60:
                score_color = "#1D9E75"
                score_label = "Good understanding"
            elif score >= 30:
                score_color = "#EF9F27"
                score_label = "Partial understanding"
            else:
                score_color = "#D85A30"
                score_label = "Needs review"

            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown(
                    f'<div style="text-align:center;padding:20px;'
                    f'border-radius:12px;background:{score_color}22;'
                    f'border:1.5px solid {score_color}55;">'
                    f'<div style="font-size:32px;font-weight:700;color:{score_color};">'
                    f'{score}%</div>'
                    f'<div style="font-size:12px;color:{score_color};">'
                    f'{score_label}</div></div>',
                    unsafe_allow_html=True
                )

            with col2:
                # Misconception détectée
                if result["misconception_detected"]:
                    st.error(f"⚠️ Misconception detected : *{result['misconception']}*")
                    st.markdown(f"**Correction :** {result['correction']}")
                else:
                    st.success("✅ No major misconception detected")
                    st.markdown(f"**Feedback :** {result['feedback']}")

                if result.get("encouragement"):
                    st.markdown(
                        f'<div style="margin-top:10px;padding:10px;'
                        f'border-radius:8px;background:#378ADD22;'
                        f'border-left:3px solid #378ADD;font-size:13px;">'
                        f'💡 {result["encouragement"]}</div>',
                        unsafe_allow_html=True
                    )

            # Afficher la réponse correcte
            with st.expander("See the reference answer"):
                kb = KNOWLEDGE_BASE[topic]
                st.markdown(kb["correct"])
                st.markdown("**Key concepts to include :**")
                st.markdown(", ".join([f"`{kw}`" for kw in kb["keywords"]]))

    st.divider()

    # Progression de l'étudiant
    st.markdown("### Your progress")
    topics = list(QUESTIONS.keys())
    cols = st.columns(len(topics))
    for i, t_name in enumerate(topics):
        with cols[i]:
            st.markdown(
                f'<div style="text-align:center;padding:8px;'
                f'border-radius:8px;background:var(--background-color);'
                f'border:1px solid #ccc;font-size:11px;">'
                f'{t_name.replace("_"," ").title()}</div>',
                unsafe_allow_html=True
            )

print("✅ app.py mis à jour avec le module NLP")
