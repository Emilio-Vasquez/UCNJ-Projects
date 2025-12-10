// ========================================
// Login & Authentication System
// This file handles all user login, signup, and session management
// ========================================

// ========================================
// Configuration: Settings for authentication
// ========================================
const AUTH_CONFIG = {
  // Session timeout: how long a user stays logged in (24 hours in milliseconds)
  SESSION_TIMEOUT: 24 * 60 * 60 * 1000,
  // Password validation rule: checks that password has uppercase, lowercase, number, special character, and is at least 8 chars
  PASSWORD_REGEX: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).{8,}$/, 
};

// ========================================
// Session Management: Create, get, and clear user sessions
// ========================================

// Create a new session for a logged-in user
// Save user info and expiration time to browser storage
function createSession(userEmail, userName = '', method = 'email') {
  // Create session object with user details
  const sessionData = {
    email: userEmail, // User's email address
    name: userName, // User's name
    method: method, // How they logged in (email only for this app)
    loginTime: Date.now(), // When they logged in
    expiresAt: Date.now() + AUTH_CONFIG.SESSION_TIMEOUT, // When session expires
  };
  
  // Save session as JSON string to browser storage
  localStorage.setItem('authSession', JSON.stringify(sessionData));
  // Also set a simple flag for quick authentication checks
  localStorage.setItem('isAuthenticated', 'true');
}

// Get the current user's session if it exists and hasn't expired
function getSession() {
  // Try to get session from browser storage
  const session = localStorage.getItem('authSession');
  if (!session) return null; // No session found
  
  try {
    // Parse the JSON string back into an object
    const data = JSON.parse(session);
    // Check if the session has expired (current time > expiration time)
    if (data.expiresAt < Date.now()) {
      // Session is expired, clear it
      clearSession();
      return null;
    }
    // Session is valid, return it
    return data;
  } catch (e) {
    // If parsing fails, session is corrupted, so clear it
    clearSession();
    return null;
  }
}

// Check if there is a valid user session currently
function isAuthenticated() {
  // Return true if getSession finds a valid session
  return getSession() !== null;
}

// Remove the user's session (logout)
function clearSession() {
  // Delete session data from browser storage
  localStorage.removeItem('authSession');
  localStorage.removeItem('isAuthenticated');
}

// Send user to the dashboard after successful login
function redirectToDashboard() {
  // Navigate to the main dashboard page
  window.location.href = 'to-do-project.html';
}

// Check on page load if user is already logged in
// If yes, skip the login page and go to dashboard
function checkAuthOnLoad() {
  // If user has a valid session, redirect them to dashboard
  if (isAuthenticated()) {
    redirectToDashboard();
  }
}

// ========================================
// Form Validation: Check if user inputs are correct
// ========================================

// Check if email format is valid
function validateEmail(email) {
  // Regular expression pattern for valid email format
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  // Return true if email matches the pattern
  return re.test(email);
}

// Check if password meets security requirements
function validatePassword(password) {
  // Test password against the AUTH_CONFIG regex pattern
  return AUTH_CONFIG.PASSWORD_REGEX.test(password);
}

// Check if two passwords match (for signup confirmation)
function validatePasswordsMatch(password, confirm) {
  // Return true if both passwords are identical
  return password === confirm;
}

// Clear all error messages from the form
function clearErrorMessages() {
  // Find all error message elements and empty them
  document.querySelectorAll('.error-msg').forEach(el => el.textContent = '');
  // Find all form message elements, empty them, and remove styling
  document.querySelectorAll('.form-message').forEach(el => {
    el.textContent = '';
    el.classList.remove('success', 'error');
  });
}

// Display an error message next to a specific form field
function showErrorMessage(fieldId, message) {
  // Find the error element for this field
  const errorEl = document.getElementById(fieldId);
  if (errorEl) {
    // Show the error message text
    errorEl.textContent = message;
  }
}

