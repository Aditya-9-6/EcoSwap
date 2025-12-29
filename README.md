# EcoSwap 2.0 - Voice-Enabled Sustainability AI

EcoSwap 2.0 is a Django-based web application that helps users find sustainable alternatives to everyday products using AI (Groq Llama-3).

## Features
- **Green Brain AI**: Finds eco-friendly alternatives with impact scores.
- **Voice Command**: Use your microphone to search hands-free.
- **Gamification**: Earn Eco-Points and track plastic saved.
- **Dashboard**: Visual impact charts.

## Setup Instructions

1. **Clone & Install**
   ```bash
   git clone <url>
   cd ecoswap
   pip install -r requirements.txt
   ```

2. **Environment Setup**
   Create a `.env` file in the root:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   SECRET_KEY=your_secret_key
   DEBUG=True
   ```
   *Get your key from [console.groq.com](https://console.groq.com)*

3. **Database**
   ```bash
   python manage.py migrate
   ```

4. **Run Server**
   ```bash
   python manage.py runserver
   ```
   Visit `http://127.0.0.1:8000`

## Mobile & Network Usage

 To access on your mobile device (on the same Wi-Fi):

 1. Find your computer's local IP address:
    * **Windows**: Open terminal and run `ipconfig` (Look for IPv4 Address, e.g., `192.168.1.5`)
 2. Run the server with:
    ```bash
    python manage.py runserver 0.0.0.0:8000
    ```
 3. Open your mobile browser and go to: `http://<your-ip-address>:8000`

## Tech Stack
- Django 5.0
- Tailwind CSS
- Groq API (Llama-3)
- Chart.js
