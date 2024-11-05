import DashboardHeader from '@/components/DashboardHeader';
import React from 'react';

export default function DashboardLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <main className='antialiased min-h-screen'>
            <DashboardHeader />
            <div className='flex-grow'>
            {children}
            </div>
        </main>
    );
};