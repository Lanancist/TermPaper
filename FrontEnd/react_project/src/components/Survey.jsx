import { useEffect, useState } from "react";
import axios from "axios";
import { Link, useParams } from "react-router-dom";
import Questions from "./questions/Questions";

const Survey = ({ isStatistic = false }) => {
  const [data, setData] = useState([]);
  const [answers, setAnswers] = useState([]);
  const [statistics, setStatistics] = useState([]);
  const [activeBtn, setActiveBtn] = useState(true);
  const { id } = useParams();

  useEffect(() => {
    getData();
    if (isStatistic) getStatistics();
  }, []);

  const getData = async () => {
    const res = await axios.get(`http://127.0.0.1:8000/Surveys/${id}`);
    setData(res.data);
    let arr = [...JSON.parse(JSON.stringify(res.data)).questions];
    arr.forEach((item) => (item.ans = []));
    setAnswers(arr);
  };

  const getStatistics = async () => {
    try {
      const res = await axios.put(`http://127.0.0.1:8000/statistics/${id}`);
      console.log(res.data, "stat");
      setStatistics(res.data);
    } catch (error) {
      console.error(error);
    }
  };

  const handleInputChange = (ques, ans) => {
    const arrToCopy = [...answers];
    const itemToUpdate = arrToCopy.find((item) => item.ques === ques);
    itemToUpdate?.ans.push(ans);
    setAnswers(arrToCopy);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    let newObj = {
      id: data.id,
      name: data.name,
      count: data.count,
      questions: answers,
    };
    axios
      .put("http://127.0.0.1:8000/answers", {
        ...newObj,
      })
      .then((res) => {
        console.log(res.data, "res");
        setStatistics(res.data);
        setActiveBtn(false);
      });
  };
  return (
    <>
      <div className="survey">
        <div className="container">
          <h1>{data.name}</h1>
          <form>
            {data.questions &&
              data.questions.map((item, quesIndex) => {
                return (
                  <div className="ansvers" key={quesIndex}>
                    <Questions
                      question={item}
                      statistics={statistics}
                      quesIndex={quesIndex}
                      handleInputChange={handleInputChange}
                      isStatistic={isStatistic}
                    />
                    {item.type === "qo" && (
                      <input
                        type="text"
                        onKeyDown={(e) =>
                          handleInputChange(item.ques, e.target.value)
                        }
                      />
                    )}
                  </div>
                );
              })}
            {activeBtn && !isStatistic && (
              <button onClick={handleSubmit}>Отправить</button>
            )}
          </form>
          <Link to="/">Назад</Link>
        </div>
      </div>
    </>
  );
};

export default Survey;