// Display a success or error message at the bottom of a form
function showFormMessage(formId, message, isSuccess = false) {
  // Choose which message element to use (login or signup form)
  const messageEl = document.getElementById(formId === 'login' ? 'loginMessage' : 'signupMessage');
  if (messageEl) {
    // Show the message text
    messageEl.textContent = message;
    // Remove any previous styling
    messageEl.classList.remove('success', 'error');
    // Add success or error styling
    messageEl.classList.add(isSuccess ? 'success' : 'error');
  }
}

// ========================================
// Login Handler: Process login form submission
// ========================================
function handleLogin(email, password) {
  // First, clear any previous error messages
  clearErrorMessages();

  // Validation: Check email is provided and valid
  if (!email || !validateEmail(email)) {
    showErrorMessage('loginEmailError', 'Please enter a valid email');
    return; // Stop processing if invalid
  }

  // Validation: Check password is provided
  if (!password) {
    showErrorMessage('loginPasswordError', 'Password is required');
    return; // Stop processing if missing
  }

  // Get all registered users from browser storage
  const storedUsers = JSON.parse(localStorage.getItem('appUsers') || '[]');
  // Try to find user with matching email and password
  const user = storedUsers.find(u => u.email === email && u.password === btoa(password));

  if (user) {
    // User found: show success message
    showFormMessage('login', 'Logging in...', true);
    // Wait a moment then redirect to dashboard
    setTimeout(() => {
      createSession(email, user.name, 'email');
      redirectToDashboard();
    }, 500);
  } else {
    // For demo mode: allow login with any email/password (not secure for production!)
    showFormMessage('login', 'Login successful! Redirecting...', true);
    // Wait a moment then redirect to dashboard
    setTimeout(() => {
      createSession(email, email.split('@')[0], 'email'); // Use part of email as name if not registered
      redirectToDashboard();
    }, 500);
  }
}

// ========================================
// Sign Up Handler: Process signup form submission
// ========================================
function handleSignUp(name, email, password, confirmPassword) {
  // First, clear any previous error messages
  clearErrorMessages();

  // Validation: Check name is provided and at least 2 characters
  if (!name || name.trim().length < 2) {
    showErrorMessage('signupNameError', 'Name must be at least 2 characters');
    return; // Stop processing if invalid
  }

  // Validation: Check email is provided and valid
  if (!email || !validateEmail(email)) {
    showErrorMessage('signupEmailError', 'Please enter a valid email');
    return; // Stop processing if invalid
  }

  // Validation: Check password meets security requirements
  if (!password || !validatePassword(password)) {
    showErrorMessage('signupPasswordError', 'Password must be at least 8 characters and include an uppercase letter, a number, and a special character');
    return; // Stop processing if weak
  }

  // Validation: Check passwords match
  if (!confirmPassword || !validatePasswordsMatch(password, confirmPassword)) {
    showErrorMessage('signupConfirmError', 'Passwords do not match');
    return; // Stop processing if don't match
  }

  // Check if this email is already registered
  const storedUsers = JSON.parse(localStorage.getItem('appUsers') || '[]');
  if (storedUsers.some(u => u.email === email)) {
    showErrorMessage('signupEmailError', 'Email already registered');
    return; // Stop processing if email exists
  }

  // Create new user object
  const newUser = {
    id: Date.now(), // Unique ID based on current time
    name: name, // User's full name
    email: email, // User's email
    password: btoa(password), // Encode password (basic encoding, NOT secure for production)
    createdAt: Date.now(), // Account creation time
  };

  // Add new user to the list
  storedUsers.push(newUser);
  // Save updated user list to browser storage
  localStorage.setItem('appUsers', JSON.stringify(storedUsers));

  // Show success message
  showFormMessage('signup', 'Account created! Logging in...', true);
  // Wait a moment then log them in and redirect to dashboard
  setTimeout(() => {
    createSession(email, name, 'email');
    redirectToDashboard();
  }, 500);
}

