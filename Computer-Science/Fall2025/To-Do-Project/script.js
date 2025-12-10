// ========================================
// Dashboard Main Script
// This file handles all dashboard functionality: sidebar, weather, news, tasks, search, and logout
// ========================================

// Configuration: Default city and API keys for external services
const DEFAULT_CITY = 'Elizabeth';
// Weather API key from OpenWeatherMap service (used to fetch real-time weather data)
const WEATHER_API_KEY = '3881c52d695bd30fc33a09bf7ed5e071';
// News API key from NewsAPI service (used to fetch current events/headlines)
const NEWS_API_KEY = '52bb2c0d751248e78890cef156f49958';

// ========================================
// Sidebar Management: Show and hide the navigation menu
// ========================================

// Function: Open sidebar - adds 'open' styling class and hides the open button
function openSidebar() {
    // Find sidebar element and add 'open' class (triggers CSS animation)
    document.getElementById('mySidebar').classList.add('open');
    // Hide the open button so user doesn't click it again while sidebar is open
    document.getElementById('openSidebarBtn').style.display = 'none';
}

// Function: Close sidebar - removes 'open' styling class and shows the open button
function closeSidebar() {
    // Find sidebar element and remove 'open' class (triggers CSS reverse animation)
    document.getElementById('mySidebar').classList.remove('open');
    // Show the open button again so user can re-open sidebar
    document.getElementById('openSidebarBtn').style.display = 'block';
}

// ========================================
// Weather Widget: Fetch and display current weather data
// ========================================

// Function: Fetch weather - calls OpenWeatherMap API to get current weather for a city
async function fetchWeather() {
    // Find the element where weather data will be displayed
    const weatherDiv = document.getElementById('weatherData');
    // Find the element showing which city we're displaying weather for
    const currentCityLabel = document.getElementById('currentCity');
    
    // Get the city name from browser storage, or use default city if not set
    const storedCity = localStorage.getItem('city') || DEFAULT_CITY;
    
    // If weather widget doesn't exist on this page, exit early (return does nothing)
    if (!weatherDiv) return;
    
    // Update the city label to show which city we're displaying
    if (currentCityLabel) currentCityLabel.textContent = 'City: ' + storedCity;
    
    try {
        // Make API request to OpenWeatherMap with city name, API key, and request for Celsius
        const res = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(storedCity)}&appid=${WEATHER_API_KEY}&units=metric`);
        
        // Convert response from JSON format into JavaScript object
        const data = await res.json();
        
        // Check if API returned successful response (status code 200)
        if (data.cod === 200) {
            // Build HTML to display: city name, weather description, temperature, humidity
            weatherDiv.innerHTML = `
                <strong>${data.name}</strong><br>
                ${data.weather[0].main}, ${data.weather[0].description}<br>
                Temp: ${data.main.temp}&deg;C, Humidity: ${data.main.humidity}%
            `;
        } else {
            // If API returned error, display message
            weatherDiv.innerText = 'Weather data unavailable.';
            console.warn('Weather API error:', data);
        }
    } catch (err) {
        // If network request failed or other error occurred, display message
        weatherDiv.innerText = 'Weather data unavailable.';
        console.error(err);
    }
}

// ========================================
// News/Events Widget: Fetch and display current news headlines
// ========================================

// Function: Fetch news - calls NewsAPI to get latest news headlines
async function fetchNews() {
    // Find the element where news headlines will be displayed
    const eventsDiv = document.getElementById('eventsData');
    
    // If news widget doesn't exist on this page, exit early
    if (!eventsDiv) return;
    
    try {
        // Make API request to NewsAPI to get top 3 US news headlines
        const res = await fetch(`https://newsapi.org/v2/top-headlines?country=us&pageSize=3&apiKey=${NEWS_API_KEY}`);
        
        // Convert response from JSON format into JavaScript object
        const data = await res.json();
        
        // Check if API returned successful response with articles
        if (data.status === 'ok' && data.articles.length > 0) {
            // For each article, create a clickable link that opens in new tab
            eventsDiv.innerHTML = data.articles.map(a => `<div class="event-item"><a href="${a.url}" target="_blank">${a.title}</a></div>`).join('');
        } else {
            // If no articles found, display message
            eventsDiv.innerText = 'No current events found.';
            console.warn('News API returned no articles or error:', data);
        }
    } catch (err) {
        // If network request failed or other error occurred, display message
        eventsDiv.innerText = 'Events data unavailable.';
        console.error(err);
    }
}

// ========================================
// Task Management: Save, load, and add tasks from storage
// ========================================

// Variable: Store tasks for this page session (simple array of strings)
let tasks = [];

// Function: Save tasks - writes current tasks array to browser storage so they persist
function saveTasks() {
    // Convert tasks array to JSON string and save to localStorage under 'tasks' key
    localStorage.setItem('tasks', JSON.stringify(tasks));
}

