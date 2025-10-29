import React, { useState, useCallback } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import { FiMic, FiX } from 'react-icons/fi';
import { LiveKitRoom, RoomAudioRenderer } from '@livekit/components-react';
import '@livekit/components-styles';
import LiveKitVoiceAssistant from './LiveKitVoiceAssistant';

const ModalOverlay = styled(motion.div)`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
`;

const ModalContent = styled(motion.div)`
  background: #1E293B;
  border-radius: 16px;
  padding: 2rem;
  max-width: 500px;
  width: 90%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(51, 65, 85, 0.3);
`;

const NameForm = styled.form`
  display: flex;
  flex-direction: column;
  gap: 1.5rem;

  h2 {
    color: #E2E8F0;
    font-size: 1.5rem;
    margin: 0;
    text-align: center;
  }

  input {
    padding: 0.75rem 1rem;
    border-radius: 8px;
    border: 1px solid rgba(51, 65, 85, 0.5);
    background: rgba(15, 23, 42, 0.5);
    color: #E2E8F0;
    font-size: 1rem;
    transition: all 0.2s;

    &:focus {
      outline: none;
      border-color: #10B981;
      background: rgba(15, 23, 42, 0.7);
    }

    &::placeholder {
      color: #64748B;
    }
  }

  .button-group {
    display: flex;
    gap: 1rem;
  }

  button {
    flex: 1;
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    border: none;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;

    &[type="submit"] {
      background: #10B981;
      color: white;

      &:hover {
        background: #059669;
        transform: translateY(-1px);
      }
    }

    &.cancel-button {
      background: rgba(239, 68, 68, 0.1);
      color: #EF4444;
      border: 1px solid rgba(239, 68, 68, 0.3);

      &:hover {
        background: rgba(239, 68, 68, 0.2);
      }
    }
  }
`;

const CloseButton = styled.button`
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #EF4444;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    background: rgba(239, 68, 68, 0.2);
    transform: scale(1.05);
  }
`;

const VoiceRoomContainer = styled.div`
  min-height: 400px;
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

interface VoiceAssistantModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const VoiceAssistantModal: React.FC<VoiceAssistantModalProps> = ({
  isOpen,
  onClose,
}) => {
  const [isSubmittingName, setIsSubmittingName] = useState(true);
  const [name, setName] = useState('');
  const [token, setToken] = useState<string | null>(null);
  const [livekitUrl, setLivekitUrl] = useState<string>('');

  const getToken = useCallback(async (userName: string) => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/voice/get-token/?name=${encodeURIComponent(userName)}`
      );
      const data = await response.json();
      
      if (data.token && data.url) {
        setToken(data.token);
        setLivekitUrl(data.url);
        setIsSubmittingName(false);
      } else {
        console.error('Failed to get token:', data.error);
        alert('Failed to connect to voice service. Please try again.');
      }
    } catch (error) {
      console.error('Error getting token:', error);
      alert('Failed to connect to voice service. Please check your connection.');
    }
  }, []);

  const handleNameSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (name.trim()) {
      getToken(name);
    }
  };

  const handleClose = () => {
    setIsSubmittingName(true);
    setName('');
    setToken(null);
    setLivekitUrl('');
    onClose();
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <ModalOverlay
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={(e) => {
            if (e.target === e.currentTarget) handleClose();
          }}
        >
          <ModalContent
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            onClick={(e) => e.stopPropagation()}
          >
            <CloseButton onClick={handleClose}>
              <FiX size={18} />
            </CloseButton>

            <VoiceRoomContainer>
              {isSubmittingName ? (
                <NameForm onSubmit={handleNameSubmit}>
                  <h2>Start Voice Tutoring Session</h2>
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Enter your name"
                    required
                    autoFocus
                  />
                  <div className="button-group">
                    <button type="submit">Start Session</button>
                    <button
                      type="button"
                      className="cancel-button"
                      onClick={handleClose}
                    >
                      Cancel
                    </button>
                  </div>
                </NameForm>
              ) : token && livekitUrl ? (
                <LiveKitRoom
                  serverUrl={livekitUrl}
                  token={token}
                  connect={true}
                  video={false}
                  audio={true}
                  onDisconnected={handleClose}
                >
                  <RoomAudioRenderer />
                  <LiveKitVoiceAssistant />
                </LiveKitRoom>
              ) : null}
            </VoiceRoomContainer>
          </ModalContent>
        </ModalOverlay>
      )}
    </AnimatePresence>
  );
};

export default VoiceAssistantModal;
