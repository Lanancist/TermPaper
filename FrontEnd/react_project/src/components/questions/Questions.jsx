import Answer from "./Answers/Answer"

const Questions = ({question, statistics, quesIndex, handleInputChange, isStatistic}) => {
    return (
        <>
          <h5>{question?.ques}</h5>
          {question?.ans && question.ans.map((ans, index) => {
            const ratingOfAnswers = statistics.questions !== undefined ? isStatistic ? statistics.questions[quesIndex].statistics[index][ans] : statistics.questions[quesIndex].ans[index][ans] : 0;
            return <Answer ans={ans} ratingOfAnswers={ratingOfAnswers} item={question} statistics={statistics} handleInputChange={handleInputChange} isStatistic={isStatistic}/>
          })}
        </>
    )
}

export default Questions