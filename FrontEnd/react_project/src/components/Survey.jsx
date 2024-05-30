import {useEffect, useState} from "react";
import axios from "axios";
import {useParams} from "react-router-dom";

const Survey = () => {
    const [data, setData] = useState([]);
    const {id} = useParams();

    const getData = async () => {
        let res = await axios.get(`http://127.0.0.1:8000/Surveys/${id}`);
        setData(res.data);
    }
    let arr = Object.values(data);
    console.log(arr);

    useEffect(() => {
    getData();
    }, []);
    return (
        <>
            <div className="survey">
                <div className="container">
                    <h1>{data.name}</h1>
                    {arr.map((item, index) => {
                        if(index >= 3){
                            return (
                                <label>
                                    {item.ques}
                                    <select name="" id="">
                                        {item.ans?.map((item) => (
                                            <option value={item}>{item}</option>
                                        ))}
                                    </select>
                                </label>
                            )
                        }
                    })}
                </div>
            </div>
        </>
    )
}

export default Survey;