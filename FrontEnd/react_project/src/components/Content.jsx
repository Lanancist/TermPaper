import axios from "axios";
import {useEffect, useState} from "react";
import {Link} from "react-router-dom";
import Modal from "./Modal/Modal";
import {Bar, BarChart, CartesianGrid, Legend, Tooltip, XAxis, YAxis} from "recharts";

const Content = () => {
    const [contentData, setContentData] = useState([]);
    const [modalActive, setModalActive] = useState(false);
    const [modalRedirectPath, setModalRedirectPath] = useState("");
    const [modalCallback, setModalCallback] = useState(null);

    const getData = async () => {
            await axios.get("http://127.0.0.1:8000/")
                .then((res) => {
                    setContentData(res.data);
                    getDataGraph(res.data.surveys);
            });
    }
    const getDataGraph = (data) => {
    return  data.map((item) => {
          return {name: item.name, CompletedCount: item.CompletedCount};
        })

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
                            <div className="delete" onClick={() => {
                                setModalActive(true);
                                setModalCallback({func: deleteSurvey, args: item.id});
                                setModalRedirectPath("/");
                            } }>x</div>
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
                    <button onClick={() => {
                        setModalActive(true)
                        setModalRedirectPath("/addSurvey");
                    } }>Добавить анкету</button>
                    {modalActive && (<Modal setModalActive={setModalActive} path={modalRedirectPath} modalCallback={modalCallback}/>)}
                    <h3 className="allStatistick">Общая статистика</h3>
                    <BarChart width={1000} height={350} data={getDataGraph(contentData.surveys ? contentData.surveys : [])}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="name" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Bar dataKey="CompletedCount" fill="#8884d8" />
                    </BarChart>
                </div>
            </div>
        </>
    )
}

export default Content;