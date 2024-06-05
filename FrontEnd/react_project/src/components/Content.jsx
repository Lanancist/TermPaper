import axios from "axios";
import {useEffect, useState} from "react";
import {Link} from "react-router-dom";

const Content = () => {
    const [contentData, setContentData] = useState([]);
    const getData = async () => {
            const data = await axios.get("http://127.0.0.1:8000/");
            setContentData(data.data);
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
                        <div style={{ display: "flex", justifyContent: "space-between" }}>
                        <Link key={item.id} to={`/surveys/${item.id}`}>{item.name}</Link>
                            <div>Количество вопросов: {item.countQuestions}</div>
                        </div>
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
                </div>
            </div>
        </>
    )
}

export default Content;