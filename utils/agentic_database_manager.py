"""
Agentic AI Database Manager
Comprehensive database infrastructure for AI agent operations and flywheel data collection
"""

import json
import uuid
import time
import sqlite3
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import pickle
import hashlib
from collections import defaultdict
import threading

class AgentState(Enum):
    """Agent execution states"""
    INITIALIZED = "initialized"
    RUNNING = "running"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"
    TERMINATED = "terminated"

class InteractionType(Enum):
    """Types of agent interactions"""
    USER_QUERY = "user_query"
    AGENT_RESPONSE = "agent_response"
    TOOL_CALL = "tool_call"
    MEMORY_ACCESS = "memory_access"
    KNOWLEDGE_RETRIEVAL = "knowledge_retrieval"
    DECISION_POINT = "decision_point"
    ERROR_HANDLING = "error_handling"

@dataclass
class AgentMemory:
    """Agent memory structure"""
    memory_id: str
    agent_id: str
    memory_type: str  # episodic, semantic, procedural, working
    content: Dict[str, Any]
    embedding: Optional[List[float]]
    importance_score: float
    created_at: datetime
    last_accessed: datetime
    access_count: int
    retention_policy: str

@dataclass
class AgentInteraction:
    """Agent interaction log"""
    interaction_id: str
    session_id: str
    agent_id: str
    interaction_type: InteractionType
    input_data: Dict[str, Any]
    output_data: Dict[str, Any]
    context: Dict[str, Any]
    performance_metrics: Dict[str, Any]
    timestamp: datetime
    duration_ms: int
    success: bool
    error_details: Optional[str]

