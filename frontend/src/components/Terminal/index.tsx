import React, { useEffect, useRef } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { Terminal as XTerminal } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';
import { FiChevronDown, FiChevronUp } from 'react-icons/fi';
import 'xterm/css/xterm.css';

const TerminalContainer = styled(motion.div)`
  width: 100%;
  height: 100%;
  background: rgba(15, 23, 42, 0.95);
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
`;

const TerminalHeader = styled.div`
  padding: 0.75rem 1.5rem;
  background: rgba(30, 41, 59, 0.8);
  color: #E2E8F0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  border-bottom: 1px solid rgba(51, 65, 85, 0.3);
  
  h3 {
    margin: 0;
    font-size: 0.9rem;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
`;

const TerminalContent = styled.div`
  flex: 1;
  padding: 1rem;
  overflow: hidden;
`;

const StatusBar = styled.div`
  padding: 0.5rem 1.5rem;
  background: rgba(30, 41, 59, 0.8);
  border-top: 1px solid rgba(51, 65, 85, 0.3);
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.8rem;
  color: #94A3B8;
`;

interface TerminalProps {
  isOpen: boolean;
  onToggle: () => void;
  output?: string;
}

const Terminal = React.forwardRef<any, TerminalProps>(({ isOpen, onToggle, output = '' }, ref) => {
  const terminalRef = useRef<HTMLDivElement>(null);
  const terminalInstance = useRef<XTerminal | null>(null);
  const fitAddon = useRef(new FitAddon());
  const outputQueue = useRef<string[]>([]);
  const isProcessing = useRef(false);

  useEffect(() => {
    if (terminalRef.current && !terminalInstance.current) {
      const term = new XTerminal({
        cursorBlink: true,
        fontSize: 14,
        fontFamily: "'Fira Code', monospace",
        theme: {
          background: 'transparent',
          foreground: '#E2E8F0',
          cursor: '#4F46E5'
        },
      });
      
      term.loadAddon(fitAddon.current);
      term.open(terminalRef.current);
      fitAddon.current.fit();
      
      // Welcome message and commands
      term.writeln('\x1b[1;36mWelcome to Developer Terminal\x1b[0m');
      term.writeln('Type \x1b[1;33mhelp\x1b[0m to see available commands\n');
      term.write('\x1b[1;32m$\x1b[0m ');
      
      // Command handling
      let currentLine = '';
      term.onData((data) => {
        const char = data;
        
        if (char === '\r') { // Enter key
          term.write('\r\n');
          handleCommand(currentLine.trim(), term);
          currentLine = '';
          term.write('\x1b[1;32m$\x1b[0m ');
        } else if (char === '\x7f') { // Backspace
          if (currentLine.length > 0) {
            currentLine = currentLine.slice(0, -1);
            term.write('\b \b');
          }
        } else {
          currentLine += char;
          term.write(char);
        }
      });
      
      terminalInstance.current = term;
    }
  }, []);

  const handleCommand = (command: string, term: XTerminal) => {
    switch (command.toLowerCase()) {
      case 'help':
        term.writeln('\x1b[1;36mAvailable commands:\x1b[0m');
        term.writeln('  \x1b[1;33mhelp\x1b[0m    - Show this help');
        term.writeln('  \x1b[1;33mclear\x1b[0m   - Clear terminal');
        term.writeln('  \x1b[1;33mabout\x1b[0m   - About developer');
        term.writeln('  \x1b[1;33mprojects\x1b[0m - List projects');
        term.writeln('  \x1b[1;33mskills\x1b[0m   - Technical skills');
        break;
      case 'clear':
        term.clear();
        break;
      case 'about':
        term.writeln('\x1b[1;36mFull-Stack Developer\x1b[0m');
        term.writeln('Passionate about creating amazing web experiences');
        break;
      case 'projects':
        term.writeln('\x1b[1;36mFeatured Projects:\x1b[0m');
        term.writeln('  • E-Commerce Platform (React/Node.js)');
        term.writeln('  • Task Management App (Vue.js/Firebase)');
        term.writeln('  • AI Chatbot (Python/React)');
        break;
      case 'skills':
        term.writeln('\x1b[1;36mTechnical Skills:\x1b[0m');
        term.writeln('  • Frontend: React, Vue.js, TypeScript');
        term.writeln('  • Backend: Node.js, Python, PostgreSQL');
        term.writeln('  • Tools: Git, Docker, AWS');
        break;
      case '':
        break;
        term.writeln(`\x1b[1;31mCommand not found: ${command}\x1b[0m`);
        term.writeln('Type \x1b[1;33mhelp\x1b[0m for available commands');
    }
  };

  // Add a method to scroll to bottom that can be called from parent
  const scrollToBottom = () => {
    if (terminalInstance.current) {
      terminalInstance.current.scrollToBottom();
    }
  };

  // Handle output updates
  useEffect(() => {
    if (output && terminalInstance.current) {
      // Split the output by newlines and add to queue
      const lines = output.split('\n');
      outputQueue.current = [...outputQueue.current, ...lines];
      
      // Process the queue if not already processing
      const processQueue = async () => {
        if (isProcessing.current || !terminalInstance.current) return;
        
        isProcessing.current = true;
        
        while (outputQueue.current.length > 0) {
          const line = outputQueue.current.shift();
          if (line !== undefined) {
            terminalInstance.current.writeln(line);
            // Small delay to prevent UI freezing
            await new Promise(resolve => setTimeout(resolve, 10));
          }
        }
        
        isProcessing.current = false;
        scrollToBottom();
      };
      
      processQueue();
    }
  }, [output]);
  
  // Expose the scrollToBottom method via ref
  React.useImperativeHandle(ref, () => ({
    scrollToBottom: () => {
      if (terminalInstance.current) {
        terminalInstance.current.scrollToBottom();
      }
    }
  }));

  // Update terminal output when output prop changes
  useEffect(() => {
    if (terminalInstance.current && output) {
      terminalInstance.current.write(output);
      scrollToBottom();
    }
  }, [output]);

  return (
    <TerminalContainer
      initial={{ opacity: 0, height: 0 }}
      animate={isOpen ? { opacity: 1, height: '100%' } : { opacity: 0, height: 0 }}
      transition={{ duration: 0.3 }}
    >
      <TerminalHeader onClick={onToggle}>
        <h3>
          <FiChevronDown size={16} />
          Terminal
        </h3>
        <FiChevronUp size={16} />
      </TerminalHeader>
      
      <TerminalContent 
        ref={terminalRef}
        style={{ 
          padding: '0.5rem',
          flex: 1,
          minHeight: 0
        }} 
      />
      
      <StatusBar>
        <span>Developer Mode</span>
        <span>Ready</span>
      </StatusBar>
    </TerminalContainer>
  );
});

Terminal.displayName = 'Terminal';

export default Terminal;