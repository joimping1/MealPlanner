# Meal Planning WebApp - Projektübersicht

## Problem & Lösung

**Problem:**
- Zu häufige Einkäufe (3x pro Woche)
- Spontane Essensplanung führt zu Zeitverschwendung
- Unstrukturierte Lebensmittelverwaltung

**Lösung:**
Eine Web-Anwendung für systematische Wochenplanung mit automatischer Einkaufsliste, Rezeptverwaltung und intelligenter Mengenoptimierung.

## Core Features

### 1. Lebensmittel- & Haushaltsgegenständeverwaltung
- Zentrale Datenbank aller kaufbaren Items
- Kategorisierung (Fleisch, Gemüse, Haushalt, etc.)
- Standardeinheiten und Preise

### 2. Rezeptverwaltung
- Rezepte mit Zutatenlisten und Mengenangaben
- Portionsanpassung basierend auf Personenzahl
- Bildupload für Rezepte
- Bewertungs- und Kommentarsystem

### 3. Wochenplanung
- Sonntägliche Planung für die komplette Woche
- Homeoffice vs. Office Modus:
  - **Homeoffice:** Frühstück + Mittag + Abendessen
  - **Office:** Frühstück + Abendessen
- Flexible Personenzahl pro Mahlzeit
- Multi-Day-Rezepte (einmal kochen, mehrere Tage essen)
- Freundin-Anwesenheitsplanung

### 4. Intelligente Einkaufsliste
- Automatische Generierung basierend auf Wochenplan
- Mengenkonsolidierung gleicher Zutaten
- Bring!-ähnliche Benutzeroberfläche
- Checkbox-System zum Abhaken
- Kategorisierung nach Supermarkt-Bereichen

### 5. Mengenoptimierung
- Feedback-System für zu viel/zu wenig
- Automatische Mengenanpassung basierend auf Historie
- Lernender Algorithmus für individuelle Präferenzen

### 6. Partnerschaft & Sharing
- Gemeinsame Planung mit der Freundin
- Synchronisation zwischen Geräten
- Berechtigungsmanagement

## Technischer Stack

### Frontend
**Empfehlung: React mit TypeScript**
- **React 18+** mit modernen Hooks
- **TypeScript** für Type Safety
- **Vite** als Build Tool (schneller als Create React App)
- **Tailwind CSS** für Styling
- **React Hook Form** für Formularverwaltung
- **React Query/TanStack Query** für API State Management
- **React Router** für Navigation
- **Zustand** oder **Redux Toolkit** für globalen State
- **React DnD** für Drag & Drop Funktionalitäten beim Meal Planning

**UI Komponenten:**
- **Radix UI** oder **Headless UI** für accessible Komponenten
- **React Calendar** für Datumsauswahl
- **React Select** für erweiterte Dropdown-Menüs

### Backend
**Python FastAPI**
- **FastAPI** Framework
- **Pydantic** für Datenvalidierung
- **SQLAlchemy** als ORM
- **Alembic** für Database Migrations
- **python-multipart** für File Uploads
- **Pillow** für Bildverarbeitung
- **python-jose** für JWT Authentication
- **uvicorn** als ASGI Server

### Database & Backend Services
**Supabase**
- **PostgreSQL** Database
- **Authentication** mit JWT
- **Real-time Subscriptions**
- **File Storage** für Rezeptbilder
- **Row Level Security (RLS)**

### Deployment & DevOps
- **Frontend:** Vercel oder Netlify
- **Backend:** Railway, Render oder Heroku
- **Database:** Supabase (hosted PostgreSQL)
- **File Storage:** Supabase Storage

## Database Schema

### Core Tables

```sql
-- Users
users (
  id UUID PRIMARY KEY,
  email VARCHAR UNIQUE NOT NULL,
  name VARCHAR NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Lebensmittel/Items
items (
  id UUID PRIMARY KEY,
  name VARCHAR NOT NULL,
  category VARCHAR NOT NULL,
  default_unit VARCHAR NOT NULL,
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Rezepte
recipes (
  id UUID PRIMARY KEY,
  name VARCHAR NOT NULL,
  description TEXT,
  instructions TEXT,
  prep_time INTEGER,
  cook_time INTEGER,
  servings INTEGER DEFAULT 2,
  image_url VARCHAR,
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Rezept-Zutaten
recipe_ingredients (
  id UUID PRIMARY KEY,
  recipe_id UUID REFERENCES recipes(id),
  item_id UUID REFERENCES items(id),
  quantity DECIMAL NOT NULL,
  unit VARCHAR NOT NULL,
  notes VARCHAR
);

-- Wochenpläne
meal_plans (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  week_start_date DATE NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Geplante Mahlzeiten
planned_meals (
  id UUID PRIMARY KEY,
  meal_plan_id UUID REFERENCES meal_plans(id),
  recipe_id UUID REFERENCES recipes(id),
  date DATE NOT NULL,
  meal_type VARCHAR NOT NULL, -- 'breakfast', 'lunch', 'dinner'
  servings INTEGER NOT NULL,
  location VARCHAR NOT NULL, -- 'home', 'office'
  notes VARCHAR
);

-- Einkaufslisten
shopping_lists (
  id UUID PRIMARY KEY,
  meal_plan_id UUID REFERENCES meal_plans(id),
  status VARCHAR DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT NOW()
);

-- Einkaufslisten-Items
shopping_list_items (
  id UUID PRIMARY KEY,
  shopping_list_id UUID REFERENCES shopping_lists(id),
  item_id UUID REFERENCES items(id),
  quantity DECIMAL NOT NULL,
  unit VARCHAR NOT NULL,
  checked BOOLEAN DEFAULT FALSE,
  category VARCHAR
);

-- Mengen-Feedback
quantity_feedback (
  id UUID PRIMARY KEY,
  recipe_id UUID REFERENCES recipes(id),
  user_id UUID REFERENCES users(id),
  item_id UUID REFERENCES items(id),
  original_quantity DECIMAL,
  feedback VARCHAR, -- 'too_much', 'too_little', 'perfect'
  adjustment_factor DECIMAL,
  created_at TIMESTAMP DEFAULT NOW()
);
```

