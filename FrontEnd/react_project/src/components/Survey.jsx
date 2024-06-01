import {useEffect, useState} from "react";
import axios from "axios";
import {Link, useParams} from "react-router-dom";

const Survey = () => {
    const [data, setData] = useState([]);
    const {id} = useParams();

    const getData = async () => {
        const res = await axios.get(`http://127.0.0.1:8000/Surveys/${id}`);
        setData(res.data);
    }

    useEffect(() => {
        getData();
    }, []);
    return (
        <>
            <div className="survey">
                <div className="container">
                    <h1>{data.name}</h1>
                    <form>

                    {data.questions && data.questions.map((item) => {
                            return (
                                <label key={item.ques}>
                                    {item.ques}
                                    {item.ans && (
                                        <select name="" id="">
                                            {item.ans.map((item) => (
                                                <option value={item}>{item}</option>
                                            ))}
                                        </select>
                                    )}
                                    {!item.ans && <input type="text"/>}
                                </label>
                            )
                    })}
                        <button>Отправить</button>
                    </form>
                    <Link to="/">Назад</Link>
                </div>
            </div>
        </>
    )
}

export default Survey;