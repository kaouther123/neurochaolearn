
# Module NLP de feedback pédagogique
# Fonctionne sans API externe — basé sur analyse de mots-clés

# ── Base de connaissances ───────────────────────────────────────────
KNOWLEDGE_BASE = {

    "chaos": {
        "keywords": ["chaos", "chaotic", "irregular", "unpredictable", "sensitive"],
        "correct": "Chaos refers to deterministic but unpredictable behavior "
                   "arising from sensitivity to initial conditions — not randomness.",
        "misconception": "chaos is random",
        "misconception_keywords": ["random", "noise", "stochastic", "probabilistic"],
        "correction": "Careful — chaotic systems are fully deterministic. "
                      "The irregularity comes from sensitivity to initial conditions, "
                      "not from randomness or noise."
    },

    "action_potential": {
        "keywords": ["action potential", "spike", "firing", "depolarization", "repolarization"],
        "correct": "An action potential is a rapid, transient change in membrane "
                   "potential triggered when the neuron reaches threshold.",
        "misconception": "action potential is continuous",
        "misconception_keywords": ["continuous", "gradual", "smooth", "proportional"],
        "correction": "Action potentials follow an all-or-nothing principle — "
                      "they are discrete events, not graded signals."
    },

    "limit_cycle": {
        "keywords": ["limit cycle", "periodic", "closed orbit", "stable orbit", "loop"],
        "correct": "A limit cycle is a closed trajectory in phase space "
                   "that the system returns to after small perturbations.",
        "misconception": "limit cycle is equilibrium",
        "misconception_keywords": ["equilibrium", "fixed point", "rest", "static", "steady"],
        "correction": "A limit cycle is not an equilibrium — it is a sustained "
                      "oscillation. The system keeps moving along the closed orbit."
    },

    "lyapunov": {
        "keywords": ["lyapunov", "divergence", "exponent", "sensitivity", "butterfly"],
        "correct": "A positive Lyapunov exponent indicates exponential divergence "
                   "of nearby trajectories — the hallmark of chaos.",
        "misconception": "lyapunov means unstable",
        "misconception_keywords": ["unstable", "explodes", "diverges forever", "unbounded"],
        "correction": "A positive Lyapunov exponent does not mean the system explodes. "
                      "Chaotic trajectories stay bounded — they just diverge from "
                      "each other exponentially within a bounded region (the attractor)."
    },

    "hodgkin_huxley": {
        "keywords": ["hodgkin", "huxley", "sodium", "potassium", "conductance", "gate"],
        "correct": "The Hodgkin-Huxley model describes neuronal firing through "
                   "voltage-gated ion channels for sodium and potassium.",
        "misconception": "hodgkin huxley is linear",
        "misconception_keywords": ["linear", "simple", "proportional", "additive"],
        "correction": "The Hodgkin-Huxley model is highly nonlinear — "
                      "the m³h and n⁴ terms create the complex dynamics "
                      "responsible for action potentials and chaotic behavior."
    },

    "phase_portrait": {
        "keywords": ["phase portrait", "phase space", "trajectory", "attractor", "orbit"],
        "correct": "A phase portrait shows the trajectory of a dynamical system "
                   "in state space, revealing its long-term behavior geometrically.",
        "misconception": "phase portrait is time series",
        "misconception_keywords": ["time", "versus time", "temporal", "time series"],
        "correction": "A phase portrait plots state variables against each other "
                      "(e.g. V vs dV/dt), not against time. "
                      "It reveals geometric structure invisible in time series."
    }
}

# ── Analyse de la réponse étudiant ─────────────────────────────────
def analyze_response(question_topic, student_text):
    """
    Analyse le texte de l'étudiant et retourne un feedback structuré.
    """
    text_lower = student_text.lower()
    result = {
        "topic": question_topic,
        "score": 0,
        "feedback": "",
        "misconception_detected": False,
        "misconception": "",
        "correction": "",
        "encouragement": ""
    }

    if question_topic not in KNOWLEDGE_BASE:
        result["feedback"] = "Topic not found in knowledge base."
        return result

    kb = KNOWLEDGE_BASE[question_topic]

    # Compter les mots-clés corrects présents
    correct_hits = sum(1 for kw in kb["keywords"] if kw in text_lower)

    # Détecter les misconceptions
    misconception_hits = sum(
        1 for kw in kb["misconception_keywords"] if kw in text_lower
    )

    # Calculer le score
    max_score = len(kb["keywords"])
    result["score"] = min(100, int((correct_hits / max(max_score, 1)) * 100))

    # Générer le feedback
    if misconception_hits > 0:
        result["misconception_detected"] = True
        result["misconception"] = kb["misconception"]
        result["correction"] = kb["correction"]
        result["feedback"] = (
            f"Your answer shows some understanding, but contains a common misconception. "
            f"{kb['correction']}"
        )
    elif correct_hits >= 2:
        result["feedback"] = (
            f"Good understanding! {kb['correct']} "
            f"You correctly identified {correct_hits} key concept(s)."
        )
        result["encouragement"] = "Keep exploring — try adjusting the parameters to see this in action!"
    elif correct_hits == 1:
        result["feedback"] = (
            f"You are on the right track. {kb['correct']} "
            f"Try to be more specific about the mechanism involved."
        )
        result["encouragement"] = "Hint: look at the phase portrait for a visual clue."
    else:
        result["feedback"] = (
            f"Let's revisit this concept. {kb['correct']} "
            f"Try to connect what you see in the simulation to the underlying theory."
        )
        result["encouragement"] = "Tip: adjust I_ext and observe how the phase portrait changes."

    return result

# ── Questions pédagogiques par sujet ───────────────────────────────
QUESTIONS = {
    "chaos": "In your own words, what is the difference between "
             "chaotic behavior and random noise in neuronal dynamics?",

    "action_potential": "Describe what happens to the membrane potential "
                        "during an action potential. What triggers it?",

    "limit_cycle": "What does the closed loop in the phase portrait represent? "
                   "What happens to the trajectory after a small perturbation?",

    "lyapunov": "What does a positive Lyapunov exponent tell us about "
                "the behavior of the Hodgkin-Huxley neuron at high stimulus?",

    "hodgkin_huxley": "Why is the Hodgkin-Huxley model considered nonlinear? "
                      "What role do the gate variables m, h, and n play?",

    "phase_portrait": "What is the difference between a time series plot and "
                      "a phase portrait? What additional information does the "
                      "phase portrait provide?"
}

print("✅ Module NLP créé")