class AgenticDatabaseManager:
    """
    Comprehensive database manager for agentic AI systems
    Supports the complete AI agent lifecycle and flywheel data collection
    """
    
    def __init__(self, db_path: str = "agentic_ai.db"):
        self.db_path = db_path
        self.conn = None
        self.lock = threading.Lock()
        self.session_cache = {}
        self.memory_cache = {}
        self.performance_cache = defaultdict(list)
        
        self._initialize_databases()
    
    def _initialize_databases(self):
        """Initialize all agent-specific database tables"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        
        # Agent Registry - Track all agents and their capabilities
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS agent_registry (
                agent_id TEXT PRIMARY KEY,
                agent_type TEXT NOT NULL,
                capabilities TEXT NOT NULL,  -- JSON array
                version TEXT NOT NULL,
                status TEXT NOT NULL,
                configuration TEXT,  -- JSON
                performance_metrics TEXT,  -- JSON
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP,
                total_interactions INTEGER DEFAULT 0,
                success_rate REAL DEFAULT 0.0
            )
        """)
        
        # Agent Sessions - Track conversation/task sessions
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS agent_sessions (
                session_id TEXT PRIMARY KEY,
                agent_id TEXT NOT NULL,
                user_id TEXT,
                session_type TEXT NOT NULL,  -- conversation, task, workflow
                context TEXT,  -- JSON
                state TEXT NOT NULL,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ended_at TIMESTAMP,
                interaction_count INTEGER DEFAULT 0,
                goal_completion REAL DEFAULT 0.0,
                metadata TEXT,  -- JSON
                FOREIGN KEY (agent_id) REFERENCES agent_registry (agent_id)
            )
        """)
        
        # Agent Memory - Episodic, semantic, procedural memory
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS agent_memory (
                memory_id TEXT PRIMARY KEY,
                agent_id TEXT NOT NULL,
                session_id TEXT,
                memory_type TEXT NOT NULL,  -- episodic, semantic, procedural, working
                content TEXT NOT NULL,  -- JSON
                embedding BLOB,  -- Vector embedding
                importance_score REAL DEFAULT 0.5,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                access_count INTEGER DEFAULT 0,
                retention_policy TEXT DEFAULT 'standard',
                tags TEXT,  -- JSON array
                FOREIGN KEY (agent_id) REFERENCES agent_registry (agent_id),
                FOREIGN KEY (session_id) REFERENCES agent_sessions (session_id)
            )
        """)
        
        # Agent Interactions - Complete interaction logs for flywheel
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS agent_interactions (
                interaction_id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                interaction_type TEXT NOT NULL,
                input_data TEXT NOT NULL,  -- JSON
                output_data TEXT NOT NULL,  -- JSON
                context TEXT,  -- JSON
                performance_metrics TEXT,  -- JSON
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                duration_ms INTEGER DEFAULT 0,
                success BOOLEAN DEFAULT TRUE,
                error_details TEXT,
                user_feedback_score REAL,
                improvement_suggestions TEXT,  -- JSON
                FOREIGN KEY (agent_id) REFERENCES agent_registry (agent_id),
                FOREIGN KEY (session_id) REFERENCES agent_sessions (session_id)
            )
        """)
        
        # Tool Usage Logs - Track agent tool usage patterns
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS tool_usage_logs (
                usage_id TEXT PRIMARY KEY,
                agent_id TEXT NOT NULL,
                session_id TEXT NOT NULL,
                tool_name TEXT NOT NULL,
                parameters TEXT,  -- JSON
                result TEXT,  -- JSON
                execution_time_ms INTEGER DEFAULT 0,
                success BOOLEAN DEFAULT TRUE,
                error_message TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                cost_estimate REAL DEFAULT 0.0,
                FOREIGN KEY (agent_id) REFERENCES agent_registry (agent_id),
                FOREIGN KEY (session_id) REFERENCES agent_sessions (session_id)
            )
        """)
        
        # Knowledge Graph - Dynamic knowledge relationships
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_graph (
                node_id TEXT PRIMARY KEY,
                node_type TEXT NOT NULL,  -- concept, entity, relationship
                content TEXT NOT NULL,  -- JSON
                embedding BLOB,  -- Vector embedding
                confidence_score REAL DEFAULT 0.5,
                source_interaction_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                validation_status TEXT DEFAULT 'pending',
                connections TEXT,  -- JSON array of connected node_ids
                FOREIGN KEY (source_interaction_id) REFERENCES agent_interactions (interaction_id)
            )
        """)
        
        # Learning Events - Track agent learning and improvement
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS learning_events (
                event_id TEXT PRIMARY KEY,
                agent_id TEXT NOT NULL,
                event_type TEXT NOT NULL,  -- reinforcement, correction, new_pattern
                trigger_interaction_id TEXT,
                learning_data TEXT NOT NULL,  -- JSON
                performance_impact REAL DEFAULT 0.0,
                confidence REAL DEFAULT 0.5,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                applied_at TIMESTAMP,
                effectiveness_score REAL,
                FOREIGN KEY (agent_id) REFERENCES agent_registry (agent_id),
                FOREIGN KEY (trigger_interaction_id) REFERENCES agent_interactions (interaction_id)
            )
        """)
        
        # Performance Analytics - Aggregate performance data
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS performance_analytics (
                metric_id TEXT PRIMARY KEY,
                agent_id TEXT NOT NULL,
                metric_type TEXT NOT NULL,  -- response_time, accuracy, user_satisfaction
                metric_value REAL NOT NULL,
                measurement_window TEXT NOT NULL,  -- hour, day, week, month
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                context_filters TEXT,  -- JSON
                trend_direction TEXT,  -- improving, declining, stable
                FOREIGN KEY (agent_id) REFERENCES agent_registry (agent_id)
            )
        """)
        
        # User Feedback - Capture user feedback for flywheel
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS user_feedback (
                feedback_id TEXT PRIMARY KEY,
                interaction_id TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                user_id TEXT,
                feedback_type TEXT NOT NULL,  -- rating, correction, suggestion
                feedback_data TEXT NOT NULL,  -- JSON
                sentiment_score REAL,
                processed BOOLEAN DEFAULT FALSE,
                processing_results TEXT,  -- JSON
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (interaction_id) REFERENCES agent_interactions (interaction_id),
                FOREIGN KEY (agent_id) REFERENCES agent_registry (agent_id)
            )
        """)
        
        self.conn.commit()
        self._create_indexes()
    
    def _create_indexes(self):
        """Create performance indexes for agent operations"""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_agent_sessions_agent_id ON agent_sessions(agent_id)",
            "CREATE INDEX IF NOT EXISTS idx_agent_memory_agent_id ON agent_memory(agent_id)",
            "CREATE INDEX IF NOT EXISTS idx_agent_interactions_session_id ON agent_interactions(session_id)",
            "CREATE INDEX IF NOT EXISTS idx_agent_interactions_timestamp ON agent_interactions(timestamp)",
            "CREATE INDEX IF NOT EXISTS idx_tool_usage_agent_id ON tool_usage_logs(agent_id)",
            "CREATE INDEX IF NOT EXISTS idx_knowledge_graph_type ON knowledge_graph(node_type)",
            "CREATE INDEX IF NOT EXISTS idx_learning_events_agent_id ON learning_events(agent_id)",
            "CREATE INDEX IF NOT EXISTS idx_performance_analytics_agent_id ON performance_analytics(agent_id)",
            "CREATE INDEX IF NOT EXISTS idx_user_feedback_processed ON user_feedback(processed)"
        ]
        
        for index in indexes:
            self.conn.execute(index)
        self.conn.commit()
    
    def register_agent(self, agent_id: str, agent_type: str, capabilities: List[str], 
                      version: str = "1.0.0", configuration: Dict[str, Any] = None) -> bool:
        """Register a new agent in the system"""
        try:
            with self.lock:
                self.conn.execute("""
                    INSERT OR REPLACE INTO agent_registry 
                    (agent_id, agent_type, capabilities, version, status, configuration, last_active)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    agent_id,
                    agent_type,
                    json.dumps(capabilities),
                    version,
                    AgentState.INITIALIZED.value,
                    json.dumps(configuration or {}),
                    datetime.utcnow().isoformat()
                ))
                self.conn.commit()
                return True
        except Exception as e:
            print(f"Failed to register agent {agent_id}: {e}")
            return False
    
    def start_session(self, agent_id: str, session_type: str = "conversation", 
                     user_id: str = None, context: Dict[str, Any] = None) -> str:
        """Start a new agent session"""
        session_id = str(uuid.uuid4())
        
        try:
            with self.lock:
                self.conn.execute("""
                    INSERT INTO agent_sessions 
                    (session_id, agent_id, user_id, session_type, context, state)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    session_id,
                    agent_id,
                    user_id,
                    session_type,
                    json.dumps(context or {}),
                    AgentState.RUNNING.value
                ))
                self.conn.commit()
                
                # Update agent last active
                self.update_agent_status(agent_id, AgentState.RUNNING)
                
                return session_id
        except Exception as e:
            print(f"Failed to start session: {e}")
            return None
    
    def log_interaction(self, session_id: str, agent_id: str, interaction_type: InteractionType,
                       input_data: Dict[str, Any], output_data: Dict[str, Any],
                       context: Dict[str, Any] = None, duration_ms: int = 0,
                       success: bool = True, error_details: str = None) -> str:
        """Log an agent interaction for flywheel data collection"""
        interaction_id = str(uuid.uuid4())
        
        # Calculate performance metrics
        performance_metrics = {
            "response_time_ms": duration_ms,
            "input_tokens": len(str(input_data)),
            "output_tokens": len(str(output_data)),
            "timestamp": datetime.utcnow().isoformat(),
            "success": success
        }
        
        try:
            with self.lock:
                self.conn.execute("""
                    INSERT INTO agent_interactions 
                    (interaction_id, session_id, agent_id, interaction_type, input_data, 
                     output_data, context, performance_metrics, duration_ms, success, error_details)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    interaction_id,
                    session_id,
                    agent_id,
                    interaction_type.value,
                    json.dumps(input_data),
                    json.dumps(output_data),
                    json.dumps(context or {}),
                    json.dumps(performance_metrics),
                    duration_ms,
                    success,
                    error_details
                ))
                
                # Update session interaction count
                self.conn.execute("""
                    UPDATE agent_sessions 
                    SET interaction_count = interaction_count + 1
                    WHERE session_id = ?
                """, (session_id,))
                
                # Update agent total interactions
                self.conn.execute("""
                    UPDATE agent_registry 
                    SET total_interactions = total_interactions + 1,
                        last_active = ?
                    WHERE agent_id = ?
                """, (datetime.utcnow().isoformat(), agent_id))
                
                self.conn.commit()
                
                # Cache for quick access
                self.performance_cache[agent_id].append({
                    "interaction_id": interaction_id,
                    "duration_ms": duration_ms,
                    "success": success,
                    "timestamp": datetime.utcnow()
                })
                
                return interaction_id
        except Exception as e:
            print(f"Failed to log interaction: {e}")
            return None
    
    def store_memory(self, agent_id: str, session_id: str, memory_type: str,
                    content: Dict[str, Any], importance_score: float = 0.5,
                    embedding: List[float] = None, tags: List[str] = None) -> str:
        """Store agent memory for learning and context"""
        memory_id = str(uuid.uuid4())
        
        try:
            with self.lock:
                self.conn.execute("""
                    INSERT INTO agent_memory 
                    (memory_id, agent_id, session_id, memory_type, content, 
                     embedding, importance_score, tags)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    memory_id,
                    agent_id,
                    session_id,
                    memory_type,
                    json.dumps(content),
                    pickle.dumps(embedding) if embedding else None,
                    importance_score,
                    json.dumps(tags or [])
                ))
                self.conn.commit()
                
                # Cache recent memories
                self.memory_cache[agent_id] = self.memory_cache.get(agent_id, [])
                self.memory_cache[agent_id].append({
                    "memory_id": memory_id,
                    "content": content,
                    "importance_score": importance_score,
                    "created_at": datetime.utcnow()
                })
                
                return memory_id
        except Exception as e:
            print(f"Failed to store memory: {e}")
            return None
    
    def log_tool_usage(self, agent_id: str, session_id: str, tool_name: str,
                      parameters: Dict[str, Any], result: Dict[str, Any],
                      execution_time_ms: int, success: bool = True,
                      error_message: str = None, cost_estimate: float = 0.0) -> str:
        """Log tool usage for performance analysis"""
        usage_id = str(uuid.uuid4())
        
        try:
            with self.lock:
                self.conn.execute("""
                    INSERT INTO tool_usage_logs 
                    (usage_id, agent_id, session_id, tool_name, parameters, result,
                     execution_time_ms, success, error_message, cost_estimate)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    usage_id,
                    agent_id,
                    session_id,
                    tool_name,
                    json.dumps(parameters),
                    json.dumps(result),
                    execution_time_ms,
                    success,
                    error_message,
                    cost_estimate
                ))
                self.conn.commit()
                return usage_id
        except Exception as e:
            print(f"Failed to log tool usage: {e}")
            return None
    
    def record_learning_event(self, agent_id: str, event_type: str,
                             learning_data: Dict[str, Any], trigger_interaction_id: str = None,
                             performance_impact: float = 0.0, confidence: float = 0.5) -> str:
        """Record learning events for agent improvement"""
        event_id = str(uuid.uuid4())
        
        try:
            with self.lock:
                self.conn.execute("""
                    INSERT INTO learning_events 
                    (event_id, agent_id, event_type, trigger_interaction_id, 
                     learning_data, performance_impact, confidence)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    event_id,
                    agent_id,
                    event_type,
                    trigger_interaction_id,
                    json.dumps(learning_data),
                    performance_impact,
                    confidence
                ))
                self.conn.commit()
                return event_id
        except Exception as e:
            print(f"Failed to record learning event: {e}")
            return None
    
    def add_user_feedback(self, interaction_id: str, agent_id: str, user_id: str,
                         feedback_type: str, feedback_data: Dict[str, Any],
                         sentiment_score: float = None) -> str:
        """Add user feedback for flywheel improvement"""
        feedback_id = str(uuid.uuid4())
        
        try:
            with self.lock:
                self.conn.execute("""
                    INSERT INTO user_feedback 
                    (feedback_id, interaction_id, agent_id, user_id, feedback_type,
                     feedback_data, sentiment_score)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    feedback_id,
                    interaction_id,
                    agent_id,
                    user_id,
                    feedback_type,
                    json.dumps(feedback_data),
                    sentiment_score
                ))
                self.conn.commit()
                return feedback_id
        except Exception as e:
            print(f"Failed to add user feedback: {e}")
            return None
    
    def update_agent_status(self, agent_id: str, status: AgentState):
        """Update agent status and last active time"""
        try:
            with self.lock:
                self.conn.execute("""
                    UPDATE agent_registry 
                    SET status = ?, last_active = ?
                    WHERE agent_id = ?
                """, (status.value, datetime.utcnow().isoformat(), agent_id))
                self.conn.commit()
        except Exception as e:
            print(f"Failed to update agent status: {e}")
    
    def get_agent_performance_metrics(self, agent_id: str, time_window: str = "24h") -> Dict[str, Any]:
        """Get comprehensive performance metrics for an agent"""
        try:
            # Calculate time threshold
            if time_window == "1h":
                threshold = datetime.utcnow() - timedelta(hours=1)
            elif time_window == "24h":
                threshold = datetime.utcnow() - timedelta(days=1)
            elif time_window == "7d":
                threshold = datetime.utcnow() - timedelta(days=7)
            else:
                threshold = datetime.utcnow() - timedelta(days=30)
            
            # Get interaction metrics
            cursor = self.conn.execute("""
                SELECT COUNT(*) as total_interactions,
                       AVG(duration_ms) as avg_response_time,
                       SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as success_rate,
                       AVG(user_feedback_score) as avg_user_rating
                FROM agent_interactions 
                WHERE agent_id = ? AND timestamp > ?
            """, (agent_id, threshold.isoformat()))
            
            metrics = dict(cursor.fetchone())
            
            # Get tool usage metrics
            cursor = self.conn.execute("""
                SELECT tool_name, COUNT(*) as usage_count,
                       AVG(execution_time_ms) as avg_execution_time,
                       SUM(cost_estimate) as total_cost
                FROM tool_usage_logs 
                WHERE agent_id = ? AND timestamp > ?
                GROUP BY tool_name
            """, (agent_id, threshold.isoformat()))
            
            tool_metrics = [dict(row) for row in cursor.fetchall()]
            
            # Get learning events
            cursor = self.conn.execute("""
                SELECT event_type, COUNT(*) as event_count,
                       AVG(performance_impact) as avg_impact
                FROM learning_events 
                WHERE agent_id = ? AND timestamp > ?
                GROUP BY event_type
            """, (agent_id, threshold.isoformat()))
            
            learning_metrics = [dict(row) for row in cursor.fetchall()]
            
            return {
                "agent_id": agent_id,
                "time_window": time_window,
                "interaction_metrics": metrics,
                "tool_usage": tool_metrics,
                "learning_events": learning_metrics,
                "generated_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            print(f"Failed to get performance metrics: {e}")
            return {"error": str(e)}
    
    def get_flywheel_analytics(self) -> Dict[str, Any]:
        """Get comprehensive flywheel analytics across all agents"""
        try:
            # Overall system metrics
            cursor = self.conn.execute("""
                SELECT COUNT(DISTINCT agent_id) as total_agents,
                       COUNT(DISTINCT session_id) as total_sessions,
                       COUNT(*) as total_interactions,
                       AVG(duration_ms) as avg_response_time,
                       SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as overall_success_rate
                FROM agent_interactions 
                WHERE timestamp > datetime('now', '-7 days')
            """)
            
            system_metrics = dict(cursor.fetchone())
            
            # Agent performance ranking
            cursor = self.conn.execute("""
                SELECT ai.agent_id, ar.agent_type,
                       COUNT(*) as interactions,
                       AVG(ai.duration_ms) as avg_response_time,
                       SUM(CASE WHEN ai.success = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as success_rate,
                       AVG(uf.sentiment_score) as avg_sentiment
                FROM agent_interactions ai
                JOIN agent_registry ar ON ai.agent_id = ar.agent_id
                LEFT JOIN user_feedback uf ON ai.interaction_id = uf.interaction_id
                WHERE ai.timestamp > datetime('now', '-7 days')
                GROUP BY ai.agent_id, ar.agent_type
                ORDER BY success_rate DESC, avg_response_time ASC
            """)
            
            agent_rankings = [dict(row) for row in cursor.fetchall()]
            
            # Learning trends
            cursor = self.conn.execute("""
                SELECT event_type, COUNT(*) as event_count,
                       AVG(performance_impact) as avg_impact,
                       DATE(timestamp) as event_date
                FROM learning_events 
                WHERE timestamp > datetime('now', '-30 days')
                GROUP BY event_type, DATE(timestamp)
                ORDER BY event_date DESC
            """)
            
            learning_trends = [dict(row) for row in cursor.fetchall()]
            
            # User feedback trends
            cursor = self.conn.execute("""
                SELECT feedback_type, COUNT(*) as feedback_count,
                       AVG(sentiment_score) as avg_sentiment,
                       DATE(timestamp) as feedback_date
                FROM user_feedback 
                WHERE timestamp > datetime('now', '-30 days')
                GROUP BY feedback_type, DATE(timestamp)
                ORDER BY feedback_date DESC
            """)
            
            feedback_trends = [dict(row) for row in cursor.fetchall()]
            
            return {
                "system_metrics": system_metrics,
                "agent_rankings": agent_rankings,
                "learning_trends": learning_trends,
                "feedback_trends": feedback_trends,
                "generated_at": datetime.utcnow().isoformat(),
                "data_quality": {
                    "total_data_points": system_metrics.get("total_interactions", 0),
                    "feedback_coverage": len(feedback_trends) / max(system_metrics.get("total_interactions", 1), 1),
                    "learning_velocity": len(learning_trends)
                }
            }
            
        except Exception as e:
            print(f"Failed to get flywheel analytics: {e}")
            return {"error": str(e)}
    
    def cleanup_old_data(self, retention_days: int = 90):
        """Clean up old data based on retention policies"""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=retention_days)
            
            with self.lock:
                # Clean up old interactions (keep aggregated metrics)
                self.conn.execute("""
                    DELETE FROM agent_interactions 
                    WHERE timestamp < ? AND user_feedback_score IS NULL
                """, (cutoff_date.isoformat(),))
                
                # Clean up low-importance memories
                self.conn.execute("""
                    DELETE FROM agent_memory 
                    WHERE created_at < ? AND importance_score < 0.3 AND access_count < 2
                """, (cutoff_date.isoformat(),))
                
                # Clean up processed feedback
                self.conn.execute("""
                    DELETE FROM user_feedback 
                    WHERE timestamp < ? AND processed = 1
                """, (cutoff_date.isoformat(),))
                
                self.conn.commit()
                
                print(f"Cleaned up data older than {retention_days} days")
                
        except Exception as e:
            print(f"Failed to cleanup old data: {e}")
    
    def health_check(self) -> Dict[str, Any]:
        """Comprehensive health check for agentic database systems"""
        try:
            # Database connectivity
            cursor = self.conn.execute("SELECT COUNT(*) FROM agent_registry")
            agent_count = cursor.fetchone()[0]
            
            # Recent activity
            cursor = self.conn.execute("""
                SELECT COUNT(*) FROM agent_interactions 
                WHERE timestamp > datetime('now', '-1 hour')
            """)
            recent_interactions = cursor.fetchone()[0]
            
            # System performance
            cursor = self.conn.execute("""
                SELECT AVG(duration_ms) as avg_response_time,
                       SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as success_rate
                FROM agent_interactions 
                WHERE timestamp > datetime('now', '-24 hours')
            """)
            performance = dict(cursor.fetchone())
            
            return {
                "status": "healthy",
                "components": {
                    "agent_registry": {
                        "status": "healthy",
                        "agent_count": agent_count
                    },
                    "interaction_logging": {
                        "status": "healthy",
                        "recent_interactions": recent_interactions
                    },
                    "performance_monitoring": {
                        "status": "healthy",
                        "avg_response_time": performance.get("avg_response_time", 0),
                        "success_rate": performance.get("success_rate", 100)
                    }
                },
                "last_checked": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "last_checked": datetime.utcnow().isoformat()
            }

# Global instance
_agentic_db_manager = None

def get_agentic_database_manager() -> AgenticDatabaseManager:
    """Get or create the global agentic database manager instance"""
    global _agentic_db_manager
    if _agentic_db_manager is None:
        _agentic_db_manager = AgenticDatabaseManager()
    return _agentic_db_manager