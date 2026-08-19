# 🎤 AI Voice Technical Interview Agent

An AI-powered voice-based technical interview system that conducts mock interviews for **Python / AI Engineer** roles.

The application uses **Speech-to-Text, Large Language Models, and Text-to-Speech** to simulate a real technical interview and generate an AI-based interview evaluation report.

---

## 🚀 Features

- 🎤 Voice-based candidate answers
- 📝 Speech-to-Text using Deepgram
- 🤖 AI-generated technical interview questions
- 🔊 AI interviewer voice using Text-to-Speech
- 🔄 Dynamic interview conversation
- 🧠 Context-aware follow-up questions
- 📊 AI-powered interview evaluation
- ⭐ Overall, Technical, Communication, Confidence and Problem-Solving scores
- 📄 Automatic interview report generation
- 📥 Download interview report
- 🖥️ Streamlit web interface
- 🔁 Start a new interview

---

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │      Candidate      │
                    │       🎤 Voice      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Microphone      │
                    │   Audio Recording   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Deepgram       │
                    │   Speech-to-Text    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   AI Interviewer    │
                    │    Groq LLM         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Next Interview      │
                    │     Question        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Text-to-Speech    │
                    │    AI Voice         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   5 Question        │
                    │    Interview        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  AI Evaluation      │
                    │  Interview Report   │
                    └─────────────────────┘