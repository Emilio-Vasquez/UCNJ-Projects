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
        question: "1.Which programming structure allows a block of code to be executed repeatedly? ",
        options: ["Selection statement", "Loop", "Branching statement", "Function"],
        correctAnswer: "Loop"
    },
    {
        question: "2.Which selection statement is used to execute one block of code if a condition is true and another block if it's false?",
        options: ["if", "for", "while", "if-else"],
        correctAnswer: "if-else"
    },
    {
        question: "3.Which type of loop in many programming languages continues to execute as long as a certain condition is true?",
        options: ["for loop", "if loop", "while loop", "else loop"],
        correctAnswer: "while loop"
    },
    {
        question: "4.Which type of loop is often used to iterate over a sequence of items, like a list or a string?",
        options: ["while loop", "if loop", "for loop", "do-while loop"],
        correctAnswer: "for loop"
    },
    {
        question: "5.What is the purpose of the continue statement within a loop?",
        options: ["To exit the loop immediately", "To repeat the current iteration", "To skip the rest of the code in the current iteration and move to the next", "To define the loop's ending point"],
        correctAnswer: "To skip the rest of the code in the current iteration and move to the next."
    },
    {
        question: "6.What is a string in programming?",
        options: ["A sequence of numbers", "A single character", "A sequence of characters", "A collection of booleans"],
        correctAnswer: "A sequence of characters"
    },
    {
        question: "7.What is the purpose of the (r) mode when opening a file?",
        options: ["To open the file for writing", "To open the file for appending", "To open the file for reading", "To open the file for both reading and writing"],
        correctAnswer: "To open the file for reading"
    },
    {
        question: "8.What is the purpose of the strip() method often used with strings read from a file?",
        options: ["To convert the string to uppercase", "To remove leading and trailing whitespace characters", "To count the number of characters in the string", "To split the string into a list of words"],
        correctAnswer: "To remove leading and trailing whitespace characters"
    },
    {
        question: "9.What is the purpose of the (w) mode when opening a file?",
        options: ["To open the file for reading only", "To open the file for appending to the end", "To open the file for writing, overwriting the file if it exists", "To open the file for both reading and writing without overwriting"],
        correctAnswer: "To open the file for writing, overwriting the file if it exists"
    },
    {
        question: "10.Which of the following operations can be used to join two strings together?",
        options: ["Subtraction", "Multiplication", "Concatenation", "Division "],
        correctAnswer: "Concatenation"
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
