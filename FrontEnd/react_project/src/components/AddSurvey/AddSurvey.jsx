import axios from "axios";
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import Questions from "../questions/Questions";
import Error from '../Modal/Error';


const AddSurvey = () => {
    const [selectVal, setSelectVal] = useState("qma");
    const [nameOfQuestion, setNameOfQuestion] = useState("");
    const [nameOfSurvey, setNameOfSurvey] = useState("");
    const [answers, setAnswers] = useState("");
    const [questions, setQuestions] = useState([]);
    const navigate = useNavigate();
    const [visibleErr, setVisibleErr] = useState(false);
    const [textErr, setTextErr] = useState('');


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
        if ((nameOfQuestion.length === 0) || ((answers.length === 0) && (selectVal !== 'qo'))){
            setVisibleErr(true)
            setTextErr('Нельзя создать пустой вопрос. Убедитесь, что все поля заполнены!');
            return;
        }
        setVisibleErr(false)
        const ans = answers.replaceAll('/n', ' ').split(";");
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
        console.log(questions);
        if (questions == 0){
            setVisibleErr(true)
            setTextErr('Нельзя создать пустую анкету!');
            return;
        }
        const newSurvey = {
            name: nameOfSurvey,
            count: questions.length,
            questions: questions,
        }
        axios.post("http://127.0.0.1:8000/addSurveys", newSurvey).finally(() => {
        return navigate("/");
        })
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
                <p>Напишите текст вопроса</p>
                <input type="text" placeholder="Текст вопроса..." value={nameOfQuestion} onChange={(e) => nameOfQuestionHandler(e)} />
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
                <p>Напишите ответы к вопросу через точку с зяпятой ";"</p>
                <textarea type="text" value={answers} onChange={(e) => answersHandler(e)}/>
            </label>
            )}
            <div onClick={() => {setVisibleErr(false)}}>{visibleErr && (<Error setVisibleErr={visibleErr} setTextErr={textErr}/>)}</div>
            
            <button onClick={createQuestion}>Создать вопрос</button>
            <button onClick={createSurvey}>Создать анкету</button>
            </div>
          <Link to="/">Назад</Link>
          <section className="yourQuestions">
             <h3>Ваши вопросы:</h3>
          {questions?.map((item, quesIndex) => (
            <Questions question={item} quesIndex={quesIndex} handleInputChange={() => null} statistics={[]} />
          ))}
          </section>
        </div>
        </>
    )
}

export default AddSurvey;