// ========================================
// Tab Switching: Let users switch between Login and Sign Up forms
// ========================================
function initializeTabs() {
  // Get all tab buttons
  const tabs = document.querySelectorAll('.auth-tab');
  // Get all forms
  const forms = document.querySelectorAll('.auth-form');

  // Add click handler to each tab
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      // Remove active styling from all tabs
      tabs.forEach(t => t.classList.remove('active'));
      // Remove active styling from all forms
      forms.forEach(f => f.classList.remove('active'));

      // Add active styling to clicked tab
      tab.classList.add('active');
      // Get the form name from the tab's data-tab attribute
      const tabName = tab.getAttribute('data-tab');
      // Find and show the corresponding form
      const form = document.getElementById(tabName + 'Form');
      if (form) form.classList.add('active');

      // Clear any error messages when switching tabs
      clearErrorMessages();
    });
  });
}

// ========================================
// Event Listeners: Wire up all form and button interactions
// ========================================
document.addEventListener('DOMContentLoaded', () => {
  // When page loads, check if user is already logged in
  checkAuthOnLoad();

  // Set up tab switching between Login and Sign Up
  initializeTabs();

  // Set up Login form submission handler
  const loginForm = document.getElementById('loginForm');
  if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
      e.preventDefault(); // Prevent page refresh
      // Get email and password from inputs
      const email = document.getElementById('loginEmail').value;
      const password = document.getElementById('loginPassword').value;
      // Process the login
      handleLogin(email, password);
    });
  }

  // Set up Sign Up form submission handler
  const signupForm = document.getElementById('signupForm');
  if (signupForm) {
    signupForm.addEventListener('submit', (e) => {
      e.preventDefault(); // Prevent page refresh
      // Get all form inputs
      const name = document.getElementById('signupName').value;
      const email = document.getElementById('signupEmail').value;
      const password = document.getElementById('signupPassword').value;
      const confirm = document.getElementById('signupConfirm').value;
      // Process the signup
      handleSignUp(name, email, password, confirm);
    });
  }

  // Set up Forgot Password link
  const forgotLink = document.getElementById('forgotLink');
  if (forgotLink) {
    forgotLink.addEventListener('click', (e) => {
      e.preventDefault(); // Prevent navigation
      // Show alert with instructions
      alert('Password reset functionality would be implemented here.\nFor demo purposes, please create a new account or contact support.');
    });
  }

  // Real-time password validation feedback (optional visual cue)
  const signupPassword = document.getElementById('signupPassword');
  if (signupPassword) {
    signupPassword.addEventListener('input', () => {
      // Get current password value
      const password = signupPassword.value;
      // Check if it meets requirements
      const isValid = validatePassword(password);
      // Could add visual feedback here (green checkmark, etc.)
    });
  }
});

// ========================================
// Export functions for testing
// ========================================
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    createSession,
    getSession,
    isAuthenticated,
    clearSession,
    validateEmail,
    validatePassword,
    validatePasswordsMatch,
  };
}

// ========================================
// Sign Up Handler: Process signup form submission
// ========================================
function handleSignUp(name, email, password, confirmPassword) {
  // First, clear any previous error messages
  clearErrorMessages();

  // Validation: Check name is provided and at least 2 characters
  if (!name || name.trim().length < 2) {
    showErrorMessage('signupNameError', 'Name must be at least 2 characters');
    return;
  }

  // Validation: Check email is provided and valid
  if (!email || !validateEmail(email)) {
    showErrorMessage('signupEmailError', 'Please enter a valid email');
    return;
  }

  // Validation: Check password meets security requirements
  if (!password || !validatePassword(password)) {
    showErrorMessage('signupPasswordError', 'Password must be at least 8 characters and include an uppercase letter, a number, and a special character');
    return;
  }

  // Validation: Check passwords match
  if (!confirmPassword || !validatePasswordsMatch(password, confirmPassword)) {
    showErrorMessage('signupConfirmError', 'Passwords do not match');
    return;
  }

  // Check if this email is already registered
  const storedUsers = JSON.parse(localStorage.getItem('appUsers') || '[]');
  if (storedUsers.some(u => u.email === email)) {
    showErrorMessage('signupEmailError', 'Email already registered');
    return;
  }

  // Create new user object
  const newUser = {
    id: Date.now(),
    name: name,
    email: email,
    password: btoa(password), // Basic encoding (NOT secure for production)
    createdAt: Date.now(),
  };

  // Add new user to list
  storedUsers.push(newUser);
  // Save updated list to browser storage
  localStorage.setItem('appUsers', JSON.stringify(storedUsers));

  // Show success message
  showFormMessage('signup', 'Account created! Logging in...', true);
  // Wait a moment then log them in and redirect
  setTimeout(() => {
    createSession(email, name, 'email');
    redirectToDashboard();
  }, 500);
}

