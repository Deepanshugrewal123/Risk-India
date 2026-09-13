import React, { useState } from 'react';
import { ChatMessage } from '../../types/chat';
import { assistantService } from '../../services/assistantService';
import { DemoBadge } from '../common/DemoBadge';
import { Bot, Send, Sparkles, User, CornerDownLeft, Loader2 } from 'lucide-react';

export const AIAssistantSection: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'init-1',
      sender: 'user',
      timestamp: '10:42 AM',
      text: 'My area in Lower Assam has a high flood risk score of 84%. What should my family do right now?',
    },
    {
      id: 'init-2',
      sender: 'assistant',
      timestamp: '10:42 AM',
      text: 'Based on the current 84% flood risk level in Assam, prioritize moving essential documents and medicines to a safe elevated location. Disconnect main power if water enters living areas, store at least 3 days of boiled drinking water, and monitor the ASDMA local warning frequency (1079).',
      suggestedActions: [
        'Find nearest flood shelter in Kamrup',
        'Review 72-Hour Flood Grab Bag checklist',
        'Call State Disaster Control Room 1070',
      ],
      riskContext: 'AI Advisory Engine',
    },
  ]);

  const [inputQuery, setInputQuery] = useState<string>('');
  const [isTyping, setIsTyping] = useState<boolean>(false);

  const handleSend = async (queryText?: string) => {
    const textToSend = queryText || inputQuery;
    if (!textToSend.trim() || isTyping) return;

    const userMsg: ChatMessage = {
      id: 'msg-' + Date.now(),
      sender: 'user',
      timestamp: 'Just now',
      text: textToSend,
    };

    setMessages((prev) => [...prev, userMsg]);
    if (!queryText) setInputQuery('');
    setIsTyping(true);

    try {
      const reply = await assistantService.sendMessage(textToSend);
      setMessages((prev) => [...prev, reply]);
    } catch (err) {
      console.error(err);
    } finally {
      setIsTyping(false);
    }
  };

  const sampleQuestions = [
    'What should I pack in a 72-hour family emergency kit?',
    'What are early warning signs of an impending landslide?',
    'How do I safely boil/chlorinate water after a flood?',
    'Where are verified government relief shelters located?',
  ];

  return (
    <section className="py-20 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto">
      <div className="text-center max-w-2xl mx-auto mb-10">
        <div className="inline-flex items-center gap-2 mb-3">
          <span className="text-xs font-mono uppercase tracking-wider text-charcoal-500 font-semibold">
            Disaster Intelligence Advisory
          </span>
          <DemoBadge label="AI ADVISORY" />
        </div>
        <h2 className="text-3xl sm:text-5xl font-bold tracking-tight text-charcoal-950 mb-3">
          Ask Before You Act.
        </h2>
        <p className="text-sm sm:text-base text-charcoal-600">
          Instant contextual safety advice, shelter navigation, and preparedness protocols tailored to India's disaster geography.
        </p>
      </div>

      {/* Chat Mockup Window */}
      <div className="rounded-3xl bg-white border border-paper-300 shadow-floating overflow-hidden">
        {/* Chat Window Header */}
        <div className="px-6 py-4 bg-paper-50/80 border-b border-paper-200 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-xl bg-charcoal-900 text-paper-50 flex items-center justify-center">
              <Bot className="w-4 h-4" />
            </div>
            <div>
              <div className="text-xs font-bold text-charcoal-900 flex items-center gap-1.5">
                <span>RISK//INDIA Intelligence Copilot</span>
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              </div>
              <span className="text-[10px] font-mono text-charcoal-500">
                Preparedness Knowledge Base
              </span>
            </div>
          </div>
          <DemoBadge label="ADVISORY COPILOT" />
        </div>

        {/* Message Thread */}
        <div className="p-6 sm:p-8 space-y-5 max-h-[460px] overflow-y-auto bg-paper-100/30">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex gap-3 ${
                msg.sender === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              {msg.sender === 'assistant' && (
                <div className="w-7 h-7 rounded-lg bg-charcoal-900 text-paper-50 flex items-center justify-center shrink-0 mt-1">
                  <Bot className="w-3.5 h-3.5" />
                </div>
              )}

              <div
                className={`max-w-[82%] sm:max-w-[75%] rounded-2xl p-4 text-xs sm:text-sm leading-relaxed ${
                  msg.sender === 'user'
                    ? 'bg-charcoal-900 text-paper-50 shadow-subtle'
                    : 'bg-white border border-paper-300 text-charcoal-900 shadow-subtle'
                }`}
              >
                <p>{msg.text}</p>

                {/* Suggested Action Chips (if assistant) */}
                {msg.suggestedActions && msg.suggestedActions.length > 0 && (
                  <div className="mt-3 pt-3 border-t border-paper-200 flex flex-wrap gap-1.5">
                    {msg.suggestedActions.map((action, i) => (
                      <button
                        key={i}
                        onClick={() => handleSend(action)}
                        className="text-[11px] font-mono px-2.5 py-1 rounded-md bg-paper-100 text-charcoal-700 hover:bg-paper-200 border border-paper-300 transition-colors"
                      >
                        → {action}
                      </button>
                    ))}
                  </div>
                )}

                <div
                  className={`mt-2 text-[10px] font-mono ${
                    msg.sender === 'user' ? 'text-charcoal-400' : 'text-charcoal-400'
                  }`}
                >
                  {msg.timestamp}
                </div>
              </div>

              {msg.sender === 'user' && (
                <div className="w-7 h-7 rounded-lg bg-paper-200 border border-paper-300 text-charcoal-700 flex items-center justify-center shrink-0 mt-1">
                  <User className="w-3.5 h-3.5" />
                </div>
              )}
            </div>
          ))}

          {isTyping && (
            <div className="flex gap-3 items-center text-xs font-mono text-charcoal-500">
              <div className="w-7 h-7 rounded-lg bg-charcoal-900 text-paper-50 flex items-center justify-center shrink-0">
                <Bot className="w-3.5 h-3.5" />
              </div>
              <div className="flex items-center gap-1.5 px-3 py-2 rounded-xl bg-white border border-paper-200">
                <Loader2 className="w-3.5 h-3.5 animate-spin" />
                <span>Generating safety guidance...</span>
              </div>
            </div>
          )}
        </div>

        {/* Preset suggested questions */}
        <div className="px-6 py-3 bg-paper-50/70 border-t border-paper-200 flex items-center gap-2 overflow-x-auto">
          <span className="text-[10px] font-mono uppercase tracking-wider text-charcoal-400 shrink-0">
            Suggested questions:
          </span>
          {sampleQuestions.map((q, idx) => (
            <button
              key={idx}
              onClick={() => handleSend(q)}
              className="shrink-0 text-xs px-3 py-1 rounded-full bg-white border border-paper-300 text-charcoal-700 hover:border-charcoal-400 hover:bg-paper-50 transition-colors"
            >
              {q}
            </button>
          ))}
        </div>

        {/* Input Bar */}
        <div className="p-4 bg-white border-t border-paper-200">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSend();
            }}
            className="flex items-center gap-2"
          >
            <input
              type="text"
              value={inputQuery}
              onChange={(e) => setInputQuery(e.target.value)}
              placeholder="Ask anything about disaster preparedness, emergency kit, or evacuation..."
              className="flex-1 px-4 py-3 rounded-xl bg-paper-50 border border-paper-300 text-xs sm:text-sm text-charcoal-950 placeholder:text-charcoal-400 focus:outline-none focus:ring-2 focus:ring-charcoal-900 transition-shadow"
            />
            <button
              type="submit"
              disabled={!inputQuery.trim() || isTyping}
              className="p-3 rounded-xl bg-charcoal-900 text-paper-50 hover:bg-charcoal-800 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
              aria-label="Send message"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
        </div>
      </div>
    </section>
  );
};
