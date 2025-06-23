// Your existing functions for popup and logout
function openPopup() {
    document.getElementById("popup").style.display = "flex";
}
function closePopup() {
    document.getElementById("popup").style.display = "none";
}

function showLogoutPopup() {
    document.getElementById("logout-popup").style.display = "flex";
}
function confirmLogout(confirm) {
    const popup = document.getElementById("logout-popup");
    popup.style.display = "none";
    if (confirm) {
        // You can redirect or perform logout action here
        alert("You have been logged out.");
        // window.location.href = "/login"; // Optional redirect
    }
}

// Quiz data
const quizData = [
    {
        question: "1. What is Python?",
        options: ["A type of snake", "A software used exclusively for video game graphics", "A website used for downloading movies", "A high-level programming language used for many different types of applications"],
        correctAnswer: "A high-level programming language used for many different types of applications"
    },
    {
        question: "2. What does the ‘print()’ function do? ",
        options: ["It sends a document to your nearest printer", "It plays an alert anytime a variable is updated", "It displays what is inputted between the parentheses", "It draws a picture on the screen"],
        correctAnswer: "It displays what is inputted between the parentheses"
    },
    {
        question: "3. What is an Algorithm?",
        options: ["A specific solution to a specific problem", "A step-by-step process for solving a general class of problems", "A random sequence of instructions", "A type of computer hardware"],
        correctAnswer: "A step-by-step process for solving a general class of problems"
    },
    {
        question: "4.What will this code output? \n print(“Hello” + “World”)",
        options: ["Hello World", "HelloWorld", "Hello+World", "Hello World!"],
        correctAnswer: "HelloWorld"
    },
    {
        question: "5. What is a variable?",
        options: ["A button that restarts the computer", "A way to store and label data in a program", "A type of error message", "A shortcut for printing text on the screen"],
        correctAnswer: "A way to store and label data in a program "
    },
    {
        question: "6. What is a data type?",
        options: ["A category that defines what kind of value a variable holds", "A kind of error that stops your code from running", "A tool used to draw graphics on your computer", "A Python file that stores secret passwords"],
        correctAnswer: "A category that defines what kind of value a variable holds"
    },
    {
        question: "7. Which of the following are data type examples?",
        options: ["int, float, str, bool", "print, input, len, type", "for, while, if, else", "True, False, None, break"],
        correctAnswer: "int, float, str, bool"
    },
    {
        question: "8. Which is an example of a string datatype? ",
        options: ["42", "‘Python’", "False", "3.143"],
        correctAnswer: "‘Python’"
    },
    {
        question: "9. What is the purpose of an end-of-line comment in Python?",
        options: ["To end a line of code with a semicolon", "To add a comment that Python will ignore, starting with a #", "To stop the program from running", "To print hidden text to the user"],
        correctAnswer: "To add a comment that Python will ignore, starting with a #"
    },
    {
        question: "10. What is the correct way to take user input in Python?",
        options: ["scan(input)", "get.input()", "input()", "read.input()"],
        correctAnswer: "input()"
    }
  ];  

// Quiz variables
let currentQuestionIndex = 0;
let score = 0;
let userAnswers = [];
let quizStarted = false;
let questionTimerInterval;
let timeLeft = 10;  // Changed to 10 seconds
let countdownInterval;
let quizEnded = false;

// Quiz elements
const questionContainer = document.getElementById('question-container');
const resultsContainer = document.getElementById('results-container');
const finalScoreDisplay = document.getElementById('final-score');
const restartButton = document.getElementById('restart-button');
const messageContainer = document.getElementById('message-container');
const quizTitle = document.getElementById('quiz-title');
const countdownDisplay = document.getElementById('countdown');
const timerDisplay = document.getElementById('timer-seconds');
const resultsSummary = document.getElementById('results-summary').querySelector('tbody');

// Function to display the current question
function displayQuestion() {
    messageContainer.textContent = '';
    const currentQuestion = quizData[currentQuestionIndex];

    const questionElement = document.createElement('h2');
    questionElement.className = 'text-xl font-semibold mb-4 text-center special-gothic';
    questionElement.textContent = currentQuestion.question;

    const optionsElement = document.createElement('div');
    optionsElement.className = 'options-container';

    currentQuestion.options.forEach((option, index) => {
        const optionButton = document.createElement('button');
        optionButton.className = 'option-button';
        optionButton.textContent = option;
        optionButton.dataset.option = option;

        if (userAnswers[currentQuestionIndex] === option) {
            optionButton.classList.add('selected');
        }

        optionButton.addEventListener('click', () => handleOptionSelect(option));
        optionsElement.appendChild(optionButton);
    });

    questionContainer.innerHTML = '';
    questionContainer.appendChild(questionElement);
    questionContainer.appendChild(optionsElement);

    startQuestionTimer();
}