// Function: Load tasks - reads tasks from storage and displays them on page
function loadTasks() {
    // Get the JSON string from storage
    const raw = localStorage.getItem('tasks');
    
    // If data exists in storage, convert it from JSON back to array
    if (raw) {
        try {
            tasks = JSON.parse(raw);
        } catch {
            // If JSON conversion fails (corrupted data), start with empty array
            tasks = [];
        }
    }
    
    // Find the list element where tasks will be displayed
    const list = document.getElementById('taskList');
    
    // If task list doesn't exist on this page, exit early
    if (!list) return;
    
    // Clear the list (remove any old HTML)
    list.innerHTML = '';
    
    // For each task in the array, create a list item
    tasks.forEach(text => {
        // Create a new <li> element
        const li = document.createElement('li');
        // Set the text of the list item to the task text
        li.textContent = text;
        // Add CSS class for styling
        li.className = 'task-item';
        // Add click handler: when user clicks task, remove it from list
        li.addEventListener('click', () => { removeTaskElement(li, text); });
        // Add the list item to the page
        list.appendChild(li);
    });
}

// Function: Add task - takes text from input field and routes to appropriate storage location
function addTask() {
    // Find the input field where user typed task text
    const input = document.getElementById('newTaskInput');
    // If input field doesn't exist, exit early
    if (!input) return;
    
    // Get the text user typed and remove leading/trailing whitespace
    const text = input.value.trim();
    // If text is empty, don't create a task (just exit)
    if (!text) return;

    // Find the dropdown selector that chooses where task should go
    const destSelect = document.getElementById('taskDestination');
    // Get the selected destination ('local', 'today', or 'future') or default to 'local'
    const dest = destSelect ? destSelect.value : 'local';

    // Route 1: If user selected "today", add to today's tasks
    if (dest === 'today') {
        // Use 'todayTodos' storage key (used by today.html page)
        const key = 'todayTodos';
        let arr = [];
        
        // Get existing today tasks from storage
        const raw = localStorage.getItem(key);
        if (raw) {
            try {
                arr = JSON.parse(raw);
            } catch (e) {
                arr = [];
            }
        }
        
        // Create new task object with unique ID, text, completion status, priority, and timestamp
        arr.push({
            id: Date.now(), // Unique ID based on current time
            text: text, // The task text
            completed: false, // Not done yet
            priority: 'normal', // Default priority level
            createdAt: Date.now() // When task was created
        });
        
        // Save updated array back to storage
        localStorage.setItem(key, JSON.stringify(arr));
    }
    // Route 2: If user selected "future", add to week's tasks
    else if (dest === 'future') {
        // Use 'weekTasks' storage key (used by future.html page)
        let weekTasks = {};
        
        // Get existing week tasks from storage
        const raw = localStorage.getItem('weekTasks');
        if (raw) {
            try {
                weekTasks = JSON.parse(raw);
            } catch (e) {
                weekTasks = {};
            }
        }
        
        // Get today's date in YYYY-MM-DD format (used as key for today's tasks)
        const dayKey = new Date().toISOString().split('T')[0];
        
        // If this day doesn't have tasks yet, create empty array
        if (!weekTasks[dayKey]) weekTasks[dayKey] = [];
        
        // Add new task to today's date
        weekTasks[dayKey].push({
            id: Date.now(), // Unique ID based on current time
            text: text, // The task text
            completed: false // Not done yet
        });
        
        // Save updated week tasks back to storage
        localStorage.setItem('weekTasks', JSON.stringify(weekTasks));
    }
    // Route 3: If user selected "local", keep task on this page only
    else {
        // Find the task list element on this page
        const list = document.getElementById('taskList');
        if (list) {
            // Create new <li> element for task
            const li = document.createElement('li');
            // Set task text
            li.textContent = text;
            // Add styling class
            li.className = 'task-item';
            // Add click handler to remove task when clicked
            li.addEventListener('click', () => { removeTaskElement(li, text); });
            // Add list item to page
            list.appendChild(li);
        }
        // Add task text to tasks array
        tasks.push(text);
        // Save tasks array to storage
        saveTasks();
    }

    // Clear the input field so user can type next task
    input.value = '';
}

// ========================================
// Completion Rate Widget: Track task completion percentage
// ========================================

// Function: Update completion rate - calculates and displays task completion percentage
function updateCompletionRate() {
    // Get today's tasks from storage
    const todayTodosRaw = localStorage.getItem('todayTodos');
    let todayTodos = [];
    
    // Convert JSON to array
    if (todayTodosRaw) {
        try {
            todayTodos = JSON.parse(todayTodosRaw);
        } catch (e) {
            todayTodos = [];
        }
    }

    // Count how many tasks are marked as completed
    const completed = todayTodos.filter(t => t.completed).length;
    // Count total number of tasks
    const total = todayTodos.length;
    // Calculate percentage (0% if no tasks)
    const percent = total === 0 ? 0 : Math.round((completed / total) * 100);

    // Find and update the percentage text display
    const percentEl = document.getElementById('completionPercent');
    if (percentEl) percentEl.textContent = percent;
    
    // Find and update the completed count display
    const completedEl = document.getElementById('completedCount');
    if (completedEl) completedEl.textContent = completed;
    
    // Find and update the total count display
    const totalEl = document.getElementById('totalCount');
    if (totalEl) totalEl.textContent = total;

    // Update SVG progress ring graphic (circular progress bar)
    const ring = document.getElementById('progressRing');
    if (ring) {
        // Calculate the circumference (perimeter) of the circle
        const circumference = 2 * Math.PI * 35;
        // Calculate how much of the circle should be drawn based on percentage
        const offset = circumference - (percent / 100) * circumference;
        // Apply the calculations to the SVG element to draw progress ring
        ring.style.strokeDasharray = circumference;
        ring.style.strokeDashoffset = offset;
    }
}