// OAuth removed: the app now uses email/password only (no Google/Apple integration)

// ========================================
// Tab Switching: Let users switch between Login and Sign Up forms
// ========================================
function initializeTabs() {
  // Get all tab buttons
  const tabs = document.querySelectorAll('.auth-tab');
  // Get all forms
  const forms = document.querySelectorAll('.auth-form');

  // Add click handler to each tab button
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      // Remove active styling from all tabs and forms
      tabs.forEach(t => t.classList.remove('active'));
      forms.forEach(f => f.classList.remove('active'));

      // Add active styling to clicked tab
      tab.classList.add('active');
      // Get the form name from tab's data-tab attribute
      const tabName = tab.getAttribute('data-tab');
      // Find and show the corresponding form
      const form = document.getElementById(tabName + 'Form');
      if (form) form.classList.add('active');

      // Clear error messages when switching tabs
      clearErrorMessages();
    });
  });
}

// ========================================
// Event Listeners: Wire up all form and button interactions
// ========================================
document.addEventListener('DOMContentLoaded', () => {
  // When page loads, check if user is already logged in
  checkAuthOnLoad();

  // Set up tab switching between Login and Sign Up
  initializeTabs();

  // Set up Login form submission handler
  const loginForm = document.getElementById('loginForm');
  if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
      e.preventDefault(); // Prevent page refresh
      // Get values from form inputs
      const email = document.getElementById('loginEmail').value;
      const password = document.getElementById('loginPassword').value;
      // Process login
      handleLogin(email, password);
    });
  }

  // Set up Sign Up form submission handler
  const signupForm = document.getElementById('signupForm');
  if (signupForm) {
    signupForm.addEventListener('submit', (e) => {
      e.preventDefault(); // Prevent page refresh
      // Get all form field values
      const name = document.getElementById('signupName').value;
      const email = document.getElementById('signupEmail').value;
      const password = document.getElementById('signupPassword').value;
      const confirm = document.getElementById('signupConfirm').value;
      // Process signup
      handleSignUp(name, email, password, confirm);
    });
  }

  // OAuth removed: no Google/Apple buttons to initialize

  // Set up Forgot Password link
  const forgotLink = document.getElementById('forgotLink');
  if (forgotLink) {
    forgotLink.addEventListener('click', (e) => {
      e.preventDefault(); // Prevent navigation
      // Show alert with info
      alert('Password reset functionality would be implemented here.\nFor demo purposes, please create a new account or contact support.');
    });
  }

  // Real-time password strength feedback (optional)
  const signupPassword = document.getElementById('signupPassword');
  if (signupPassword) {
    signupPassword.addEventListener('input', () => {
      // Get current password input
      const password = signupPassword.value;
      // Test if it meets requirements
      const isValid = validatePassword(password);
      // Visual feedback could be added here
    });
  }
});

// ========================================
// Export functions for testing
// ========================================
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    createSession,
    getSession,
    isAuthenticated,
    clearSession,
    validateEmail,
    validatePassword,
    validatePasswordsMatch,
  };
}
