# 🚀 AI Code Migration Platform

> **AI-powered Python → Modern C++20 code migration, compilation, benchmarking, evaluation, and model performance comparison.**

## 📌 Overview

**AI Code Migration Platform** is an end-to-end LLM engineering platform that converts Python source code into optimized **Modern C++20** using configurable LLM providers.

The platform goes beyond simple translation. Generated C++ code is automatically:

* Compiled with a C++20 compiler
* Executed and validated
* Benchmarked across multiple runs
* Evaluated for migration success
* Stored as a migration report
* Added to a persistent model/provider leaderboard

The platform currently supports both **Groq cloud models** and **Ollama local models**.

---

## ✨ Features

* 🐍 Python → Modern C++20 translation
* 🤖 Multi-provider LLM architecture
* ⚡ Groq API support
* 🦙 Ollama local LLM support
* 🔌 Provider/model abstraction
* 🛠️ Automatic C++20 compilation
* ▶️ Generated executable execution
* 📊 Runtime benchmarking
* 🧠 Migration evaluation
* 📄 JSON migration reports
* 💻 Generated C++ source viewer
* ⬇️ Download generated C++ source
* 🏆 Persistent model/provider leaderboard
* 🧹 Temporary workspace cleanup
* 🖥️ Streamlit web interface
* 💻 Production-style CLI
* 🧪 Automated regression test suite
* 🔐 Environment-based API key management
* ⚙️ Centralized application configuration

---

## 🏗️ Architecture


                    Python Source
                         │
                         ▼
                  ┌─────────────┐
                  │ CLI / UI    │
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │  Provider   │
                  │   Factory   │
                  └──────┬──────┘
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
          ┌────────┐            ┌────────┐
          │  Groq  │            │ Ollama │
          └────┬───┘            └────┬───┘
               └──────────┬──────────┘
                          ▼
                  ┌─────────────┐
                  │ Translator  │
                  └──────┬──────┘
                         │
                         ▼
                    Modern C++20
                         │
                         ▼
                  ┌─────────────┐
                  │   Compiler  │
                  └──────┬──────┘
                         │
                         ▼
                    Executable
                         │
                         ▼
                  ┌─────────────┐
                  │  Executor   │
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │  Benchmark  │
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │  Evaluator  │
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │    Report   │
                  └──────┬──────┘
                         │
                ┌────────┴────────┐
                ▼                 ▼
         Output Manager       Leaderboard
                │                 │
                └────────┬────────┘
                         ▼
                  Streamlit UI


---

## 🤖 Supported Providers

### ⚡ Groq

Groq is the default cloud provider.

**Default model:**


llama-3.3-70b-versatile


Supported models registered in the platform include:

llama-3.3-70b-versatile
deepseek-r1-distill-llama-70b
qwen/qwen3-32b


### 🦙 Ollama

Ollama provides local model execution without requiring a cloud API.

Currently tested successfully with:


llama3.2


The installed Ollama model may appear as:


llama3.2:latest

The application internally resolves the configured migration model to:

llama3.2


Example:

ollama list

The `nomic-embed-text` model is an embedding model and is **not used for code migration**.

---

## 🧰 Technology Stack

| Component       | Technology                                |
| --------------- | ----------------------------------------- |
| Language        | Python                                    |
| Target Language | Modern C++20                              |
| Cloud LLM       | Groq                                      |
| Local LLM       | Ollama                                    |
| Web UI          | Streamlit                                 |
| Compiler        | g++                                       |
| Testing         | Pytest                                    |
| Persistence     | JSON                                      |
| Configuration   | Environment variables / Streamlit secrets |
| Architecture    | Modular Service Architecture              |

---

## 📁 Project Structure


AI-Code-Migration-Platform/
│
├── analyzer/
│   └── python_analyzer.py
│
├── benchmark/
│   └── benchmark.py
│
├── cli/
│   ├── arguments.py
│   └── validators.py
│
├── compiler/
│   ├── compiler.py
│   └── executor.py
│
├── evaluator/
│   └── evaluator.py
│
├── leaderboard/
│   ├── leaderboard.py
│   ├── leaderboard_entry.py
│   ├── leaderboard_store.py
│   └── manager.py
│
├── outputs/
│   └── output_manager.py
│
├── pipeline/
│   └── migration_pipeline.py
│
├── providers/
│   ├── groq/
│   ├── ollama/
│   ├── base_provider.py
│   └── provider_factory.py
│
├── report/
│   └── report_generator.py
│
├── translator/
│   ├── prompt_builder.py
│   └── translator.py
│
├── utils/
│   ├── exceptions.py
│   ├── logger.py
│   └── helpers.py
│
├── workspace/
│   └── workspace_manager.py
│
├── tests/
│
├── app.py
├── main.py
├── config.py
├── requirements.txt
└── README.md