## API Endpunkte

### Authentication
- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/logout`
- `GET /auth/me`

### Items Management
- `GET /items` - Alle Lebensmittel abrufen
- `POST /items` - Neues Item erstellen
- `PUT /items/{id}` - Item bearbeiten
- `DELETE /items/{id}` - Item löschen

### Recipe Management
- `GET /recipes` - Alle Rezepte abrufen
- `POST /recipes` - Neues Rezept erstellen
- `GET /recipes/{id}` - Einzelnes Rezept
- `PUT /recipes/{id}` - Rezept bearbeiten
- `DELETE /recipes/{id}` - Rezept löschen
- `POST /recipes/{id}/image` - Bild upload

### Meal Planning
- `GET /meal-plans` - Wochenpläne abrufen
- `POST /meal-plans` - Neuen Wochenplan erstellen
- `GET /meal-plans/{id}` - Einzelnen Plan abrufen
- `PUT /meal-plans/{id}` - Plan bearbeiten
- `POST /meal-plans/{id}/meals` - Mahlzeit hinzufügen
- `PUT /meal-plans/{id}/meals/{meal_id}` - Mahlzeit bearbeiten

### Shopping Lists
- `GET /shopping-lists/{meal_plan_id}` - Einkaufsliste generieren
- `PUT /shopping-lists/{id}/items/{item_id}` - Item als gekauft markieren
- `POST /shopping-lists/{id}/items` - Manuelles Item hinzufügen

### Feedback & Optimization
- `POST /feedback/quantity` - Mengen-Feedback senden
- `GET /recipes/{id}/optimized-quantities` - Optimierte Mengen abrufen

## Entwicklungsroadmap

### Phase 1: MVP (4-6 Wochen)
1. **Backend Setup**
   - FastAPI Projekt initialisieren
   - Supabase Integration
   - Authentication System
   - Basic API Endpunkte

2. **Frontend Setup** 
   - React App mit TypeScript
   - Routing Setup
   - Authentication UI
   - Basic Komponenten

3. **Core Features**
   - Item Management
   - Basic Recipe Management
   - Simple Meal Planning
   - Basic Shopping List

### Phase 2: Enhanced Features (3-4 Wochen)
1. **Advanced Planning**
   - Homeoffice/Office Modi
   - Multi-day Rezepte
   - Freundin-Integration

2. **Smart Features**
   - Quantity Feedback System
   - Optimierung Algorithm
   - Image Upload für Rezepte

### Phase 3: UX/Performance (2-3 Wochen)
1. **UI/UX Verbesserungen**
   - Drag & Drop Planning
   - Mobile Optimierung
   - Performance Optimierung

2. **Advanced Features**
   - Meal History & Analytics
   - Recipe Recommendations
   - Export/Import Funktionen

## Besondere Implementierungsdetails

### JWT Authentication mit Supabase
```python
# FastAPI Dependency für geschützte Routen
async def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(401, "Missing authorization header")
    
    try:
        token = authorization.split(" ")[1]  # Bearer token
        payload = jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=["HS256"])
        return payload["sub"]
    except jwt.PyJWTError:
        raise HTTPException(401, "Invalid token")
```

### Intelligent Shopping List Generation
```python
def generate_shopping_list(meal_plan_id: str) -> Dict:
    # Alle geplanten Mahlzeiten für die Woche abrufen
    planned_meals = get_planned_meals(meal_plan_id)
    
    # Zutaten konsolidieren
    consolidated_items = {}
    for meal in planned_meals:
        recipe = get_recipe(meal.recipe_id)
        for ingredient in recipe.ingredients:
            adjusted_quantity = ingredient.quantity * (meal.servings / recipe.servings)
            
            if ingredient.item_id in consolidated_items:
                consolidated_items[ingredient.item_id] += adjusted_quantity
            else:
                consolidated_items[ingredient.item_id] = adjusted_quantity
    
    return consolidated_items
```

### Quantity Optimization Algorithm
```python
def get_optimized_quantity(recipe_id: str, item_id: str, user_id: str, base_quantity: float) -> float:
    feedback_history = get_quantity_feedback(recipe_id, item_id, user_id)
    
    if not feedback_history:
        return base_quantity
    
    # Berechne Durchschnitt der Anpassungsfaktoren
    avg_adjustment = sum(f.adjustment_factor for f in feedback_history) / len(feedback_history)
    
    return base_quantity * avg_adjustment
```

## Deployment Konfiguration

### Docker Setup (Optional)
```dockerfile
# Dockerfile für Backend
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables
```env
# Backend (.env)
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_JWT_SECRET=your_jwt_secret
DATABASE_URL=postgresql://...

# Frontend (.env)
VITE_API_URL=http://localhost:8000
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

Dieses Projekt bietet eine solide Grundlage für eine moderne Meal-Planning Anwendung mit allen gewünschten Features und Raum für zukünftige Erweiterungen.