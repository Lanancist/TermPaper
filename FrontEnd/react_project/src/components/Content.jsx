import axios from "axios";
import {useEffect, useState} from "react";
import {Link} from "react-router-dom";

const Content = () => {
    const [contentData, setContentData] = useState([]);
    const getData = async () => {
            const data = await axios.get("http://127.0.0.1:8000/");
            setContentData(Object.values(data.data));
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
                    {contentData.map((item, index) => (
                        <div style={{ display: "flex", justifyContent: "space-between" }}>
                        <Link key={item.id} to={`/surveys/${item.id}`}>{item.name}</Link>
                            {index === 0 ? <div>Общее количество вопросов: {item}</div> :
                                <div>Количество вопросов: {item.countQuestions}</div>}
                        </div>
                    ))}
                </div>
            </div>
        </>
    )
}

export default Content;