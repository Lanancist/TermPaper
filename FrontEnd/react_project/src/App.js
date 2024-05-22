import axios from "axios";
import "./App.css";
import Content from "./components/Content";
import Header from "./components/Header";
import NavBar from "./components/NavBar";

function App() {
  const getListAnc = async () => {
    const data = await axios.get(" http://127.0.0.1:8000/listAnc");
    console.log(data);
  };
  getListAnc();
  return (
    <div className="app-weapper">
      <Header />
      <div className="container">
        <NavBar />
        <Content />
      </div>
    </div>
  );
}

export default App;
