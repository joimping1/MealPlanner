import uuid
from datetime import datetime, date
from typing import Dict, List, Optional

class DataStore:
    """In-memory data store for the meal planning application"""
    
    def __init__(self):
        self.items: Dict[str, dict] = {}
        self.recipes: Dict[str, dict] = {}
        self.meal_plans: Dict[str, dict] = {}
        self.shopping_list: Dict[str, dict] = {}
        
        # Initialize with some basic food categories and items
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with basic food categories"""
        # Basic food items
        basic_items = [
            ('Hähnchenbrust', 'Fleisch', 'g'),
            ('Rinderhackfleisch', 'Fleisch', 'g'),
            ('Lachs', 'Fisch', 'g'),
            ('Kartoffeln', 'Gemüse', 'g'),
            ('Zwiebeln', 'Gemüse', 'Stück'),
            ('Karotten', 'Gemüse', 'g'),
            ('Tomaten', 'Gemüse', 'Stück'),
            ('Paprika', 'Gemüse', 'Stück'),
            ('Reis', 'Getreide', 'g'),
            ('Nudeln', 'Getreide', 'g'),
            ('Milch', 'Milchprodukte', 'ml'),
            ('Eier', 'Milchprodukte', 'Stück'),
            ('Käse', 'Milchprodukte', 'g'),
            ('Butter', 'Milchprodukte', 'g'),
            ('Olivenöl', 'Öle & Fette', 'ml'),
            ('Salz', 'Gewürze', 'g'),
            ('Pfeffer', 'Gewürze', 'g'),
            ('Küchenrollen', 'Haushalt', 'Packung'),
            ('Spülmittel', 'Haushalt', 'Flasche'),
        ]
        
        for name, category, unit in basic_items:
            self.add_item(name, category, unit)
    
    def add_item(self, name: str, category: str, default_unit: str) -> str:
        """Add a new food item"""
        item_id = str(uuid.uuid4())
        self.items[item_id] = {
            'id': item_id,
            'name': name,
            'category': category,
            'default_unit': default_unit,
            'created_at': datetime.now()
        }
        return item_id
    
    def delete_item(self, item_id: str) -> bool:
        """Delete a food item"""
        if item_id in self.items:
            del self.items[item_id]
            return True
        return False
    
    def add_recipe(self, name: str, description: str, instructions: str,
                   prep_time: int, cook_time: int, servings: int, 
                   ingredients: List[dict]) -> str:
        """Add a new recipe"""
        recipe_id = str(uuid.uuid4())
        self.recipes[recipe_id] = {
            'id': recipe_id,
            'name': name,
            'description': description,
            'instructions': instructions,
            'prep_time': prep_time,
            'cook_time': cook_time,
            'servings': servings,
            'ingredients': ingredients,
            'created_at': datetime.now()
        }
        return recipe_id
    
    def update_recipe(self, recipe_id: str, name: str, description: str, 
                     instructions: str, prep_time: int, cook_time: int,
                     servings: int, ingredients: List[dict]) -> bool:
        """Update an existing recipe"""
        if recipe_id in self.recipes:
            self.recipes[recipe_id].update({
                'name': name,
                'description': description,
                'instructions': instructions,
                'prep_time': prep_time,
                'cook_time': cook_time,
                'servings': servings,
                'ingredients': ingredients,
                'updated_at': datetime.now()
            })
            return True
        return False
    
    def delete_recipe(self, recipe_id: str) -> bool:
        """Delete a recipe"""
        if recipe_id in self.recipes:
            del self.recipes[recipe_id]
            return True
        return False
    
    def add_meal_plan(self, week_start_date: date) -> str:
        """Add a new meal plan"""
        plan_id = str(uuid.uuid4())
        self.meal_plans[plan_id] = {
            'id': plan_id,
            'week_start_date': week_start_date,
            'planned_meals': [],
            'created_at': datetime.now()
        }
        return plan_id
    
    def add_planned_meal(self, plan_id: str, recipe_id: str, meal_date: date,
                        meal_type: str, servings: int, location: str, 
                        notes: str = '') -> bool:
        """Add a planned meal to a meal plan"""
        if plan_id in self.meal_plans and recipe_id in self.recipes:
            meal = {
                'recipe_id': recipe_id,
                'date': meal_date,
                'meal_type': meal_type,
                'servings': servings,
                'location': location,
                'notes': notes
            }
            self.meal_plans[plan_id]['planned_meals'].append(meal)
            return True
        return False
    
    def remove_planned_meal(self, plan_id: str, meal_index: int) -> bool:
        """Remove a planned meal from a meal plan"""
        if plan_id in self.meal_plans:
            planned_meals = self.meal_plans[plan_id]['planned_meals']
            if 0 <= meal_index < len(planned_meals):
                planned_meals.pop(meal_index)
                return True
        return False
    
    def delete_meal_plan(self, plan_id: str) -> bool:
        """Delete a meal plan"""
        if plan_id in self.meal_plans:
            del self.meal_plans[plan_id]
            return True
        return False
    
    def add_shopping_item(self, item_id: str, quantity: float, unit: str, notes: str = '') -> str:
        """Add item to general shopping list"""
        shopping_item_id = str(uuid.uuid4())
        self.shopping_list[shopping_item_id] = {
            'id': shopping_item_id,
            'item_id': item_id,
            'quantity': quantity,
            'unit': unit,
            'notes': notes,
            'checked': False,
            'created_at': datetime.now()
        }
        return shopping_item_id
    
    def remove_shopping_item(self, shopping_item_id: str) -> bool:
        """Remove item from general shopping list"""
        if shopping_item_id in self.shopping_list:
            del self.shopping_list[shopping_item_id]
            return True
        return False
    
    def toggle_shopping_item(self, shopping_item_id: str) -> bool:
        """Toggle checked status of shopping item"""
        if shopping_item_id in self.shopping_list:
            self.shopping_list[shopping_item_id]['checked'] = not self.shopping_list[shopping_item_id]['checked']
            return True
        return False
    
    def clear_checked_shopping_items(self) -> int:
        """Remove all checked items from shopping list"""
        to_remove = [item_id for item_id, item in self.shopping_list.items() if item['checked']]
        for item_id in to_remove:
            del self.shopping_list[item_id]
        return len(to_remove)
