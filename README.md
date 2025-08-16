# Project Overview

The primary objective of this project is to analyze Spotify public data by building a fully automated serverless data pipeline using AWS services. This is a lightweight solution designed for cost-effectiveness and relatively low volumes of data

Using a simple Python script which is executed and scheduled using AWS Lambda + Eventbridge, the Spotify API can be consumed and the resulting JSON responses are stored in an S3 bucket, this process is executed on a daily basis and separated directories are created per day, containing data about the 20 most followed artists in Spotify which is then cleaned, transformed and queried using Athena (SQL) for analytics and insights.

## Tech Stack
* Python: Consumption of the Spotify API , file uploads to S3
* Lambda + Eventbridge: Execution and daily scheduling of the Python script
* S3: Storage of raw unprocessed data (bronze layer)
* Athena: Data cleanup, analytics and business intelligence.

## Architecture Diagram

<img width="500" height="470" alt="Architecture Diagram drawio" src="https://github.com/user-attachments/assets/b5b718a0-4301-47d3-b148-481ab35f2da1" />
