import Header from '@/components/Header';
import React from 'react';

export default function HomeLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <main className='flex flex-col h-full'>
            <Header />
            <div className='flex-grow'>
            {children}
            </div>
        </main>
    );
};