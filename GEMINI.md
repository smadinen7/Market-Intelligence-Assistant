'''# GEMINI.md - CEO AI Assistant

## Project Overview

This project is a Streamlit web application called "CEO AI Assistant". It is designed to be a financial intelligence platform for executives, investors, and analysts. The application provides two main workflows:

1.  **Internal Analysis:** Users can upload their own financial documents (PDFs, CSVs, etc.) for analysis. The application will extract key metrics, provide a summary, and allow the user to ask questions about the document.

2.  **Market Analysis:** Users can research public companies by name. The application will provide a comprehensive analysis of the company, including its business model, financial performance, and competitive position.

The application is built using Python and leverages the following key technologies:

*   **Frontend:** Streamlit
*   **AI Framework:** CrewAI
*   **Large Language Models (LLMs):** Google Gemini and Groq Llama
*   **Core Libraries:** pandas, PyPDF, python-dotenv

### Architecture

The application follows a multi-agent AI architecture, where different AI agents with specialized roles collaborate to perform financial analysis tasks. The main components of the architecture are:

*   **`Home.py`:** The main entry point of the Streamlit application.
*   **`pages/`:** Contains the different pages of the application, corresponding to the two main workflows.
*   **`financial_agents.py`:** Defines the different AI agents used in the application.
*   **`financial_tasks.py`:** Defines the tasks that the AI agents can perform.
*   **`utils.py`:** Contains utility functions, including the `CentralMemory` class for managing the application's state.

## Building and Running

To build and run this project, you will need to have Python 3.11 and `pip` installed. You will also need to get API keys from Google AI Studio and GroqCloud.

1.  **Clone the repository:**

    ```sh
    git clone <repository-url>
    cd ceo-ai-assistant
    ```

2.  **Create and activate a virtual environment:**

    ```sh
    python3.11 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**

    Create a file named `.env` in the root of your project directory and add your API keys:

    ```env
    GEMINI_API_KEY="your_google_api_key_here"
    GROQ_API_KEY="your_groq_api_key_here"
    ```

5.  **Run the application:**

    ```sh
    streamlit run Home.py
    ```

## Development Conventions

*   **Code Style:** The code follows the standard PEP 8 style guide for Python.
*   **Modularity:** The application is organized into modules with clear responsibilities (e.g., `financial_agents.py`, `financial_tasks.py`, `utils.py`).
*   **Object-Oriented Programming:** The `CentralMemory` class is used to manage the application's state in an object-oriented way.
*   **Session Management:** Streamlit's `session_state` is used to maintain the application's state between user interactions.
*   **AI Agents:** The CrewAI framework is used to create and manage the AI agents.
'''