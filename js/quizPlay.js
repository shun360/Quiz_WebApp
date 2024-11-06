let correctCount = 0; 
let totalQuestions = 0; 

window.onload = function() {
    loadQuiz();
    updateStats();
}

async function loadQuiz() {
    try {
        const response = await fetch('http://localhost:8000/api/quizzes');
        const questions = await response.json();
        totalQuestions = questions.length; 
        displayQuiz(questions); 
    } catch (error) {
        console.error("クイズデータの読み込みに失敗しました:", error);
        alert("クイズデータの読み込みに失敗しました。再度試してください。");
    }
}

function displayQuiz(questions) {
    let quizContainer = document.getElementById('quiz-container');
    questions.forEach(question => {
        let questionElement = document.createElement('h3');
        questionElement.innerText = '問' + question.id + ': ' + question.text;
        quizContainer.appendChild(questionElement);

        let choicesTable = document.createElement('table');
        choicesTable.id = `question-${question.id}`;
        let row = document.createElement('tr');
        question.choices.forEach((choice, index) => {
            let button = document.createElement('button');
            button.innerText = choice;
            button.onclick = () => handleAnswer(question.id, index + 1, question.correctAnswer);

            let td = document.createElement('td');
            td.appendChild(button);
            row.appendChild(td);
        });
        choicesTable.appendChild(row);
        quizContainer.appendChild(choicesTable);

        let space = document.createElement('br');
        quizContainer.appendChild(space);
    });
}

function handleAnswer(questionId, selectedAnswer, correctAnswer) {
    if (isQuestionAnswered(questionId)) return;
    if (selectedAnswer === correctAnswer) correctCount++;
    disableButtons(questionId); 
    updateStats();
}

function isQuestionAnswered(questionId) {
    let buttons = document.querySelectorAll(`#question-${questionId} button`);
    return Array.from(buttons).some(button => button.disabled);
}

function disableButtons(questionId) {
    let buttons = document.querySelectorAll(`#question-${questionId} button`);
    buttons.forEach(button => button.disabled = true);
}

function updateStats() {
    let correctCountElement = document.getElementById('correctCount');
    let accuracyRateElement = document.getElementById('accuracyRate');
    let accuracyRate = totalQuestions > 0 ? (correctCount / totalQuestions) * 100 : 0;
    accuracyRate = Math.min(accuracyRate, 100);
    correctCountElement.innerText = `正解数: ${correctCount}`;
    accuracyRateElement.innerText = `正解率: ${accuracyRate.toFixed(2)}%`;
}
