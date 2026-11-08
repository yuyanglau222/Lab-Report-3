# BSD3513 / BSD2513 Artificial Intelligence — Lab Report 3

## Chapter 3: Knowledge Representation System (Scholarship Advisory Rule-Based System)

## 📌 Project Overview

This repository contains the Python source code and Streamlit web application for **Lab Report 3 (Question 2)** in **BSD3513 Introduction to Artificial Intelligence** at Universiti Malaysia Pahang Al-Sultan Abdullah (UMPSA).

The system implements a transparent **Rule-Based Expert System** to assist university academic and financial aid committees in evaluating student scholarship eligibility based on applicant facts and prioritized `IF-THEN` production rules.

---

## 📋 Applicant Facts Evaluated

Each scholarship applicant is evaluated across six attributes:
1. **Cumulative GPA (`cgpa`)** — Scale $0.00$ to $4.00$
2. **Monthly Family Income (`family_income`)** — In MYR
3. **Co-curricular Involvement Score (`co_curricular_score`)** — Scale $0$ to $100$
4. **Community Service Hours (`community_service_hours`)** — Total hours
5. **Current Semester of Study (`semester`)** — Semester $1$ to $12$
6. **Disciplinary Actions (`disciplinary_actions`)** — Number of records

---

## ⚙️ Rule Base & Conflict Resolution

The inference engine evaluates all rules simultaneously using conjunctive (`AND`) logic. If multiple rules match an applicant's profile, **conflict resolution** selects the rule with the **highest priority**:

| Rule Name | Priority | Decision | Condition Summary |
| :--- | :---: | :---: | :--- |
| **Top merit candidate** | `100` | `AWARD FULL` | $\text{CGPA} \ge 3.7$, $\text{Score} \ge 80$, $\text{Income} \le 8000$, $\text{Disciplinary} = 0$ |
| **Low CGPA not eligible** | `95` | `REJECT` | $\text{CGPA} < 2.5$ |
| **Serious disciplinary record** | `90` | `REJECT` | $\text{Disciplinary} \ge 2$ |
| **Good candidate partial scholarship** | `80` | `AWARD PARTIAL` | $\text{CGPA} \ge 3.3$, $\text{Score} \ge 60$, $\text{Income} \le 12000$, $\text{Disciplinary} \le 1$ |
| **Need-based review** | `70` | `REVIEW` | $\text{CGPA} \ge 2.5$, $\text{Income} \le 4000$ |

---

## 📂 Repository Structure

```text
.
├── rbs_streamlit.py          
├── requirements.txt    
└── README.md           
```

---

## 🚀 How to Run Locally

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Streamlit app:**
   ```bash
   streamlit run rbs_streamlit.py
   ```
