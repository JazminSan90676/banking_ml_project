import React, { useState } from "react";

export default function FormularioCliente() {
  const [formData, setFormData] = useState({
    age: "",
    job: "",
    balance: "",
    duration: ""
  });
  const [resultado, setResultado] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await fetch("http://localhost:5000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData)
    });
    const data = await res.json();
    setResultado(data);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <input name="age" onChange={handleChange} value={formData.age} placeholder="Edad" className="w-full p-2 border rounded" />
      <input name="job" onChange={handleChange} value={formData.job} placeholder="Trabajo" className="w-full p-2 border rounded" />
      <input name="balance" onChange={handleChange} value={formData.balance} placeholder="Balance" className="w-full p-2 border rounded" />
      <input name="duration" onChange={handleChange} value={formData.duration} placeholder="Duración de llamada" className="w-full p-2 border rounded" />

      <button className="bg-blue-600 text-white px-4 py-2 rounded w-full">Predecir</button>

      {resultado && (
        <div className="mt-4 p-3 bg-gray-100 rounded text-center">
          <p>Predicción: {resultado.prediction === 1 ? "✅ Aceptará depósito" : "❌ No aceptará"}</p>
          <p>Probabilidad: {(resultado.probability * 100).toFixed(2)}%</p>
        </div>
      )}
    </form>
  );
}
