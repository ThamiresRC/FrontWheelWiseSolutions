import Link from "next/link";
import Image from "next/image"; 

export default function Header() {
    return (
        <header className="bg-purple-800 text-white p-4">
            <nav className="flex items-center justify-between max-w-6xl mx-auto">
                
                <div className="flex items-center">
                    <Image
                        src="/image/logo.png" 
                        alt="Logo da Wheel Wise Solutions"
                        width={50} 
                        height={50} 
                        className="mr-2" 
                    />
                    <h1 className="text-xl font-bold">Wheel Wise Solutions</h1>
                </div>

                <div className="flex space-x-4">
                    <Link href="/" className="hover:text-yellow-300 transition duration-300">Home</Link>
                    <Link href="/login" className="hover:text-yellow-300 transition duration-300">Login</Link>
                    <Link href="/cadastro" className="hover:text-yellow-300 transition duration-300">Cadastro</Link>
                    <Link href="/equipe" className="hover:text-yellow-300 transition duration-300">Nossa Equipe</Link>
                </div>
            </nav>
        </header>
    );
}

