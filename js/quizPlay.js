

let correctCount = 0; // 正解数
let totalQuestions = 0; // 出題された問題数

// ページ読み込み時にクイズと保存されたデータをロード
window.onload = function() {
    // ローカルストレージをクリアして状態をリセット
    localStorage.removeItem('correctCount');
    localStorage.removeItem('totalQuestions');
    correctCount = 0;
    totalQuestions = 0;

    loadQuiz();
    updateStats(); // 初期状態を表示
}

// JSONデータを取得してクイズを表示する
async function loadQuiz() {
    const response = await fetch('../json/quiz_calc.json');
    const data = await response.json();
    const questions = data.questions;

    totalQuestions = questions.length; // 全問題数を取得
    let quizContainer = document.getElementById('quiz-container');

    questions.forEach(question => {
        // 問題文の表示
        let questionElement = document.createElement('h3');
        questionElement.innerText = '問' + question.id + ': ' + question.text;
        quizContainer.appendChild(questionElement);

        // 選択肢の表示
        let choicesTable = document.createElement('table');
        choicesTable.id = `question-${question.id}`; // 各問題に固有のIDを付与
        let row = document.createElement('tr');
        question.choices.forEach((choice, index) => {
            let button = document.createElement('button');
            button.innerText = choice;
            button.style.width = '100px';
            button.style.height = '50px';
            button.onclick = () => checkAnswer(question.id, index + 1, question.correctAnswer);

            let td = document.createElement('td');
            td.appendChild(button);
            row.appendChild(td);
        });
        choicesTable.appendChild(row);
        quizContainer.appendChild(choicesTable);

        // スペースを追加
        let space = document.createElement('br');
        quizContainer.appendChild(space);
    });
}

// 正解・不正解の表示と正解数のカウント
function checkAnswer(questionId, selectedAnswer, correctAnswer) {
    // 既に回答済みの場合は何もしない
    let buttons = document.querySelectorAll(`#question-${questionId} button`);
    // すでに無効化されている場合は何もしない
    if (Array.from(buttons).some(button => button.disabled)) {
        return;
    }

    if (selectedAnswer === correctAnswer) {
        correctCount++;
    }

    // 正解数と正解率の更新
    updateStats();
    saveStats(); // データを保存

      // 押された問題のボタンだけを無効化
      buttons.forEach(button => {
        button.disabled = true;
    });
}

// 正解数と正解率を表示する
function updateStats() {
    let correctCountElement = document.getElementById('correctCount');
    let accuracyRateElement = document.getElementById('accuracyRate');

    // 正解率を計算（0を避けるためにtotalQuestionsが0でないことを確認）
    let accuracyRate = totalQuestions > 0 ? (correctCount / totalQuestions) * 100 : 0;

    // 最大値を100%に制限
    accuracyRate = Math.min(accuracyRate, 100);

    correctCountElement.innerText = `正解数: ${correctCount}`;
    accuracyRateElement.innerText = `正解率: ${accuracyRate.toFixed(2)}%`;
}

// 正解数と正解率をローカルストレージに保存する
function saveStats() {
    localStorage.setItem('correctCount', correctCount);
    localStorage.setItem('totalQuestions', totalQuestions);
}

// ローカルストレージから正解数と正解率を読み込む
function loadStats() {
    let savedCorrectCount = localStorage.getItem('correctCount');
    let savedTotalQuestions = localStorage.getItem('totalQuestions');

    if (savedCorrectCount !== null && savedTotalQuestions !== null) {
        correctCount = parseInt(savedCorrectCount);
        totalQuestions = parseInt(savedTotalQuestions);

        // 正解数と正解率の表示を更新
        updateStats();
    }
}
