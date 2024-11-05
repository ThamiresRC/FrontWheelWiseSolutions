'use client'
import React from 'react';
import FormularioCadastro from '@/components/FormularioCadastro';

const CadastroPage: React.FC = () => {
  return (
    <div className='flex flex-col items-center min-h-screen justify-center bg-background'>
      <h1 className='text-4xl font-semibold text-primary mb-6'>Cadastro</h1>
      <FormularioCadastro />
    </div>
  );
};

export default CadastroPage;
