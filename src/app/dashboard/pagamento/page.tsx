'use client'
import React from 'react';
import FormularioPagamento from '@/components/FormularioPagamento';
import { useRouter } from 'next/navigation';

const PagamentoPage: React.FC = () => {
  const router = useRouter();

  return (
    <div className="flex flex-col items-center min-h-screen justify-center bg-background p-4">
      <h1 className="text-3xl font-semibold mb-4">Efetuar Pagamento</h1>
      <FormularioPagamento />
      <button
        onClick={() => router.push('/dashboard')}
        className="mt-4 p-2 bg-gray-300 text-gray-800 rounded hover:bg-gray-400"
      >
        Voltar
      </button>
    </div>
  );
};

export default PagamentoPage;
