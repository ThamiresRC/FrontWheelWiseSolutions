'use client';
import React, { useState } from 'react';
import { Autoplay, Navigation, Pagination } from 'swiper/modules';
import { Swiper, SwiperSlide } from 'swiper/react';
import 'swiper/swiper-bundle.css';

const images = [
  { src: '/image/homem1.jpg', alt: 'homem1' },
  { src: '/image/mulher1.jpg', alt: 'mulher1' },
  { src: '/image/mao.jpg', alt: 'mao' },
  { src: '/image/TWheelWiseSolutions.png', alt: 'celular' },
];

const faqs = [
  {
    question: "Como funciona o diagnóstico remoto de veículos?",
    answer: "O diagnóstico remoto utiliza tecnologias avançadas para acessar dados do veículo à distância, oferecendo resultados precisos e imediatos.",
  },
  {
    question: "Quais tipos de veículos são compatíveis?",
    answer: "Nosso sistema é compatível com a maioria dos veículos modernos.",
  },
  {
    question: "É seguro compartilhar dados do meu veículo?",
    answer: "Sim, todos os dados são criptografados e tratados com o mais alto nível de segurança.",
  },
  {
    question: "Quais os locais de abrangência?",
    answer: "Abrangência em todo o território nacional. Você pode acionar os serviços e os benefícios em qualquer cidade e estado brasileiro que possua o atendimento.",
  },
];

const HomePage: React.FC = () => {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  const toggleFAQ = (index: number) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <div className="flex flex-col items-center p-4">
      
      <div className="flex flex-row items-center justify-between w-full max-w-6xl">
        <div className="flex flex-col max-w-lg">
          <h1 className="text-4xl font-bold mb-2">
            Diagnósticos Avançados de Veículos em Todo o Mundo Junto Com a Wheel Wise Solutions
          </h1>
          <p className="text-lg text-gray-700">
            O diagnóstico remoto de veículos é possível com diagnósticos modernos e software. Experimente o acesso remoto.
          </p>
        </div>

        <Swiper
          modules={[Navigation, Pagination, Autoplay]}
          pagination={{ clickable: true }}
          navigation
          autoplay={{ delay: 3000 }}
          loop={true}
          className="w-full max-w-2xl h-80"
        >
          {images.map((image, index) => (
            <SwiperSlide key={index}>
              <img
                src={image.src}
                alt={image.alt}
                className="w-full h-full object-cover rounded-lg"
              />
            </SwiperSlide>
          ))}
        </Swiper>
      </div>

      
      <div className="mt-20 w-full max-w-4xl text-center">
        <p className="text-4xl font-bold mb-2">
          Por que escolher Wheel Wise Solutions?
        </p>
      </div>

      
      <div className="mt-8 grid grid-cols-1 sm:grid-cols-3 gap-6 w-full max-w-4xl text-center">
        <div>
          <img src="/image/servico.jpg" alt="Serviço 1" className="w-full h-50 object-cover rounded-lg" />
          <p className="mt-2 text-lg font-semibold">Serviço Confiável</p>
        </div>
        <div>
          <img src="/image/equipamento.jpg" alt="Serviço 2" className="w-full h-50 object-cover rounded-lg" />
          <p className="mt-2 text-lg font-semibold">Equipamento de Ponta</p>
        </div>
        <div>
          <img src="/image/atendimento.jpg" alt="Serviço 3" className="w-full h-50 object-cover rounded-lg" />
          <p className="mt-2 text-lg font-semibold">Atendimento Especializado</p>
        </div>
      </div>

      <div className="w-full mt-10 bg-cover bg-center h-80" style={{ backgroundImage: "url('/image/teste.png')" }}></div>

      <div className="w-full max-w-4xl mt-10 text-center">
        <h3 className="text-3xl font-bold mb-6">Tire suas dúvidas sobre a Wheel Wise Solutions</h3>
        <div className="space-y-4">
          {faqs.map((faq, index) => (
            <div
              key={index}
              className="border rounded-lg p-4 cursor-pointer bg-gray-100"
              onClick={() => toggleFAQ(index)}
            >
              <div className="flex justify-between items-center">
                <p className="text-lg font-semibold">{faq.question}</p>
                <span className="text-2xl">{openIndex === index ? '▲' : '▼'}</span>
              </div>
              {openIndex === index && (
                <p className="mt-2 text-gray-700">{faq.answer}</p>
              )}
            </div>
          ))}
        </div>
      </div>

      <div className="mt-16 text-center">
        <h3 className="text-3xl font-bold mb-4">Clube Wheel Wise Solutions</h3>
        <p className="text-lg text-gray-700 mb-10">
          Olha só as vantagens exclusivas de usar o aplicativo Wheel Wise Solutions!
        </p>
      </div>

      <div className="mt-8 grid grid-cols-1 sm:grid-cols-3 gap-6 w-full max-w-4xl text-center">
        <div>
          <img src="/image/amigos.jpg" alt="amigos" className="w-full h-50 object-cover rounded-lg" />
          <p className="mt-2 text-lg font-semibold">Wheel Wise Solutions Friends</p>
          <p>
          Ganhe pontos e troque por dinheiro. Dá pra economizar até 35% do seguro.</p>
        </div>
        <div>
          <img src="/image/convite.png" alt="convite" className="w-full h-50 object-cover rounded-lg" />
          <p className="mt-2 text-lg font-semibold">Convide e Ganhe R$ 230</p>
          <p>
          R$ 230 no seu bolso e R$ 230 de desconto pra pessoa convidada.</p>
        </div>
        <div>
          <img src="/image/beneficio.png" alt="beneficio" className="w-full h-50 object-cover rounded-lg" />
          <p className="mt-2 text-lg font-semibold">Clube de Benefícios</p>
          <p>
          Vantagens e descontos em vários parceiros.</p>
        </div>
      </div>

      <div className="mt-10 text-center max-w-4xl">
        <p className="text-lg text-gray-700">
          Aproveite todos os benefícios do nosso clube e tenha uma experiência de diagnóstico única e eficiente!
        </p>
      </div>
    </div>
  );
}

export default HomePage;


