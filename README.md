# Proxima Tech Smart Dashboard MVP

> An interactive, AI-powered dashboard for analyzing residency trends, demographic data, and sentiment analysis.

![Python](https://img.shields.io/badge/language-Python-blue) ![Streamlit](https://img.shields.io/badge/framework-Streamlit-red) ![Plotly](https://img.shields.io/badge/visualization-Plotly-green) ![OpenAI](https://img.shields.io/badge/AI-OpenAI-yellow)

Proxima Tech Smart Dashboard combines **Streamlit**, **Plotly**, and **OpenAI's API** to provide insights into demographic trends and immigration data, with interactive plots and AI-enhanced analysis.

---

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Code Walkthrough](#code-walkthrough)
5. [Example Outputs](#example-outputs)
6. [Project Structure](#project-structure)
7. [Contributing](#contributing)
8. [License](#license)
9. [Contact](#contact)

---

## Features

- **AI-Powered Insights**: Uses OpenAI's API to generate meaningful responses to user queries.
- **Interactive Visualizations**: Leverages Plotly to create dynamic charts (scatter plots, heatmaps, and bar charts).
- **Synthetic Data Generation**: Generates realistic datasets for trust, corruption, and policy impact analysis.
- **Custom News Feed**: Displays curated news headlines with sentiment analysis.
- **User-Friendly Interface**: Built using Streamlit for a seamless user experience.

---

## Installation

Follow these steps to set up the dashboard locally:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/velocitatem/proxima_tech.git
   cd proxima_tech
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate     # For Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables**:
   Add your OpenAI API key to a `.env` file in the project directory:
   ```bash
   OPENAI_API_KEY=your_openai_api_key
   ```

5. **Run the Application**:
   ```bash
   streamlit run main.py
   ```

---

## Usage

1. Launch the dashboard and use the sidebar to enter your query.
2. View AI-generated answers, interactive charts, and curated news.
3. Explore synthetic data visualizations like:
   - Trust in Government vs. Corruption Perception
   - Policy Impact Score vs. Sentiment Analysis

---

## Code Walkthrough

- **`main.py`**: Entry point for the Streamlit application.
- **`generate_data()`**: Creates a synthetic dataset with demographic and trust metrics.
- **`get_data()`**: Fetches AI-generated insights from OpenAI's API and caches results.
- **`extract_data()`**: Extracts CSV-formatted responses for plotting.
- **`generate_plot()`**: Creates visualizations dynamically based on the data.
- **`NEWS`**: Static news data with sentiment scores for display.

---

## Example Outputs

### **Trust in Government vs Corruption**
![Scatter Plot Example](https://via.placeholder.com/600x300.png?text=Example+Scatter+Plot)

### **News Feed**
- *"Venezuelan residents in Spain increased by 46% this year, reaching 140,214 approvals."* ✅
- *"There was a significant 75% decrease in residency approvals for Ukrainians."* ❌

### **Dynamic Plots**
User queries like *"What is the demographic distribution of immigrants?"* produce real-time visualizations.

---

## Project Structure

```plaintext
proxima_tech/
├── main.py                  # Streamlit dashboard entry point
├── cache.json               # Local cache for API responses
├── requirements.txt         # Project dependencies
├── .env                     # OpenAI API Key
└── README.md                # Project documentation
```

---

## Contributing

We welcome contributions! Follow these steps:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/my-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add my feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/my-feature
   ```
5. Open a pull request on GitHub.

---

---

**Proxima Tech Smart Dashboard** — Empowering data-driven decisions with AI-powered visualizations 🚀.
