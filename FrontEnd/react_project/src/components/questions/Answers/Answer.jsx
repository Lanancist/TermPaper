const Answer = ({ans, ratingOfAnswers, item, statistics, handleInputChange, isStatistic}) => {
    return (
        <>
                          <label>
                            {!isStatistic && (
                              <>
                              {item.type === "qma" ? (
                              <input
                                type="checkbox"
                                onChange={() => handleInputChange(item.ques, ans)}
                                value={ans}
                              />
                            ) : item.type === "qoa" ? (
                              <input
                                type="radio"
                                name={item.ques}
                                onChange={() => handleInputChange(item.ques, ans)}
                                value={ans}
                              />
                            ) : null}
                              </>
                            )}
                            <span>
                            {ans}
                            </span>
                            <div>
                              {!Array.isArray(statistics) ? <progress value={ratingOfAnswers} max="100">{ratingOfAnswers}%</progress> : null}
                            <span>
                            {!Array.isArray(statistics) && ratingOfAnswers + "%"}
                            </span>
                            </div>
                          </label>
        </>
    )
}

export default Answer
