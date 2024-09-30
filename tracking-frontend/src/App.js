import React from 'react';
import Tracking from './Tracking';

function App() {
  return (
    <div className="App">
      <h1>Real-Time Shipment Tracking</h1>
      <Tracking shipmentId={2} />
    </div>
  );
}

export default App;

