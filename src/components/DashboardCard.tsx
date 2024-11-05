import React from 'react';
import Image from 'next/image';

interface DashboardCardProps {
  imageSrc: string;
  title: string;
  description: string;
}

const DashboardCard: React.FC<DashboardCardProps> = ({ imageSrc, title, description }) => {
  return (
    <div className="flex items-center p-4 border rounded shadow-md">
      <div className="flex-shrink-0">
        <Image
          src={imageSrc}
          alt={title}
          width={150} 
          height={150} 
          className="rounded-lg"
        />
      </div>
      <div className="ml-4"> 
        <h2 className="text-xl font-semibold">{title}</h2>
        <p className="mt-2 text-gray-600">{description}</p>
      </div>
    </div>
  );
};

export default DashboardCard;
