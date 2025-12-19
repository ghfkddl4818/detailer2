import React, { useState, useEffect } from 'react';

interface LogoProps {
  variant?: 'header' | 'hero' | 'footer';
  className?: string;
}

const Logo: React.FC<LogoProps> = ({ variant = 'header', className = '' }) => {
  // Common filename patterns to try
  const candidates = [
    './logo.png',
    '/logo.png',
    'logo.png',
    './logo.jpg',
    '/logo.jpg',
    'logo.jpg',
    './logo.svg'
  ];

  const [candidateIndex, setCandidateIndex] = useState(0);
  const [hasError, setHasError] = useState(false);

  // Reset when variant changes
  useEffect(() => {
    setCandidateIndex(0);
    setHasError(false);
  }, []);

  const handleError = () => {
    const nextIndex = candidateIndex + 1;
    if (nextIndex < candidates.length) {
      setCandidateIndex(nextIndex);
    } else {
      setHasError(true);
    }
  };

  const isHero = variant === 'hero';
  
  // Tailwind classes
  const imgClass = isHero 
    ? 'h-40 md:h-56 w-auto mix-blend-multiply' 
    : 'h-12 w-auto mix-blend-multiply';

  // FALLBACK: Clean Text Logo
  if (hasError) {
    return (
      <div className={`flex items-center justify-center ${className}`}>
        <span className={`
          font-bold tracking-widest text-primary font-sans
          ${isHero ? 'text-4xl md:text-5xl' : 'text-xl'}
        `}>
          DETAILER
        </span>
      </div>
    );
  }

  return (
    <img 
      src={candidates[candidateIndex]}
      alt="DETAILER" 
      className={`${imgClass} ${className} object-contain`}
      onError={handleError}
    />
  );
};

export default Logo;