import React from 'react';
import { FutureRiskCommandCenter } from './FutureRiskCommandCenter';

interface FutureRiskHeroSectionProps {
  onOpenFullMap?: () => void;
  onSelectLocation?: (regionId?: string) => void;
  onViewDetailedPage?: () => void;
  onViewEarlyWarnings?: () => void;
}

export const FutureRiskHeroSection: React.FC<FutureRiskHeroSectionProps> = ({
  onOpenFullMap,
  onSelectLocation,
  onViewDetailedPage,
  onViewEarlyWarnings
}) => {
  return (
    <FutureRiskCommandCenter
      onOpenFullMap={onOpenFullMap}
      onSelectRegion={onSelectLocation}
      onViewDetailedPage={onViewDetailedPage}
      onViewEarlyWarnings={onViewEarlyWarnings}
    />
  );
};
