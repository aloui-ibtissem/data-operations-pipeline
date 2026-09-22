# Data Operations Pipeline

End-to-end data engineering pipeline for ingesting, transforming,
validating and serving trusted business data.

## Project status

 In development

## Technology stack

- Python
- SQL
- DuckDB
- dbt
- Pandas
- PyArrow
- Pytest

## Architecture

The project implements a reproducible modern data pipeline covering:

1. Data ingestion
2. Raw data storage
3. Data quality validation
4. Data transformation
5. Data modelling
6. Analytics-ready datasets
7. Automated testing and CI

## Production architecture

The local implementation is designed to be portable to an AWS-based
data platform using services such as Amazon S3, AWS Glue and Amazon
Athena.

## Repository structure

```text
data-operations-pipeline/
├── data/
├── src/
├── dbt_project/
├── sql/
├── tests/
├── docs/
└── .github/

