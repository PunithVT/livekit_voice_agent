-- PostgreSQL initialization script for LiveKit Voice Agent

-- Create tables
CREATE TABLE IF NOT EXISTS subtopics (
    id SERIAL PRIMARY KEY,
    topic VARCHAR(255) NOT NULL,
    subtopic VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS conversations (
    id SERIAL PRIMARY KEY,
    room_name VARCHAR(255) NOT NULL,
    user_identity VARCHAR(255) NOT NULL,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    status VARCHAR(50) DEFAULT 'active',
    metadata JSONB
);

CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

CREATE TABLE IF NOT EXISTS user_profiles (
    id SERIAL PRIMARY KEY,
    user_identity VARCHAR(255) UNIQUE NOT NULL,
    display_name VARCHAR(255),
    preferences JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS session_analytics (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations(id) ON DELETE CASCADE,
    metric_name VARCHAR(100) NOT NULL,
    metric_value NUMERIC,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_subtopics_topic ON subtopics(topic);
CREATE INDEX IF NOT EXISTS idx_conversations_room ON conversations(room_name);
CREATE INDEX IF NOT EXISTS idx_conversations_user ON conversations(user_identity);
CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp);
CREATE INDEX IF NOT EXISTS idx_analytics_conversation ON session_analytics(conversation_id);
CREATE INDEX IF NOT EXISTS idx_analytics_metric ON session_analytics(metric_name);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers for updated_at columns
CREATE TRIGGER update_subtopics_updated_at
    BEFORE UPDATE ON subtopics
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_profiles_updated_at
    BEFORE UPDATE ON user_profiles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data
INSERT INTO subtopics (topic, subtopic, content) VALUES
('Mathematics', 'Algebra Basics', 'Algebra is a branch of mathematics that uses letters and symbols to represent numbers and quantities in formulas and equations.'),
('Mathematics', 'Geometry Fundamentals', 'Geometry is the study of shapes, sizes, and properties of figures and spaces.'),
('Physics', 'Newtonian Mechanics', 'Classical mechanics describes the motion of objects and the forces that affect them.'),
('Computer Science', 'Data Structures', 'Data structures are ways of organizing and storing data efficiently for various operations.')
ON CONFLICT DO NOTHING;

-- Create views for common queries
CREATE OR REPLACE VIEW conversation_summary AS
SELECT
    c.id,
    c.room_name,
    c.user_identity,
    c.started_at,
    c.ended_at,
    c.status,
    COUNT(m.id) as message_count,
    MAX(m.timestamp) as last_message_at
FROM conversations c
LEFT JOIN messages m ON c.id = m.conversation_id
GROUP BY c.id, c.room_name, c.user_identity, c.started_at, c.ended_at, c.status;

-- Grant permissions (adjust as needed for your setup)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO livekit;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO livekit;
