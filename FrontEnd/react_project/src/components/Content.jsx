import axios from "axios";
import {useEffect, useState} from "react";
import {Link} from "react-router-dom";
import Modal from "./Modal/Modal";

const Content = () => {
    const [contentData, setContentData] = useState([]);
    const [modalActive, setModalActive] = useState(false);

    const getData = async () => {
            const data = await axios.get("http://127.0.0.1:8000/");
            setContentData(data.data);
    }
    
    const deleteSurvey = async (id) => {
        await axios.delete(`http://127.0.0.1:8000/admin/Surveys/${id}`);
        getData()
    }

    useEffect(() => {
        getData();
    }, [])

    return (
        <>
            <div className="content">
                <div className="container">
                    <h3 className="content-title">
                        Контент
                    </h3>
                    <div className="content-inner">
                        <div className="surveys">
                            <div>Общее количество анкет: {contentData.countSurveys}</div>
                    {contentData.surveys?.map((item) => (
                        <>
                        <div style={{ display: "flex", justifyContent: "space-between" }}>
                        <Link key={item.id} to={`/surveys/${item.id}`}>{item.name}</Link>
                            <div>Количество вопросов: {item.countQuestions}</div>
                            <div className="delete" onClick={() => deleteSurvey(item.id)}>x</div>
                        </div>
                        </>
                    ))}
                        </div>
                        <div className="statistics">
                            <h3>Статистика</h3>
                                <div>Общее количество анкет: {contentData.countSurveys}</div>
                    {contentData.surveys?.map((item) => (
                        <div style={{ display: "flex", justifyContent: "space-between" }}>
                        <Link key={item.id} to={`/statistic/${item.id}`}>{item.name}</Link>
                            <div>Количество вопросов: {item.countQuestions}</div>
                        </div>
                    ))}
                        </div>
                    </div>
                    <button onClick={() => setModalActive(true)}>Добавить анкету</button>
                    {modalActive && (<Modal setModalActive={setModalActive} />)}
                </div>
            </div>
        </>
    )
}

export default Content;