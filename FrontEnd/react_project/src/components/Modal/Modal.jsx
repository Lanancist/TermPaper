import { useState } from "react";
import { useNavigate } from "react-router-dom";

const Modal = ({setModalActive, path, modalCallback = null}) => {
    const [login, setLogin] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();
    console.log(modalCallback);
    const handleEnter = (path) => {
        if(login === "admin" && password === "admin"){
            if(modalCallback !== null) modalCallback.func(modalCallback.args);
        setModalActive(false)
        return navigate(path)
        }
        setModalActive(false);
    }
    return <>
            <div className="modal">
                <div className="modal-inner">
                <h4>Введите логин и пароль</h4>
                <input type="text" placeholder="логин" value={login} onChange={(e) => setLogin(e.target.value)}/>
                <input type="text" placeholder="пароль" value={password} onChange={(e) => setPassword(e.target.value)} />
                <button onClick={() => handleEnter(path) }>Войти</button>
                </div>
            </div>
    </>
}

export default Modal;