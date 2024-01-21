# Tweet Timelapse Generator

## Overview

This project aims to create a timelapse video by capturing daily changes in a user's tweets. The process involves scraping daily tweets, summarizing them using a Large Language Model (LLM), and generating images based on them using a Stable Diffusion Framework (Deforum).

## Installation

Clone the repository:

   ```bash
   git clone https://github.com/ataberkasar/sec199-term-project.git
   cd .\sec199-term-project\
   ```

Install dependencies:

```bash
   pip install -r requirements.txt
```

## Usage

```bash
   python main.py elonmusk
```
This will scrape the latest tweets of [@elonmusk](https://twitter.com/elonmusk), create llm_prompts.txt, and provide instructions for the next steps.
You should manually input the prompts from llm_prompts.txt into your LLM (e.g., ChatGPT) and copy-paste the generated summaries into llm_outputs.txt.
Continue to generate deforum_prompts.txt based on the LLM outputs.

Note: The instructions on how to use Stable Diffusion or Deforum are currently out of scope of this project; however, simple guidelines for their usage will be provided in future updates.
