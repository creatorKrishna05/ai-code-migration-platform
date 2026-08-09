# ⚡ AI Code Migration Platform

<p align="center">

**AI-powered Python → C++20 code migration with automated compilation, execution, benchmarking, evaluation, and reporting.**

<br>

<a href="https://ai-code-migration-platform-zievvdkcz9mr83emx2brgv.streamlit.app/">
  <strong>🚀 Live Demo</strong>
</a>
&nbsp;&nbsp;•&nbsp;&nbsp;
<a href="https://github.com/creatorKrishna05/ai-code-migration-platform">
  <strong>💻 GitHub Repository</strong>
</a>

</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![C++20](https://img.shields.io/badge/C%2B%2B-20-00599C?style=for-the-badge\&logo=cplusplus\&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.61.1-FF4B4B?style=for-the-badge\&logo=streamlit\&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLM-orange?style=for-the-badge)
![Tests](https://img.shields.io/badge/Tests-170%20Passed-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

</p>

---

## 🚀 Live Application

### **Try the AI Code Migration Platform**

👉 **https://ai-code-migration-platform-zievvdkcz9mr83emx2brgv.streamlit.app/**

The application is deployed on **Streamlit Community Cloud** and provides an end-to-end Python-to-C++20 migration workflow.

### What the live application does

```text
Python Source
      │
      ▼
   AI Analysis
      │
      ▼
Python → C++20
      │
      ▼
 C++ Compilation
      │
      ▼
 Executable
      │
      ▼
   Execution
      │
      ▼
 Benchmarking
      │
      ▼
  Evaluation
      │
      ▼
 Migration Report
      │
      ▼
  Leaderboard
```

---

# 🧠 Overview

**AI Code Migration Platform** is a production-oriented AI application designed to automate the migration of Python programs into **standalone, compilable modern C++20 programs**.

Unlike a basic code translator, the platform validates the entire migration lifecycle:

> **Translate → Analyze → Compile → Execute → Benchmark → Evaluate → Report**

The system uses an extensible provider architecture so different LLM backends can be integrated without changing the core migration pipeline.

---

# ✨ Key Capabilities

| Capability                    | Status |
| ----------------------------- | :----: |
| Python → C++20 translation    |    ✅   |
| LLM-powered migration         |    ✅   |
| Groq provider                 |    ✅   |
| Ollama provider               |    ✅   |
| Provider factory architecture |    ✅   |
| Python source analysis        |    ✅   |
| Automatic C++ compilation     |    ✅   |
| Executable validation         |    ✅   |
| Runtime execution             |    ✅   |
| Multi-run benchmarking        |    ✅   |
| Migration evaluation          |    ✅   |
| JSON reporting                |    ✅   |
| Leaderboard                   |    ✅   |
| CLI interface                 |    ✅   |
| Streamlit interface           |    ✅   |
| Structured logging            |    ✅   |
| Centralized exceptions        |    ✅   |
| Automated test suite          |    ✅   |
| Cloud deployment              |    ✅   |

---

# 🏗️ System Architecture

```text
                         ┌─────────────────────────┐
                         │       User / Client      │
                         └────────────┬────────────┘
                                      │
                       ┌──────────────▼──────────────┐
                       │       CLI / Streamlit       │
                       └──────────────┬──────────────┘
                                      │
                       ┌──────────────▼──────────────┐
                       │       Input Validation      │
                       └──────────────┬──────────────┘
                                      │
                       ┌──────────────▼──────────────┐
                       │      Provider Factory       │
                       └──────────────┬──────────────┘
                                      │
                   ┌──────────────────┴──────────────────┐
                   │                                     │
          ┌────────▼────────┐                  ┌─────────▼────────┐
          │      Groq       │                  │      Ollama      │
          │      LLM        │                  │       LLM        │
          └────────┬────────┘                  └─────────┬────────┘
                   │                                     │
                   └──────────────────┬──────────────────┘
                                      │
                       ┌──────────────▼──────────────┐
                       │        Translator           │
                       │       Python → C++20        │
                       └──────────────┬──────────────┘
                                      │
                       ┌──────────────▼──────────────┐
                       │      Python Analyzer         │
                       └──────────────┬──────────────┘
                                      │
                       ┌──────────────▼──────────────┐
                       │         Compiler             │
                       │          g++ / C++20         │
                       └──────────────┬──────────────┘
                                      │
                       ┌──────────────▼──────────────┐
                       │         Executor             │
                       └──────────────┬──────────────┘
                                      │
                       ┌──────────────▼──────────────┐
                       │        Benchmark             │
                       │      Multiple Runs           │
                       └──────────────┬──────────────┘
                                      │
                       ┌──────────────▼──────────────┐
                       │         Evaluator            │
                       └──────────────┬──────────────┘
                                      │
                       ┌──────────────▼──────────────┐
                       │      Report Generator        │
                       └──────────────┬──────────────┘
                                      │
                       ┌──────────────▼──────────────┐
                       │       Output Manager         │
                       └──────────────┬──────────────┘
                                      │
                       ┌──────────────▼──────────────┐
                       │         Leaderboard          │
                       └─────────────────────────────┘
```

---

# 🔄 End-to-End Migration Workflow

The platform treats code migration as a complete engineering pipeline rather than a single LLM request.

### 1. Source Validation

The input Python file is validated before the migration begins.

### 2. LLM Translation

The selected provider generates standalone modern **C++20** source code.

### 3. Source Analysis

The Python source is analyzed to provide additional structural information to the migration process.

### 4. Compilation

Generated C++ is compiled using the configured C++ compiler and C++20 standard.

### 5. Execution

The compiled executable is executed with configurable timeout protection.

### 6. Benchmarking

The generated program is executed multiple times to calculate runtime performance.

### 7. Evaluation

Translation, compilation, execution, and benchmark results are aggregated into an overall migration result.

### 8. Reporting

A structured migration report is generated.

### 9. Leaderboard

Migration results can be recorded for performance comparison.

---

# 🤖 LLM Provider Architecture

The project uses a provider abstraction to keep LLM integrations independent from the migration pipeline.

```text
                 ┌──────────────────────┐
                 │    BaseProvider      │
                 └──────────┬───────────┘
                            │
                 ┌──────────┴───────────┐
                 │                      │
        ┌────────▼────────┐    ┌────────▼────────┐
        │  GroqProvider   │    │ OllamaProvider  │
        └─────────────────┘    └─────────────────┘
```

### Groq

The deployed application currently uses:

```text
Provider: Groq
Model: openai/gpt-oss-120b
```

### Ollama

Ollama support allows local LLM execution during development and experimentation.

The provider factory makes it possible to add future providers without rewriting the migration pipeline.

---

# 🛠️ Technology Stack

### Core

* **Python**
* **C++20**
* **g++**

### AI / LLM

* **Groq**
* **Ollama**

### Application

* **Streamlit**
* **argparse**

### Engineering

* **Pytest**
* **Ruff**
* **Black**
* **python-dotenv**
* **Structured logging**
* **Custom exception hierarchy**

### Deployment

* **GitHub**
* **Streamlit Community Cloud**

---

# 📂 Project Structure

```text
AI-Code-Migration-Platform/
│
├── analyzer/
│   ├── __init__.py
│   └── python_analyzer.py
│
├── benchmark/
│   ├── __init__.py
│   └── benchmark.py
│
├── cli/
│   ├── __init__.py
│   ├── arguments.py
│   └── validators.py
│
├── compiler/
│   ├── __init__.py
│   ├── compiler.py
│   └── executor.py
│
├── evaluator/
│   ├── __init__.py
│   └── evaluator.py
│
├── leaderboard/
│   ├── __init__.py
│   ├── leaderboard_entry.py
│   ├── leaderboard_store.py
│   └── manager.py
│
├── pipeline/
│   ├── __init__.py
│   └── migration_pipeline.py
│
├── providers/
│   ├── __init__.py
│   ├── base_provider.py
│   ├── groq_provider.py
│   ├── ollama_provider.py
│   └── provider_factory.py
│
├── report/
│   ├── __init__.py
│   └── report_generator.py
│
├── translator/
│   ├── __init__.py
│   ├── prompt_builder.py
│   └── translator.py
│
├── utils/
│   ├── __init__.py
│   ├── exceptions.py
│   ├── helpers.py
│   └── logger.py
│
├── workspace/
│   ├── __init__.py
│   └── workspace_manager.py
│
├── tests/
│   ├── test_analyzer/
│   ├── test_benchmark/
│   ├── test_cli/
│   ├── test_compiler/
│   ├── test_evaluator/
│   ├── test_groq/
│   ├── test_leaderboard/
│   ├── test_pipeline/
│   ├── test_report/
│   ├── test_translator/
│   ├── test_workspace/
│   └── test_main.py
│
├── app.py
├── config.py
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

---

# ⚙️ Getting Started

## Prerequisites

Make sure the following are installed:

* Python 3.x
* Git
* g++
* An LLM provider/API key

---

## 1. Clone

```bash
git clone https://github.com/creatorKrishna05/ai-code-migration-platform.git
cd ai-code-migration-platform
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Configuration

Create a `.env` file from `.env.example`.

Example:

```env
GROQ_API_KEY=your_groq_api_key
```

For Streamlit Cloud, configure secrets through the application's deployment settings.

> **Never commit API keys or credentials to GitHub.**

---

# 💻 CLI

The platform includes a complete command-line interface.

### Basic migration

```bash
python main.py migrate examples/sample.py
```

### Select provider

```bash
python main.py migrate examples/sample.py --provider groq
```

### Select model

```bash
python main.py migrate examples/sample.py \
    --provider groq \
    --model "openai/gpt-oss-120b"
```

### Configure benchmark runs

```bash
python main.py migrate examples/sample.py --benchmark-runs 5
```

### Configure execution timeout

```bash
python main.py migrate examples/sample.py --timeout 30
```

### Generate JSON report

```bash
python main.py migrate examples/sample.py --report-json
```

---

# 🌐 Run the Web Application

Start Streamlit locally:

```bash
streamlit run app.py
```

Then open the local Streamlit URL displayed in the terminal.

---

# 📊 Benchmarking

The benchmark system executes the generated program multiple times and calculates the average runtime.

Example production verification:

```text
Benchmark runs:       5
Average execution:    0.001900 seconds
```

This provides a simple performance signal for generated C++ programs.

---

# 📄 Output Artifacts

A successful migration can generate:

```text
outputs/
├── source.cpp
├── program
├── report.json
└── leaderboard.json
```

On Windows, the compiled executable may use:

```text
program.exe
```

The exact executable name depends on the operating system.

---

# 🏆 Leaderboard

The leaderboard tracks migration results and provides a foundation for comparing migration performance.

Current local storage:

```text
outputs/leaderboard.json
```

For production-scale deployments, persistent external storage can be introduced in future iterations.

---

# 🧪 Testing & Quality

The project has a comprehensive automated test suite.

Run:

```bash
python -m pytest -q
```

### Current verification

```text
170 passed in 3.67s
```

### Coverage areas

* CLI argument parsing
* CLI validation
* Provider initialization
* Groq provider
* Ollama provider
* Translation
* Python analysis
* Compilation
* Execution
* Benchmarking
* Evaluation
* Reporting
* Leaderboard
* Workspace management
* Pipeline orchestration
* Application entry point

---

# ☁️ Production Deployment

The application is deployed on **Streamlit Community Cloud**.

### Live application

🚀 **https://ai-code-migration-platform-zievvdkcz9mr83emx2brgv.streamlit.app/**

The deployed environment has successfully completed an end-to-end migration using:

```text
Groq
  ↓
openai/gpt-oss-120b
  ↓
Python → C++20
  ↓
g++
  ↓
Executable
  ↓
5× Benchmark
  ↓
Evaluation
  ↓
Report
  ↓
Leaderboard
```

### Production verification

```text
Application startup             ✅
Dependencies                    ✅
Groq provider                   ✅
LLM generation                  ✅
Translation                     ✅
C++ compilation                 ✅
Executable execution            ✅
Benchmarking                    ✅
Evaluation                      ✅
Report generation               ✅
Output generation               ✅
Leaderboard                     ✅
End-to-end pipeline             ✅
```

---

# 🛡️ Error Handling

The platform implements centralized exception handling.

Supported failure categories include:

* CLI validation errors
* Provider errors
* Translation errors
* Compilation errors
* Execution errors
* Benchmarking errors
* Evaluation errors
* Pipeline errors

CLI exit codes:

```text
0 → Success
1 → Application / migration failure
2 → Invalid CLI input
```

---

# 📝 Logging

The application uses structured logging across the migration lifecycle.

Example:

```text
Starting migration pipeline.
Starting code translation.
Sending translation request to Groq.
Code translation completed successfully.
Starting C++ compilation.
C++ compilation completed successfully.
Execution completed with return code: 0.
Benchmark completed.
Evaluation completed successfully.
Migration report generated successfully.
Migration pipeline completed successfully.
```

---

# 🔒 Security

Generated C++ code is compiled and executed as part of the migration process.

Current safeguards include:

* Configurable execution timeout
* Temporary workspaces
* Input validation
* Structured exception handling
* Environment-based secret management
* Controlled compilation workflow

For unrestricted production workloads, additional isolation such as **containerization or sandboxed execution** is recommended.

---

# 🧭 Engineering Principles

The project is designed around several software engineering principles:

### Separation of Concerns

Each major responsibility is implemented as an independent service.

### Provider Abstraction

LLM providers implement a common interface.

### Dependency Injection

Core pipeline components are wired explicitly through the application composition layer.

### Centralized Error Handling

Application failures use a structured exception hierarchy.

### Testability

Services are independently testable through unit and integration tests.

### Observability

Important pipeline events are captured through structured logging.

### Extensibility

New providers and migration capabilities can be added without redesigning the entire system.

---

# 🚧 Roadmap

### Near Term

* [ ] Stronger execution sandboxing
* [ ] Persistent cloud leaderboard
* [ ] Improved Streamlit result dashboard
* [ ] Migration history
* [ ] Better generated-code validation
* [ ] More integration tests

### Future

* [ ] Additional LLM providers
* [ ] Containerized compilation
* [ ] Advanced performance analytics
* [ ] Parallel benchmarking
* [ ] Semantic equivalence checking
* [ ] Multi-language migration support
* [ ] Enterprise deployment architecture

---

# 🎯 Why This Project?

Traditional code migration can require significant manual effort.

This platform explores how LLMs can be integrated into a **complete software engineering workflow**, where generated code is not simply returned to the user but is:

```text
Generated
   ↓
Analyzed
   ↓
Compiled
   ↓
Executed
   ↓
Benchmarked
   ↓
Evaluated
   ↓
Reported
```

This makes the project more than an AI code-generation demo—it is an **end-to-end AI-assisted migration pipeline**.

---

# 📈 Project Status

| Area                     |     Status    |
| ------------------------ | :-----------: |
| Core architecture        |  🟢 Complete  |
| Python → C++20 migration |  🟢 Complete  |
| Groq integration         |  🟢 Complete  |
| Ollama integration       |  🟢 Complete  |
| Compiler pipeline        |  🟢 Complete  |
| Execution pipeline       |  🟢 Complete  |
| Benchmarking             |  🟢 Complete  |
| Evaluation               |  🟢 Complete  |
| Reporting                |  🟢 Complete  |
| Leaderboard              |  🟢 Complete  |
| CLI                      |  🟢 Complete  |
| Streamlit UI             |  🟢 Complete  |
| Cloud deployment         |  🟢 Complete  |
| Automated tests          | 🟢 170 passed |
| Advanced sandboxing      |   🟡 Planned  |
| Persistent cloud storage |   🟡 Planned  |

---

# 👨‍💻 Author

### Krishna

BCA Student & AI/ML Developer

GitHub:
https://github.com/creatorKrishna05

---

# 📜 License

This project is licensed under the **MIT License**.

See [`LICENSE`](LICENSE) for details.

---

# ⭐ Support the Project

If you find this project interesting or useful:

⭐ **Star the repository**

🍴 **Fork the project**

🐛 **Open an issue**

💡 **Suggest an improvement**

---

<p align="center">

### 🚀 AI Code Migration Platform

**Translate. Compile. Execute. Benchmark. Evaluate.**

<br>

<a href="https://ai-code-migration-platform-zievvdkcz9mr83emx2brgv.streamlit.app/">
  <strong>🌐 Launch Live Demo →</strong>
</a>

</p>
