import React, { useState, useEffect, useMemo } from 'react';
import styled from 'styled-components';
import { GlobalStyle } from './styles/GlobalStyles';
import { SidebarModules, type ModuleType } from './components/SidebarModules';
import MainContent from './components/MainContent/MainContent';
import VoiceAssistant from './components/VoiceAssistant';
import NotesPanel from './components/NotesPanel';
import { 
  FiHome,
  FiCode,
  FiList,
  FiDatabase,
  FiLayers,
  FiFileText,
  FiAlertTriangle,
  FiCpu,
  FiGitBranch,
  FiServer
} from 'react-icons/fi';
import { api } from './services/api';

const AppContainer = styled.div`
  display: flex;
  background: #000000;
  min-height: 100vh;
  width: 100%;
  box-sizing: border-box;
  overflow: hidden;
`;

const ContentWrapper = styled.div`
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 320px;
  margin-left: 280px;
  height: 100vh;
  overflow: hidden;
  background: #000000;
  gap: 0;
  padding: 0;
  box-sizing: border-box;
`;

const MainContentArea = styled.div`
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow-y: auto;
  background: #000000;
  padding: 0;
  box-sizing: border-box;
  
  &::-webkit-scrollbar {
    width: 10px;
  }
  
  &::-webkit-scrollbar-track {
    background: transparent;
  }
  
  &::-webkit-scrollbar-thumb {
    background: #334155;
    border-radius: 4px 0 0 4px;
    border: none;
    
    &:hover {
      background: #475569;
    }
  }
`;

const RightSidebar = styled.div`
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #000000;
  border-left: 1px solid #333;
  box-sizing: border-box;
`;

const VoiceAssistantSection = styled.div`
  flex: 1;
  padding: 2rem 1rem;
  margin: 1rem;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  position: relative;
  z-index: 1;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  
  & > div {
    margin-top: 3rem;
  }
`;

const NotesSection = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 50%;
  max-height: 50%;
  background: #ffffff;
  border-top: 1px solid #e5e7eb;
  margin-top: auto;
  box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.05);
`;

const NotesHeader = styled.div`
  padding: 0.75rem 1.25rem;
  border-bottom: 1px solid #e5e7eb;
  background: #f9fafb;
  
  h3 {
    margin: 0;
    color: #4b5563;
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
`;

const LoadingContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100%;
  color: #fff;
  font-size: 1.2rem;
`;

const ErrorContainer = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100%;
  color: #ef4444;
  padding: 2rem;
  text-align: center;
  
  button {
    margin-top: 1rem;
    padding: 0.5rem 1rem;
    background: #3b82f6;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    
    &:hover {
      background: #2563eb;
    }
  }
`;

const App: React.FC = () => {
  const [modules, setModules] = useState<ModuleType[]>([]);
  const [activeModule, setActiveModule] = useState<string>('');
  const [isListening, setIsListening] = useState<boolean>(false);
  const [showEditor, setShowEditor] = useState<boolean>(false);
  const [showTerminal, setShowTerminal] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch modules from the backend
  useEffect(() => {
    const fetchModules = async () => {
      try {
        console.log('Fetching modules...');
        const modulesData = await api.getModules();
        console.log('Fetched modules:', modulesData);
        
        if (modulesData && modulesData.length > 0) {
          // Map API response to the expected ModuleType structure
          const mappedModules = modulesData.map(module => ({
            id: module.id.toString(),
            label: module.title,
            icon: getIconComponent(module.icon_name || 'FiCode'),
            description: module.description,
            content: module.lessons?.map(lesson => ({
              title: lesson.title,
              description: lesson.explanation || '',
              code: lesson.code_snippet || '',
              explanation: lesson.explanation || ''
            })) || [],
            snippet: module.lessons?.[0]?.code_snippet || '',
            duration: module.duration || '10 min',
            lastUpdated: new Date(module.updated_at).toLocaleDateString(),
            exercises: module.lessons?.filter(l => l.is_exercise).length || 0,
            status: 'not-started' as const // Ensure type is the specific string literal
          }));
          
          setModules(mappedModules);
          if (mappedModules.length > 0) {
            setActiveModule(mappedModules[0].id);
          }
        }
      } catch (error) {
        console.error('Error in fetchModules:', error);
        setError('Failed to load modules. Please try again later.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchModules();
  }, []);

  // Helper function to get icon component by name
  const getIconComponent = (iconName: string) => {
    const iconMap: Record<string, React.ComponentType<{ size?: number }>> = {
      FiHome,
      FiCode,
      FiList,
      FiDatabase,
      FiLayers,
      FiFileText,
      FiAlertTriangle,
      FiCpu,
      FiGitBranch,
      FiServer
    };
    
    return iconMap[iconName] || FiCode;
  };

  // Find the active module data
  const activeModuleData = useMemo(() => {
    if (!Array.isArray(modules) || modules.length === 0) {
      console.log('No modules available or modules is not an array');
      return null;
    }

    // Compare IDs as strings since that's how we're storing them
    const found = modules.find(module => module.id === activeModule);
    if (!found) {
      console.log('No module found with id:', activeModule, 'Available modules:', modules);
      return modules[0] || null;
    }
    
    return found;
  }, [activeModule, modules]);

  const toggleVoiceAssistant = () => {
    setIsListening(prev => !prev);
  };

  const handleRetry = () => {
    setError(null);
    setIsLoading(true);
    // This will trigger the useEffect to fetch data again
    setModules([]);
    setActiveModule('');
  };

  if (isLoading) {
    return <LoadingContainer>Loading modules...</LoadingContainer>;
  }

  if (error) {
    return (
      <ErrorContainer>
        <p>{error}</p>
        <button onClick={handleRetry}>Retry</button>
      </ErrorContainer>
    );
  }

  if (!activeModuleData) {
    return <ErrorContainer>No module data available</ErrorContainer>;
  }

  return (
    <>
      <GlobalStyle />
      <AppContainer>
        {/* Left Sidebar - Course Modules */}
        <SidebarModules
          activeModule={activeModule}
          setActiveModule={setActiveModule}
          modules={modules}
        />
        
        <ContentWrapper>
          <MainContentArea>
            <MainContent 
              module={activeModuleData}
              showEditor={showEditor}
              showTerminal={showTerminal}
              onShowEditor={setShowEditor}
              _onShowTerminal={setShowTerminal}
              _isIntegratedTerminal={true}
              _onToggleTerminal={() => setShowTerminal(prev => !prev)}
            />
          </MainContentArea>
          
          {/* Right Sidebar */}
          <RightSidebar>
            {/* Top Half - Voice Assistant */}
            <VoiceAssistantSection>
              <VoiceAssistant 
                isListening={isListening}
                onToggle={toggleVoiceAssistant}
              />
            </VoiceAssistantSection>
            
            {/* Bottom Half - Notes */}
            <NotesSection>
              <NotesHeader>
                <h3>Notes</h3>
              </NotesHeader>
              <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
                <NotesPanel 
                  isOpen={true}
                  onClose={() => {}}
                  hideHeader={true}
                />
              </div>
            </NotesSection>
          </RightSidebar>
        </ContentWrapper>
      </AppContainer>
    </>
  );
};

export default App;