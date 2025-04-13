# 🧠 AI Content Moderation Platform

## 💼 What It Does

A system for publishing content (posts, offers, etc.) with built-in moderation and analysis using AI.

### Core Features

- 🔒 User authentication and authorization  
- ⚡️ Streaming content processing via Kafka  
- 🧠 Content analysis using LLMs (moderation, classification, tagging, sentiment)  
- 🛢 Data storage using PostgreSQL  
- 📊 Admin panel to review and manage flagged content  

---

## 🧱 Modules

### 👤 Users

- Registration / Login  
- User roles: `admin`, `user`  

### ✍️ Content Creation

- Users can create posts or announcements  
- Content is sent to a Kafka topic for asynchronous processing  

### 🤖 LLM Worker

- Listens to Kafka for new content  
- Analyzes:
  - Banned phrases  
  - Spam detection  
  - Auto-tagging  
  - Sentiment analysis  
- Sends the result back to the database or triggers an alert  

### 🛠 Admin Panel

- List of suspicious or flagged content  
- Admin actions:
  - ✅ Approve  
  - ❌ Delete  
  - ✏️ Request correction  

### 📈 Dashboard

- Statistics:
  - Number of submissions  
  - Classification results  
  - User activity  
