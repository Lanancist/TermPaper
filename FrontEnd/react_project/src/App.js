import axios from "axios";
import "./App.css";
import Header from "./components/Header";
import Content from "./components/Content";
import {Route, Routes} from "react-router-dom";
import Survey from "./components/Survey";


function App() {
  // const getListAnc = async () => {
  //   const data = await axios.get(" http://127.0.0.1:8000/");
  //   console.log(data);
  // };
  // getListAnc();
  return (
    <div className="app-weapper">
      <Header />
        {/*<Content />*/}
        <Routes>
            <Route path="/" element={<Content/>} />
            <Route path="/surveys/:id" element={<Survey/>} />
        </Routes>
      {/*<div className="container">*/}
      {/*  /!*<NavBar />*!/*/}
      {/*  /!*<Content />*!/*/}
      {/*</div>*/}
    </div>
  );
}

export default App;
