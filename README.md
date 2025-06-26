# Diamond Price Prediction

A full-stack web application for predicting diamond prices using machine learning. Built with Django (and legacy Flask), this project allows users to register, log in, input diamond features, and receive instant price predictions. The app also provides dashboards, visualizations, explainable AI, and export features.

## Features
- User registration, login, and profile management
- Step-by-step wizard for diamond feature input
- Live prediction with AJAX (instant results)
- Dashboard with prediction history and interactive charts
- Download prediction history as CSV or PDF
- Feature importance (explainable AI)
- Light/dark mode toggle
- Accessibility enhancements (ARIA, keyboard navigation, skip links)
- Educational content about diamonds, the 4Cs, and machine learning
- Responsible buying callouts and external resources

## Project Structure
```
Ineuron_Project/
├── DimondPricePrediction/           # ML package, legacy Flask app, and scripts
├── diamond_project/                 # Django project settings
├── predictor/                       # Django app (views, models, templates)
├── artifacts/                       # Trained model and preprocessor
├── logs/                            # Log files
├── db.sqlite3                       # SQLite database
├── manage.py                        # Django entry point
└── ...
```

## Setup Instructions
1. **Clone the repository:**
   ```sh
   git clone https://github.com/kali8271/Ineuron_Project.git
   cd Ineuron_Project
   ```
2. **Create and activate a virtual environment:**
   ```sh
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   # Or: source .venv/bin/activate  # On Linux/Mac
   ```
3. **Install dependencies:**
   ```sh
   pip install -r DimondPricePrediction/requirements.txt
   ```
4. **Run migrations:**
   ```sh
   python manage.py migrate
   ```
5. **Run the development server:**
   ```sh
   python manage.py runserver
   ```
6. **Access the app:**
   Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Usage
- Register a new account or log in.
- Use the step-by-step wizard to enter diamond features.
- View your prediction history and download it as CSV or PDF.
- Explore feature importance and educational content on the dashboard and home page.

## Testing
- Run unittests for the model trainer:
  ```sh
  python test_model_trainer.py
  ```

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](LICENSE)

---
**Author:** kali8271