'use client'
import React, { useState } from 'react';
import CardMembro from '@/components/CardMembro';

const teamMembers = [
  { name: 'Pedro Henrique Jorge De Paula RM558833', src: '/image/eus.jpeg' },
  { name: 'Juliana de Andrade Sousa RM558834', src: '/image/JuFoto.jpeg' },
  { name: 'Thamires Ribeiro Cruz RM558128', src: '/image/thaFoto.jpeg' },
];

const EquipePage: React.FC = () => {
  const [members] = useState(teamMembers);

  return (
    <div className="flex flex-col items-center py-8 bg-background min-h-screen">
      <h1 className="text-4xl font-semibold mb-6 text-primary">Nossa Equipe</h1>
      <div className="flex flex-wrap justify-center">
        {members.map((member, index) => (
          <CardMembro key={index} name={member.name} src={member.src} />
        ))}
      </div>
    </div>
  );
};

export default EquipePage;

