// Main JavaScript file for Meal Planner application

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert-dismissible');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Enhance form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Shopping list functionality
    initializeShoppingList();
    
    // Recipe form enhancements
    initializeRecipeForm();
    
    // Meal planning enhancements
    initializeMealPlanning();
});

// Shopping List Functions
function initializeShoppingList() {
    const checkboxes = document.querySelectorAll('.shopping-list input[type="checkbox"]');
    
    checkboxes.forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
            const label = this.closest('.form-check').querySelector('label');
            if (this.checked) {
                label.classList.add('shopping-item-checked');
            } else {
                label.classList.remove('shopping-item-checked');
            }
            updateShoppingProgress();
        });
    });
}

function updateShoppingProgress() {
    const total = document.querySelectorAll('.shopping-list input[type="checkbox"]').length;
    const checked = document.querySelectorAll('.shopping-list input[type="checkbox"]:checked').length;
    
    const progressBar = document.querySelector('.shopping-progress');
    if (progressBar) {
        const percentage = total > 0 ? (checked / total) * 100 : 0;
        progressBar.style.width = percentage + '%';
        progressBar.setAttribute('aria-valuenow', percentage);
    }
}

// Recipe Form Functions
function initializeRecipeForm() {
    const addIngredientBtn = document.querySelector('[onclick="addIngredient()"]');
    if (addIngredientBtn) {
        // Ingredient form is already handled by inline functions
        // Add any additional enhancements here
        
        // Auto-suggest units based on selected item
        document.addEventListener('change', function(e) {
            if (e.target.name && e.target.name.startsWith('ingredient_item_')) {
                const index = e.target.name.split('_')[2];
                const unitField = document.querySelector(`input[name="ingredient_unit_${index}"]`);
                const selectedOption = e.target.selectedOptions[0];
                
                if (selectedOption && unitField && !unitField.value) {
                    // Extract default unit from option text if available
                    const optionText = selectedOption.textContent;
                    const unitMatch = optionText.match(/\(([^)]+)\)$/);
                    if (unitMatch) {
                        // This would need item data to work properly
                        // For now, we'll leave it empty
                    }
                }
            }
        });
    }
}

// Meal Planning Functions
function initializeMealPlanning() {
    // Auto-set reasonable defaults for meal planning forms
    const servingsInput = document.querySelector('input[name="servings"]');
    if (servingsInput && !servingsInput.value) {
        servingsInput.value = 2;
    }
    
    // Enhance date inputs with better UX
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(function(input) {
        // Add visual feedback for date selection
        input.addEventListener('change', function() {
            this.classList.add('is-valid');
        });
    });
    
    // Location-based meal type suggestions
    const locationSelect = document.querySelector('select[name="location"]');
    const mealTypeSelect = document.querySelector('select[name="meal_type"]');
    
    if (locationSelect && mealTypeSelect) {
        locationSelect.addEventListener('change', function() {
            if (this.value === 'office' && mealTypeSelect.value === 'lunch') {
                // Suggest changing to breakfast or dinner for office days
                const message = 'Tipp: Für Bürotage wird meist nur Frühstück oder Abendessen geplant.';
                showToast(message, 'info');
            }
        });
    }
}

// Utility Functions
function showToast(message, type = 'info') {
    // Create a simple toast notification
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(toast);
    
    // Auto-remove after 4 seconds
    setTimeout(function() {
        if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
        }
    }, 4000);
}

function confirmDelete(message = 'Sind Sie sicher, dass Sie diesen Eintrag löschen möchten?') {
    return confirm(message);
}

// Form Helper Functions
function resetForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.reset();
        form.classList.remove('was-validated');
    }
}

function validateRequired(input) {
    if (!input.value.trim()) {
        input.classList.add('is-invalid');
        return false;
    } else {
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
        return true;
    }
}

// Recipe scaling functionality
function scaleRecipe(factor, recipeId) {
    const quantityElements = document.querySelectorAll(`[data-recipe="${recipeId}"] .quantity-value`);
    
    quantityElements.forEach(function(element) {
        const originalQuantity = parseFloat(element.dataset.original || element.textContent);
        const newQuantity = (originalQuantity * factor).toFixed(1);
        element.textContent = newQuantity;
        
        if (!element.dataset.original) {
            element.dataset.original = originalQuantity;
        }
    });
}

// Local storage helpers for shopping lists
function saveShoppingListState(planId, state) {
    const key = `shopping_list_${planId}`;
    localStorage.setItem(key, JSON.stringify(state));
}

function loadShoppingListState(planId) {
    const key = `shopping_list_${planId}`;
    const saved = localStorage.getItem(key);
    return saved ? JSON.parse(saved) : {};
}

// Print functionality
function printShoppingList() {
    // Hide non-printable elements before printing
    const elementsToHide = document.querySelectorAll('.btn, .alert, .navbar');
    elementsToHide.forEach(el => el.style.display = 'none');
    
    window.print();
    
    // Restore elements after printing
    elementsToHide.forEach(el => el.style.display = '');
}

// Search functionality (if needed)
function filterItems(searchTerm, containerSelector) {
    const container = document.querySelector(containerSelector);
    if (!container) return;
    
    const items = container.querySelectorAll('.list-item, .card');
    const term = searchTerm.toLowerCase();
    
    items.forEach(function(item) {
        const text = item.textContent.toLowerCase();
        if (text.includes(term)) {
            item.style.display = '';
        } else {
            item.style.display = 'none';
        }
    });
}

// Add global error handler
window.addEventListener('error', function(e) {
    console.error('JavaScript Error:', e.error);
    showToast('Ein Fehler ist aufgetreten. Bitte laden Sie die Seite neu.', 'danger');
});

// Template filters for Jinja2 (custom functions)
function addDays(date, days) {
    const result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
}

// Export functions for use in templates
window.MealPlanner = {
    showToast,
    confirmDelete,
    resetForm,
    validateRequired,
    scaleRecipe,
    printShoppingList,
    filterItems,
    saveShoppingListState,
    loadShoppingListState
};
