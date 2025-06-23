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
      question: "1.Which of the following statements accurately describes a fundamental difference between Python lists and dictionaries? ",
      options: ["Lists are mutable sequences, while dictionaries are immutable mappings", 
        "Lists store elements in a specific, ordered sequence accessed by integer indices, while dictionaries store key-value pairs accessed by unique keys", 
        "Dictionaries can only contain elements of the same data type, whereas lists can contain elements of mixed data types",
         "Lists are generally more efficient for looking up specific elements than dictionaries"],
      correctAnswer: "Lists store elements in a specific, ordered sequence accessed by integer indices, while dictionaries store key-value pairs accessed by unique keys"
  },
  {
    question: `<pre style="display: inline;">my_dict = {'a': 1, 'b': 2, 'c': 3}\nresult = my_dict.get('d', my_dict.pop('b'))</pre> 2. What will be the value of result and what will my_dict contain after executing this code?`,
    options: ["result will be 2, and my_dict will be {'a': 1, 'c': 3, 'd': 2}",
       "result will be None, and my_dict will be {'a': 1, 'c': 3} ",
        "result will be 2, and my_dict will be {'a': 1, 'c': 3} ",
        "The code will give KeyError"],
    correctAnswer: "result will be 2, and my_dict will be {'a': 1, 'c': 3} "
  },
  {
      question: `<pre style="display: inline; "my_list = [1, 2, 3, 4]\nnew_list = my_list[1:-1]\nnew_list[0] = 5\nfinal_list = my_list + new_list</pre> 3. What will be the value of final_list after executing this code?"`,
      options: ["[1, 2, 3, 4, 5, 3]", 
        "[1, 5, 3, 4, 5, 3]", 
        "[1, 2, 3, 4, 2, 3]", 
        "[1, 2, 3, 4, 5]"],
      correctAnswer: "[1, 2, 3, 4, 5, 3] "
  },
  {
      question: "4.You want to create a function that sometimes returns a value and sometimes doesn't, depending on a secret internal calculation. If it doesn't explicitly return anything, what does Python implicitly return?",
      options: ["False", "None", "An empty tuple ()", "It raises a SilentReturnError that you never see"],
      correctAnswer: "None"
  },
  {
      question: "5.What is the main purpose of the 'if __name__ == '__main__': block in a Python script?",
      options: ["To define the main function of the script ",
         "To ensure that certain code only runs when the script is executed directly (not when it's imported as a module)",
         "To prevent errors when the script is imported", 
         "To prevent errors when the script is exported"],
      correctAnswer: "To ensure that certain code only runs when the script is executed directly (not when it's imported as a module)"
  },
  {
      question: "6.Consider a recursive function designed to calculate the factorial of a non-negative integer n. Which of the following are essential components for this function to work correctly?",
      options: ["A conditional statement that checks if n is equal to 0 (the base case)",
         "A recursive call to the same function with a modified input that moves towards the base case (e.g., n-1)",
         "A loop that iterates from 1 to n to perform the multiplication",
         "A return statement that provides the factorial value for the base case (e.g., returning 1 when n is 0)",
         "The use of global variables to store intermediate calculation results",
         "Calling a different helper function to handle the base case"],
      correctAnswer: ["A conditional statement that checks if n is equal to 0 (the base case)",
        "A recursive call to the same function with a modified input that moves towards the base case (e.g., n-1)", 
        "A return statement that provides the factorial value for the base case (e.g., returning 1 when n is 0)" ]
  },
  {
      question: "7.Consider the base cases in the provided Fibonacci function (if n <= 0: return 0 and elif n == 1: return n). What is their primary purpose in the recursive process?",
      options: ["To define the starting values of the Fibonacci sequence",
         "To prevent the function from calling itself infinitely",
         "To optimize the calculation for small values of n", "To handle invalid negative inputs",
         "To ensure that the function returns a value for all possible non-negative integer inputs",
         "To guide the recursive calls towards simpler subproblems"],
      correctAnswer: ["To prevent the function from calling itself infinitely","To ensure that the function returns a value for all possible non-negative integer inputs",
        "To guide the recursive calls towards simpler subproblems"]
  },
  {
      question: "8.What is the purpose of the self parameter in class methods?",
      options: ["It refers to a global variable", "It refers to the class itself",
         " It refers to the specific instance of the object calling the method",
        "It refers to another class being inherited"],
      correctAnswer: "It refers to the specific instance of the object calling the methods"
  },
  {
      question: "9. What is the purpose of the init method in a Python class?",
      options: ["It deletes objects", "It initializes an objects attributes",
         "It is used to inherit from another class", "It is used to inherit from another class"],
      correctAnswer: "It initializes an objects attributes"
  },
  {
      question: `<pre style="display: "nums = [1, 2, 3, 4]\nsquared = list(map(lambda x: x ** 2, nums))\nprint(squared)</pre> 10. What is the output of the following code?"`,
      options: ["1, 2, 3, 4]", "[1, 4, 9, 16]", "[2, 4, 6, 8]", "Error"],
      correctAnswer: "[1, 4, 9, 16]"
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
