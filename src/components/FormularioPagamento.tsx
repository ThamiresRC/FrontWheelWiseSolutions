'use client'
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';

const FormularioPagamento: React.FC = () => {
  const router = useRouter();
  const [formData, setFormData] = useState({
    nome: '',
    numeroCartao: '',
    dataValidade: '',
    cvv: '',
    detalhes: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Dados do pagamento:', formData);
    router.push('/dashboard'); 
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4 w-full max-w-md">
      <input
        type="text"
        name="nome"
        placeholder="Nome do Titular"
        value={formData.nome}
        onChange={handleChange}
        className="p-2 border rounded"
        required
      />
      <input
        type="text"
        name="numeroCartao"
        placeholder="Número do Cartão"
        value={formData.numeroCartao}
        onChange={handleChange}
        className="p-2 border rounded"
        required
      />
      <div className="flex space-x-4">
        <input
          type="text"
          name="dataValidade"
          placeholder="Data de Validade (MM/AA)"
          value={formData.dataValidade}
          onChange={handleChange}
          className="p-2 border rounded flex-1"
          required
        />
        <input
          type="text"
          name="cvv"
          placeholder="CVV"
          value={formData.cvv}
          onChange={handleChange}
          className="p-2 border rounded flex-1"
          required
        />
      </div>
      <textarea
        name="detalhes"
        placeholder="Adicionar Detalhes (opcional)"
        value={formData.detalhes}
        onChange={handleChange}
        className="p-2 border rounded"
        rows={4}
      />
      <button type="submit" className="p-3 bg-purple-600 text-white rounded hover:bg-purple-700 transition duration-300">
        Efetuar Pagamento
      </button>
    </form>
  );
};

export default FormularioPagamento;

