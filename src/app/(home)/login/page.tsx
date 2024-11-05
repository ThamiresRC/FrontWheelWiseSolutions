import React from 'react';
import FormularioLogin from '@/components/FormularioLogin';

const LoginPage: React.FC = () => {

  return (
    <div className='flex flex-col items-center min-h-screen justify-center bg-background'>
      <h1 className='text-4xl font-semibold text-primary mb-6'>Login</h1>
      <FormularioLogin />
    </div>
  );
};

export default LoginPage;



