from typing import List, Dict
from collections import defaultdict

def calculate_recipe_quantities(base_quantity: float, base_servings: int, target_servings: int) -> float:
    """Calculate scaled quantities for different serving sizes"""
    if base_servings == 0:
        return base_quantity
    
    scaling_factor = target_servings / base_servings
    return base_quantity * scaling_factor

def consolidate_shopping_items(shopping_items: List[Dict]) -> List[Dict]:
    """Consolidate shopping list items by combining same items with same units"""
    consolidated = defaultdict(lambda: {
        'item_id': '',
        'item_name': '',
        'quantity': 0,
        'unit': '',
        'category': '',
        'sources': []
    })
    
    for item in shopping_items:
        # Create a unique key for consolidation (item_id + unit)
        key = f"{item['item_id']}_{item['unit']}"
        
        if consolidated[key]['item_id'] == '':
            # First occurrence of this item+unit combination
            consolidated[key].update({
                'item_id': item['item_id'],
                'item_name': item['item_name'],
                'quantity': item['quantity'],
                'unit': item['unit'],
                'category': item['category'],
                'sources': [{
                    'recipe_name': item['recipe_name'],
                    'meal_date': item['meal_date'],
                    'meal_type': item['meal_type'],
                    'quantity': item['quantity']
                }]
            })
        else:
            # Add to existing item
            consolidated[key]['quantity'] += item['quantity']
            consolidated[key]['sources'].append({
                'recipe_name': item['recipe_name'],
                'meal_date': item['meal_date'],
                'meal_type': item['meal_type'],
                'quantity': item['quantity']
            })
    
    # Convert to list and round quantities
    result = []
    for item in consolidated.values():
        item['quantity'] = round(item['quantity'], 2)
        result.append(item)
    
    # Sort by category and name
    result.sort(key=lambda x: (x['category'], x['item_name']))
    
    return result

def format_quantity(quantity: float, unit: str) -> str:
    """Format quantity for display"""
    if quantity == int(quantity):
        return f"{int(quantity)} {unit}"
    else:
        return f"{quantity:.1f} {unit}"

def get_week_dates(week_start_date):
    """Get all dates for a week starting from week_start_date"""
    from datetime import timedelta
    
    dates = []
    for i in range(7):
        dates.append(week_start_date + timedelta(days=i))
    return dates

def get_meal_type_display(meal_type: str) -> str:
    """Get display name for meal type"""
    meal_types = {
        'breakfast': 'Frühstück',
        'lunch': 'Mittagessen',
        'dinner': 'Abendessen'
    }
    return meal_types.get(meal_type, meal_type)

def get_location_display(location: str) -> str:
    """Get display name for location"""
    locations = {
        'home': 'Zuhause',
        'office': 'Büro'
    }
    return locations.get(location, location)
