import React from 'react';
import "./globals.css";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang='pt-BR'>
      <body className='antialiased min-h-screen'>
        {children}
        <footer className="bg-purple-800 text-white text-center p-4 mt-auto">
          <p>&copy; 2024 WheelWiseSolutions</p>
        </footer>
      </body>
    </html>
  );
};
