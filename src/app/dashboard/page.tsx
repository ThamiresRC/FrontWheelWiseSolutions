'use client'
import React from 'react';
import DashboardCard from '@/components/DashboardCard';

const DashboardPage: React.FC = () => {
  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">Conte com todo o cuidado da Wheel Wise Solutions pelos canais digitais</h1>
      
      <DashboardCard 
        imageSrc="/image/mensagem.jpg" 
        title="Para agilizar seu atendimento, utilize nossos aplicativos ou fale conosco pelo Whatsapp." 
        description="(11)98547-1154"
      />

      <div className="flex items-center mt-8">
        <div className="w-1/3"> 
          <img 
            src="/image/mulhercarro.jpg" 
            alt="mulher carro"
            className="w-full h-auto rounded-lg" 
          />
        </div>
        <div className="ml-4 w-2/3"> 
          <h2 className="text-xl font-semibold">Os seguros online foram pensados pra vc fazer do seu jeito</h2>
          <p className="mt-2 text-gray-600">Chega de pagar por escolhas que você não fez, né? A gente quer facilitar a sua vida com seguros online que são a sua cara. Aí dá pra ficar sempre numa boa e viver o que tem de melhor no seu dia a dia.
          Aproveite os seguros online pra ousar nas escolhas e fazer do seu jeito.</p>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;

