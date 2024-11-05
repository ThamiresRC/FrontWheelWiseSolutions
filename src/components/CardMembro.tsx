'use client'
import React from 'react';
import Image from 'next/image';

interface CardMembroProps {
  name: string;
  src: string;
}

const CardMembro: React.FC<CardMembroProps> = ({ name, src }) => {
  return (
    <div className="flex flex-col items-center border rounded-lg shadow-lg p-4 m-2 bg-white hover:shadow-xl transition-shadow duration-300">
      <Image src={src} alt={name} width={150} height={150} className="rounded-full" />
      <p className="text-lg font-medium mt-2 text-center">{name}</p>
    </div>
  );
};

export default CardMembro;
