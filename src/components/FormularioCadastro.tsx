'use client';
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';

interface FormData {
  nome: string;
  cpf: string;
  email: string;
  dataNascimento: string;
  senha: string;
  confirmarSenha: string;
}

const FormularioCadastro: React.FC = () => {
  const router = useRouter();
  const [formData, setFormData] = useState<FormData>({
    nome: '',
    cpf: '',
    email: '',
    dataNascimento: '',
    senha: '',
    confirmarSenha: '',
  });

  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError(null);
    setSuccess(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (formData.senha !== formData.confirmarSenha) {
      setError("As senhas não coincidem.");
      return;
    }

    try {
      // Envia os dados para a API
      const response = await axios.post('http://localhost:5000/api/cadastro', formData);
      console.log('Dados enviados:', response.data);
      setSuccess('Cadastro realizado com sucesso!');
      router.push('/login'); // Redireciona para a página de login
    } catch (error) {
      console.error('Erro ao enviar os dados:', error);
      setError('Ocorreu um erro ao cadastrar. Tente novamente.');
    }
  };

  return (
    <form onSubmit={handleSubmit} className='flex flex-col gap-4 w-full max-w-md mx-auto p-6 border border-gray-300 rounded-lg shadow-md bg-white'>
      <input
        type='text'
        name='nome'
        placeholder='Nome'
        value={formData.nome}
        onChange={handleChange}
        className='p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400'
        required
      />
      <input
        type='text'
        name='cpf'
        placeholder='CPF'
        value={formData.cpf}
        onChange={handleChange}
        className='p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400'
        required
      />
      <input
        type='email'
        name='email'
        placeholder='Email'
        value={formData.email}
        onChange={handleChange}
        className='p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400'
        required
      />
      <input
        type='date'
        name='dataNascimento'
        placeholder='Data nascimento'
        value={formData.dataNascimento}
        onChange={handleChange}
        className='p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400'
        required
      />
      <input
        type='password'
        name='senha'
        placeholder='Criar Senha'
        value={formData.senha}
        onChange={handleChange}
        className='p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400'
        required
      />
      <input
        type='password'
        name='confirmarSenha'
        placeholder='Confirmar Senha'
        value={formData.confirmarSenha}
        onChange={handleChange}
        className='p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400'
        required
      />
      {error && <p className='text-red-500 text-sm'>{error}</p>}
      {success && <p className='text-green-500 text-sm'>{success}</p>}
      <button type='submit' className='p-3 bg-purple-600 text-white rounded hover:bg-purple-700 transition duration-300'>
        Confirmar Cadastro
      </button>
    </form>
  );
};

export default FormularioCadastro;

