import React, { useEffect, useState } from 'react';
import axios from 'axios';

const App = () => {
    const [message, setMessage] = useState('');

    useEffect(() => {
        // Make an API call to Flask backend
        axios.get('http://127.0.0.1:5000/api/test')
            .then(response => {
                setMessage(response.data.message);
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                setMessage('Error connecting to the backend');
            });
    }, []);

    return (
        <div>
            <h1>React Frontend</h1>
            <p>Backend Message: {message}</p>
        </div>
    );
};

export default App;