// Listener: When storage changes on other pages/tabs, update completion rate
// This allows real-time updates when tasks are marked complete on today.html
window.addEventListener('storage', updateCompletionRate);

// ========================================
// Search: Find pages and features by keyword
// ========================================

// Configuration: List of searchable pages with keywords
const searchPages = [
    { name: 'Home', url: '#home', keywords: ['home', 'welcome'] },
    { name: 'Weather', url: '#weather', keywords: ['weather', 'temperature', 'celsius', 'fahrenheit'] },
    { name: 'Tasks', url: '#today', keywords: ['tasks', 'todo', 'add task'] },
    { name: 'Premium', url: 'premiumwebpage/premium.html', keywords: ['premium', 'upgrade', 'tier', 'plan'] },
    { name: 'Current Events', url: '#today', keywords: ['events', 'news', 'current'] }
];

// Function: Perform search - finds matching pages based on user's search query
function performSearch(query) {
    // Find the search results display area
    const resultsDiv = document.getElementById('searchResults');
    
    // If search query is empty, clear results and exit
    if (!query.trim()) {
        resultsDiv.innerHTML = '';
        return;
    }
    
    // Convert search query to lowercase for case-insensitive matching
    const q = query.toLowerCase();
    
    // Find all pages where keywords match search query
    const matches = searchPages.filter(p =>
        // Check if any keyword contains search text or search text contains keyword
        p.keywords.some(kw => kw.includes(q) || q.includes(kw)) ||
        // Also check if page name matches search text
        p.name.toLowerCase().includes(q)
    );
    
    // If no matches found, display "no results" message
    if (matches.length === 0) {
        resultsDiv.innerHTML = '<div class="search-result-item">No results found</div>';
        return;
    }
    
    // Create clickable links for each matching page
    resultsDiv.innerHTML = matches.map(m => `<a href="${m.url}" class="search-result-item">${m.name}</a>`).join('');
}

// ========================================
// Event Listeners: Wire up all interactions when page loads
// ========================================

document.addEventListener('DOMContentLoaded', () => {
    // ---------- Search Panel Setup ----------
    // Find search button, panel, and input field
    const searchToggleBtn = document.getElementById('searchToggleBtn');
    const searchPanel = document.getElementById('searchPanel');
    const searchInput = document.getElementById('searchInput');
    
    // If search elements exist, set up click handler for search button
    if (searchToggleBtn && searchPanel) {
        // When user clicks search button, toggle search panel visibility
        searchToggleBtn.addEventListener('click', (e) => {
            e.stopPropagation(); // Prevent event from bubbling up
            searchPanel.classList.toggle('active'); // Show or hide search panel
            // If panel is now visible, focus the input so user can start typing
            if (searchPanel.classList.contains('active')) {
                searchInput.focus();
            }
        });
        
        // When user types in search box, perform search in real-time
        if (searchInput) {
            searchInput.addEventListener('input', (e) => performSearch(e.target.value));
        }
        
        // When user clicks outside search panel, close it
        document.addEventListener('click', (e) => {
            if (e.target !== searchToggleBtn && !e.target.closest('.search-panel')) {
                searchPanel.classList.remove('active'); // Hide panel
                const sr = document.getElementById('searchResults');
                if (sr) sr.innerHTML = ''; // Clear search results
            }
        });
    }

    // ---------- Task Input and Add Button Setup ----------
    // Find the "Add Task" button
    const addBtn = document.getElementById('addTaskBtn');
    // If button exists, add click handler to create new task
    if (addBtn) addBtn.addEventListener('click', addTask);
    
    // Find the task input field
    const input = document.getElementById('newTaskInput');
    // If input exists, allow user to press Enter to add task (in addition to clicking button)
    if (input) input.addEventListener('keydown', (e) => { if (e.key === 'Enter') addTask(); });

    // ---------- Initialize Page Data on Load ----------
    // Load saved tasks from storage and display them
    loadTasks();
    // Calculate and display task completion percentage
    updateCompletionRate();
    // Fetch and display current weather
    fetchWeather();
    // Fetch and display current news headlines
    fetchNews();

    // ---------- Logout Button Setup ----------
    // Find the logout button in sidebar
    const logoutBtn = document.getElementById('logoutBtn');
    // If logout button exists, add click handler
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            // Remove session data from storage (logs user out)
            localStorage.removeItem('authSession');
            localStorage.removeItem('isAuthenticated');
            // Send user back to login page
            window.location.href = 'login.html';
        });
    }
});

