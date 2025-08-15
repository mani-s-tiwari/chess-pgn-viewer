# ♞ BaddKnight - Synchronized Chess PGN Viewer

**A dynamic web-based PGN viewer with game synchronization, analysis tools, and related game discovery**

![Screenshot](https://example.com/screenshot.png) <!-- Replace with actual screenshot -->

## ✨ Features

- **Dynamic PGN Loading**
  - Instantly view games from uploaded PGN files
  - Navigate between multiple games in a single file
  - Real-time board updates

- **Game Synchronization**
  - Synchronize moves across multiple views
  - Compare related games with matching move sequences
  - Side-by-side game comparison

- **Interactive Analysis**
  - Move-by-move navigation (keyboard shortcuts supported)
  - Auto-play functionality with adjustable speed
  - Current move highlighting in move list

- **Modern Interface**
  - Responsive design works on desktop and tablets
  - Light/dark mode toggle
  - Clean, intuitive controls

## 🛠️ Technology Stack

- **Frontend**: 
  - Chessboard.js + chess.js for board interaction
  - Vanilla JavaScript for dynamic UI
  - CSS Flexbox/Grid for responsive layout

- **Backend** (Django example):
  ```python
  # Sample PGN processing view
  def load_pgn(request):
      pgn_text = request.FILES['pgn_file'].read().decode()
      games = parse_pgn(pgn_text) # Your parsing logic
      return JsonResponse({'games': games})
