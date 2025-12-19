export enum ServiceType {
  TRANSLATION = 'TRANSLATION',
  PARTIAL = 'PARTIAL',
  FULL = 'FULL'
}

export interface ServiceItem {
  id: string;
  title: string;
  price: string;
  description: string;
  features: string[];
  summary: string;
  type: ServiceType;
}

export enum PortfolioCategory {
  TRANSLATION = '번역',
  CREATION = '제작'
}

export interface PortfolioItem {
  id: string;
  title: string;
  category: PortfolioCategory;
  beforeImage?: string;
  afterImage: string;
  description: string;
}
