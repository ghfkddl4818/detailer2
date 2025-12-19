import React, { useState } from 'react';
import { PORTFOLIO_ITEMS } from '../constants';
import { PortfolioCategory, PortfolioItem } from '../types';
import { ZoomIn } from 'lucide-react';
import Modal from './ui/Modal';
import FadeIn from './ui/FadeIn';

const Portfolio: React.FC = () => {
  const [activeTab, setActiveTab] = useState<PortfolioCategory>(PortfolioCategory.TRANSLATION);
  const [selectedItem, setSelectedItem] = useState<PortfolioItem | null>(null);

  const filteredItems = PORTFOLIO_ITEMS.filter(item => item.category === activeTab);

  return (
    <section id="portfolio" className="py-24 relative">
      {/* Subtle background separator - a very faint wash */}
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

        {/* Tabs */}
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

        {/* Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {filteredItems.map((item, index) => (
            <FadeIn key={item.id} delay={index * 100}>
              <div 
                className="group cursor-pointer bg-white p-3 rounded-2xl shadow-card hover:shadow-xl hover:-translate-y-1 transition-all duration-300 border border-white/60"
                onClick={() => setSelectedItem(item)}
              >
                <div className="relative overflow-hidden rounded-xl bg-gray-50 aspect-[3/4] border border-gray-100">
                  {/* If Translation: Show Split View Preview */}
                  {item.category === PortfolioCategory.TRANSLATION ? (
                    <div className="flex h-full w-full">
                      <div className="w-1/2 relative h-full border-r border-white/20">
                        <img 
                          src={item.beforeImage} 
                          alt="Before" 
                          className="object-cover w-full h-full opacity-80 group-hover:scale-105 transition-transform duration-700 ease-out" 
                        />
                        <div className="absolute top-2 left-2 bg-black/60 backdrop-blur-sm text-white text-[10px] px-2 py-1 rounded">Before</div>
                      </div>
                      <div className="w-1/2 relative h-full">
                        <img 
                          src={item.afterImage} 
                          alt="After" 
                          className="object-cover w-full h-full group-hover:scale-105 transition-transform duration-700 ease-out" 
                        />
                        <div className="absolute top-2 right-2 bg-primary/90 backdrop-blur-sm text-white text-[10px] px-2 py-1 rounded shadow-sm">After</div>
                      </div>
                    </div>
                  ) : (
                    // Creation Preview
                    <div className="h-full w-full relative">
                        <img 
                          src={item.afterImage} 
                          alt={item.title} 
                          className="object-cover w-full h-full object-top group-hover:scale-105 transition-transform duration-700 ease-out" 
                        />
                        <div className="absolute bottom-0 left-0 right-0 h-1/3 bg-gradient-to-t from-black/40 to-transparent"></div>
                    </div>
                  )}
                  
                  {/* Hover Overlay */}
                  <div className="absolute inset-0 bg-primary/20 backdrop-blur-[1px] opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
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

      {/* Lightbox Modal */}
      <Modal isOpen={!!selectedItem} onClose={() => setSelectedItem(null)}>
        {selectedItem && (
          <div className="flex flex-col md:flex-row gap-4 h-full bg-gray-50 p-4 rounded-lg">
            {selectedItem.category === PortfolioCategory.TRANSLATION ? (
              <>
                 <div className="flex-1 overflow-auto flex flex-col items-center">
                    <span className="sticky top-0 bg-gray-800 text-white px-3 py-1 rounded-b mb-2 text-sm z-10 shadow-md">Before (원본)</span>
                    <img src={selectedItem.beforeImage} alt="Before" className="max-w-full shadow-md" />
                 </div>
                 <div className="flex-1 overflow-auto flex flex-col items-center">
                    <span className="sticky top-0 bg-primary text-white px-3 py-1 rounded-b mb-2 text-sm z-10 shadow-md">After (번역본)</span>
                    <img src={selectedItem.afterImage} alt="After" className="max-w-full shadow-md" />
                 </div>
              </>
            ) : (
              <div className="w-full h-full overflow-auto flex justify-center">
                 <img src={selectedItem.afterImage} alt="Full Detail Page" className="max-w-full shadow-lg" />
              </div>
            )}
          </div>
        )}
      </Modal>
    </section>
  );
};

export default Portfolio;