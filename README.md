# OWASPShield

## Project Overview
OWASPShield is a beginner-friendly cybersecurity awareness and security assistance project designed to help users understand common web application security risks.

## Product
A cybersecurity assistant that provides information about common web security vulnerabilities and basic security checks.

## Target User
Students, beginner developers, and individuals interested in learning web application security.

## Problem
Many beginners are unaware of common web application vulnerabilities and struggle to understand how to identify basic security risks.

## Data Source
OWASP Top 10 documentation and manually prepared sample security questions and rules.

## Project Goal
To make basic web security knowledge easier to understand through a simple Python-based interactive application.


## How to Run

### 1. Activate virtual environment

```bash
source .venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Start the FastAPI server

```bash
uvicorn app.main:app --reload
```

### 4. Open API documentation

Visit: http://127.0.0.1:8000/docs

### 5. Run data analysis

```bash
python -m analysis.explore
```

### 6. Run smart search

```bash
python -m app.smart_search
```
