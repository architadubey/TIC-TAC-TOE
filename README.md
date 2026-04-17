# Tic Tac Toe AI - V2 / V3 Web Engine

A sophisticated, full-stack implementation of the classic Tic Tac Toe game. This project features two distinct versions: an elegant desktop application built with `customtkinter` and a vibrant web application built using Python Flask, Vanilla JS, CSS Glassmorphism, and HTML5. 

Both versions boast an **Unbeatable AI** powered by the Minimax algorithm with Alpha-Beta pruning.

---

## 🌟 Features

- **Dual Interfaces**: Choose between a standalone Desktop App or a responsive Full-Stack Web App.
- **Unbeatable AI**: The "Unbeatable" difficulty setting uses the Minimax algorithm to ensure the computer never loses.
- **Game Modes**: 
  - Player vs. Computer
  - Player vs. Player
- **Adjustable Difficulty (PVC Mode)**:
  - **Easy**: The AI makes random moves.
  - **Medium**: The AI takes immediate wins or blocks immediate losses, but otherwise guesses randomly.
  - **Unbeatable**: The AI calculates the entire game tree.
- **Modern User Interface**: Both the web and desktop versions follow modern UI trends, utilizing dark themes, sleek scoreboards, dynamic SVG winning strike lines, and glassmorphic designs.
- **Interactive Toggles**: Control who goes first (Player or Computer) seamlessly.

---

## 🛠️ Tech Stack

### Web Version
- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3 (Glassmorphism), Vanilla JavaScript, SVG Animations
- **Communication**: Asynchronous Fetch API (JSON)

### Desktop Version
- **Language**: Python
- **GUI Toolkit**: `customtkinter`, `tkinter`

---

## 📦 Installation & Setup

1. **Clone the Repository** (or download the project folder)
2. **Setup a Python Environment**: Ensure you are running Python 3.8+
3. **Install Dependencies**:
   ```bash
   pip install flask customtkinter
   ```

---

## 🚀 Usage

You can run either the web server or the desktop application depending on your preference.

### Running the Desktop Application
The desktop application is self-contained. It renders a GUI directly on your machine.
```bash
python main.py
```

### Running the Web Application
The web app utilizes Flask as an API and file server. 
1. Start the Flask server:
```bash
python app.py
```
2. Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🧠 Core Concepts

### Minimax Algorithm
The brain of the "Unbeatable" AI difficulty relies on the **Minimax Algorithm**, which falls under game theory. Because Tic Tac Toe is a zero-sum game of perfect information, we can evaluate a tree of all possible game states. 

- The AI tries to **Maximize** its score (aiming for +10).
- The AI expects the human player to **Minimize** the AI's score (aiming for -10).
- By recursively traversing all potential outcomes down to terminal states (win, lose, or draw), the algorithm guarantees that the AI always plays optimally.

### Alpha-Beta Pruning
To optimize game tree traversal, the code inherently tracks the best guaranteed score pathways to prune off sections of calculation that perform worst than already explored branches. While Tic Tac Toe is a small game, this approach represents an advanced strategy used in chess and checker AI engines.

---

## 📂 Project Structure

```text
/
├── main.py                # Desktop Application Entry Point
├── app.py                 # Flask Web Server Entry Point / API
├── project_explanation.txt# Detailed technical breakdown
├── templates/
│   └── index.html         # Main Web App UI Structure
└── static/
    ├── style.css          # Glassmorphic Stylesheets
    └── app.js             # Web UI Logic & API Communication
```
