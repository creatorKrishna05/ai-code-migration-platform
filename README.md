# 🚀 AI Code Migration Platform

> **AI-powered Python → Modern C++20 code migration, compilation,
> benchmarking, evaluation, and model performance comparison.**

## 📌 Overview

AI Code Migration Platform is an end-to-end LLM engineering project that
converts Python source code into optimized **Modern C++20** using
configurable LLM providers.

The platform does more than code translation. It validates the generated
C++ code by compiling and executing it, benchmarks runtime performance,
evaluates the migration result, generates a migration report, and stores
results in a persistent leaderboard.

## ✨ Features

-   🐍 Python → Modern C++20 translation
-   🤖 Multi-provider LLM architecture
-   ⚡ Groq support
-   🦙 Ollama support
-   🔌 Provider/model abstraction
-   🛠️ Automatic C++ compilation
-   ▶️ Generated executable execution
-   📊 Runtime benchmarking
-   🧠 Migration evaluation
-   📄 JSON migration reports
-   💻 Generated C++ source viewer
-   ⬇️ Download generated `source.cpp`
-   🏆 Persistent model/provider leaderboard
-   🧹 Temporary workspace cleanup
-   🖥️ Streamlit web interface
-   🧪 Comprehensive automated test suite

## 🏗️ Architecture


                 Python Source
                       │
                       ▼
                 ┌────────────┐
                 │ Translator │
                 └─────┬──────┘
                       │
                       ▼
                 Modern C++20
                       │
                       ▼
                 ┌────────────┐
                 │  Compiler  │
                 └─────┬──────┘
                       │
                       ▼
                  Executable
                       │
                       ▼
                 ┌────────────┐
                 │ Benchmark  │
                 └─────┬──────┘
                       │
                       ▼
                 ┌────────────┐
                 │ Evaluator  │
                 └─────┬──────┘
                       │
                       ▼
                Migration Report
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
       Output Manager        Leaderboard
             │                   │
             └─────────┬─────────┘
                       ▼
                 Streamlit UI


## 🤖 Supported Providers

### Groq

Default provider:


groq


Default model:


llama-3.3-70b-versatile


### Ollama

Local Ollama support:

ollama


Example migration model:

llama3.2:latest


> `nomic-embed-text` is an embedding model and is not used for code
> migration.

## 🧰 Technology Stack

  Component         Technology
  ----------------- ----------------------------
  Language          Python
  Target Language   Modern C++20
  LLM Provider      Groq
  Local LLM         Ollama
  Web UI            Streamlit
  Compiler          C++ compiler
  Testing           Pytest
  Persistence       JSON
  Logging           Python logging
  Architecture      Modular / Service-oriented

## 📁 Project Structure


AI-Code-Migration-Platform/
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
│   └── leaderboard_store.py
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
│   └── provider_factory.py
│
├── report/
│   └── report_generator.py
│
├── translator/
│   └── translator.py
│
├── utils/
│   ├── exceptions.py
│   ├── logger.py
│   └── ...
│
├── workspace/
│   └── workspace_manager.py
│
├── app.py
├── main.py
├── config.py
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

### 1. Clone the repository


git clone <YOUR_GITHUB_REPOSITORY_URL>
cd AI-Code-Migration-Platform


### 2. Create a virtual environment

python -m venv .venv


Activate it on Windows:

.venv\Scripts\activate


### 3. Install dependencies

pip install -r requirements.txt

### 4. Configure environment variables

Create a `.env` file:


GROQ_API_KEY=your_groq_api_key
OLLAMA_BASE_URL=http://localhost:11434


Do not commit `.env` or API keys to GitHub.

## 🦙 Ollama Setup

Install and start Ollama, then pull a supported local model:


ollama pull llama3.2


Verify installed models:

ollama list


The application should use:

llama3.2:latest

for Ollama migration.

## ▶️ Run the Streamlit Application


streamlit run app.py


Then open the local Streamlit URL shown in the terminal.

### Application Flow

