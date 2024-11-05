'use client'
import React from 'react';
import FormularioAgendarManutencao from '@/components/FormularioAgendarManutencao';
import { useRouter } from 'next/navigation';

const AgendarManutencaoPage: React.FC = () => {
  const router = useRouter();

  return (
    <div className="flex flex-col items-center min-h-screen justify-center bg-background p-4">
      <h1 className="text-3xl font-semibold mb-4">Agendar Manutenção</h1>
      <FormularioAgendarManutencao />
      <button
        onClick={() => router.push('/dashboard')}
        className="mt-4 p-2 bg-gray-300 text-gray-800 rounded hover:bg-gray-400"
      >
        Voltar
      </button>
    </div>
  );
};

export default AgendarManutencaoPage;
