# UNSW Chatbot

## Project Overview
The UNSW Chatbot is designed to enhance the experience of students, faculty, and visitors at the University of New South Wales by providing a responsive and intuitive chat interface. Built using React for the frontend and Flask for the backend, this chatbot leverages OpenAI's powerful GPT-3.5 model to deliver accurate and context-aware responses based on the UNSW website content.

## Features
- **Dynamic Interaction**: Engage with the chatbot through a sleek web interface.
- **Context-Aware Responses**: Get answers to queries based on specific content from the UNSW website.
- **Real-Time Communication**: Instant communication setup using Flask and React.
- **Scalable Architecture**: Designed to be scalable for future enhancements like direct integration with UNSW databases.

## Technology Stack
- **Frontend**: React.js
- **Backend**: Flask
- **API**: OpenAI GPT-3.5
- **Styling**: CSS

## Setup and Installation
```bash
# Clone the repository
git clone https://github.com/your-github-username/unsw-chatbot.git

# Navigate into the directory
cd unsw-chatbot

# Install dependencies
npm install

# Run the React app
npm start

# Navigate into the backend directory
cd backend

# Setup virtual environment (optional)
python -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Run the Flask server
flask run