---

# 🚀 Getting Started

## 1. Clone the Repository


git clone <YOUR_GITHUB_REPOSITORY_URL>
cd AI-Code-Migration-Platform


## 2. Create a Virtual Environment

python -m venv .venv


Activate on Windows:

.venv\Scripts\activate

## 3. Install Dependencies


pip install -r requirements.txt


---

## 4. Configure Environment Variables

Create a `.env` file:


GROQ_API_KEY=your_groq_api_key
OLLAMA_BASE_URL=http://localhost:11434


Never commit `.env` or API keys to GitHub.

---

# ⚡ Groq Setup

Set your Groq API key in `.env`:


GROQ_API_KEY=your_groq_api_key

The default provider is:

groq

The default model is:


llama-3.3-70b-versatile

---

# 🦙 Ollama Setup

Install Ollama and make sure the Ollama service is running.

Verify installed models:


ollama list


Example:

NAME
llama3.2:latest
nomic-embed-text:latest


For migration, use:

llama3.2

Example CLI migration:


python main.py migrate examples/sample.py --provider ollama --report-json


Ollama migration has been successfully verified end-to-end.

---

# 💻 CLI Usage

The platform provides a production-style command-line interface.

## Default Migration


python main.py migrate examples/sample.py


## Generate JSON Report

python main.py migrate examples/sample.py --report-json


## Specify Provider


python main.py migrate examples/sample.py --provider groq --report-json


## Specify Provider and Model


python main.py migrate examples/sample.py \
    --provider groq \
    --model llama-3.3-70b-versatile \
    --report-json


Ollama:

python main.py migrate examples/sample.py \
    --provider ollama \
    --report-json

The CLI automatically resolves the default model registered for the selected provider.

---

# 🔄 Migration Pipeline


Python Source
      ↓
CLI Validation
      ↓
Provider Factory
      ↓
LLM Provider
      ↓
Translation
      ↓
C++20 Compilation
      ↓
Executable Execution
      ↓
Benchmarking
      ↓
Evaluation
      ↓
Migration Report
      ↓
Output Persistence
      ↓
Leaderboard


---

# 🖥️ Streamlit Application

Run:


streamlit run app.py


The application provides:

* Provider selection
* Model selection
* Python file upload
* Migration execution
* Translation status
* Compilation status
* Execution status
* Benchmark results
* Program output
* Generated C++20 source viewer
* C++ source download
* Migration report download
* Model/provider leaderboard

### Application Flow

1. Select an LLM provider.
2. Select the provider-specific model.
3. Upload a Python `.py` file.
4. Click **Migrate Code**.
5. The platform translates Python into C++20.
6. Generated C++ is compiled.
7. The executable is executed.
8. Runtime performance is benchmarked.
9. The migration is evaluated.
10. A migration report is generated.
11. Results are stored in the leaderboard.
12. Generated artifacts become available for download.

---

# 🧪 Testing

Run the complete test suite:

python -m pytest -q

### Current Test Status


170 passed

Latest verified result:

170 passed in 3.18s


The project maintains automated tests across CLI validation, providers, translation, compilation, execution, benchmarking, evaluation, reporting, leaderboard functionality, and pipeline behavior.

---

# ✅ End-to-End Verification

The complete migration pipeline has been successfully verified using:


python main.py migrate examples/sample.py --report-json


Verified stages:

Translation      ✅
Compilation      ✅
Execution        ✅
Benchmarking     ✅
Evaluation       ✅
Report Generation ✅
Output Persistence ✅
Leaderboard       ✅
Workspace Cleanup ✅


Example result:


Provider: groq
Model: llama-3.3-70b-versatile
Translation: SUCCESS
Compilation: SUCCESS
Execution: SUCCESS
Benchmark: ~0.03 seconds
Output: 30

A more complex migration example has also been successfully tested:


python main.py migrate examples/complex_sample.py --report-json


