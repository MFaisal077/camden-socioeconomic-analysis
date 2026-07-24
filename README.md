# Camden Socioeconomic Analysis

An end-to-end data engineering and analytics MVP developed for **Sprault** to identify and visualise financial vulnerability across the London Borough of Camden using multiple public-sector datasets.

---

## Overview

This project consolidates fragmented socioeconomic datasets into a unified analytical platform to support evidence-based decision making.

The system automates data ingestion, cleaning, storage, modelling and visualisation, enabling policymakers and stakeholders to identify areas experiencing financial hardship and understand the underlying drivers.

Current indicators include:

- Universal Credit claimant data
- Employment status of claimants
- Council Tax Support
- Emergency Food Parcel distribution (Trussell Trust)

---

## Objectives

The primary objective is to transform publicly available datasets into actionable insights by:

- Identifying concentrations of financial vulnerability
- Highlighting areas experiencing in-work poverty
- Comparing local hardship indicators
- Supporting targeted policy interventions
- Providing interactive dashboards for stakeholders

---

## Architecture

```
                 Public Datasets
                       │
      ┌────────────────┼────────────────┐
      │                │                │
Universal Credit   Council Tax     Food Bank Data
                       │
                Python ETL Pipeline
                       │
                 PostgreSQL Database
                       │
          SQL Views & Business Logic
                       │
      ┌────────────────┴───────────────┐
      │                                │
   Power BI Dashboard         Streamlit Dashboard
```

---

## Technology Stack

| Component | Technology |
|----------|------------|
| Programming | Python |
| Database | PostgreSQL |
| Query Language | SQL |
| Data Processing | Pandas |
| Dashboarding | Power BI |
| Web Application | Streamlit |
| Version Control | Git & GitHub |

---

## Repository Structure

```
analysis/
│
├── notebooks and exploratory analysis

output/
│
├── exported reports
├── processed datasets

sql/
│
├── database schema
├── SQL views
├── analytical queries

src/
│
├── ETL pipeline
├── database utilities
├── data cleaning
├── analysis modules

README.md

requirements.txt
```

---

## Current Features

- Automated ETL pipeline
- PostgreSQL relational database
- SQL analytical views
- Universal Credit analysis
- Working Poor calculations
- Council Tax Support analysis
- Emergency Food Parcel analysis
- Interactive Power BI dashboard
- Streamlit web dashboard

---

## Key Insights

Current analysis demonstrates that:

- Financial vulnerability exists even within relatively affluent boroughs.
- Significant numbers of Universal Credit claimants remain in employment.
- Multiple socioeconomic indicators provide a more complete picture of hardship than any individual dataset.
- Geographic variation across wards enables targeted intervention strategies.

---

## Dashboard Preview

*(Add screenshots here)*

### Financial Vulnerability Dashboard

![Dashboard](docs/dashboard.png)

---

## Future Development

Planned work includes:

- Additional socioeconomic datasets
- Financial Vulnerability Index
- Predictive modelling
- Temporal trend analysis
- Automated reporting
- API integration
- Expanded dashboard functionality

---

## Status

🚧 **This repository represents an active MVP under development.**

The architecture, datasets, and analytical models continue to evolve as new functionality is implemented.

---

## Author

Muhammad Faisal

Developed for **Sprault** as part of the Financial Vulnerability MVP.
