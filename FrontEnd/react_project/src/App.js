import axios from "axios";
import "./App.css";
import Header from "./components/Header";
import Content from "./components/Content";
import {Route, Routes} from "react-router-dom";
import Survey from "./components/Survey";
import AddSurvey from "./components/AddSurvey/AddSurvey";


function App() {
  return (
    <div className="app-weapper">
      <Header />
        <Routes>
            <Route path="/" element={<Content/>} />
            <Route path="/surveys/:id" element={<Survey/>} />
            <Route path="/statistic/:id" element={<Survey isStatistic />} />
            <Route path="/addSurvey" element={<AddSurvey />} />
        </Routes>
    </div>
  );
}

export default App;
