import Answer from "./Answers/Answer"

const Questions = ({question, statistics, quesIndex, handleInputChange}) => {
    return (
        <>
          <h5>{question.ques}</h5>
          {question.ans && question.ans.map((ans, index) => {
            const ratingOfAnswers = statistics.questions !== undefined ? statistics.questions[quesIndex].ans[index][ans] : 0;
            return <Answer ans={ans} ratingOfAnswers={ratingOfAnswers} item={question} statistics={statistics} handleInputChange={handleInputChange}/>
          })}
        </>
    )
}

export default Questions