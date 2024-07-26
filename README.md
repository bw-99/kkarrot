# 📦 Electronics Marketplace using Amazon eCommerce Dataset

## 🌟 Overview

Welcome to the Electronics Marketplace! This project is focused on building a user-friendly platform for second-hand trading of electronic products, leveraging the rich Amazon eCommerce dataset. The dataset provides a wealth of information, enabling us to implement sophisticated recommendation systems and user-friendly features.

The core of this project involves a deep learning recommender system model trained on the Amazon eCommerce dataset using the `torch` package. This model is deployed using Flask, providing an efficient and scalable solution for delivering personalized product recommendations to users.

![image](https://github.com/user-attachments/assets/2d642538-4ad3-4c2c-9360-5f983fd6b0bd)


## 📊 1. Used Dataset

- **Dataset Source**: [Amazon eCommerce Dataset](https://amazon-reviews-2023.github.io/)

This dataset contains detailed information on a wide range of electronic products, customer reviews, and ratings. It's the foundation for our product recommendations and other features.

## 🚀 2. Supported Features

### 🏠 2.1 Home Feed Recommendation via Multi-Stage Recommendation
- **Description**: When users visit the homepage, they are greeted with a personalized list of product recommendations based on their browsing history and preferences. This feature employs a Multi-stage recommendation concept:
  - **Item Retrieval**: Utilizes a Two-Tower model to efficiently retrieve a relevant set of items.
  - **Item Scoring**: Implements Graph Neural Network Link Prediction to score and rank these items, providing highly personalized recommendations.

### 🔄 2.2 Session-Based Recommendation
- **Description**: This feature tracks user interactions with products and suggests subsequent items that align with the user's interests, enhancing the shopping experience. The system is implemented using GRU (Gated Recurrent Units) to model user sessions and predict next-item recommendations.

## 🔧 3. Upcoming Features

### 🔐 3.1 Authentication
#### 3.1.1 User Sign In/Sign Up
- **Description**: Secure user authentication for account creation and login.

#### 3.1.2 Session Management
- **Description**: Secure session handling, tracking user sessions, and managing session timeouts.

#### 3.1.3 Permission Management
- **Description**: Defining user roles and permissions to control access to various platform features.

### 🧠 3.2 Recommendation Enhancements
#### 3.2.1 Continuous Training
- **Description**: Implementing continuous learning to improve recommendation accuracy with new data.

#### 3.2.2 Autonomous Optimal Model Selection
- **Description**: Utilizing algorithms to autonomously select the most effective recommendation models based on performance metrics.

### 🛠️ 3.3 Additional Features
#### 3.3.1 Add to Cart and Favorite
- **Description**: Users can add products to their cart and mark items as favorites for easy access later.

#### 3.3.2 Service Structuring with Kubernetes (k8s)
- **Description**: Using Kubernetes for container orchestration, enhancing the scalability and manageability of the service architecture.

## 🛠️ Tech Stack

### 🤖 Deep Learning
- **torch**: `2.1.0+cu118` 
  - A powerful library for deep learning, used for building and training the recommendation models.
- **torch_geometric**: `2.5.2`
  - A library for geometric deep learning, useful for handling complex data structures like graphs.

### 🌐 Backend
- **Flask**: `2.1.2`
  - A lightweight WSGI web application framework, used as the core framework for building the backend.
- **flask-restx**: `0.5.1`
  - An extension for Flask that adds support for quickly building REST APIs, with built-in support for data validation and API documentation.