1.  Select an LLM provider.
2.  Select the provider-specific model.
3.  Upload a Python `.py` file.
4.  Click **Migrate Code**.
5.  The platform translates the Python source into C++20.
6.  The generated C++ is compiled.
7.  The executable is run.
8.  Runtime performance is benchmarked.
9.  The migration result is evaluated.
10. A report and leaderboard entry are generated.
11. Generated C++ and migration report can be downloaded.

## 💻 CLI Usage

The platform also supports the migration pipeline through the CLI.

Example:


python main.py migrate path/to/source.py


Provider/model options can be supplied according to the CLI arguments
supported by the project.

## 🧪 Testing

Run the complete test suite:


python -m pytest -q


Current project status:


152 tests passed


The project is developed with a strong focus on regression safety and
modular testing.

## 🏆 Leaderboard

Every successful migration can be recorded with:

-   Provider
-   Model
-   Benchmark time
-   Execution time
-   Overall success

Results are persisted to:


outputs/leaderboard.json


Successful migrations are ranked before failed migrations, and lower
benchmark time receives a better ranking.

## 📊 Migration Outputs

The Streamlit interface provides:

### Migration Status

-   Translation
-   Compilation
-   Execution

### Performance

-   Benchmark time
-   Execution time

### Program Output

Output produced by the generated C++ executable.

### Generated Source

The generated Modern C++20 source code can be viewed directly in the
application and downloaded as:


source.cpp


### Migration Report

The migration report can be downloaded as:


migration_report.json


## 🧠 Engineering Principles

The project follows:

-   **Single Responsibility Principle (SRP)**
-   **Single Source of Truth (SSOT)**
-   **Loose Coupling**
-   Dependency injection where appropriate
-   Modular service boundaries
-   Centralized configuration
-   Structured logging
-   Explicit exception handling
-   Temporary workspace isolation
-   Automated testing
-   Clean separation between backend and UI

## 🔄 End-to-End Pipeline

Upload Python
     ↓
Provider Selection
     ↓
LLM Translation
     ↓
C++20 Validation
     ↓
Compilation
     ↓
Execution
     ↓
Benchmarking
     ↓
Evaluation
     ↓
Report Generation
     ↓
Output Persistence
     ↓
Leaderboard Update

## 🎯 Project Goal

The long-term goal is to build a production-ready AI code migration
platform capable of comparing multiple LLM providers and models on real
code migration workloads.

Future provider/model support can include additional commercial and
open-source LLMs without changing the core migration pipeline.

## 🔮 Future Improvements

-   Additional LLM providers
-   More migration quality metrics
-   Aggregated model leaderboard
-   Historical benchmark analytics
-   Side-by-side Python/C++ comparison
-   Larger project/repository migration
-   Dockerized deployment
-   Cloud deployment
-   Authentication and user workspaces
-   Advanced evaluation datasets
-   Model cost/performance comparison

## 📸 Interface

The Streamlit interface provides a clean dashboard for:

-   Provider/model configuration
-   Python source upload
-   Migration execution
-   Migration status
-   Performance metrics
-   Program output
-   Generated C++20 code
-   Downloadable artifacts
-   Model leaderboard

## 🔐 Security

-   Keep API keys in environment variables.
-   Never commit `.env` files.
-   Do not expose provider credentials in generated reports.
-   Use temporary workspaces for compilation/execution artifacts.
-   Review generated code before executing untrusted source in
    production environments.

## 👨‍💻 Development Status

**Current status: Production-ready core pipeline + Streamlit interface**


Python → C++20              ✅
Groq                       ✅
Ollama                     ✅
Compilation                ✅
Execution                  ✅
Benchmarking               ✅
Evaluation                 ✅
Report Generation          ✅
Leaderboard Backend        ✅
Leaderboard UI             ✅
C++ Code Viewer            ✅
Artifact Downloads         ✅
Temporary Cleanup          ✅
Streamlit Application      ✅
Automated Tests            ✅ 152 passed


------------------------------------------------------------------------

## 📄 License

Add the project's license information here before public distribution.