// Function to handle option selection
function handleOptionSelect(selectedOption) {
    userAnswers[currentQuestionIndex] = selectedOption;
    clearTimeout(questionTimerInterval);

    const isCorrect = selectedOption === quizData[currentQuestionIndex].correctAnswer;
    if (isCorrect) {
        score++;
    }
    if (currentQuestionIndex < quizData.length - 1) {
        currentQuestionIndex++;
        timeLeft = 10;
        displayQuestion();
    } else {
        calculateScore();
        showResults();
    }
}

// Function to calculate the user's score
function calculateScore() {
    // No need to calculate again, the score is updated on every correct answer.
}

// Function to display the results container
function showResults() {
    questionContainer.classList.add('hidden');
    resultsContainer.classList.remove('hidden');
    finalScoreDisplay.textContent = score; // Display the score here
    quizTitle.textContent = "Quiz Results";
    clearTimeout(questionTimerInterval);
    displayQuizSummary();
}

// Function to display the quiz summary in a table
function displayQuizSummary() {
    resultsSummary.innerHTML = '';
    quizData.forEach((question, index) => {
        const row = document.createElement('tr');
        const questionCell = document.createElement('td');
        questionCell.textContent = question.question;

        const userAnswerCell = document.createElement('td');
        userAnswerCell.textContent = userAnswers[index] || '-';

        const correctAnswerCell = document.createElement('td');
        correctAnswerCell.textContent = question.correctAnswer;

        const resultCell = document.createElement('td');
        resultCell.textContent = userAnswers[index] === question.correctAnswer ? 'Correct' : 'Incorrect';
        if (userAnswers[index] === question.correctAnswer) {
            resultCell.style.color = 'green';
        } else {
            resultCell.style.color = 'red';
        }

        row.appendChild(questionCell);
        row.appendChild(userAnswerCell);
        row.appendChild(correctAnswerCell);
        row.appendChild(resultCell);
        resultsSummary.appendChild(row);
    });
}

// Function to restart the quiz
function restartQuiz() {
    currentQuestionIndex = 0;
    score = 0;
    userAnswers = [];
    resultsContainer.classList.add('hidden');
    questionContainer.classList.remove('hidden');
    quizTitle.textContent = "Level 2: Loops & text files";
    quizStarted = false;
    timeLeft = 10; // Reset timer
    quizEnded = false;
    if (countdownInterval) {
        clearInterval(countdownInterval);
    }
    countdownDisplay.textContent = '';
    startQuiz();
}

// Event listeners
restartButton.addEventListener('click', restartQuiz);

// Timer functions
function startQuestionTimer() {
    timeLeft = 10;  // Reset to 10 seconds for each question
    timerDisplay.textContent = `00:${timeLeft}`;
    clearTimeout(questionTimerInterval);
    questionTimerInterval = setInterval(() => {
        timeLeft--;
        const formattedTime = timeLeft < 10 ? `00:0${timeLeft}` : `00:${timeLeft}`;
        timerDisplay.textContent = formattedTime;
        if (timeLeft <= 0) {
            clearTimeout(questionTimerInterval);
            handleNextQuestion(); // Call function to go to next question
        }
    }, 1000);
}

function handleNextQuestion() {
    if (currentQuestionIndex < quizData.length - 1) {
        currentQuestionIndex++;
        timeLeft = 10;
        displayQuestion();
    } else {
        calculateScore();
        showResults();
    }
}

function startQuiz() {
    if (!quizStarted) {
        let count = 3;
        countdownDisplay.textContent = count;
        questionContainer.classList.add('hidden');
        resultsContainer.classList.add('hidden');
        timerDisplay.classList.add('hidden');
        document.querySelectorAll('main > :not(#countdown)').forEach(el => el.style.display = 'none');
        countdownInterval = setInterval(() => {
            count--;
            countdownDisplay.textContent = count;
            if (count <= 0) {
                clearInterval(countdownInterval);
                countdownDisplay.textContent = '';
                quizStarted = true;
                document.querySelectorAll('main > :not(#countdown)').forEach(el => el.style.display = '');
                questionContainer.classList.remove('hidden');
                timerDisplay.classList.remove('hidden');
                displayQuestion();
            }
        }, 1000);
    } else {
        timeLeft = 10;
        displayQuestion();
    }
}

// Start the quiz when the page loads
startQuiz();
