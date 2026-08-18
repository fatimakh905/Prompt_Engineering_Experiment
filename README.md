<div align="center">

# Prompt Engineering Experiment

### Customer Support Chatbot

<img src="./image.jpg" width="85%" alt="Prompt Engineering Experiment">

</div>

---

## About

A prompt engineering experiment exploring how different system prompts influence the behavior of an LLM-based customer support chatbot.

The experiment compares **three system prompts  Basic, Structured, and Robust**  using the same customer-support test cases.

The implementation uses **direct Gemini API calls in Python**, without prompt-engineering frameworks.


## Experiment

The chatbot is designed for a fictional software company, **NovaSoft**, which provides project-management software for businesses.

The prompts were tested across six customer-support scenarios:

- General customer support
- Billing issues
- Ambiguous requests
- Unknown information
- Policy boundaries
- Private account access

The same test cases were used for each prompt to make the comparison consistent.

### Approach

```text
System Prompt
      ↓
Customer Query
      ↓
Gemini API
      ↓
Generated Response
      ↓
Results
```

Three system prompts were progressively developed:

**Basic → Structured → Robust**

Each version introduced additional instructions to improve control over the chatbot's behavior.


## Prompt Engineering Techniques

| Technique | Where It Was Used | Purpose |
|---|---|---|
| Basic Prompting | Prompt 1 | Defined the chatbot's role and basic response behavior |
| Structured Prompting | Prompt 2 | Added explicit responsibilities, constraints, and clarification rules |
| Few-Shot Prompting | Prompt 3 | Provided example customer interactions to demonstrate the desired behavior |
| Boundary Instructions | Prompts 2 & 3 | Prevented the chatbot from inventing policies, refunds, account access, or internal information |
| Controlled Generation | All Prompts | Used a temperature of `0.2` to keep responses relatively consistent during comparison |
  
## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
cd YOUR-REPOSITORY
```

### 2. Install the dependency

```bash
pip install -U google-genai
```

### 3. Set your Gemini API key

The API key is loaded through the `GEMINI_API_KEY` environment variable.

**Windows PowerShell:**

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

**macOS / Linux:**

```bash
export GEMINI_API_KEY="YOUR_API_KEY"
```

### 4. Run the experiment

```bash
python Prompt_Engineering.py
```

The experiment runs the same test cases against all three system prompts.

### 5. View the results

Generated responses are saved to: results.txt


## Repository Structure

```text
PromptEngineering/
│
├── image.jpg
├── Prompt_Engineering.py
├── results.txt
├── Report.pdf
└── README.md
```

---

## Deliverables

| File                             | Description                                            |
| --------------------------------- | ------------------------------------------------------ |
| `Prompt_Engineering.py`    | Raw API implementation and experiment setup             |
| `results.txt`                    | Generated responses from all three prompt variations    |
| `Report.pdf`  | Detailed experiment analysis and findings                |
| `README.md`                      | Project documentation                                    |

---

## Core Insights

The experiment demonstrated that more explicit system prompts can provide better control over LLM behavior.

The strongest improvements came from defining specific boundaries around unsupported information, account access, billing actions, and situations where the model should ask for clarification instead of making assumptions.

---

## API Security

The Gemini API key is **not stored in the source code or repository**.

It is provided through the `GEMINI_API_KEY` environment variable when running the experiment.

---

<div align="center">

**Prompt Engineering · LLM Applications · Python**

</div>
