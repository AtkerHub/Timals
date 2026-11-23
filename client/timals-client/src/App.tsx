import { useState, useEffect } from "react";
import apiClient from "./api/axios";

function App () {
    const [message, setMessage] = useState(''); //Message from backend from JSON
    const [isLoading, setIsLoading] = useState(true); //If site is in loading state while waiting for response from backend is loading


    const checkConnection = async () => {
        setIsLoading(true);

        try {
            const response = await apiClient.get('/');

            setMessage(response.data.message);
        } catch (err) {
            console.error(err);
            setMessage('Connect error with Backend')
        } finally {
            setIsLoading(false);
        }
    };

    useEffect( () => {
        checkConnection();
    },[]);

    return( 
        <div>
            <h1> Timals </h1>

            <button disabled={isLoading} onClick = {checkConnection} >
                {isLoading ? 'Loading...' : 'Check connection'}
            </button>

            {isLoading ? <p>Connecting with backend</p> : <p>Response from FastApi: {message}</p>}
        </div>
    );
}

export default App;