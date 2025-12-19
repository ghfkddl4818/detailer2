import React, { useState, useEffect } from 'react';
import { PORTFOLIO_ITEMS } from '../constants';
import { PortfolioCategory, PortfolioItem } from '../types';
import { ZoomIn } from 'lucide-react';
import Modal from './ui/Modal';
import FadeIn from './ui/FadeIn';

// Simple ImageWithFallback helper without heavy spinners
const ImageWithFallback = ({ src, fallbackSrc, alt, className, containerClassName = "", ...props }: any) => {
  const [imgSrc, setImgSrc] = useState(src);
  
  useEffect(() => {
    setImgSrc(src);
  }, [src]);

  const handleError = () => {
    if (imgSrc !== fallbackSrc && fallbackSrc) {
      setImgSrc(fallbackSrc);
    }
  };

  return (
    <div className={`bg-gray-50 ${containerClassName}`}>
      <img 
        src={imgSrc} 
        alt={alt} 
        className={className} 
        onError={handleError}
        loading="lazy"
        {...props} 
      />
    </div>
  );
};

const Portfolio: React.FC = () => {
  const [activeTab, setActiveTab] = useState<PortfolioCategory>(PortfolioCategory.TRANSLATION);
  const [selectedItem, setSelectedItem] = useState<PortfolioItem | null>(null);

  const filteredItems = PORTFOLIO_ITEMS.filter(item => item.category === activeTab);

  return (
    <section id="portfolio" className="py-24 relative">
      <div className="absolute top-0 inset-x-0 h-px bg-gradient-to-r from-transparent via-gray-200 to-transparent opacity-50"></div>

      <div className="container mx-auto px-6 relative z-10">
        <div className="text-center mb-16">
          <FadeIn>
            <h2 className="text-3xl font-bold text-primary mb-4">포트폴리오</h2>
            <p className="text-gray-500 max-w-2xl mx-auto">
              실제 작업 방식과 동일한 형태로 제작한 예시입니다.<br />
              한국 판매용 문구와 구성으로 깔끔하게 정리했습니다.
            </p>
          </FadeIn>
        </div>

        <FadeIn delay={100}>
          <div className="flex justify-center mb-12">
            <div className="inline-flex bg-white/60 backdrop-blur-sm p-1.5 rounded-xl shadow-sm border border-white/40">
              {Object.values(PortfolioCategory).map((category) => (
                <button
                  key={category}
                  onClick={() => setActiveTab(category)}
                  className={`px-6 py-2.5 rounded-lg text-sm font-medium transition-all duration-300 ${
                    activeTab === category
                      ? 'bg-white text-primary shadow-sm ring-1 ring-black/5'
                      : 'text-gray-500 hover:text-gray-700 hover:bg-white/50'
                  }`}
                >
                  {category} 예시
                </button>
              ))}
            </div>
          </div>
        </FadeIn>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {filteredItems.map((item, index) => (
            <FadeIn key={item.id} delay={index * 100}>
              <div 
                className="group cursor-pointer bg-white p-3 rounded-2xl shadow-card hover:shadow-xl hover:-translate-y-1 transition-all duration-300 border border-white/60"
                onClick={() => setSelectedItem(item)}
              >
                <div className="relative overflow-hidden rounded-xl bg-gray-50 aspect-[3/4] border border-gray-100">
                  {item.category === PortfolioCategory.TRANSLATION ? (
                    <div className="flex h-full w-full">
                      <div className="w-1/2 relative h-full border-r border-white/20 bg-gray-50">
                        <ImageWithFallback 
                          src={item.beforeImage} 
                          alt="Before" 
                          containerClassName="w-full h-full"
                          className="object-cover w-full h-full object-top opacity-80 group-hover:scale-105 transition-transform duration-700 ease-out" 
                        />
                        <div className="absolute top-2 left-2 bg-black/60 backdrop-blur-sm text-white text-[10px] px-2 py-1 rounded z-20">Before</div>
                      </div>
                      <div className="w-1/2 relative h-full bg-gray-50">
                        <ImageWithFallback 
                          src={item.afterImage} 
                          alt="After" 
                          containerClassName="w-full h-full"
                          className="object-cover w-full h-full object-top group-hover:scale-105 transition-transform duration-700 ease-out" 
                        />
                        <div className="absolute top-2 right-2 bg-primary/90 backdrop-blur-sm text-white text-[10px] px-2 py-1 rounded shadow-sm z-20">After</div>
                      </div>
                    </div>
                  ) : (
                    <div className="h-full w-full relative bg-gray-50">
                      <ImageWithFallback 
                        src={item.afterImage} 
                        alt={item.title} 
                        containerClassName="w-full h-full"
                        className="object-cover w-full h-full object-top group-hover:scale-105 transition-transform duration-700 ease-out" 
                      />
                      <div className="absolute bottom-0 left-0 right-0 h-1/3 bg-gradient-to-t from-black/40 to-transparent z-20 pointer-events-none"></div>
                    </div>
                  )}
                  
                  <div className="absolute inset-0 bg-primary/20 backdrop-blur-[1px] opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center z-30 pointer-events-none">
                    <div className="bg-white/90 p-3 rounded-full text-primary shadow-lg transform translate-y-4 group-hover:translate-y-0 transition-transform duration-300">
                      <ZoomIn size={24} />
                    </div>
                  </div>
                </div>
                
                <div className="mt-4 px-1 pb-1">
                  <h3 className="text-lg font-bold text-primary">{item.title}</h3>
                  <p className="text-sm text-gray-500 mt-1 line-clamp-1">{item.description}</p>
                </div>
              </div>
            </FadeIn>
          ))}
        </div>
      </div>

      <Modal isOpen={!!selectedItem} onClose={() => setSelectedItem(null)}>
        {selectedItem && (
          <div className="flex flex-col md:flex-row gap-4 min-h-0 h-full">
            {selectedItem.category === PortfolioCategory.TRANSLATION ? (
              <>
                <div className="flex-1 flex flex-col items-center bg-gray-50 rounded-lg overflow-hidden border border-gray-200 shadow-sm">
                  <div className="w-full bg-gray-800 text-white px-4 py-3 text-center text-sm font-medium sticky top-0 z-10 shadow-md flex justify-between items-center">
                    <span>Before (원본)</span>
                    <span className="text-[10px] bg-white/20 px-2 py-0.5 rounded">스크롤하여 확인</span>
                  </div>
                  <div className="w-full overflow-y-auto custom-scrollbar bg-white relative">
                      <ImageWithFallback 
                        src={selectedItem.beforeImage} 
                        alt="Before Full" 
                        containerClassName="w-full min-h-[300px]"
                        className="w-full max-w-[860px] mx-auto h-auto block" 
                      />
                  </div>
                </div>
                
                <div className="flex-1 flex flex-col items-center bg-gray-50 rounded-lg overflow-hidden border border-gray-200 shadow-sm">
                  <div className="w-full bg-primary text-white px-4 py-3 text-center text-sm font-medium sticky top-0 z-10 shadow-md flex justify-between items-center">
                      <span>After (번역본)</span>
                      <span className="text-[10px] bg-white/20 px-2 py-0.5 rounded">스크롤하여 확인</span>
                  </div>
                  <div className="w-full overflow-y-auto custom-scrollbar bg-white relative">
                      <ImageWithFallback 
                        src={selectedItem.afterImage} 
                        alt="After Full" 
                        containerClassName="w-full min-h-[300px]"
                        className="w-full max-w-[860px] mx-auto h-auto block" 
                      />
                  </div>
                </div>
              </>
            ) : (
              <div className="w-full h-full flex flex-col bg-gray-50 rounded-lg overflow-hidden border border-gray-200 shadow-sm">
                <div className="w-full bg-white px-4 py-3 border-b border-gray-200 text-center font-bold text-primary sticky top-0 z-10">
                  {selectedItem.title}
                </div>
                <div className="w-full overflow-y-auto custom-scrollbar flex justify-center bg-gray-100 relative">
                  <ImageWithFallback 
                    src={selectedItem.afterImage} 
                    alt="Full Detail Page" 
                    containerClassName="w-full max-w-[860px] min-h-[500px]"
                    className="w-full max-w-[860px] h-auto shadow-sm" 
                  />
                </div>
              </div>
            )}
          </div>
        )}
      </Modal>
    </section>
  );
};

export default Portfolio;