import { ChatMessage } from '../types/chat';

const PRESET_KNOWLEDGE_BASE: { keywords: string[]; reply: string; suggestedActions: string[] }[] = [
  {
    keywords: ['flood', 'water', 'submerged', 'assam', 'bihar'],
    reply:
      'Based on high flood indices, prioritize moving elderly family members, medicines, and essential documents to higher ground immediately. Disconnect electrical breakers if water enters living areas, and never wade through moving water. Boil all drinking water or use chlorine tablets.',
    suggestedActions: ['Find nearest flood shelter', 'View Flood Safety Guide', 'Call ASDMA 1079']
  },
  {
    keywords: ['landslide', 'hill', 'mandi', 'shimla', 'wayanad', 'mountain', 'slope'],
    reply:
      'In active landslide corridors like Mandi and Wayanad, watch for warning signs: tilting trees, new fissures in ground/retaining walls, or sudden muddy water runoff. If you hear loud rumbling, evacuate immediately to stable ground perpendicular to the slide path.',
    suggestedActions: ['View Landslide Guide', 'Check NH Road Transit Passability', 'Emergency Helplines']
  },
  {
    keywords: ['cyclone', 'storm', 'wind', 'odisha', 'coast', 'sea'],
    reply:
      'For cyclonic systems, secure loose roof sheets, tape glass windows crosswise, charge communication banks, and keep at least 72 hours of dry rations. Fishermen must strictly remain ashore. Cooperate with district evacuation wardens for shelter transit.',
    suggestedActions: ['Locate Cyclone Shelter', 'View Cyclone Guide', 'Listen to IMD Advisory']
  },
  {
    keywords: ['help', 'donate', 'volunteer', 'ngo', 'aid'],
    reply:
      'To provide relief assistance safely and effectively, connect exclusively with verified government relief channels or audited grassroots NGOs. Do not send unrequested unsolicited goods. Financial contributions to official relief funds provide the highest immediate utility for field responders.',
    suggestedActions: ['Explore Help Others Hub', 'View Verified Agencies', 'Register as Volunteer']
  },
  {
    keywords: ['kit', 'supplies', 'emergency bag', 'prepare', 'bag'],
    reply:
      'A standard Indian Disaster Emergency Kit (Grab Bag) should contain: 3 days of potable water, dry rations (flattened rice, biscuits, nuts), waterproof pouch for identity cards/deeds, battery-powered radio, LED torch, first-aid kit with ORS and chlorine tablets, power bank, and cash in small denominations.',
    suggestedActions: ['Download Emergency Checklist', 'Check Area Risk', 'Share with Family']
  }
];

export const assistantService = {
  sendMessage: async (userMessage: string): Promise<ChatMessage> => {
    // Simulate AI response delay
    await new Promise((res) => setTimeout(res, 600));

    const lower = userMessage.toLowerCase();
    const match = PRESET_KNOWLEDGE_BASE.find((entry) =>
      entry.keywords.some((k) => lower.includes(k))
    );

    if (match) {
      return {
        id: 'msg-' + Date.now(),
        sender: 'assistant',
        timestamp: 'Just now',
        text: match.reply,
        suggestedActions: match.suggestedActions,
        riskContext: 'AI Advisory Engine'
      };
    }

    return {
      id: 'msg-' + Date.now(),
      sender: 'assistant',
      timestamp: 'Just now',
      text:
        'I am analyzing your query based on current national disaster risk heuristics. Prioritize safety, verify local warnings through official SDMA / DDMA control rooms, and keep emergency supplies ready.',
      suggestedActions: ['Analyze My Area', 'View Preparedness Guides', 'Emergency Helplines'],
      riskContext: 'AI Advisory Engine'
    };
  }
};
