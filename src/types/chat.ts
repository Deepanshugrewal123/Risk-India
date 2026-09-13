export interface ChatMessage {
  id: string;
  sender: 'user' | 'assistant';
  timestamp: string;
  text: string;
  suggestedActions?: string[];
  disasterReference?: string;
  riskContext?: string;
}

export interface PreparednessGuide {
  disaster: string;
  iconName: string;
  tagline: string;
  overview: string;
  phases: {
    phase: 'Before' | 'During' | 'After';
    title: string;
    instructions: string[];
    criticalItem?: string;
  }[];
}
