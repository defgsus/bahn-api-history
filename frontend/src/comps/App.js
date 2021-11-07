import React from "react";
import { StateProvider } from "../state";
import FrontPage from "./FrontPage";


const App = (props) => {

    return (
        <StateProvider>
            <FrontPage/>
        </StateProvider>
    );
};

export default App;

