import React, { useState, useRef, useEffect } from 'react';
import styled, { keyframes } from 'styled-components';
import { FiHelpCircle } from 'react-icons/fi';

const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(-5px); }
  to { opacity: 1; transform: translateY(0); }
`;

const TooltipContainer = styled.div`
  position: relative;
  display: inline-flex;
  align-items: center;
  margin-left: 8px;
  z-index: 10;
`;

const HelpIcon = styled(FiHelpCircle)`
  color: #6B7280;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &:hover {
    color: #3B82F6;
    transform: scale(1.1);
  }
`;

const TooltipContent = styled.div<{ isVisible: boolean }>`
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  margin-top: 8px;
  background: white;
  color: #1F2937;
  padding: 12px 16px;
  border-radius: 8px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 
              0 2px 4px -1px rgba(0, 0, 0, 0.06);
  width: 280px;
  font-size: 14px;
  line-height: 1.5;
  opacity: ${props => (props.isVisible ? 1 : 0)};
  visibility: ${props => (props.isVisible ? 'visible' : 'hidden')};
  transition: all 0.2s ease;
  animation: ${fadeIn} 0.2s ease-out;
  z-index: 1000;
  
  &::before {
    content: '';
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    border-width: 6px;
    border-style: solid;
    border-color: transparent transparent white transparent;
  }
`;

const CloseButton = styled.button`
  position: absolute;
  top: 8px;
  right: 8px;
  background: none;
  border: none;
  color: #9CA3AF;
  cursor: pointer;
  font-size: 16px;
  line-height: 1;
  padding: 4px;
  border-radius: 50%;
  
  &:hover {
    color: #6B7280;
    background: #F3F4F6;
  }
`;

interface HelpTooltipProps {
  content: React.ReactNode;
  position?: 'top' | 'right' | 'bottom' | 'left';
  className?: string;
}

export const HelpTooltip: React.FC<HelpTooltipProps> = ({
  content,
  position = 'top',
  className,
}) => {
  const [isVisible, setIsVisible] = useState(false);
  const tooltipRef = useRef<HTMLDivElement>(null);

  // Close tooltip when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (tooltipRef.current && !tooltipRef.current.contains(event.target as Node)) {
        setIsVisible(false);
      }
    };

    if (isVisible) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isVisible]);

  const toggleTooltip = (e: React.MouseEvent) => {
    e.stopPropagation();
    setIsVisible(!isVisible);
  };

  return (
    <TooltipContainer 
      ref={tooltipRef} 
      className={className}
      onClick={toggleTooltip}
    >
      <HelpIcon size={18} />
      <TooltipContent isVisible={isVisible}>
        <CloseButton onClick={(e) => {
          e.stopPropagation();
          setIsVisible(false);
        }}>
          ×
        </CloseButton>
        {content}
      </TooltipContent>
    </TooltipContainer>
  );
};

export default HelpTooltip;
