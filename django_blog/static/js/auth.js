// Authentication-specific JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Password visibility toggle
    const passwordToggles = document.querySelectorAll('.password-toggle');
    
    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const passwordInput = this.previousElementSibling;
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            
            // Toggle eye icon
            this.textContent = type === 'password' ? '👁️' : '👁️‍🗨️';
        });
    });
    
    // Form validation feedback
    const authForms = document.querySelectorAll('.auth-form');
    
    authForms.forEach(form => {
        const inputs = form.querySelectorAll('input[required]');
        
        inputs.forEach(input => {
            // Add real-time validation
            input.addEventListener('input', function() {
                validateField(this);
            });
            
            // Add validation on blur
            input.addEventListener('blur', function() {
                validateField(this);
            });
        });
        
        // Form submission validation
        form.addEventListener('submit', function(e) {
            let isValid = true;
            const inputs = this.querySelectorAll('input[required]');
            
            inputs.forEach(input => {
                if (!validateField(input)) {
                    isValid = false;
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showFormError('Please fill in all required fields correctly.');
            }
        });
    });
    
    // Close alert messages
    const closeButtons = document.querySelectorAll('.close-alert');
    
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.parentElement.style.display = 'none';
        });
    });
    
    // Auto-hide success messages after 5 seconds
    setTimeout(function() {
        const successAlerts = document.querySelectorAll('.alert-success');
        successAlerts.forEach(alert => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.style.display = 'none';
            }, 500);
        });
    }, 5000);
    
    // Helper functions
    function validateField(field) {
        const errorDiv = field.parentElement.querySelector('.auth-error') || 
                        createErrorDiv(field.parentElement);
        
        if (field.validity.valid) {
            errorDiv.textContent = '';
            field.classList.remove('invalid');
            field.classList.add('valid');
            return true;
        } else {
            showFieldError(field, errorDiv);
            return false;
        }
    }
    
    function createErrorDiv(parent) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'auth-error';
        parent.appendChild(errorDiv);
        return errorDiv;
    }
    
    function showFieldError(field, errorDiv) {
        field.classList.add('invalid');
        field.classList.remove('valid');
        
        if (field.validity.valueMissing) {
            errorDiv.textContent = 'This field is required.';
        } else if (field.validity.typeMismatch) {
            errorDiv.textContent = 'Please enter a valid email address.';
        } else if (field.validity.tooShort) {
            errorDiv.textContent = `Minimum length is ${field.minLength} characters.`;
        } else if (field.validity.patternMismatch) {
            errorDiv.textContent = 'Please match the requested format.';
        } else {
            errorDiv.textContent = 'Please enter a valid value.';
        }
    }
    
    function showFormError(message) {
        // Create or find error container
        let errorContainer = document.querySelector('.form-error-container');
        if (!errorContainer) {
            errorContainer = document.createElement('div');
            errorContainer.className = 'alert alert-error form-error-container';
            const form = document.querySelector('.auth-form');
            form.parentElement.insertBefore(errorContainer, form);
        }
        
        errorContainer.innerHTML = `
            ${message}
            <button type="button" class="close-alert">&times;</button>
        `;
        
        // Add event listener to close button
        errorContainer.querySelector('.close-alert').addEventListener('click', function() {
            errorContainer.style.display = 'none';
        });
    }
    
    // Password strength indicator (for registration page)
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    
    passwordInputs.forEach(input => {
        if (input.name.includes('password')) {
            input.addEventListener('input', function() {
                checkPasswordStrength(this.value);
            });
        }
    });
    
    function checkPasswordStrength(password) {
        const strengthIndicator = document.querySelector('.password-strength') || 
                                 createPasswordStrengthIndicator();
        
        let strength = 0;
        let tips = [];
        
        // Check password length
        if (password.length >= 8) strength++;
        else tips.push('Make it at least 8 characters long.');
        
        // Check for mixed case
        if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
        else tips.push('Use both uppercase and lowercase letters.');
        
        // Check for numbers
        if (/\d/.test(password)) strength++;
        else tips.push('Include at least one number.');
        
        // Check for special characters
        if (/[^A-Za-z0-9]/.test(password)) strength++;
        else tips.push('Include at least one special character.');
        
        // Update strength indicator
        const strengthText = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong'][strength];
        const strengthClass = ['very-weak', 'weak', 'fair', 'good', 'strong'][strength];
        
        strengthIndicator.innerHTML = `
            <div class="strength-bar">
                <div class="strength-fill ${strengthClass}" style="width: ${strength * 25}%"></div>
            </div>
            <div class="strength-text">Password strength: <strong>${strengthText}</strong></div>
            ${tips.length > 0 ? `<div class="strength-tips">${tips.join(' ')}</div>` : ''}
        `;
    }
    
    function createPasswordStrengthIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'password-strength';
        const passwordField = document.querySelector('input[type="password"][name*="password"]');
        passwordField.parentElement.appendChild(indicator);
        return indicator;
    }
});
