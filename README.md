# Building a Simple Serverless API with AWS: My Learning Journey

## Introduction

This project was all about learning how to build and deploy APIs using AWS. The goal was to create a simple serverless API that interacts with a DynamoDB database, where you can add, get, and delete movies. This guide walks you through the AWS services I used, how I set everything up, and a quick demo on how to make API requests using Postman.

## AWS Services Used

Here are the main AWS services I used to make this project work:

- **IAM (Identity and Access Management)**: Helps in creating roles and permissions for Lambda, API Gateway, and DynamoDB to work together.
- **AWS Lambda**: This is where all the magic happens. It runs the code that handles the API requests.
- **Amazon API Gateway**: This is how we expose our Lambda function as a RESTful API, so the world can interact with it.
- **Amazon DynamoDB**: A fast and flexible NoSQL database that stores all the movie data.
- **AWS CloudWatch**: Helps monitor and log all the activities and errors that happen in the API.

## What We Did

### 1. Set Up DynamoDB

I created a DynamoDB table called **Movies**, with **Title** as the primary key. This table is where all the movie data gets stored.

### 2. Created the Lambda Function

I wrote a simple Python function for Lambda to handle the main tasks (add, get, delete). It talks to DynamoDB to store, retrieve, or delete movie records. I gave this function the necessary permissions using IAM.

### 3. Set Up API Gateway

I connected **API Gateway** to the Lambda function, making it available as a public API. I set up the routes (GET, POST, DELETE) and allowed requests from any domain by enabling **CORS**.

### 4. Enabled CloudWatch Logging

I turned on **CloudWatch** to keep track of all API calls. This helps with debugging, troubleshooting, and seeing how well the API is performing.

## API Demo in Postman

Here’s how you can interact with the API using **Postman**:

### 1. POST Request (Add a Movie)

**Request**:

```http
POST https://your-api-gateway-url/movies
Content-Type: application/json
```
**Body**:

```http
{
    "Title": "Spirited Away",
    "director": "Hayao Miyazaki",
    "year": "2001",
    "rating": "8.6"
}
```

**Response**:

```http
{
    "message": "Movie added successfully"
}

```

### 2. GET Request (Retrieve All Movies)

**Request**:

```http
POST https://your-api-gateway-url/movies
```

**Response**:

```http
{
    "Title": "Spirited Away",
    "director": "Hayao Miyazaki",
    "year": "2001",
    "rating": "8.6"
}
```
