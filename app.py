import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime, timedelta
from data_store import DataStore
from utils import calculate_recipe_quantities, consolidate_shopping_items

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "fallback-secret-key")

# Initialize data store
data_store = DataStore()

# Add custom Jinja2 filters
@app.template_filter('add_days')
def add_days_filter(date, days):
    """Add days to a date"""
    from datetime import timedelta
    return date + timedelta(days=days)

@app.template_filter('nl2br')
def nl2br_filter(value):
    """Convert newlines to <br> tags"""
    return value.replace('\n', '<br>\n')

@app.route('/')
def index():
    """Dashboard showing overview of recent activity"""
    recent_recipes = list(data_store.recipes.values())[-5:]
    current_week_plans = []
    
    # Get current week's meal plans
    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())
    
    for plan in data_store.meal_plans.values():
        if plan['week_start_date'] == week_start:
            current_week_plans.append(plan)
    
    return render_template('index.html', 
                         recent_recipes=recent_recipes,
                         current_week_plans=current_week_plans)

@app.route('/items')
def items():
    """Food items management page"""
    category_filter = request.args.get('category', '')
    
    filtered_items = data_store.items.values()
    if category_filter:
        filtered_items = [item for item in filtered_items if item['category'] == category_filter]
    
    categories = list(set(item['category'] for item in data_store.items.values()))
    
    return render_template('items.html', 
                         items=filtered_items,
                         categories=categories,
                         selected_category=category_filter)

@app.route('/items/add', methods=['POST'])
def add_item():
    """Add new food item"""
    name = request.form.get('name', '').strip()
    category = request.form.get('category', '').strip()
    default_unit = request.form.get('default_unit', '').strip()
    
    if not all([name, category, default_unit]):
        flash('Alle Felder sind erforderlich', 'error')
        return redirect(url_for('items'))
    
    item_id = data_store.add_item(name, category, default_unit)
    flash(f'Lebensmittel "{name}" wurde hinzugefügt', 'success')
    
    return redirect(url_for('items'))

@app.route('/items/<item_id>/delete', methods=['POST'])
def delete_item(item_id):
    """Delete food item"""
    if data_store.delete_item(item_id):
        flash('Lebensmittel wurde gelöscht', 'success')
    else:
        flash('Lebensmittel nicht gefunden', 'error')
    
    return redirect(url_for('items'))

@app.route('/recipes')
def recipes():
    """Recipe management page"""
    return render_template('recipes.html', recipes=data_store.recipes.values())

@app.route('/recipes/<recipe_id>')
def recipe_detail(recipe_id):
    """Recipe detail page"""
    recipe = data_store.recipes.get(recipe_id)
    if not recipe:
        flash('Rezept nicht gefunden', 'error')
        return redirect(url_for('recipes'))
    
    # Calculate ingredients with item details
    ingredients_with_details = []
    for ingredient in recipe['ingredients']:
        item = data_store.items.get(ingredient['item_id'])
        if item:
            ingredients_with_details.append({
                **ingredient,
                'item_name': item['name'],
                'item_category': item['category']
            })
    
    return render_template('recipe_detail.html', 
                         recipe=recipe,
                         ingredients=ingredients_with_details)

@app.route('/recipes/new')
def new_recipe():
    """New recipe form"""
    return render_template('recipe_form.html', 
                         recipe=None,
                         items=data_store.items.values())

@app.route('/recipes/<recipe_id>/edit')
def edit_recipe(recipe_id):
    """Edit recipe form"""
    recipe = data_store.recipes.get(recipe_id)
    if not recipe:
        flash('Rezept nicht gefunden', 'error')
        return redirect(url_for('recipes'))
    
    return render_template('recipe_form.html', 
                         recipe=recipe,
                         items=data_store.items.values())

@app.route('/recipes/save', methods=['POST'])
def save_recipe():
    """Save recipe (create or update)"""
    recipe_id = request.form.get('recipe_id')
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    instructions = request.form.get('instructions', '').strip()
    prep_time = request.form.get('prep_time', type=int) or 0
    cook_time = request.form.get('cook_time', type=int) or 0
    servings = request.form.get('servings', type=int) or 2
    
    if not name:
        flash('Rezeptname ist erforderlich', 'error')
        return redirect(url_for('new_recipe'))
    
    # Parse ingredients
    ingredients = []
    ingredient_count = len([key for key in request.form.keys() if key.startswith('ingredient_item_')])
    
    for i in range(ingredient_count):
        item_id = request.form.get(f'ingredient_item_{i}')
        quantity = request.form.get(f'ingredient_quantity_{i}', type=float)
        unit = request.form.get(f'ingredient_unit_{i}', '').strip()
        notes = request.form.get(f'ingredient_notes_{i}', '').strip()
        
        if item_id and quantity and unit:
            ingredients.append({
                'item_id': item_id,
                'quantity': quantity,
                'unit': unit,
                'notes': notes
            })
    
    if recipe_id:
        # Update existing recipe
        data_store.update_recipe(recipe_id, name, description, instructions, 
                               prep_time, cook_time, servings, ingredients)
        flash(f'Rezept "{name}" wurde aktualisiert', 'success')
    else:
        # Create new recipe
        recipe_id = data_store.add_recipe(name, description, instructions, 
                                        prep_time, cook_time, servings, ingredients)
        flash(f'Rezept "{name}" wurde erstellt', 'success')
    
    return redirect(url_for('recipe_detail', recipe_id=recipe_id))

@app.route('/recipes/<recipe_id>/delete', methods=['POST'])
def delete_recipe(recipe_id):
    """Delete recipe"""
    if data_store.delete_recipe(recipe_id):
        flash('Rezept wurde gelöscht', 'success')
    else:
        flash('Rezept nicht gefunden', 'error')
    
    return redirect(url_for('recipes'))

