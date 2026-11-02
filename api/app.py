import os
from pathlib import Path
from flask import Flask, render_template, abort, jsonify, request
from jinja2 import DictLoader

# Load environment variables if available
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    else:
        load_dotenv()
except ImportError:
    pass

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "smile-secret-key-production-change-me")

# Optional Supabase client integration
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_PUBLISHABLE_KEY")
supabase = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception:
        supabase = None

# SMILE Trainers details
trainers = [
    {
        "id": "mahesh-masal",
        "name": "Mr. Mahesh Masal",
        "role": "Program Patron",
        "description": "Human Mind Coach and Corporate Trainer",
        "category": "Program Leadership"
    },
    {
        "id": "nanda-hampiholi",
        "name": "Ms. Nanda Hampiholi",
        "role": "Lead Trainer & Program Director",
        "description": "NLP Master Trainer and Transformational Coach",
        "category": "Program Leadership"
    },
    {
        "id": "om-kiran",
        "name": "Om Kiran",
        "role": "Trainer",
        "description": "Human Mind Coach and Corporate Trainer",
        "category": "Trainers Crew"
    },
    {
        "id": "deenaz-ahmed",
        "name": "Deenaz Ahmed",
        "role": "Trainer",
        "description": "Professional Development Coach and Corporate Trainer",
        "category": "Trainers Crew"
    },
    {
        "id": "suresh-rao",
        "name": "Suresh Rao",
        "role": "Trainer",
        "description": "Master Trainer and Chief Consultant",
        "category": "Trainers Crew"
    },
    {
        "id": "anand-kustagi",
        "name": "Anand Kustagi",
        "role": "Trainer",
        "description": "Public Speaking Mentor and Soft Skills Trainer",
        "category": "Trainers Crew"
    },
    {
        "id": "shiva-shekhar",
        "name": "Shiva Shekhar",
        "role": "Trainer",
        "description": "Innovation Facilitator and Youth Transformation Coach",
        "category": "Trainers Crew"
    },
    {
        "id": "greeshma",
        "name": "Greeshma",
        "role": "Trainer",
        "description": "Creative Youth Life Coach and NLP Practitioner",
        "category": "Trainers Crew"
    },
    {
        "id": "praveen-deshpande",
        "name": "Praveen Deshpande",
        "role": "Trainer",
        "description": "JCI Trainer, Youth Potential and Personal Excellence Coach",
        "category": "Trainers Crew"
    },
    {
        "id": "dr-kedar",
        "name": "Dr. Kedar",
        "role": "Trainer",
        "description": "JCI National Trainer and NLP Practitioner",
        "category": "Trainers Crew"
    }
]

