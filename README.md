# Patent Maintenance Management Platform

Django-based web application for processing patent maintenance datasets, calculating jurisdiction-specific maintenance fees, and generating structured portfolio reports.

The platform integrates automated calculation workflows, Excel-based reporting utilities, portfolio analytics, and AI-assisted categorization features into a centralized internal management system.

## Features

- Patent maintenance fee calculation workflows
- Multi-jurisdiction fee processing
- Excel import/export utilities
- Portfolio overview and reporting generation
- AI-assisted categorization and prompt workflows
- User authentication and activity tracking
- Structured dataset processing and normalization
- Django admin integration
- Automated report generation

## Tech Stack

- Python
- Django
- PostgreSQL / SQLite
- pandas
- openpyxl
- HTML/CSS
- Excel/VBA workflows

## Architecture

```text
Patent Dataset Upload
          ↓
Validation & Processing
          ↓
Maintenance Fee Calculation
          ↓
Portfolio Analysis & Categorization
          ↓
Excel Report Generation
          ↓
Stored Results & User Access
```

## Project Structure

```text
Patent Maintenance Management/
│
├── calculator/
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   ├── 0002_calculationresult.py
│   │   ├── 0003_rename_uploaded_at_calculationresult_created_at_and_more.py
│   │   ├── 0004_alter_calculationresult_file_path.py
│   │   ├── 0005_calculationresult_custom_name.py
│   │   ├── 0006_customprompt_gptprompthistory.py
│   │   ├── 0007_gptresult_delete_customprompt_and_more.py
│   │   ├── 0008_delete_calculation_gptresult_created_by.py
│   │   ├── 0009_calculationresult_created_by.py
│   │   └── __init__.py
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── Calculate.html
│   │   ├── feesdollars.html
│   │   ├── gpt.html
│   │   ├── home.html
│   │   ├── login.html
│   │   └── logout.html
│   │
│   ├── services/
│   │   ├── calculation.py
│   │   ├── excel_utils.py
│   │   ├── exceptions.py
│   │   ├── locate.py
│   │   ├── overview.py
│   │   ├── remaininglife.py
│   │   └── total.py
│   │
│   ├── fees_reader/
│   │   ├── config.json
│   │   ├── exceptions.py
│   │   ├── fees_reader.py
│   │   ├── main.py
│   │   └── operations.py
│   │
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── core/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── static/
│   └── styles1.css
│
├── manage.py
├── requirements.txt
├── README.md
└── .gitattributes
```
## Key Components

- Maintenance fee calculation engine
- Portfolio overview generation
- Remaining patent life analysis
- Excel reporting utilities
- AI-assisted categorization workflows
- User authentication and tracking
- Dataset normalization and processing

## Notes

Designed for patent portfolio maintenance workflows involving large structured datasets, automated fee calculations, reporting pipelines, and internal operational tooling.
