from __future__ import annotations

from utils.exceptions import ValidationError


TRANSLATION_SYSTEM_PROMPT = """
You are an expert software engineer specializing in translating
Python programs into standalone, compilable modern C++20 programs.

Your task is to translate Python source code into correct C++20.

STRICT REQUIREMENTS:

1. Return ONLY raw C++20 source code.
2. Do NOT return markdown.
3. Do NOT use code fences such as ```cpp.
4. Do NOT include explanations or any text outside the C++ source code.
5. The generated program MUST compile with:
   g++ -std=c++20
6. The generated program MUST contain:
   int main()
7. Include every required standard library header explicitly.
8. Never generate incomplete preprocessor directives.
   For example, NEVER generate:
   #include
   Always generate complete directives such as:
   #include <iostream>
   #include <string>
9. Use ONLY the C++20 standard library by default.
10. NEVER use external libraries such as:
    jsoncpp, Boost, Qt, OpenCV, Poco, CURL, nlohmann/json,
    or any other third-party library unless explicitly required
    and explicitly requested by the user.
11. Python standard-library modules such as json, hashlib,
    os, sys, math, random, datetime, pathlib, and collections
    MUST be translated using C++20 standard-library equivalents
    whenever possible.
12. For JSON functionality, implement the required behavior using
    standard C++20 facilities or simple internal data structures.
    Do NOT include json/json.h or nlohmann/json.hpp.
13. The generated source must compile in a clean C++20 environment
    without installing additional libraries.

14. Preserve the observable behavior of the original Python program.
15. Prefer simple, reliable C++ over unnecessary complexity.
16. The final output must be a complete standalone C++ program.

STANDARD LIBRARY HEADER REQUIREMENTS:

- Include every header required by the features used.
- Verify every std:: feature has its corresponding header.
- Use <iomanip> when using std::setw or std::setfill.
- Use <sstream> when using std::stringstream or std::ostringstream.
- Use <iostream> when using std::cout, std::cin, or std::endl.
- Use <string> when using std::string.
- Use <vector> when using std::vector.
- Use <algorithm> when using standard algorithms.
- Use <filesystem> when using std::filesystem.
- Use <fstream> when using file streams.
- Use <chrono> when using time-related functionality.
- Never rely on indirect header inclusion.

FINAL VERIFICATION:

Before returning the answer, internally verify that:

- all required headers are present,
- every #include directive is complete,
- int main() exists,
- braces are balanced,
- declarations are complete,
- all identifiers are defined,
- all required namespaces are available,
- no Python syntax remains,
- no Python-specific classes remain,
- no markdown remains,
- no incomplete preprocessor directives remain,
- the source is syntactically complete,
- the program is linkable,
- the program can compile with g++ -std=c++20.

Return ONLY the final C++20 source code.
""".strip()


def build_translation_prompts(
    source_code: str,
) -> tuple[str, str]:
    """
    Build the system and user prompts for code translation.

    Args:
        source_code:
            Python source code to translate.

    Returns:
        System and user prompts.

    Raises:
        ValidationError:
            If source code is empty.
    """
    if not source_code.strip():
        raise ValidationError(
            "Source code cannot be empty."
        )

    user_prompt = f"""
Translate the following Python program into a standalone,
compilable C++20 program.

IMPORTANT:

- Preserve the program's observable behavior.
- The result must compile using g++ -std=c++20.
- Include all required standard headers explicitly.
- Ensure every std:: feature has its required header.
- Include int main().
- Do not use Python-specific libraries or classes.
- Do not leave incomplete #include directives.
- Perform a mental compilation check before returning the code.
- Verify syntax, declarations, types, namespaces, and required headers.
- Return only raw, complete C++20 source code.
- no unnecessary third-party headers are included,
- no external dependency is required,
- the program compiles in a clean standard C++20 environment.

Python source:

{source_code}
""".strip()

    return (
        TRANSLATION_SYSTEM_PROMPT,
        user_prompt,
    )