# Shared Jinja header and footer
BASE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}SMILE Trainers{% endblock %}</title>

    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: Arial, sans-serif;
            background: #eef5fc;
            color: #1d2b3a;
        }

        header {
            background: #ffffff;
            min-height: 250px;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 35px 20px;
            box-shadow: 0 5px 18px rgba(20, 46, 82, 0.10);
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 28px;
            max-width: 850px;
        }

        .logo {
            width: 125px;
            height: 125px;
            border-radius: 50%;
            background: #ffc24b;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 43px;
            flex-shrink: 0;
            box-shadow: 0 7px 13px #d9b35d;
        }

        .brand h1 {
            color: #2058a5;
            font-size: 36px;
            margin-bottom: 16px;
        }

        .brand p {
            color: #526779;
            font-size: 17px;
            line-height: 1.5;
        }

        main {
            max-width: 1100px;
            margin: auto;
            padding: 65px 24px;
            min-height: 400px;
        }

        .page-title {
            text-align: center;
            color: #2058a5;
            font-size: 38px;
            margin-bottom: 15px;
        }

        .subtitle {
            text-align: center;
            margin-bottom: 40px;
            color: #526779;
            line-height: 1.6;
        }

        .section-title {
            color: #2058a5;
            margin: 35px 0 22px;
            font-size: 24px;
        }

        .trainer-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 22px;
        }

        .trainer-card {
            background: white;
            padding: 28px 18px;
            border-radius: 14px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(20, 46, 82, 0.09);
            border-bottom: 4px solid #2058a5;
        }

        .trainer-icon {
            width: 76px;
            height: 76px;
            border-radius: 50%;
            background: #ffc24b;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
            margin: 0 auto 18px;
        }

        .trainer-card h3 {
            color: #2058a5;
            margin-bottom: 10px;
            font-size: 19px;
        }

        .trainer-card p {
            color: #526779;
            line-height: 1.6;
            margin-bottom: 18px;
            font-size: 14px;
        }

        .role {
            color: #2058a5 !important;
            font-weight: bold;
        }

        .btn {
            display: inline-block;
            background: #2058a5;
            color: white;
            padding: 12px 20px;
            border-radius: 7px;
            text-decoration: none;
            font-weight: bold;
            border: none;
            cursor: pointer;
        }

        .btn:hover {
            background: #123a72;
        }

        .details-card {
            max-width: 650px;
            margin: auto;
            padding: 40px 25px;
            background: white;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 5px 18px rgba(20, 46, 82, 0.10);
        }

        .details-card .trainer-icon {
            width: 110px;
            height: 110px;
            font-size: 45px;
        }

        .details-card h2 {
            color: #2058a5;
            margin-bottom: 20px;
        }

        .details-card p {
            line-height: 1.8;
            margin-bottom: 12px;
        }

        footer {
            background: #142e52;
            color: white;
            text-align: center;
            padding: 24px 12px;
            line-height: 1.8;
        }

        @media (max-width: 750px) {
            header {
                min-height: 210px;
                padding: 28px 16px;
            }

            .brand {
                gap: 16px;
            }

            .logo {
                width: 85px;
                height: 85px;
                font-size: 30px;
            }

            .brand h1 {
                font-size: 28px;
                margin-bottom: 8px;
            }

            .brand p {
                font-size: 14px;
            }

            main {
                padding: 45px 16px;
            }

            .page-title {
                font-size: 30px;
            }

            .trainer-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 14px;
            }

            .trainer-card {
                padding: 22px 10px;
            }
        }

        @media (max-width: 430px) {
            .trainer-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>

<body>
    <header>
        <div class="brand">
            <div class="logo">😊</div>
            <div>
                <h1>SMILE</h1>
                <p>Life Skills &amp; Emotional Intelligence Program</p>
            </div>
        </div>
    </header>

    {% block content %}{% endblock %}

    <footer>
        <strong>SMILE</strong><br>
        Empowering Trainers, Building Futures<br>
        Dharwad, Karnataka
    </footer>
</body>
</html>
"""

# Jinja template: trainers list
TRAINERS_PAGE = """
{% extends "base.html" %}
{% block title %}SMILE - Trainers{% endblock %}

{% block content %}
<main>
    <h1 class="page-title">Our Trainers</h1>
    <p class="subtitle">
        Meet the team behind the SMILE Life Skills Program.
    </p>

    <h2 class="section-title">Program Leadership</h2>
    <div class="trainer-grid">
        {% for trainer in trainers if trainer.category == 'Program Leadership' %}
        <div class="trainer-card">
            <div class="trainer-icon">😊</div>
            <h3>{{ trainer.name }}</h3>
            <p class="role">{{ trainer.role }}</p>
            <p>{{ trainer.description }}</p>
            <a class="btn"
               href="{{ url_for('trainer_detail', trainer_id=trainer.id) }}">
               View Details
            </a>
        </div>
        {% endfor %}
    </div>

    <h2 class="section-title">Trainers Crew</h2>
    <div class="trainer-grid">
        {% for trainer in trainers if trainer.category == 'Trainers Crew' %}
        <div class="trainer-card">
            <div class="trainer-icon">😊</div>
            <h3>{{ trainer.name }}</h3>
            <p class="role">{{ trainer.role }}</p>
            <p>{{ trainer.description }}</p>
            <a class="btn"
               href="{{ url_for('trainer_detail', trainer_id=trainer.id) }}">
               View Details
            </a>
        </div>
        {% endfor %}
    </div>
</main>
{% endblock %}
"""

# Jinja template: one separate URL per trainer
DETAIL_PAGE = """
{% extends "base.html" %}
{% block title %}{{ trainer.name }} - SMILE{% endblock %}

{% block content %}
<main>
    <h1 class="page-title">Trainer Details</h1>
    <p class="subtitle">SMILE Trainers Tracking System</p>

    <div class="details-card">
        <div class="trainer-icon">😊</div>
        <h2>{{ trainer.name }}</h2>

        <p><strong>Role:</strong> {{ trainer.role }}</p>
        <p><strong>Category:</strong> {{ trainer.category }}</p>
        <p><strong>Expertise:</strong> {{ trainer.description }}</p>

        <a class="btn" href="{{ url_for('trainers_page') }}">
            Back to Trainers
        </a>
    </div>
</main>
{% endblock %}
"""

# DictLoader allows templates to extend base.html without needing filesystem template files
app.jinja_loader = DictLoader({
    'base.html': BASE,
    'trainers.html': TRAINERS_PAGE,
    'detail.html': DETAIL_PAGE
})


@app.route("/")
@app.route("/api")
@app.route("/api/")
def home():
    if request.args.get("format") == "json" or request.headers.get("Accept") == "application/json":
        return jsonify({
            "project": "SMILE Life Skills & Emotional Intelligence Program",
            "status": "online",
            "trainers_count": len(trainers),
            "endpoints": {
                "trainers": "/api/trainers",
                "health": "/api/health"
            }
        })
    return trainers_page()


@app.route("/api/health")
def health():
    return jsonify({
        "status": "healthy",
        "project": "SMILE Life Skills & Emotional Intelligence Program",
        "supabase_configured": bool(SUPABASE_URL and SUPABASE_KEY)
    })


@app.route("/trainers", methods=["GET"])
@app.route("/api/trainers", methods=["GET"])
def trainers_page():
    if request.args.get("format") == "json" or request.headers.get("Accept") == "application/json":
        return jsonify(trainers)
    return render_template('trainers.html', trainers=trainers)


@app.route("/trainer/<trainer_id>", methods=["GET"])
@app.route("/api/trainer/<trainer_id>", methods=["GET"])
def trainer_detail(trainer_id):
    trainer = next(
        (t for t in trainers if t["id"] == trainer_id),
        None
    )

    if trainer is None:
        if request.args.get("format") == "json" or request.headers.get("Accept") == "application/json":
            return jsonify({"error": "Trainer not found"}), 404
        abort(404)

    if request.args.get("format") == "json" or request.headers.get("Accept") == "application/json":
        return jsonify(trainer)

    return render_template('detail.html', trainer=trainer)


if __name__ == "__main__":
    app.run(debug=True)
