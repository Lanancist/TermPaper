import axios from "axios";
import { useState } from "react";
import { Link } from "react-router-dom";

const AddSurvey = () => {
    const [selectVal, setSelectVal] = useState("qma");
    const [nameOfQuestion, setNameOfQuestion] = useState("");
    const [nameOfSurvey, setNameOfSurvey] = useState("");
    const [answers, setAnswers] = useState("");
    const [questions, setQuestions] = useState([]);

    const selectHandler = (e) => {
        setSelectVal(e.target.value)
    }

    const nameOfQuestionHandler = (e) => {
        setNameOfQuestion(e.target.value);
    }

    const nameOfSurveyHandler = (e) => {
        setNameOfSurvey(e.target.value)
    }

    const answersHandler = (e) => {
        setAnswers(e.target.value);
    }

    const createQuestion = () => {
        const ans = answers.split(",");
        const newQuestion = {
            type: selectVal,
            ques: nameOfQuestion,
            countAns: ans.length,
            ans: ans
        }
        setQuestions([...questions, newQuestion]);
        setAnswers("");
        setSelectVal("qma");
        setNameOfQuestion("");

    }

    const createSurvey = () => {
        const newSurvey = {
            name: nameOfSurvey,
            count: questions.length,
            questions: questions,
        }
        axios.post("http://127.0.0.1:8000/addSurveys", newSurvey)
    }

console.log(questions);
    return (
        <>
        <div className="container">
            <div className="addSurvey-inner">
            <label>
                <p>Напишите название анкеты</p>
                <input type="text" placeholder="Название анкеты..." value={nameOfSurvey} onChange={(e) => nameOfSurveyHandler(e)} />
            </label>
            <label>
                <p>Напишите название вопроса</p>
                <input type="text" placeholder="Название вопроса..." value={nameOfQuestion} onChange={(e) => nameOfQuestionHandler(e)} />
            </label>
            <label>
                <p>Выберите тип вопроса</p>
                <select onChange={(e) => selectHandler(e)} value={selectVal}>
                    <option value="qma">Несколько ответов</option>
                    <option value="qoa">Один ответ</option>
                    <option value="qo">Открытый ответ</option>
                </select>
            </label>
            {selectVal !== "qo" && (
            <label>
                <p>Напишите ответы к вопросу через запятую</p>
                <input type="text" value={answers} onChange={(e) => answersHandler(e)}/>
            </label>
            )}
            <button onClick={createQuestion}>Создать вопрос</button>
            <button onClick={createSurvey}>Создать анкету</button>
            </div>
          <Link to="/">Назад</Link>
        </div>
        </>
    )
}

export default AddSurvey;