import React, { useState } from 'react';
import styled, { keyframes } from 'styled-components';
import { motion } from 'framer-motion';
import { FiMic } from 'react-icons/fi';
import VoiceAssistantModal from './VoiceAssistantModal';

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

const VoiceButton = styled(motion.button)`
  position: relative;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: rgba(16, 185, 129, 0.1);
  border: 2px solid rgba(16, 185, 129, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 100;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2);

  &:hover {
    border-color: rgba(16, 185, 129, 0.8);
    background: rgba(16, 185, 129, 0.15);
    transform: scale(1.05);
    box-shadow: 0 6px 20px rgba(16, 185, 129, 0.3);
  }
`;

const WaveContainer = styled.div<{ show: boolean }>`
  position: absolute;
  top: -25px;
  left: -25px;
  right: -25px;
  bottom: -25px;
  display: ${props => props.show ? 'flex' : 'none'};
  align-items: center;
  justify-content: center;
  gap: 5px;
`;

const WaveBar = styled.div<{ delay: number; color: string }>`
  width: 6px;
  height: 30px;
  background: ${props => props.color};
  border-radius: 3px;
  animation: ${wave} 1.2s ease-in-out infinite;
  animation-delay: ${props => props.delay}s;
  opacity: 0.9;
`;

const VoiceStatus = styled(motion.div)`
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(30, 41, 59, 0.95);
  backdrop-filter: blur(10px);
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.8rem;
  white-space: nowrap;
  border: 1px solid rgba(51, 65, 85, 0.3);
  color: #E2E8F0;
  z-index: 101;
`;

const DefaultState = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  color: #10B981;
  
  .mic-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    margin-bottom: 0.5rem;
  }
  
  .click-text {
    font-size: 0.7rem;
    color: #94A3B8;
  }
`;

const VoiceAssistant: React.FC = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isAnimating, setIsAnimating] = useState(false);

  const handleClick = () => {
    setIsAnimating(true);
    setTimeout(() => {
      setIsModalOpen(true);
      setIsAnimating(false);
    }, 300);
  };

  const waveColors = [
    '#10B981', // Emerald
    '#3B82F6', // Blue
    '#8B5CF6', // Purple
    '#EC4899', // Pink
    '#F59E0B', // Amber
    '#EF4444', // Red
    '#06B6D4', // Cyan
    '#84CC16', // Lime
  ];

  return (
    <>
      <div style={{ position: 'relative', display: 'flex', justifyContent: 'center' }}>
        <VoiceButton
          onClick={handleClick}
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
        >
          {!isAnimating ? (
            <DefaultState>
              <div className="mic-icon">
                <FiMic size={24} color="#10B981" />
              </div>
              <div className="click-text">Voice Tutor</div>
            </DefaultState>
          ) : (
            <WaveContainer show={isAnimating}>
              {waveColors.map((color, index) => (
                <WaveBar 
                  key={index} 
                  delay={index * 0.15} 
                  color={color}
                />
              ))}
            </WaveContainer>
          )}

          {isAnimating && (
            <VoiceStatus
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
            >
              🎤 Starting...
            </VoiceStatus>
          )}
        </VoiceButton>
      </div>

      <VoiceAssistantModal 
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
      />
    </>
  );
};

export default VoiceAssistant;
