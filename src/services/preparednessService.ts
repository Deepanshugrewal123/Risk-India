import { PREPAREDNESS_GUIDES } from '../data/preparedness';
import { PreparednessGuide } from '../types/chat';

export type { PreparednessGuide };

export const preparednessService = {
  /**
   * Get all emergency preparedness guides
   */
  getGuides: async (): Promise<PreparednessGuide[]> => {
    await new Promise((res) => setTimeout(res, 80));
    return PREPAREDNESS_GUIDES;
  },

  /**
   * Get specific guide by hazard name
   */
  getGuideByHazard: async (hazard: string): Promise<PreparednessGuide | undefined> => {
    await new Promise((res) => setTimeout(res, 60));
    return PREPAREDNESS_GUIDES.find(
      (g) => g.disaster.toLowerCase() === hazard.toLowerCase()
    );
  }
};
