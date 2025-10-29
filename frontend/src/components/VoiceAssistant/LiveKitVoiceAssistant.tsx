import React, { useEffect, useState } from 'react';
import styled, { keyframes } from 'styled-components';
import {
  useVoiceAssistant,
  BarVisualizer,
  VoiceAssistantControlBar,
  useTrackTranscription,
  useLocalParticipant,
} from '@livekit/components-react';
import { Track } from 'livekit-client';

const wave = keyframes`
  0% {
    transform: scaleY(0.3);
  }
  50% {
    transform: scaleY(1);
  }
  100% {
    transform: scaleY(0.3);
  }
`;

const Container = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 1rem;
  background: rgba(15, 23, 42, 0.5);
  border-radius: 12px;
  border: 1px solid rgba(51, 65, 85, 0.3);
`;

const VisualizerContainer = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100px;
  background: rgba(30, 41, 59, 0.5);
  border-radius: 8px;
  padding: 1rem;
`;

const ControlSection = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const ConversationContainer = styled.div`
  max-height: 300px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 1rem;
  background: rgba(15, 23, 42, 0.3);
  border-radius: 8px;

  &::-webkit-scrollbar {
    width: 6px;
  }

  &::-webkit-scrollbar-track {
    background: rgba(30, 41, 59, 0.3);
    border-radius: 3px;
  }

  &::-webkit-scrollbar-thumb {
    background: rgba(100, 116, 139, 0.5);
    border-radius: 3px;

    &:hover {
      background: rgba(100, 116, 139, 0.7);
    }
  }
`;

const Message = styled.div<{ type: 'agent' | 'user' }>`
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding: 0.75rem;
  border-radius: 8px;
  background: ${props => 
    props.type === 'agent' 
      ? 'rgba(16, 185, 129, 0.1)' 
      : 'rgba(59, 130, 246, 0.1)'};
  border-left: 3px solid ${props => 
    props.type === 'agent' 
      ? '#10B981' 
      : '#3B82F6'};

  .message-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: ${props => 
      props.type === 'agent' 
        ? '#10B981' 
        : '#3B82F6'};
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .message-text {
    color: #E2E8F0;
    font-size: 0.9rem;
    line-height: 1.5;
  }
`;

const StatusBadge = styled.div<{ state: string }>`
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  background: ${props => {
    switch (props.state) {
      case 'listening':
        return 'rgba(16, 185, 129, 0.1)';
      case 'thinking':
        return 'rgba(59, 130, 246, 0.1)';
      case 'speaking':
        return 'rgba(139, 92, 246, 0.1)';
      default:
        return 'rgba(100, 116, 139, 0.1)';
    }
  }};
  color: ${props => {
    switch (props.state) {
      case 'listening':
        return '#10B981';
      case 'thinking':
        return '#3B82F6';
      case 'speaking':
        return '#8B5CF6';
      default:
        return '#64748B';
    }
  }};
  border: 1px solid ${props => {
    switch (props.state) {
      case 'listening':
        return 'rgba(16, 185, 129, 0.3)';
      case 'thinking':
        return 'rgba(59, 130, 246, 0.3)';
      case 'speaking':
        return 'rgba(139, 92, 246, 0.3)';
      default:
        return 'rgba(100, 116, 139, 0.3)';
    }
  }};
`;

interface TranscriptionSegment {
  id?: string;
  text: string;
  type?: 'agent' | 'user';
  firstReceivedTime?: number;
}

const LiveKitVoiceAssistant: React.FC = () => {
  const { state, audioTrack, agentTranscriptions } = useVoiceAssistant();
  const localParticipant = useLocalParticipant();
  const { segments: userTranscriptions } = useTrackTranscription({
    publication: localParticipant.microphoneTrack,
    source: Track.Source.Microphone,
    participant: localParticipant.localParticipant,
  });

  const [messages, setMessages] = useState<TranscriptionSegment[]>([]);

  useEffect(() => {
    const agentMessages: TranscriptionSegment[] = 
      agentTranscriptions?.map((t) => ({ ...t, type: 'agent' as const })) ?? [];
    
    const userMessages: TranscriptionSegment[] = 
      userTranscriptions?.map((t) => ({ ...t, type: 'user' as const })) ?? [];
    
    const allMessages = [...agentMessages, ...userMessages].sort(
      (a, b) => (a.firstReceivedTime ?? 0) - (b.firstReceivedTime ?? 0)
    );
    
    setMessages(allMessages);
  }, [agentTranscriptions, userTranscriptions]);

  return (
    <Container>
      <VisualizerContainer>
        <BarVisualizer state={state} barCount={7} trackRef={audioTrack} />
      </VisualizerContainer>
      
      <ControlSection>
        <div style={{ display: 'flex', justifyContent: 'center' }}>
          <StatusBadge state={state}>
            {state === 'listening' && '🎤 Listening'}
            {state === 'thinking' && '🤔 Thinking'}
            {state === 'speaking' && '🗣️ Speaking'}
            {state === 'idle' && '⏸️ Idle'}
            {!['listening', 'thinking', 'speaking', 'idle'].includes(state) && `Status: ${state}`}
          </StatusBadge>
        </div>
        
        <VoiceAssistantControlBar />
        
        {messages.length > 0 && (
          <ConversationContainer>
            {messages.map((msg, index) => (
              <Message key={msg.id || index} type={msg.type || 'user'}>
                <div className="message-label">
                  {msg.type === 'agent' ? 'Tutor' : 'You'}
                </div>
                <div className="message-text">{msg.text}</div>
              </Message>
            ))}
          </ConversationContainer>
        )}
      </ControlSection>
    </Container>
  );
};

export default LiveKitVoiceAssistant;