Verified output:


Output: 60


Ollama has also been successfully verified:


python main.py migrate examples/sample.py --provider ollama --report-json


Verified:


Provider: ollama
Model: llama3.2
Translation: SUCCESS
Compilation: SUCCESS
Execution: SUCCESS
Output: 30

---

# 🏆 Leaderboard

Successful migrations can be recorded with:

* Provider
* Model
* Benchmark time
* Execution time
* Overall success

Results are persisted to:


outputs/leaderboard.json


Successful migrations are ranked ahead of failed migrations, with faster benchmark results receiving better rankings.

---

# 📊 Migration Outputs

After a successful migration, the platform generates:


outputs/
├── source.cpp
├── program.exe
├── report.json
└── leaderboard.json

### Generated C++ Source

The generated Modern C++20 source can be viewed and downloaded.

### Executable

The compiled executable is saved as:


outputs/program.exe


### Migration Report

JSON migration results are saved as:


outputs/report.json

The report contains migration status and performance information.

---

# ⚙️ Configuration

Central configuration is maintained in:


config.py


Configuration includes:

* Application metadata
* Provider registry
* Model registry
* API keys
* Ollama URL
* Compiler configuration
* C++20 standard
* Optimization flags
* Benchmark runs
* Execution timeout
* Supported file extensions
* Runtime directories

Example:


Default Provider: groq
Default Model: llama-3.3-70b-versatile
C++ Standard: c++20
Optimization: -O3
Benchmark Runs: 5
Execution Timeout: 10 seconds


---

# 🧠 Engineering Principles

The project follows:

* **Single Responsibility Principle (SRP)**
* **Single Source of Truth (SSOT)**
* **Loose Coupling**
* Dependency Injection
* Modular Service Boundaries
* Centralized Configuration
* Structured Logging
* Explicit Exception Handling
* Temporary Workspace Isolation
* Automated Testing
* Separation of Backend and UI
* Provider Abstraction

---

# 🔐 Security

* API keys are loaded through environment variables or Streamlit secrets.
* `.env` files must never be committed.
* Provider credentials are not included in migration reports.
* Compilation uses isolated temporary workspaces.
* Temporary workspaces are cleaned after migration.
* Generated code should be reviewed before executing untrusted source.
* Production deployments should use additional sandboxing for untrusted code execution.

---

# 🎯 Project Goal   

The long-term goal is to build a production-ready AI code migration platform capable of comparing multiple LLM providers and models on real-world code migration workloads.

The architecture is designed so additional providers can be introduced without changing the core migration pipeline.

---

# 🔮 Future Improvements

* Additional LLM providers
* More migration quality metrics
* Advanced semantic evaluation
* Aggregated model leaderboard
* Historical benchmark analytics
* Side-by-side Python/C++ comparison
* Large repository/project migration
* Dockerized execution
* Cloud deployment
* Authentication
* User workspaces
* Advanced evaluation datasets
* Model cost/performance comparison
* Secure sandboxed code execution

---

# 📸 Interface

The Streamlit dashboard provides:

* Provider/model configuration
* Python source upload
* Migration execution
* Migration status
* Performance metrics
* Program output
* Generated C++20 code
* Downloadable artifacts
* Model leaderboard

---

# 📈 Current Development Status

| Component                | Status       |
| ------------------------ | ------------ |
| Python → C++20           | ✅            |
| Groq Provider            | ✅            |
| Ollama Provider          | ✅            |
| Provider Factory         | ✅            |
| Model Registry           | ✅            |
| CLI                      | ✅            |
| CLI Validation           | ✅            |
| C++20 Compilation        | ✅            |
| Execution                | ✅            |
| Benchmarking             | ✅            |
| Evaluation               | ✅            |
| Report Generation        | ✅            |
| Leaderboard Backend      | ✅            |
| Leaderboard UI           | ✅            |
| C++ Code Viewer          | ✅            |
| Artifact Downloads       | ✅            |
| Temporary Cleanup        | ✅            |
| Streamlit Application    | ✅            |
| Automated Tests          | ✅ 170 passed |
| Groq E2E Migration       | ✅            |
| Ollama E2E Migration     | ✅            |
| Complex Sample Migration | ✅            |

### Overall Status

**Production-ready core migration pipeline + Streamlit interface**

---

## 📄 License

Add the project's license information before public distribution.
