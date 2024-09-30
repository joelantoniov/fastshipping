import React, { useState, useEffect } from 'react';

const Tracking = () => {
  const [status, setStatus] = useState('Waiting for updates...');
  const [location, setLocation] = useState('Waiting for updates...');
  const shipmentId = 2; // This can be dynamic or passed as props

  useEffect(() => {
    // Create WebSocket connection
    const socket = new WebSocket(`ws://127.0.0.1:8000/ws/tracking/${shipmentId}/`);

    // On receiving a message, update the status and location
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setStatus(data.status);
      setLocation(data.location);
    };

    // Clean up on unmount
    return () => socket.close();
  }, []);

  return (
    <div>
      <h1>Shipment Tracking</h1>
      <p>Status: {status}</p>
      <p>Location: {location}</p>
    </div>
  );
};

export default Tracking;

