# app.py
import json
from typing import List, Dict, Any, Tuple
import operator
import streamlit as st

# -------------------------------------------------------------
# 1) Minimal Rule Engine
# -------------------------------------------------------------

OPS = {
    "==": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
    "in": lambda a, b: a in b,
    "not_in": lambda a, b: a not in b,
}

# EXACT Rules required by Question 2 specifications
DEFAULT_RULES: List[Dict[str, Any]] = [
    {
        "name": "Top merit candidate",
        "priority": 100,
        "conditions": [
            ["cgpa", ">=", 3.7],
            ["co_curricular_score", ">=", 80],
            ["family_income", "<=", 8000],
            ["disciplinary_actions", "==", 0]
        ],
        "action": {
            "decision": "AWARD FULL",
            "reason": "Excellent academic & co-curricular performance, with acceptable need"
        }
    },
    {
        "name": "Good candidate partial scholarship",
        "priority": 80,
        "conditions": [
            ["cgpa", ">=", 3.3],
            ["co_curricular_score", ">=", 60],
            ["family_income", "<=", 12000],
            ["disciplinary_actions", "<=", 1]
        ],
        "action": {
            "decision": "AWARD PARTIAL",
            "reason": "Good academic & involvement record with moderate need"
        }
    },
    {
        "name": "Need-based review",
        "priority": 70,
        "conditions": [
            ["cgpa", ">=", 2.5],
            ["family_income", "<=", 4000]
        ],
        "action": {
            "decision": "REVIEW",
            "reason": "High need but borderline academic score"
        }
    },
    {
        "name": "Low CGPA not eligible",
        "priority": 95,
        "conditions": [
            ["cgpa", "<", 2.5]
        ],
        "action": {
            "decision": "REJECT",
            "reason": "CGPA below minimum scholarship requirement"
        }
    },
    {
        "name": "Serious disciplinary record",
        "priority": 90,
        "conditions": [
            ["disciplinary_actions", ">=", 2]
        ],
        "action": {
            "decision": "REJECT",
            "reason": "Too many disciplinary records"
        }
    }
]

def evaluate_condition(facts: Dict[str, Any], cond: List[Any]) -> bool:
    """Evaluate a single condition: [field, op, value]."""
    if len(cond) != 3:
        return False
    field, op, value = cond
    if field not in facts or op not in OPS:
        return False
    try:
        return OPS[op](facts[field], value)
    except Exception:
        return False

def rule_matches(facts: Dict[str, Any], rule: Dict[str, Any]) -> bool:
    """All conditions must evaluate to True (Conjunctive / AND logic)."""
    return all(evaluate_condition(facts, c) for c in rule.get("conditions", []))

def run_rules(facts: Dict[str, Any], rules: List[Dict[str, Any]]) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """
    Evaluates rules against facts:
    - Filters all firing rules
    - Resolves conflicts using priority (highest priority fires first)
    """
    fired = [r for r in rules if rule_matches(facts, r)]
    if not fired:
        return ({"decision": "REVIEW", "reason": "No matching criteria met for standard categories"}, [])

    # Conflict resolution: sort descending by priority
    fired_sorted = sorted(fired, key=lambda r: r.get("priority", 0), reverse=True)
    best_action = fired_sorted[0].get("action", {"decision": "REVIEW", "reason": "No action specified"})
    return best_action, fired_sorted

# -------------------------------------------------------------
# 2) Streamlit Web Interface
# -------------------------------------------------------------
st.set_page_config(page_title="Scholarship Advisory Rule-Based System", page_icon="🎓", layout="wide")
st.title("🎓 Scholarship Advisory Expert System")
st.caption("BSD2513 / BSD3513 Artificial Intelligence — Chapter 3: Knowledge Representation System")

with st.sidebar:
    st.header("Applicant Facts")
    cgpa = st.number_input("Cumulative GPA (CGPA)", min_value=0.0, max_value=4.0, value=3.75, step=0.05, format="%.2f")
    family_income = st.number_input("Monthly Family Income (MYR)", min_value=0, value=5000, step=250)
    co_curricular_score = st.slider("Co-curricular Score (0–100)", min_value=0, max_value=100, value=85)
    community_service_hours = st.number_input("Community Service Hours", min_value=0, value=20, step=2)
    semester = st.number_input("Current Semester of Study", min_value=1, max_value=12, value=3, step=1)
    disciplinary_actions = st.number_input("Disciplinary Actions on Record", min_value=0, max_value=10, value=0, step=1)

    st.divider()
    st.header("Rule Base Configuration (JSON)")
    st.caption("Editable knowledge base: modify thresholds or priorities live.")
    default_json = json.dumps(DEFAULT_RULES, indent=2)
    rules_text = st.text_area("JSON Rules", value=default_json, height=350)

    run = st.button("Evaluate Eligibility", type="primary", use_container_width=True)

# Build facts dictionary
facts = {
    "cgpa": float(cgpa),
    "family_income": float(family_income),
    "co_curricular_score": int(co_curricular_score),
    "community_service_hours": int(community_service_hours),
    "semester": int(semester),
    "disciplinary_actions": int(disciplinary_actions),
}

# Parse and validate JSON rules
try:
    rules = json.loads(rules_text)
    assert isinstance(rules, list), "Rules must be a valid JSON array"
except Exception as e:
    st.error(f"Invalid JSON syntax. Reverting to default rule base. Details: {e}")
    rules = DEFAULT_RULES

col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("📋 Input Applicant Facts")
    st.json(facts)

with col_right:
    st.subheader("📜 Active Rule Base")
    with st.expander("Expand to view active inference rules", expanded=False):
        st.code(json.dumps(rules, indent=2), language="json")

st.divider()

# Inference evaluation section
if run:
    action, fired = run_rules(facts, rules)

    col_res1, col_res2 = st.columns([1, 1])
    
    with col_res1:
        st.subheader("⚖️ Advisory Decision")
        decision = action.get("decision", "REVIEW")
        reason = action.get("reason", "-")

        if decision == "AWARD FULL":
            st.success(f"### 🎉 FULL SCHOLARSHIP AWARDED\n**Reason:** {reason}")
        elif decision == "AWARD PARTIAL":
            st.info(f"### 🥈 PARTIAL SCHOLARSHIP AWARDED\n**Reason:** {reason}")
        elif decision == "REJECT":
            st.error(f"### ❌ NOT ELIGIBLE (REJECTED)\n**Reason:** {reason}")
        else:
            st.warning(f"### ⚠️ COMMITTEE REVIEW REQUIRED\n**Reason:** {reason}")

    with col_res2:
        st.subheader("🔍 Fired Rules & Conflict Resolution")
        if not fired:
            st.info("No rule conditions were satisfied.")
        else:
            st.caption("Fired rules sorted by priority (Highest priority governs final decision):")
            for idx, r in enumerate(fired, start=1):
                is_selected = " ⭐ (Highest Priority — Executed)" if idx == 1 else ""
                st.markdown(f"**{idx}. {r.get('name', '(Unnamed)')}** — Priority: `{r.get('priority', 0)}`{is_selected}")
                st.caption(f"Action: `{r.get('action')}`")
                with st.expander(f"Condition Details ({r.get('name')})"):
                    for cond in r.get("conditions", []):
                        st.code(f"{cond[0]} {cond[1]} {cond[2]}")
else:
    st.info("Configure the applicant parameters on the sidebar and click **Evaluate Eligibility** to trigger inference.")