# SMILE - Life Skills & Emotional Intelligence Program
**Smile Project**

A comprehensive tracking, learning, and management platform for the SMILE Life Skills & Emotional Intelligence Program in Dharwad, Karnataka.

---

## 🌟 Overview & Features

- **Home & Landing Page (`index.html`, `landingpage1.html`)**: Complete presentation of the SMILE program, vision, leadership, objectives, anthem, and contact information.
- **Our Team & Trainers Tracking (`trainers.html`, `/trainers`, `/trainer/<id>`)**: Detailed profiles of Program Patron Mr. Mahesh Masal, Program Director Ms. Nanda Hampiholi, and the entire Trainers Crew. Available both as static profiles and dynamic Python Flask serverless endpoints.
- **Program Information & Objectives (`program.html`, `objectives.html`, `Advisors.html`)**: In-depth curriculum context, target group details, and advisory board.
- **Curriculum & Modules (`module.html`, `modules.html`)**: 8 core development modules covering Self Awareness, Emotional Intelligence, Communication, Discipline, Decision Making, Stress Management, Leadership, and Digital Literacy.
- **Multimedia & Video Sessions (`video.html`, `multimedia.html`)**: Multi-method learning approach and video training library.
- **Participant Feedback (`Testimonies.html`)**: Participant stories and program impact reviews.
- **Trainer Registration & Authentication (`registration.html`, `loginpage.html`)**: Secure trainer registration and login portal with client-side credential verification.
- **Interactive Navigation & Dashboards (`menu.html`, `AdminPannel.html`, `chiefadmin.html`)**: Central menu system, session reporting portal with photo/video upload validation, and chief administrator content hub.

---

## 📂 Project Structure (Vercel-Ready)

```text
Smile Project/
├── api/
│   ├── .env                    # Local environment variables
│   ├── .env.example            # Template for deployment environment variables
│   ├── app.py                  # Python Flask serverless application & API logic
│   ├── index.py                # Vercel entrypoint for Python Serverless Functions
│   └── requirements.txt        # Python dependencies for serverless functions
├── public/
│   ├── images/                 # Image assets directory
│   ├── index.html              # Primary entrypoint (served at root /)
│   ├── landingpage1.html       # Preserved original landing page
│   ├── trainers.html           # Team & trainers roster
│   ├── loginpage.html          # Trainer login
│   ├── registration.html       # Trainer registration
│   ├── menu.html               # Main dashboard menu
│   ├── AdminPannel.html        # Admin session report panel
│   ├── Advisors.html           # Program advisors
│   ├── chiefadmin.html         # Chief administrator panel
│   ├── module.html             # Curriculum & modules
│   ├── modules.html            # Curriculum alias
│   ├── multimedia.html         # Multimedia approach overview
│   ├── objectives.html         # Program objectives
│   ├── program.html            # Why SMILE program
│   ├── Testimonies.html        # Feedback & testimonials
│   ├── video.html              # Training videos
│   ├── *.html                  # Individual trainer profile pages
│   └── *.jpeg                  # Program photos and assets
├── .env.example                # Project root environment variable template
├── .gitignore                  # Git ignore rules for clean repository
├── package.json                # Project metadata and npm scripts
├── requirements.txt            # Python dependencies for Vercel deployment
├── vercel.json                 # Vercel routing, rewrites, and security configuration
└── README.md                   # Project documentation
```

---

## 🚀 Deploying to Vercel

### Option 1: Deploy with Vercel Git Integration (Recommended)
1. Push this repository to **GitHub**, **GitLab**, or **Bitbucket**.
2. Open the [Vercel Dashboard](https://vercel.com/) and click **Add New Project**.
3. Import your **Smile Project** repository.
4. (Optional) Under **Environment Variables**, add any custom values from `.env.example`:
   - `SUPABASE_URL`
   - `SUPABASE_PUBLISHABLE_KEY`
   - `FLASK_SECRET_KEY`
   - `ADMIN_USERNAME`
   - `ADMIN_PASSWORD`
5. Click **Deploy**. Vercel will automatically build and deploy the static assets from `public/` and serverless functions from `api/`.

### Option 2: Deploy using Vercel CLI
```bash
npm install -g vercel
vercel
```

---

## 💻 Local Development

### Running the Python Flask Backend
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the application
python api/app.py
```
The Flask application will start at `http://127.0.0.1:5000/`.

### Serving the Static Site
You can open any file in `public/` directly in a web browser, or serve it using Python's built-in HTTP server:
```bash
python -m http.server 3000 --directory public
```
Then visit `http://localhost:3000/`.

---

## 🔌 API Endpoints

- `GET /` — Serves `index.html` (Landing page)
- `GET /trainers` — Dynamic trainer list page (or static view via `/trainers.html`)
- `GET /api/trainers` — Returns list of all trainers in JSON or HTML
- `GET /trainer/<trainer_id>` — Detail view for a specific trainer (e.g. `/trainer/mahesh-masal`)
- `GET /api/health` — Backend health check and configuration status
