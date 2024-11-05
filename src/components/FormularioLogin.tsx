'use client';
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';

interface FormData {
  email: string;
  senha: string;
}

const FormularioLogin: React.FC = () => {
  const router = useRouter();
  const [formData, setFormData] = useState<FormData>({ email: '', senha: '' });
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError(null); 
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

   
    if (!formData.email || !formData.senha) {
      setError("Por favor, preencha todos os campos.");
      return;
    }

    console.log('Dados enviados:', formData);
    router.push('/dashboard'); 
  };

  return (
    <div className="flex flex-col items-center">
      <form onSubmit={handleSubmit} className="flex flex-col gap-4 w-full max-w-sm mx-auto p-6 bg-white rounded-lg shadow-lg border border-gray-200 transition-transform transform hover:scale-105">
        <h2 className="text-2xl font-bold text-center text-purple-800 mb-4">Bem-vindo de volta!</h2>
        
        {error && <p className="text-red-500 text-sm">{error}</p>}

        <input
          type='email'
          name='email'
          placeholder='Email'
          value={formData.email}
          onChange={handleChange}
          className='p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-purple-500'
          required
        />
        
        <input
          type='password'
          name='senha'
          placeholder='Senha'
          value={formData.senha}
          onChange={handleChange}
          className='p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-purple-500'
          required
        />

        <button type='submit' className='p-3 bg-purple-600 text-white rounded hover:bg-purple-700 transition-colors'>
          Login
        </button>
      </form>
    </div>
  );
};

export default FormularioLogin;

