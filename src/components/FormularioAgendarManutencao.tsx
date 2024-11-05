'use client'
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';

const FormularioAgendarManutencao: React.FC = () => {
  const router = useRouter();
  const [formData, setFormData] = useState({
    dataHora: '',
    tipoManutencao: '',
    detalhes: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Dados da manutenção:', formData);
    router.push('/dashboard'); 
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4 w-full max-w-md">
      <input
        type="datetime-local"
        name="dataHora"
        placeholder='Data'
        value={formData.dataHora}
        onChange={handleChange}
        className="p-2 border rounded"
        required
      />
      <input
        type="text"
        name="tipoManutencao"
        placeholder="Tipo de Manutenção"
        value={formData.tipoManutencao}
        onChange={handleChange}
        className="p-2 border rounded"
        required
      />
      <textarea
        name="detalhes"
        placeholder="Adicionar Detalhes"
        value={formData.detalhes}
        onChange={handleChange}
        className="p-2 border rounded"
        rows={4}
      />
      <button type="submit" className="p-3 bg-purple-600 text-white rounded hover:bg-purple-700 transition duration-300">
        Agendar Manutenção
      </button>
    </form>
  );
};

export default FormularioAgendarManutencao;
