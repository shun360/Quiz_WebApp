let correctCount = 0;  // 正解数
let totalQuestions = 0;  // 問題数

// ページがロードされたときに実行される処理
window.onload = function() {
    const page = window.location.pathname;  // 現在のページのURLパスを取得

    // officialquizright.htmlの場合、計算クイズを読み込む
    if (page.includes('officialquizright.html')) {
        loadQuizFromAPI(1);  // 1 は計算クイズのID
    }
    // officialquizleft.htmlの場合、漢字クイズを読み込む
    else if (page.includes('officialquizleft.html')) {
        loadQuizFromAPI(2);  // 2 は漢字クイズのID
    }
    updateStats();  // クイズの進行状況を更新
}

// APIからクイズデータを取得して表示する関数
async function loadQuizFromAPI(qid) {
    try {
        // FastAPIのエンドポイントからクイズデータを取得
        const response = await fetch(`http://localhost:8000/api/quizzes/${qid}`);
        const quizData = await response.json();  // JSONとして解析
        
        // クイズの問題を取得
        const questions = quizData.questions;
        totalQuestions = questions.length;  // 問題数を設定
        displayQuiz(questions);  // クイズを画面に表示
    } catch (error) {
        console.error("クイズデータの取得に失敗しました:", error);
        alert("クイズデータの読み込みに失敗しました。再度試してください。");
    }
}

// クイズの問題を画面に表示する関数
function displayQuiz(questions) {
    let quizContainer = document.getElementById('quiz-container');  // クイズを表示するHTML要素を取得
    questions.forEach(question => {
        let questionElement = document.createElement('h3');  // 問題のテキストを表示する要素を作成
        questionElement.innerText = '問 ' + question.no + ': ' + question.text;  // 問題のテキストを設定
        quizContainer.appendChild(questionElement);  // 画面に追加

        let choicesTable = document.createElement('table');  // 選択肢を表示するためのテーブルを作成
        choicesTable.id = `question-${question.no}`;  // 質問ごとにIDを付ける
        let row = document.createElement('tr');  // 選択肢を並べる行を作成

        // 選択肢をボタンとして表示
        question.choices.forEach((choice, index) => {
            let button = document.createElement('button');
            button.innerText = choice;  // 選択肢のテキストをボタンに設定
            button.onclick = () => handleAnswer(question.no, index + 1, question.correctAnswer);  // 回答処理を設定

            let td = document.createElement('td');  // ボタンをテーブルに配置
            td.appendChild(button);
            row.appendChild(td);
        });
        choicesTable.appendChild(row);
        quizContainer.appendChild(choicesTable);  // クイズを画面に追加

        let space = document.createElement('br');  // クイズの間にスペースを入れる
        quizContainer.appendChild(space);
    });
}

// 回答を処理する関数
function handleAnswer(questionNo, selectedAnswer, correctAnswer) {
    if (isQuestionAnswered(questionNo)) return;  // すでに回答している場合は無視
    if (selectedAnswer === correctAnswer) correctCount++;  // 正解ならカウント
    disableButtons(questionNo);  // 回答後にボタンを無効化
    updateStats();  // 統計を更新
}

// 問題がすでに回答済みかどうかを確認する関数
function isQuestionAnswered(questionNo) {
    let buttons = document.querySelectorAll(`#question-${questionNo} button`);  // ボタンを取得
    return Array.from(buttons).some(button => button.disabled);  // すでに無効化されているボタンがあれば回答済み
}

// ボタンを無効化する関数
function disableButtons(questionNo) {
    let buttons = document.querySelectorAll(`#question-${questionNo} button`);
    buttons.forEach(button => button.disabled = true);  // ボタンを無効化
}

// 正解数と正解率を表示する関数
function updateStats() {
    let correctCountElement = document.getElementById('correctCount');  // 正解数表示の要素を取得
    let accuracyRateElement = document.getElementById('accuracyRate');  // 正解率表示の要素を取得
    let accuracyRate = totalQuestions > 0 ? (correctCount / totalQuestions) * 100 : 0;  // 正解率を計算
    accuracyRate = Math.min(accuracyRate, 100);  // 最大100に制限
    correctCountElement.innerText = `正解数: ${correctCount}`;  // 正解数を表示
    accuracyRateElement.innerText = `正解率: ${accuracyRate.toFixed(2)}%`;  // 正解率を表示（小数点以下2桁）
}
