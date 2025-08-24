# Overview

A meal planning web application designed to systematically organize weekly meal plans and automatically generate shopping lists. The app helps users reduce shopping frequency from 3 times per week to once per week through structured meal planning, recipe management, and intelligent quantity optimization.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Template Engine**: Jinja2 templates with Bootstrap 5 dark theme for responsive UI
- **JavaScript**: Vanilla JavaScript for client-side interactions (tooltips, form validation, shopping list functionality)
- **Styling**: Bootstrap 5 with custom CSS overrides for meal planning specific components
- **Icons**: Feather Icons for consistent iconography throughout the interface

## Backend Architecture
- **Framework**: Flask web application with session-based state management
- **Data Storage**: In-memory data store using Python dictionaries (DataStore class)
- **Route Structure**: RESTful-style routes for recipes, meal plans, items, and shopping lists
- **Business Logic**: Utility functions for recipe quantity calculations and shopping list consolidation

## Data Models
- **Items**: Food and household items with categories, units, and metadata
- **Recipes**: Structured recipes with ingredients, cooking times, and serving information
- **Meal Plans**: Weekly meal planning with flexible scheduling for home/office modes
- **Shopping Lists**: Auto-generated consolidated lists from meal plan requirements

## Key Features
- **Recipe Management**: CRUD operations for recipes with ingredient scaling based on servings
- **Weekly Planning**: Sunday planning sessions for complete week with homeoffice vs office modes
- **Smart Shopping Lists**: Automatic consolidation of ingredients across multiple recipes
- **Quantity Learning**: Feedback system for adjusting portions based on usage patterns
- **Multi-person Planning**: Support for varying person counts per meal

## Architecture Patterns
- **MVC Pattern**: Clear separation between templates (views), Flask routes (controllers), and data store (model)
- **Utility Functions**: Centralized business logic for calculations and data processing
- **Session Management**: Flask sessions for user state persistence
- **Responsive Design**: Mobile-first approach with Bootstrap grid system

# External Dependencies

- **Bootstrap 5**: Frontend CSS framework with dark theme support
- **Feather Icons**: Icon library for consistent UI elements
- **Flask**: Core web framework for Python backend
- **Jinja2**: Template engine integrated with Flask
- **Python Standard Library**: UUID generation, datetime handling, collections utilities

Note: The application currently uses an in-memory data store but is architected to easily migrate to a persistent database solution like PostgreSQL with minimal code changes.