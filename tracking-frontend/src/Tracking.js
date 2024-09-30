import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Tracking = () => {
  const [shipments, setShipments] = useState([]);
  const [trackingNumber, setTrackingNumber] = useState('');
  const [originAddress, setOriginAddress] = useState('');
  const [destinationAddress, setDestinationAddress] = useState('');
  const [status, setStatus] = useState('pending');  // Default to 'pending'

  // Fetch all shipments when component loads
  useEffect(() => {
    fetchShipments();
  }, []);

  // Function to fetch shipments
  const fetchShipments = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/shipping/shipments/');
      setShipments(response.data);
    } catch (error) {
      console.error('Error fetching shipments:', error);
    }
  };

  // Function to create a new shipment
  const createShipment = async (e) => {
    e.preventDefault();
    try {
      const newShipment = { tracking_number: trackingNumber, origin_address: originAddress, destination_address: destinationAddress, status };
      await axios.post('http://127.0.0.1:8000/api/shipping/shipments/', newShipment);
      fetchShipments(); // Refresh shipment list after creation
    } catch (error) {
      console.error('Error creating shipment:', error);
    }
  };

  return (
    <div>
      <h1>Real-Time Shipment Tracking</h1>

      <h2>Create Shipment</h2>
      <form onSubmit={createShipment}>
        <label>
          Tracking Number:
          <input
            type="text"
            value={trackingNumber}
            onChange={(e) => setTrackingNumber(e.target.value)}
          />
        </label>
        <br />
        <label>
          Origin Address:
          <input
            type="text"
            value={originAddress}
            onChange={(e) => setOriginAddress(e.target.value)}
          />
        </label>
        <br />
        <label>
          Destination Address:
          <input
            type="text"
            value={destinationAddress}
            onChange={(e) => setDestinationAddress(e.target.value)}
          />
        </label>
        <br />
        <label>
          Status:
          <input
            type="text"
            value={status}
            onChange={(e) => setStatus(e.target.value)}
          />
        </label>
        <br />
        <button type="submit">Create Shipment</button>
      </form>

      <h2>All Shipments</h2>
      <ul>
        {shipments.map((shipment) => (
          <li key={shipment.id}>
            {shipment.tracking_number} - {shipment.origin_address} to {shipment.destination_address} - {shipment.status}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Tracking;

