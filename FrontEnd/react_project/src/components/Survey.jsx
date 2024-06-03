import {useEffect, useState} from "react";
import axios from "axios";
import {Link, useParams} from "react-router-dom";

const Survey = () => {
    const [data, setData] = useState([]);
    const [answers, setAnswers] = useState([]);
    const [statistics, setStatistics] = useState([]);
    const {id} = useParams();

    useEffect(() => {
        getData();
    }, []);

    const getData = async () => {
        const res = await axios.get(`http://127.0.0.1:8000/Surveys/${id}`);
        setData(res.data);
        let arr = [...JSON.parse(JSON.stringify(res.data)).questions]
        arr.forEach((item) => item.ans = []);
        setAnswers(arr);
    }
    // console.log(data)
    const handleInputChange = (ques, ans) => {
        const arrToCopy = [...answers];
        const itemToUpdate = arrToCopy.find((item) => item.ques === ques);
        itemToUpdate?.ans.push(ans);
        setAnswers(arrToCopy);
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        let newObj = {
            id: data.id,
            name: data.name,
            count: data.count,
            questions: answers
        }
        axios.put("http://127.0.0.1:8000/answers", {
            ...newObj
        }).then((res)=> {
        setStatistics(res.data)
        })
    }
    console.log(statistics)
    return (
        <>
            <div className="survey">
                <div className="container">
                    <h1>{data.name}</h1>
                    <form>

                    {data.questions && data.questions.map((item, quesIndex) => {
                            return (
                                <div className="ansvers" key={item.ques}>
                                    {item.ques}
                                    {item.ans && (
                                        item.ans.map((ans, index) => (
                                            <label>
                                                {item.type === "qma" ? <input type="checkbox" onChange={() => handleInputChange(item.ques, ans)} value={ans}/> : item.type === "qoa" ?
                                        <input type="radio" name={item.ques} onChange={() => handleInputChange(item.ques, ans)} value={ans} /> : null}
                                                {ans}
                                                {statistics?.questions[quesIndex]?.ans[index]}
                                            </label>
                                        ))
                                    )}
                                    {item.type === "qo" && <input type="text" onKeyDown={(e) => handleInputChange(item.ques, e.target.value)} />}
                                </div>
                            )
                    })}
                        <button onClick={handleSubmit} >Отправить</button>
                    </form>
                    <Link to="/">Назад</Link>
                </div>
            </div>
        </>
    )
}

export default Survey;