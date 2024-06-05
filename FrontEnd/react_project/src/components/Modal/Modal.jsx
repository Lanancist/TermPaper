import { useState } from "react";
import { Navigate, redirect, useNavigate } from "react-router-dom";

const Modal = ({setModalActive}) => {
    const [login, setLogin] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const handleEnter = () => {
        if(login === "admin" && password === "admin"){
        setModalActive(false)
        return navigate("/addSurvey")
        }
    }
    return <>
            <div className="modal">
                <div className="modal-inner">
                <h4>Введите логин и пароль</h4>
                <input type="text" placeholder="логин" value={login} onChange={(e) => setLogin(e.target.value)}/>
                <input type="text" placeholder="пароль" value={password} onChange={(e) => setPassword(e.target.value)} />
                <button onClick={handleEnter}>Войти</button>
                </div>
            </div>
    </>
}

export default Modal;