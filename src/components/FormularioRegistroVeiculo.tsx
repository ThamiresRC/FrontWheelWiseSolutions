'use client'
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';

const FormularioRegistroVeiculo: React.FC = () => {
  const router = useRouter();
  const [formData, setFormData] = useState({
    marca: '',
    modelo: '',
    ano: '',
    placa: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Dados do veículo:', formData);
   
    router.push('/dashboard');
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4 w-full max-w-md">
      <input
        type="text"
        name="marca"
        placeholder="Marca"
        value={formData.marca}
        onChange={handleChange}
        className="p-2 border rounded"
        required
      />
      <input
        type="text"
        name="modelo"
        placeholder="Modelo"
        value={formData.modelo}
        onChange={handleChange}
        className="p-2 border rounded"
        required
      />
      <input
        type="number"
        name="ano"
        placeholder="Ano"
        value={formData.ano}
        onChange={handleChange}
        className="p-2 border rounded"
        required
      />
      <input
        type="text"
        name="placa"
        placeholder="Placa"
        value={formData.placa}
        onChange={handleChange}
        className="p-2 border rounded"
        required
      />
      <button type="submit" className="p-3 bg-purple-600 text-white rounded hover:bg-purple-700 transition duration-300">
        Registrar Veículo
      </button>
    </form>
  );
};

export default FormularioRegistroVeiculo;
