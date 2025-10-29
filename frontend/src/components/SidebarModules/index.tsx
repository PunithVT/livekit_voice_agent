import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { FiCode } from 'react-icons/fi';

export interface ContentItem {
  title: string;
  description: string;
  code: string;
  explanation: string;
}

export type ModuleContent = string | ContentItem;

interface ModuleType {
  id: string;
  label: string;
  icon: React.ComponentType<{ size?: number }>;
  badge?: string;
  description: string;
  content: ModuleContent[];
  snippet: string;
  duration: string;
  lastUpdated: string;
  exercises: number;
  status: 'not-started' | 'in-progress' | 'completed';
}

interface SidebarModulesProps {
  activeModule: string;
  setActiveModule: (moduleId: string) => void;
  modules: ModuleType[];
}

const SidebarContainer = styled(motion.div)`
  width: 280px;
  background: #ffffff;
  border-right: 1px solid #e5e7eb;
  position: fixed;
  left: 0;
  top: 0;
  height: 100vh;
  padding: 1.5rem 1rem;
  overflow-y: auto;
  z-index: 100;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
`;

const Logo = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 3rem;
  padding: 0 0.5rem;
`;

const LogoIcon = styled.div`
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #10B981 0%, #3B82F6 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 1.1rem;
`;

const LogoText = styled.div`
  color: #1f2937;
  font-size: 1.5rem;
  font-weight: 700;
`;

const ModuleSection = styled.div`
  margin-bottom: 2.5rem;
`;

const SectionTitle = styled.h3`
  color: #6b7280;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin: 1.5rem 0 0.75rem 0.5rem;
  padding: 0;
`;

const ModuleItem = styled(motion.div)<{ active?: boolean }>`
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 1rem;
  margin-bottom: 0.25rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  background: ${props => props.active ? '#f3f4f6' : 'transparent'};
  border-left: 3px solid ${props => props.active ? '#3b82f6' : 'transparent'};

  &:hover {
    background: #f9fafb;
    transform: none;
  }
`;

const ModuleIcon = styled.div<{ active?: boolean }>`
  color: ${props => props.active ? '#3b82f6' : '#6b7280'};
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
`;

const ModuleText = styled.div<{ active?: boolean }>`
  color: ${props => props.active ? '#1f2937' : '#4b5563'};
  font-weight: ${props => props.active ? '600' : '400'};
  flex: 1;
  font-size: 0.9rem;
`;

const StatusBadge = styled.span<{ $status: 'not-started' | 'in-progress' | 'completed' }>`
  font-size: 0.7rem;
  font-weight: 500;
  padding: 0.2rem 0.5rem;
  border-radius: 9999px;
  margin-left: 0.5rem;
  text-transform: capitalize;
  background-color: ${({ $status }) => 
    $status === 'completed' ? '#10b981' : 
    $status === 'in-progress' ? '#f59e0b' : '#e5e7eb'};
  color: ${({ $status }) => $status === 'not-started' ? '#4b5563' : 'white'};
`;

const ProgressButton = styled(motion.button)`
  width: 100%;
  background: linear-gradient(135deg, #10B981 0%, #3B82F6 100%);
  border: none;
  color: white;
  padding: 1rem 1.5rem;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  margin-top: 2rem;
  transition: all 0.3s ease;

  &:hover {
    box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4);
  }
`;

const SidebarModules: React.FC<SidebarModulesProps> = ({
  activeModule,
  setActiveModule,
  modules
}) => {
  return (
    <SidebarContainer
      initial={{ x: -100 }}
      animate={{ x: 0 }}
      transition={{ type: 'spring', damping: 25 }}
    >
      <Logo>
        <LogoIcon>🐍</LogoIcon>
        <LogoText>PyMaster</LogoText>
      </Logo>

      <ModuleSection>
        <SectionTitle>Python Learning Path</SectionTitle>
        {modules.map((module) => (
          <ModuleItem
            key={module.id}
            active={activeModule === module.id}
            onClick={() => setActiveModule(module.id)}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <ModuleIcon active={activeModule === module.id}>
              <module.icon size={18} />
            </ModuleIcon>
            <ModuleText active={activeModule === module.id}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%' }}>
                <span>{module.label}</span>
              </div>
              <div style={{ 
                display: 'flex', 
                justifyContent: 'space-between',
                alignItems: 'center',
                marginTop: '4px',
                gap: '0.5rem',
                flexWrap: 'wrap'
              }}>
                <span style={{ 
                  fontSize: '0.75rem', 
                  color: activeModule === module.id ? '#6b7280' : '#9ca3af',
                }}>
                  {module.duration} • {module.exercises} exercises
                </span>
                <StatusBadge $status={module.status}>
                  {module.status === 'in-progress' ? 'In Progress' : module.status}
                </StatusBadge>
              </div>
            </ModuleText>
          </ModuleItem>
        ))}
      </ModuleSection>

      <ProgressButton
        onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
      >
        <FiCode size={16} />
        Start Coding
      </ProgressButton>
    </SidebarContainer>
  );
};

export type { ModuleType };
export { SidebarModules };