@app.route('/meal-plans')
def meal_plans():
    """Meal plans overview"""
    plans = sorted(data_store.meal_plans.values(), 
                  key=lambda x: x['week_start_date'], reverse=True)
    return render_template('meal_plans.html', meal_plans=plans)

@app.route('/meal-plans/new')
def new_meal_plan():
    """New meal plan form"""
    return render_template('meal_plan_form.html', 
                         meal_plan=None,
                         recipes=data_store.recipes.values())

@app.route('/meal-plans/<plan_id>')
def meal_plan_detail(plan_id):
    """Meal plan detail page"""
    meal_plan = data_store.meal_plans.get(plan_id)
    if not meal_plan:
        flash('Wochenplan nicht gefunden', 'error')
        return redirect(url_for('meal_plans'))
    
    # Get planned meals with recipe details
    meals_with_details = []
    for meal in meal_plan['planned_meals']:
        recipe = data_store.recipes.get(meal['recipe_id'])
        if recipe:
            meals_with_details.append({
                **meal,
                'recipe_name': recipe['name'],
                'recipe': recipe
            })
    
    return render_template('meal_plan_detail.html', 
                         meal_plan=meal_plan,
                         planned_meals=meals_with_details,
                         recipes=data_store.recipes.values())

@app.route('/meal-plans/save', methods=['POST'])
def save_meal_plan():
    """Save meal plan"""
    plan_id = request.form.get('plan_id')
    week_start_str = request.form.get('week_start_date')
    if not week_start_str:
        flash('Wochenbeginn ist erforderlich', 'error')
        return redirect(url_for('new_meal_plan'))
    week_start_date = datetime.strptime(week_start_str, '%Y-%m-%d').date()
    
    if plan_id:
        # Update existing plan
        data_store.meal_plans[plan_id]['week_start_date'] = week_start_date
        flash('Wochenplan wurde aktualisiert', 'success')
    else:
        # Create new plan
        plan_id = data_store.add_meal_plan(week_start_date)
        flash('Neuer Wochenplan wurde erstellt', 'success')
    
    return redirect(url_for('meal_plan_detail', plan_id=plan_id))

@app.route('/meal-plans/<plan_id>/add-meal', methods=['POST'])
def add_planned_meal(plan_id):
    """Add meal to plan"""
    recipe_id = request.form.get('recipe_id')
    date_str = request.form.get('date')
    meal_type = request.form.get('meal_type')
    servings = int(request.form.get('servings', 2))
    location = request.form.get('location', 'home')
    notes = request.form.get('notes', '').strip()
    
    if not all([recipe_id, date_str, meal_type]):
        flash('Rezept, Datum und Mahlzeit sind erforderlich', 'error')
        return redirect(url_for('meal_plan_detail', plan_id=plan_id))
        
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    if data_store.add_planned_meal(plan_id, recipe_id, date, meal_type, servings, location, notes):
        flash('Mahlzeit wurde hinzugefügt', 'success')
    else:
        flash('Fehler beim Hinzufügen der Mahlzeit', 'error')
    
    return redirect(url_for('meal_plan_detail', plan_id=plan_id))

@app.route('/meal-plans/<plan_id>/remove-meal/<int:meal_index>', methods=['POST'])
def remove_planned_meal(plan_id, meal_index):
    """Remove meal from plan"""
    if data_store.remove_planned_meal(plan_id, meal_index):
        flash('Mahlzeit wurde entfernt', 'success')
    else:
        flash('Fehler beim Entfernen der Mahlzeit', 'error')
    
    return redirect(url_for('meal_plan_detail', plan_id=plan_id))

@app.route('/meal-plans/<plan_id>/shopping-list')
def shopping_list(plan_id):
    """Generate and display shopping list"""
    meal_plan = data_store.meal_plans.get(plan_id)
    if not meal_plan:
        flash('Wochenplan nicht gefunden', 'error')
        return redirect(url_for('meal_plans'))
    
    # Generate shopping list
    shopping_items = []
    
    for planned_meal in meal_plan['planned_meals']:
        recipe = data_store.recipes.get(planned_meal['recipe_id'])
        if not recipe:
            continue
        
        # Calculate quantities for this meal's servings
        for ingredient in recipe['ingredients']:
            item = data_store.items.get(ingredient['item_id'])
            if not item:
                continue
            
            # Scale quantity based on servings
            scaled_quantity = calculate_recipe_quantities(
                ingredient['quantity'], 
                recipe['servings'], 
                planned_meal['servings']
            )
            
            shopping_items.append({
                'item_id': ingredient['item_id'],
                'item_name': item['name'],
                'quantity': scaled_quantity,
                'unit': ingredient['unit'],
                'category': item['category'],
                'recipe_name': recipe['name'],
                'meal_date': planned_meal['date'].strftime('%d.%m.%Y'),
                'meal_type': planned_meal['meal_type']
            })
    
    # Consolidate items
    consolidated_items = consolidate_shopping_items(shopping_items)
    
    # Group by category
    categories = {}
    for item in consolidated_items:
        category = item['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(item)
    
    return render_template('shopping_list.html', 
                         meal_plan=meal_plan,
                         categories=categories,
                         total_items=len(consolidated_items))

@app.route('/meal-plans/<plan_id>/delete', methods=['POST'])
def delete_meal_plan(plan_id):
    """Delete meal plan"""
    if data_store.delete_meal_plan(plan_id):
        flash('Wochenplan wurde gelöscht', 'success')
    else:
        flash('Wochenplan nicht gefunden', 'error')
    
    return redirect(url_for('meal_plans'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
