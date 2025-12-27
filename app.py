from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'mystery_key_secret'  # Required for session management

# ---------------- GAME DATA ----------------
ALL_PUZZLES = [
    ("I speak without a mouth and hear without ears. I have nobody, but I come alive with wind.", "echo", "It repeats what you say."),
    ("The more you take, the more you leave behind. What am I?", "footsteps", "They appear when you walk."),
    ("I am always hungry, I must always be fed. The finger I touch will soon turn red.", "fire", "It is hot and dangerous."),
    ("I have keys but no locks. I have space but no room.", "keyboard", "Used to type."),
    ("I can fly without wings and cry without eyes.", "cloud", "It floats in the sky."),
    ("The more you have of it, the less you see.", "darkness", "Opposite of light."),
    ("What can travel around the world while staying in a corner?", "stamp", "Found on letters."),
    ("What has hands but cannot clap?", "clock", "Tells time."),
    ("I shave every day, but my beard stays the same.", "barber", "It's a profession.")
]

PUZZLES_TO_PLAY = 3

# ---------------- ROUTES ----------------

# Choose.html should always be first
@app.route('/choose', methods=['GET', 'POST'])
def choose():
    # Clear previous game session data
    session.clear()

    if request.method == 'POST':
        choice = request.form.get('option')
        session['user_choice'] = int(choice)
        return redirect(url_for('index'))

    return render_template('choose.html')


@app.route('/')
def index():
    # If user_choice is not set, always redirect to /choose
    if 'user_choice' not in session:
        return redirect(url_for('choose'))

    choice = session['user_choice']

    if choice == 1:
        # Show the riddle game landing page
        return render_template('index.html')
    else:
        # Option 2 → Tic-Tac-Toe
        return render_template('ttt.html')


@app.route('/game', methods=['GET', 'POST'])
def game():
    # Initialize puzzles only if not already done
    if 'puzzles' not in session:
        session['puzzles'] = random.sample(ALL_PUZZLES, PUZZLES_TO_PLAY)
        session['current_index'] = 0
        session['score'] = 0

    index = session.get('current_index', 0)
    puzzles = session.get('puzzles', [])

    if index >= len(puzzles):
        return redirect(url_for('result', status='win'))

    current_riddle, current_answer, current_hint = puzzles[index]

    if request.method == 'POST':
        user_input = request.form.get('answer', '').strip().lower()
        if user_input == current_answer:
            session['current_index'] += 1
            return redirect(url_for('game'))
        else:
            return redirect(url_for('result', status='lose'))

    return render_template('game.html',
                           riddle=current_riddle,
                           hint=current_hint,
                           progress=f"Puzzle {index + 1} of {PUZZLES_TO_PLAY}")


@app.route('/result/<status>')
def result(status):
    return render_template('result.html', status=status)


# Optional: prevent caching to avoid browser auto-reloading index.html
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


if __name__ == '__main__':
    app.run(debug=True)
