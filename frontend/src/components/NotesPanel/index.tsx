import React, { useState } from 'react';
import styled from 'styled-components';
// Motion effects removed for simplicity
import { FiX, FiSave } from 'react-icons/fi';

const Panel = styled.div`
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: transparent;
  box-sizing: border-box;
  overflow: hidden;
`;

const PanelHeader = styled.div`
  padding: 0.75rem 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(15, 23, 42, 0.6);
  
  h3 {
    margin: 0;
    color: #E2E8F0;
    font-size: 0.9rem;
    font-weight: 500;
  }
`;

const NotesContent = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 1rem;
  overflow: auto;
  box-sizing: border-box;
  background: rgba(30, 41, 59, 0.95);
`;

const TextArea = styled.textarea`
  flex: 1;
  width: 100%;
  min-height: 200px;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(51, 65, 85, 0.3);
  padding: 0.75rem;
  color: #E2E8F0;
  font-size: 0.875rem;
  line-height: 1.5;
  resize: none;
  transition: all 0.2s ease;
  box-sizing: border-box;
  margin-bottom: 1rem;
  
  &:focus {
    outline: none;
    border-color: #4F46E5;
    box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.2);
  }
  
  &::placeholder {
    color: #64748B;
  }
`;

const CloseButton = styled.button`
  background: none;
  border: none;
  color: #94A3B8;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  
  &:hover {
    background: rgba(239, 68, 68, 0.1);
    color: #EF4444;
  }
`;

const SaveButton = styled.button`
  background: linear-gradient(135deg, #4F46E5 0%, #7E22CE 100%);
  border: none;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
  font-size: 0.875rem;
  
  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(79, 70, 229, 0.3);
  }
`;

interface NotesPanelProps {
  isOpen: boolean;
  onClose: () => void;
  hideHeader?: boolean;
}

const NotesPanel: React.FC<NotesPanelProps> = ({ isOpen, onClose, hideHeader = false }) => {
  const [notes, setNotes] = useState('');

  const handleSave = () => {
    // Save notes logic here
    console.log('Notes saved:', notes);
  };

  if (!isOpen) return null;

  return (
    <Panel>
      {!hideHeader && (
        <PanelHeader>
          <h3>Notes</h3>
          <CloseButton onClick={onClose}>
            <FiX size={16} />
          </CloseButton>
        </PanelHeader>
      )}
      
      <NotesContent>
        <TextArea
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          placeholder="Write your notes here..."
        />
        
        <SaveButton onClick={handleSave}>
          <FiSave size={14} />
          Save Notes
        </SaveButton>
      </NotesContent>
    </Panel>
  );
};

export default NotesPanel;