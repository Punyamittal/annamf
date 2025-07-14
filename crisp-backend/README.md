# CRISPR Backend Service

This is the backend service for the CRISPR gene analysis module. It provides API endpoints for analyzing crop genes and generating CRISPR gRNA recommendations.

## Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
Create a `.env` file in the crisp-backend directory with:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

3. Run the server:
```bash
python main.py
```

The server will start on `http://localhost:5000`

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/crops` - Get available crops
- `GET /api/traits/{crop}` - Get available traits for a crop
- `POST /api/generate-report` - Generate gene analysis report

## Features

- Gene sequence analysis using Ensembl API
- CRISPR gRNA design and scoring
- Integration with Google Gemini AI for explanations
- Support for 50+ crops and their traits
- Real-time gene data fetching

## Usage

The frontend will automatically connect to this backend service when the crisp module is accessed. Make sure the backend is running before using the frontend. 