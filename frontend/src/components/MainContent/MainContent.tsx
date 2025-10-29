import React, { useState, useRef, useEffect, Suspense } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { FiPlay, FiCode, FiClock, FiAward, FiCalendar, FiX, FiTerminal } from 'react-icons/fi';
import { type ModuleType, type ModuleContent } from '../SidebarModules';
import HelpTooltip from '../HelpTooltip';
import { Terminal as XTerminal } from 'xterm';
import type { ITerminalOptions } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';
import 'xterm/css/xterm.css';

// Lazy load Monaco Editor
const MonacoEditor = React.lazy(() => import('@monaco-editor/react'));

// Extend the base ModuleType with additional properties
interface ExtendedModuleType extends Omit<ModuleType, 'status'> {
  duration: string;
  exercises: number;
  content: ModuleContent[];
  snippet: string;
  status: 'not-started' | 'in-progress' | 'completed';
}

interface ScrollToggleProps {
  $isActive: boolean;
}

const ScrollToggle = styled.button<ScrollToggleProps>`
  background: #1E293B;
  border: 1px solid #334155;
  color: #E2E8F0;
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-size: 0.75rem;
  transition: all 0.2s;
  min-width: 60px;
  height: 32px;
  position: relative;
  
  &:hover {
    background: #334155;
    transform: translateY(-1px);
  }
  
  &:active {
    transform: translateY(0);
  }
  
  /* Indicator dot */
  &::before {
    content: '';
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: ${props => props.$isActive ? '#10B981' : '#EF4444'};
    margin-right: 4px;
  }
`;

const ContentContainer = styled.div<{ autoScroll?: boolean }>`
  overflow-y: ${props => props.autoScroll ? 'hidden' : 'auto'};
  flex: 1;
  overflow-y: auto;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  position: relative;
  padding: 1rem;
  background: #000000;
  min-height: 100vh;
  box-sizing: border-box;
  
  /* Custom scrollbar */
  &::-webkit-scrollbar {
    width: 10px;
  }
  
  &::-webkit-scrollbar-track {
    background: transparent;
    margin: 1rem 0;
  }
  
  &::-webkit-scrollbar-thumb {
    background: #334155;
    border-radius: 4px;
    border: 2px solid #000000;
    
    &:hover {
      background: #475569;
    }
  }
  
  @media (max-width: 768px) {
    padding: 0.75rem;
  }
`;

const Content = styled(motion.div)`
  min-height: calc(100vh - 2rem);
  background: #ffffff;
  position: relative;
  z-index: 1;
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
`;

const EditorSection = styled(motion.div)`
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 95%;
  max-width: 1200px;
  background: #0F172A;
  background: linear-gradient(160deg, #0F172A 0%, #1E293B 100%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-bottom: none;
  border-radius: 16px 16px 0 0;
  box-shadow: 0 -10px 30px rgba(0, 0, 0, 0.2);
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  overflow: hidden;
  z-index: 100;
  margin: 0 auto;
  backdrop-filter: blur(10px);
  
  @media (max-width: 768px) {
    width: 100%;
    border-radius: 0;
  }
`;

const TerminalContainer = styled.div`
  height: 100%;
  padding: 1.25rem;
  background: rgba(0, 0, 0, 0.25);
  
  .xterm {
    height: 100%;
    padding: 1.25rem;
    border-radius: 12px;
    background: rgba(0, 0, 0, 0.4);
    box-shadow: 
      inset 0 2px 4px rgba(0, 0, 0, 0.3),
      0 4px 6px -1px rgba(0, 0, 0, 0.1), 
      0 2px 4px -1px rgba(0, 0, 0, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.05);
    
    .xterm-viewport {
      scrollbar-width: thin;
      scrollbar-color: rgba(255, 255, 255, 0.2) transparent;
      
      &::-webkit-scrollbar {
        width: 6px;
        height: 6px;
      }
      
      &::-webkit-scrollbar-track {
        background: transparent;
      }
      
      &::-webkit-scrollbar-thumb {
        background-color: rgba(255, 255, 255, 0.2);
        border-radius: 3px;
      }
    }
  }
`;

const EditorHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.875rem 1.75rem;
  background: rgba(15, 23, 42, 0.95);
  backdrop-filter: blur(12px);
  color: #E2E8F0;
  font-weight: 500;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  position: relative;
  
  &::after {
    content: '';
    position: absolute;
    bottom: -1px;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  }
  
  & > div:first-child {
    font-size: 0.9375rem;
    font-weight: 600;
    letter-spacing: 0.3px;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    
    &::before {
      content: '>';
      color: #60A5FA;
      font-weight: bold;
    }
  }
`;

const EditorContent = styled.div`
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
`;

const CloseButton = styled.button`
  background: rgba(239, 68, 68, 0.15);
  border: 1px solid rgba(239, 68, 68, 0.25);
  color: #FCA5A5;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-size: 0.8125rem;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  margin-left: auto;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  
  &:hover {
    background: rgba(239, 68, 68, 0.2);
    color: #FECACA;
    transform: translateY(-1px);
  }
  
  &:active {
    transform: translateY(0);
  }
`;

const Badge = styled.span`
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: #F1F5F9;
  color: #475569;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease;
  border: 1px solid #E2E8F0;
  
  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  }
  border-radius: 9999px;
  font-size: 0.875rem;
`;

interface MainContentProps {
  module: ExtendedModuleType;
  showEditor: boolean;
  showTerminal: boolean;
  onShowEditor: (show: boolean) => void;
  _onShowTerminal?: (show: boolean) => void;
  _isIntegratedTerminal?: boolean;
  _onToggleTerminal?: () => void;
  _closeTerminal?: () => void;
}

const MainContent: React.FC<MainContentProps> = ({
  module,
  showEditor,
  showTerminal,
  onShowEditor,
  _onShowTerminal = () => {},
  _isIntegratedTerminal = false,
  _onToggleTerminal = () => {},
  _closeTerminal = () => {}
}) => {
  const [currentSnippet, setCurrentSnippet] = useState(module.snippet);
  const [codeOutput, setCodeOutput] = useState<{ [key: number]: string }>({});
  const [runningCode, setRunningCode] = useState<number | null>(null);
  const [autoScroll, setAutoScroll] = useState(true);
  const contentRef = useRef<HTMLDivElement>(null);
  const terminalRef = useRef<HTMLDivElement>(null);

  // Auto-scroll effect
  useEffect(() => {
    if (autoScroll && contentRef.current) {
      contentRef.current.scrollTop = contentRef.current.scrollHeight;
    }
  }, [module, autoScroll]);

  const [terminal, setTerminal] = useState<XTerminal | null>(null);
  const fitAddon = useRef<FitAddon>(new FitAddon());

  // Initialize terminal
  useEffect(() => {
    if (terminalRef.current && !terminal) {
      const terminalOptions: ITerminalOptions = {
        cursorBlink: true,
        theme: {
          background: '#ffffff',
          foreground: '#1f2937',
          cursor: '#1f2937',
          cursorAccent: '#1f2937',
        },
        fontSize: 14,
        fontFamily: '"Fira Code", monospace',
      };
      
      const newTerminal = new XTerminal(terminalOptions);

      newTerminal.loadAddon(fitAddon.current);
      newTerminal.open(terminalRef.current);
      fitAddon.current.fit();

      // Welcome message
      newTerminal.writeln('Welcome to the terminal!');
      newTerminal.writeln('Type `help` to see available commands.\r\n');

      // Simple command handling
      newTerminal.onData((data) => {
        if (data === '\r') {
          newTerminal.writeln('\r\nCommand not implemented yet.\r\n');
        }
      });

      setTerminal(newTerminal);

      // Handle window resize
      const handleResize = () => fitAddon.current?.fit();
      window.addEventListener('resize', handleResize);

      return () => {
        window.removeEventListener('resize', handleResize);
        newTerminal.dispose();
      };
    }
  }, [terminal]);

  // Handle terminal visibility changes
  useEffect(() => {
    if (terminal && terminalRef.current && fitAddon.current) {
      setTimeout(() => fitAddon.current?.fit(), 100);
    }
  }, [showTerminal, terminal]);

  // Use the terminal-related props to avoid unused variable warnings
  const terminalProps = {
    _onShowTerminal,
    _isIntegratedTerminal,
    _onToggleTerminal,
    _closeTerminal
  };
  
  // Log terminal props in development to avoid unused variable warnings
  if (process.env.NODE_ENV === 'development') {
    console.log('Terminal props:', terminalProps);
  }

  const handleRunCode = async (snippet: string, index: number) => {
    setRunningCode(index);
    setCodeOutput(prev => ({ ...prev, [index]: 'Running code...' }));
    
    try {
      // Simulate code execution
      await new Promise(resolve => setTimeout(resolve, 1000));
      setCodeOutput(prev => ({
        ...prev,
        [index]: 'Code executed successfully!\n' + snippet
      }));
    } catch (error) {
      setCodeOutput(prev => ({
        ...prev,
        [index]: 'Error executing code: ' + (error as Error).message
      }));
    } finally {
      setRunningCode(null);
    }
  };
  
  // Update currentSnippet when module changes
  useEffect(() => {
    setCurrentSnippet(module.snippet);
  }, [module]);

  const handleSnippetClick = (snippet: string) => {
    setCurrentSnippet(snippet);
    onShowEditor(true);
  };

  const renderModuleContent = () => (
    <div ref={contentRef} style={{ height: '100%', overflow: 'auto', background: 'white', padding: '2rem' }}>
      <div style={{ maxWidth: '800px', margin: '0 auto' }}>
        <h1 style={{ fontSize: '2.5rem', fontWeight: 'bold', color: '#1F2937', marginBottom: '1rem' }}>
          {module.label}
        </h1>
        
        <p style={{ fontSize: '1.125rem', color: '#4B5563', marginBottom: '2rem' }}>
          {module.description}
        </p>
        
        <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem', flexWrap: 'wrap' }}>
          {module.duration && (
            <Badge>
              <FiClock size={18} />
              <span>{module.duration}</span>
            </Badge>
          )}
          
          {module.exercises && (
            <Badge>
              <FiAward size={18} />
              <span>{module.exercises} exercises</span>
            </Badge>
          )}
          
          {module.lastUpdated && (
            <Badge>
              <FiCalendar size={18} />
              <span>Updated: {module.lastUpdated}</span>
            </Badge>
          )}
        </div>
        
        {/* Code Snippet Section */}
        <div style={{ marginTop: '2rem' }}>
          <div style={{ 
            display: 'flex', 
            justifyContent: 'space-between',
            alignItems: 'center',
            marginBottom: '1rem'
          }}>
            <h2 style={{ fontSize: '1.25rem', fontWeight: '600', color: '#1F2937' }}>Code Example</h2>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <button
                onClick={() => handleSnippetClick(module.snippet)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                  backgroundColor: '#F3F4F6',
                  border: 'none',
                  borderRadius: '0.375rem',
                  padding: '0.5rem 1rem',
                  cursor: 'pointer',
                  fontSize: '0.875rem',
                  color: '#4B5563'
                }}
              >
                <FiCode size={16} />
                <span>Open in Editor</span>
              </button>
              
              <button
                onClick={() => handleRunCode(module.snippet, 0)}
                disabled={runningCode === 0}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                  backgroundColor: runningCode === 0 ? '#9CA3AF' : '#10B981',
                  border: 'none',
                  borderRadius: '0.375rem',
                  padding: '0.5rem 1rem',
                  cursor: runningCode === 0 ? 'not-allowed' : 'pointer',
                  fontSize: '0.875rem',
                  color: 'white',
                  transition: 'background-color 0.2s'
                }}
              >
                <FiPlay size={16} />
                <span>{runningCode === 0 ? 'Running...' : 'Run Code'}</span>
              </button>
            </div>
          </div>
          
          <pre style={{
            backgroundColor: '#1E293B',
            color: '#E2E8F0',
            padding: '1.5rem',
            borderRadius: '0.5rem',
            overflowX: 'auto',
            fontSize: '0.875rem',
            lineHeight: '1.5',
            margin: 0,
            whiteSpace: 'pre-wrap',
            fontFamily: '"Fira Code", monospace'
          }}>
            <code>{module.snippet}</code>
          </pre>
          
          {codeOutput[0] && (
            <div style={{ 
              marginTop: '1rem',
              backgroundColor: '#F9FAFB',
              border: '1px solid #E5E7EB',
              borderRadius: '0.5rem',
              padding: '1rem',
              fontFamily: '"Fira Code", monospace',
              whiteSpace: 'pre-wrap',
              fontSize: '0.875rem',
              color: '#1F2937',
              maxHeight: '200px',
              overflowY: 'auto'
            }}>
              {codeOutput[0]}
            </div>
          )}
        </div>
        
        {/* Module Content */}
        <div style={{ marginTop: '3rem' }}>
          <h2 style={{ 
            fontSize: '1.5rem', 
            fontWeight: '600', 
            color: '#1F2937',
            marginBottom: '1.5rem',
            paddingBottom: '0.5rem',
            borderBottom: '1px solid #E5E7EB'
          }}>
            What You'll Learn
          </h2>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
            {module.content?.map((item, index) => {
              if (typeof item === 'string') {
                return (
                  <div 
                    key={index}
                    onMouseEnter={(e: React.MouseEvent<HTMLDivElement>) => {
                      const target = e.currentTarget;
                      target.style.transform = 'translateY(-2px)';
                      target.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)';
                    }}
                    onMouseLeave={(e: React.MouseEvent<HTMLDivElement>) => {
                      const target = e.currentTarget;
                      target.style.transform = '';
                      target.style.boxShadow = '';
                    }}
                    style={{
                      display: 'flex',
                      alignItems: 'flex-start',
                      gap: '0.75rem',
                      padding: '1rem',
                      backgroundColor: '#F9FAFB',
                      borderRadius: '0.5rem',
                      border: '1px solid #E5E7EB',
                      transition: 'all 0.2s'
                    }}
                  >
                    <div style={{
                      flexShrink: 0,
                      width: '24px',
                      height: '24px',
                      backgroundColor: '#10B981',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      color: 'white',
                      fontSize: '0.75rem',
                      fontWeight: '600'
                    }}>
                      {index + 1}
                    </div>
                    <p style={{ margin: 0, color: '#4B5563', lineHeight: '1.6' }}>{item}</p>
                  </div>
                );
              } else {
                // Handle ContentItem type
                return (
                  <div 
                    key={index}
                    style={{
                      backgroundColor: '#F9FAFB',
                      borderRadius: '0.5rem',
                      border: '1px solid #E5E7EB',
                      overflow: 'hidden',
                      transition: 'all 0.2s'
                    }}
                  >
                    <div 
                      onMouseEnter={(e: React.MouseEvent<HTMLDivElement>) => {
                        const target = e.currentTarget;
                        target.style.transform = 'translateY(-2px)';
                        target.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)';
                      }}
                      onMouseLeave={(e: React.MouseEvent<HTMLDivElement>) => {
                        const target = e.currentTarget;
                        target.style.transform = '';
                        target.style.boxShadow = '';
                      }}
                      style={{
                        padding: '1rem',
                        cursor: 'pointer',
                        transition: 'all 0.2s'
                      }}
                      onClick={() => handleSnippetClick(item.code)}
                    >
                      <div style={{ display: 'flex', gap: '0.75rem', marginBottom: '0.5rem' }}>
                        <div style={{
                          flexShrink: 0,
                          width: '24px',
                          height: '24px',
                          backgroundColor: '#3B82F6',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          color: 'white',
                          fontSize: '0.75rem',
                          fontWeight: '600',
                          borderRadius: '4px'
                        }}>
                          {index + 1}
                        </div>
                        <h3 style={{ 
                          margin: 0, 
                          color: '#1F2937', 
                          fontWeight: '600',
                          fontSize: '1rem'
                        }}>
                          {item.title}
                        </h3>
                      </div>
                      <p style={{ 
                        margin: '0.5rem 0 0 0', 
                        color: '#4B5563', 
                        lineHeight: '1.6',
                        fontSize: '0.9375rem',
                        paddingLeft: 'calc(24px + 0.75rem)'
                      }}>
                        {item.description}
                      </p>
                    </div>
                    {item.code && (
                      <pre style={{
                        margin: 0,
                        padding: '1rem',
                        backgroundColor: '#1E293B',
                        color: '#E2E8F0',
                        fontSize: '0.875rem',
                        lineHeight: '1.5',
                        borderTop: '1px solid #334155',
                        overflowX: 'auto',
                        fontFamily: '"Fira Code", monospace',
                        whiteSpace: 'pre-wrap',
                        wordBreak: 'break-word'
                      }}>
                        <code>{item.code}</code>
                      </pre>
                    )}
                  </div>
                );
              }
            })}
          </div>
        </div>
      </div>
    </div>
  );

  const helpContent = (
    <div style={{ padding: '8px 0' }}>
      <h3 style={{ margin: '0 0 12px 0', fontSize: '16px', color: '#111827' }}>Module Information</h3>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        <div>
          <strong>Duration:</strong> {module.duration} to complete
        </div>
        <div>
          <strong>Exercises:</strong> {module.exercises} hands-on exercises included
        </div>
        <div>
          <strong>Last Updated:</strong> {module.lastUpdated}
        </div>
        <div style={{ marginTop: '8px', fontSize: '14px', color: '#4B5563' }}>
          This module will help you understand key concepts through examples and practical exercises.
        </div>
      </div>
    </div>
  );

  const toggleAutoScroll = () => {
    setAutoScroll(prev => !prev);
  };

  return (
    <ContentContainer ref={contentRef} autoScroll={autoScroll}>
      <div style={{ 
        position: 'fixed', 
        top: '1rem', 
        right: '1.5rem',
        zIndex: 1000,
        display: 'flex',
        gap: '0.75rem',
        alignItems: 'center',
        backgroundColor: 'rgba(0, 0, 0, 0.7)',
        padding: '0.25rem 1rem',
        borderRadius: '20px',
        border: '1px solid #1F2937',
        backdropFilter: 'blur(4px)'
      }}>
        <span style={{ fontSize: '0.8rem', color: '#9CA3AF' }}>Auto-scroll:</span>
        <ScrollToggle 
          onClick={toggleAutoScroll}
          $isActive={autoScroll}
          title={autoScroll ? 'Click to disable auto-scroll' : 'Click to enable auto-scroll'}
        >
          {autoScroll ? 'ON' : 'OFF'}
        </ScrollToggle>
        <div style={{ width: '1px', height: '20px', background: '#374151' }}></div>
        <HelpTooltip content={helpContent} position="bottom" />
      </div>
      <Content
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
      >
        {renderModuleContent()}
      </Content>
      
      <EditorSection
        style={{
          transform: showEditor ? 'translateY(0)' : 'translateY(100%)',
          height: showEditor ? '60vh' : '0',
        }}
      >
        <EditorHeader>
          <div>Code Editor</div>
          <CloseButton onClick={() => onShowEditor(false)}>
            <FiX size={18} />
            Close
          </CloseButton>
        </EditorHeader>
        <EditorContent>
          <div style={{ flex: 1, minHeight: '400px' }}>
            <Suspense fallback={<div>Loading editor...</div>}>
              <MonacoEditor
                height="100%"
                defaultLanguage="python"
                value={currentSnippet}
                onChange={(value: string | undefined) => value && setCurrentSnippet(value)}
                theme="vs-light"
                options={{
                  minimap: { enabled: false },
                  fontSize: 14,
                  wordWrap: 'on',
                  automaticLayout: true,
                  scrollBeyondLastLine: false,
                }}
              />
            </Suspense>
          </div>
          {showTerminal && (
            <div style={{ 
              display: 'flex', 
              flexDirection: 'column',
              height: '300px',
              backgroundColor: '#ffffff',
              borderTop: '1px solid #e2e8f0',
              overflow: 'hidden'
            }}>
              <div style={{ 
                padding: '0.5rem 1rem', 
                backgroundColor: '#f8fafc', 
                borderBottom: '1px solid #e2e8f0',
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                color: '#475569',
                fontSize: '0.875rem'
              }}>
                <FiTerminal size={16} />
                <span>Terminal</span>
              </div>
              <div ref={terminalRef} style={{ flex: 1, padding: '0.5rem' }} />
            </div>
          )}
        </EditorContent>
      </EditorSection>
    </ContentContainer>
  );
};

export default MainContent;