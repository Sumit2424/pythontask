🚀 Getting Started: Running the Backend

Before we explore the story behind this system, let’s begin with the essentials—how to run it.

1. **Create and activate your virtual environment**
   ```powershell
   py -3.13 -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
2. **Install all dependencies**
   ```powershell
   pip install -r backend/requirements.txt
   python -m spacy download en_core_web_sm
   ```
3. **Add your Speech-to-Text key**
   Create a `.env` file inside `backend/`:
   ```env
   GEMINI_API_KEY=your_key_here
   ```
4. **Start the server**
   ```powershell
   cd backend
   uvicorn api.app:app --reload
   ```

The backend is now available at **http://localhost:8000**, and you can POST audio files to `POST /upload-audio`.

---

## 🌱 The Story Behind the Meeting Task Extraction Backend
This project did not begin with code — it began with a realization. Meetings produce massive amounts of scattered information. People speak spontaneously, ideas overlap, and tasks get buried inside casual conversation. After meetings end, teams often remember only fragments of what was decided.

We wanted something smarter. Something that could listen like a human, understand intent, and convert speech into organized, actionable work. We imposed a constraint: **No large language models**—no GPT, no Gemini text models, no transformers. We wanted something explainable, controllable, lightweight. This constraint shaped everything: the architecture, the algorithms, the design philosophy. The system you see today emerged from that challenge.

---

## 🧠 How We Thought About the Problem
The earliest challenge was conceptual: **How does a system decide whether a sentence in a meeting is a task?** Humans do this intuitively. Machines do not.

Keyword lists failed instantly—new verbs appear constantly, task phrasing varies, questions can imply tasks, and some task-like sentences are actually status updates. This pushed us toward probabilistic thinking. We needed a system that:
- learns patterns rather than memorizing words,
- understands structure, not just text,
- infers meaning from grammar and dependency relations,
- detects subtle cues like deadlines or urgency,
- operates without LLMs,
- remains fast and interpretable.

That realization led to the hybrid architecture we built: **classical ML + deterministic NLP + spaCy**. Sentence splitting—something seemingly trivial—turned out to be one of the hardest pieces because STT outputs often lack punctuation, making it difficult to detect boundaries. We solved this with a shared spaCy pipeline, custom fallbacks, and priority-based splitting rules.

---

## ⚠️ Challenges Faced During Development
1. **Incorrect sentence boundaries**  
   STT transcripts often merge multiple ideas.  
   *Solution:* spaCy sentence boundaries + regex fallback + custom heuristics.

2. **Distinguishing tasks from non-tasks**  
   Humans instinctively know “Can you hear me?” isn’t a task while “Rahul, please update the API docs” is. Models struggle.  
   *Solution:* TF-IDF + Logistic Regression classifier plus imperative/request/obligation rules.

3. **No LLMs allowed**  
   Without LLMs we couldn’t rely on semantic embeddings, forcing us to use verbs, subjects, dependency trees, and statistical classification.  
   *Outcome:* Greater stability and explainability.

4. **Extracting deadlines from ambiguous phrases**  
   Expressions like “sometime next week” or “before Friday” are vague.  
   *Solution:* `dateparser` with sliding windows + preserving raw text when parsing fails.

5. **Assigning tasks without hardcoding names**  
   The system must generalize to any team.  
   *Solution:* spaCy NER + syntactic role inference.

6. **Consistent pipeline performance**  
   Multiple modules loading spaCy slowed everything down.  
   *Solution:* Shared, cached spaCy loader (`spacy_utils.py`) for uniform behavior.

---

## 🧠 How the System Understands a Meeting
1. **Split** the transcript into meaningfully separated sentences.
2. **Identify** which sentences represent tasks using ML probability + linguistic patterns.
3. **Extract the who** via named entities and syntactic roles.
4. **Extract the when** by parsing natural language deadlines.
5. **Extract urgency** using linguistic cues and heuristics.
6. **Compose** the final structured task object as actionable JSON.

---

## � The Codebase as a Living System
```
The project is organized to support clarity, extensibility, and independent iteration of ML, NLP, and API concerns:

backend/
├── api/                 # FastAPI layer
├── assingment/          # Ownership and skill-based logic
├── ml/                  # Modern model training & data
├── mlmodel/             # Legacy models (to be phased out)
├── nlp/                 # Sentence splitting, extraction, parsing
├── services/            # Speech-to-text clients
├── temp/                # Temporary audio files
└── requirements.txt


Every folder has a clear responsibility, and each layer interacts only through defined interfaces.

🔧 Setting Up the Environment

The setup story is simple:

Create a Python virtual environment.

Install dependencies.

Download the spaCy model.

Add your STT provider’s API key.

Run the FastAPI server.

The system boots quickly and starts listening for audio.

🎓 Training the Classifier

Behind the scenes, the classifier learns from examples.
All training sentences — each labeled as task or non-task — live in a CSV file.
The training script transforms text into TF-IDF vectors, fits a logistic regression model, evaluates accuracy, and stores the trained model and vectorizer.

Whenever new meeting data becomes available, you can retrain the classifier to make it smarter and more attuned to your organization’s communication style.

⚙️ Runtime: How Everything Comes Together

At runtime, the pipeline unfolds exactly as described earlier.
The process transforms one long transcript into a set of well-understood tasks.
Every design decision — thresholds, fallback rules, entity logic — aims to maximize accuracy without losing interpretability.

The final response is crafted to be both machine-friendly and human-readable.

🌐 API: How Consumers Interact

External systems interact with a small, elegant API surface:

/upload-audio accepts a meeting recording and returns extracted tasks.

/health reports readiness.

Everything else happens behind the scenes.

🔍 Testing & Quality

We treat quality as a continuous process:

Unit tests verify NLP modules individually.

Integration tests confirm end-to-end pipeline behavior.

Accuracy reports monitor classifier drift over time.

Linting and type checking keep the codebase clean.

This ensures that the system doesn’t just work — it stays reliable as it evolves.

🚀 Operating the System

Running the server, retraining models, debugging issues, or swapping STT providers follows clear operational procedures. Nothing is hidden. Nothing is magical. Everything is observable and controllable.

🌄 The Road Ahead

There is still more to do:

migrating from legacy models to the new ML pipeline

refining action phrase extraction

calibrating confidence scores

supporting batch processing

adding evaluation suites for new industries

exploring lightweight on-device deployments

But the foundation is strong.
The story of this backend is one of clarity, structure, and a deep respect for traditional NLP’s strengths.

This system turns the chaos of meetings into organized action — thoughtfully, reliably, and without ever relying on a large language model.