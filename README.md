# 📦 Electronics Marketplace using Amazon eCommerce Dataset

## 🌟 Overview

This project aims to develop a user-friendly platform for second-hand trading of electronic products, specifically inspired by the popular Korean platform 당근마켓. By utilizing the extensive Amazon eCommerce dataset, we can implement advanced recommendation systems and other user-friendly features to enhance the experience.

The core of this project involves a deep learning recommender system model trained on the Amazon eCommerce dataset using the `torch` package. This model is deployed using Flask, providing an efficient and scalable solution for delivering personalized product recommendations to users.

### Home Page
<p align="center">
  <img alt="Light" src="https://github.com/user-attachments/assets/13ea3444-5807-4bb6-a27a-03b18a6eb396" width="49%">
  <img alt="Dark" src="https://github.com/user-attachments/assets/1f89794d-454e-4a95-b57c-37139351bdc12" width="49%">
</p>

### Product Page
<p align="center">
  <img alt="Light" src="https://github.com/user-attachments/assets/9c482230-a41a-4b63-9731-fd646d98aa13" width="49%">
  <img alt="Dark" src="https://github.com/user-attachments/assets/e955f60e-bd4e-474e-a1e9-f539311c6162" width="49%">
</p>


## 🐋 0. Docker
docker run -it -v {PATH_TO_WORKSPACE}:/work --shm-size=10G  bb1702/kkarrot:latest

if you install or delete dependencies, libraries => docker commit {container_id} {name} and share 


## 📊 1. Used Dataset

- **Dataset Source**: [Amazon eCommerce Dataset](https://amazon-reviews-2023.github.io/)

This dataset contains detailed information on a wide range of electronic products, customer reviews, and ratings. It's the foundation for our product recommendations and other features.

## 🚀 2. Supported Features

### 🏠 2.1 Home Feed Recommendation
- **Description**: When users visit the homepage, they are greeted with a personalized list of product recommendations based on their browsing history and preferences. This feature employs a Multi-stage recommendation concept:
  - **Item Retrieval**: Utilizes a Two-Tower model to efficiently retrieve a relevant set of items.
  - **Item Scoring**: Implements Graph Neural Network Link Prediction to score and rank these items, providing highly personalized recommendations.


https://github.com/user-attachments/assets/31312fa2-63bf-4544-8b74-83ba8446c245


### 🔄 2.2 Session-Based Recommendation
- **Description**: This feature tracks user interactions with products and suggests subsequent items that align with the user's interests, enhancing the shopping experience. The system is implemented using [TailNet (2020, RecSys)](https://dl.acm.org/doi/10.1145/3383313.3412222) to model user sessions and predict next-item recommendations.


https://github.com/user-attachments/assets/7d579439-9969-4679-b79d-42f882b60521


## 🔧 3. Upcoming Features

### 🔐 3.1 Authentication
#### 3.1.1 User Sign In/Sign Up
- Secure user authentication for account creation and login.
- OAuth functionality for easier sign-in, improving user convenience.

### 🧠 3.2 Recommendation Enhancements
#### 3.2.1 Continual Training
- Implement continuoual learning, by employing knowledge distillation, to improve recommendation accuracy with new data.

#### 3.2.2 Autonomous Optimal Model Selection
- Utilize algorithms to autonomously select the most effective recommendation models based on performance metrics.

### 🛠️ 3.3 Additional Features
#### 3.3.1 Add to Cart and Favorite
- Users can add products to their cart and mark items as favorites for easy access later.

#### 3.3.2 Service Structuring with Kubernetes (k8s)
- Using Kubernetes for container orchestration, enhancing the scalability and manageability of the service architecture.

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
- **Swagger**: Integrated with Flask to provide API documentation, aiding collaboration between frontend and backend teams.

### 💻 Frontend
- **React**: `18.3.1`
  - A JavaScript library for building user interfaces, ensuring a responsive and dynamic user experience.
- **axios**: `1.7.2`
  - A promise-based HTTP client for making API requests from the frontend, used for data fetching and state management.

### 🛠️ DevOps
- **Docker**
  - Used for creating containerized environments to ensure consistent development, testing, and deployment, facilitating seamless collaboration among team members by sharing Docker images.
