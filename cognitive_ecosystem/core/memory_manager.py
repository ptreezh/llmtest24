"""
记忆管理器

管理智能体的多层次记忆系统，包括：
- 工作记忆 (Working Memory): 当前任务相关的临时信息
- 短期记忆 (Short-term Memory): 近期经历和学习内容
- 长期记忆 (Long-term Memory): 持久化的知识和经验
- 情景记忆 (Episodic Memory): 具体事件和经历
- 语义记忆 (Semantic Memory): 概念性知识和规则
"""

import json
import numpy as np
import logging
import pickle
import sqlite3
from typing import Dict, List, Any, Optional, Tuple, Set, Union
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict, deque
import hashlib
from enum import Enum
import threading
import time
import math
from abc import ABC, abstractmethod


class MemoryType(Enum):
    """记忆类型"""
    WORKING = "working"          # 工作记忆
    SHORT_TERM = "short_term"    # 短期记忆
    LONG_TERM = "long_term"      # 长期记忆
    EPISODIC = "episodic"        # 情景记忆
    SEMANTIC = "semantic"        # 语义记忆


class MemoryImportance(Enum):
    """记忆重要性"""
    CRITICAL = "critical"        # 关键记忆
    HIGH = "high"               # 高重要性
    MEDIUM = "medium"           # 中等重要性
    LOW = "low"                 # 低重要性
    TRIVIAL = "trivial"         # 琐碎记忆


class MemoryStatus(Enum):
    """记忆状态"""
    ACTIVE = "active"           # 活跃状态
    DORMANT = "dormant"         # 休眠状态
    DECAYING = "decaying"       # 衰减状态
    ARCHIVED = "archived"       # 归档状态
    FORGOTTEN = "forgotten"     # 已遗忘


@dataclass
class MemoryItem:
    """记忆项"""
    memory_id: str
    agent_id: str
    content: Any
    memory_type: MemoryType
    importance: MemoryImportance
    status: MemoryStatus
    created_at: datetime
    last_accessed: datetime
    access_count: int = 0
    decay_rate: float = 0.1
    strength: float = 1.0
    associations: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'memory_id': self.memory_id,
            'agent_id': self.agent_id,
            'content': self.content,
            'memory_type': self.memory_type.value,
            'importance': self.importance.value,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'last_accessed': self.last_accessed.isoformat(),
            'access_count': self.access_count,
            'decay_rate': self.decay_rate,
            'strength': self.strength,
            'associations': self.associations,
            'tags': self.tags,
            'context': self.context,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemoryItem':
        """从字典创建"""
        return cls(
            memory_id=data['memory_id'],
            agent_id=data['agent_id'],
            content=data['content'],
            memory_type=MemoryType(data['memory_type']),
            importance=MemoryImportance(data['importance']),
            status=MemoryStatus(data['status']),
            created_at=datetime.fromisoformat(data['created_at']),
            last_accessed=datetime.fromisoformat(data['last_accessed']),
            access_count=data.get('access_count', 0),
            decay_rate=data.get('decay_rate', 0.1),
            strength=data.get('strength', 1.0),
            associations=data.get('associations', []),
            tags=data.get('tags', []),
            context=data.get('context', {}),
            metadata=data.get('metadata', {})
        )


@dataclass
class MemoryQuery:
    """记忆查询"""
    query_text: str
    memory_types: List[MemoryType] = field(default_factory=lambda: list(MemoryType))
    importance_threshold: MemoryImportance = MemoryImportance.LOW
    time_range: Optional[Tuple[datetime, datetime]] = None
    tags: List[str] = field(default_factory=list)
    context_filters: Dict[str, Any] = field(default_factory=dict)
    max_results: int = 10
    similarity_threshold: float = 0.5


@dataclass
class MemorySearchResult:
    """记忆搜索结果"""
    memory_item: MemoryItem
    relevance_score: float
    similarity_score: float
    recency_score: float
    importance_score: float
    final_score: float


@dataclass
class MemoryStatistics:
    """记忆统计"""
    agent_id: str
    total_memories: int
    memory_type_distribution: Dict[MemoryType, int]
    importance_distribution: Dict[MemoryImportance, int]
    status_distribution: Dict[MemoryStatus, int]
    avg_strength: float
    avg_access_count: float
    oldest_memory: Optional[datetime]
    newest_memory: Optional[datetime]
    memory_growth_rate: float
    forgetting_rate: float


class MemoryEncoder(ABC):
    """记忆编码器抽象基类"""
    
    @abstractmethod
    def encode(self, content: Any) -> np.ndarray:
        """编码内容为向量"""
        pass
    
    @abstractmethod
    def similarity(self, vector1: np.ndarray, vector2: np.ndarray) -> float:
        """计算相似度"""
        pass


class SimpleMemoryEncoder(MemoryEncoder):
    """简单记忆编码器"""
    
    def __init__(self, embedding_dim: int = 128):
        self.embedding_dim = embedding_dim
        self.word_to_idx = {}
        self.idx_to_word = {}
        self.vocab_size = 0
    
    def encode(self, content: Any) -> np.ndarray:
        """编码内容为向量"""
        if isinstance(content, str):
            return self._encode_text(content)
        elif isinstance(content, dict):
            return self._encode_dict(content)
        elif isinstance(content, list):
            return self._encode_list(content)
        else:
            return self._encode_text(str(content))
    
    def _encode_text(self, text: str) -> np.ndarray:
        """编码文本"""
        words = text.lower().split()
        vector = np.zeros(self.embedding_dim)
        
        for word in words:
            if word not in self.word_to_idx:
                self.word_to_idx[word] = self.vocab_size
                self.idx_to_word[self.vocab_size] = word
                self.vocab_size += 1
            
            idx = self.word_to_idx[word]
            # 简单的词向量表示
            vector[idx % self.embedding_dim] += 1
        
        # 归一化
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        
        return vector
    
    def _encode_dict(self, data: dict) -> np.ndarray:
        """编码字典"""
        text = " ".join(f"{k} {v}" for k, v in data.items())
        return self._encode_text(text)
    
    def _encode_list(self, data: list) -> np.ndarray:
        """编码列表"""
        text = " ".join(str(item) for item in data)
        return self._encode_text(text)
    
    def similarity(self, vector1: np.ndarray, vector2: np.ndarray) -> float:
        """计算余弦相似度"""
        dot_product = np.dot(vector1, vector2)
        norm1 = np.linalg.norm(vector1)
        norm2 = np.linalg.norm(vector2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)


class MemoryManager:
    """记忆管理器"""
    
    def __init__(self, 
                 data_dir: str = "cognitive_ecosystem/data/memory",
                 encoder: Optional[MemoryEncoder] = None,
                 max_working_memory: int = 7,
                 max_short_term_memory: int = 100,
                 decay_interval: int = 3600):  # 1小时
        
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # 记忆编码器
        self.encoder = encoder or SimpleMemoryEncoder()
        
        # 记忆容量限制
        self.max_working_memory = max_working_memory
        self.max_short_term_memory = max_short_term_memory
        
        # 记忆存储
        self.memories: Dict[str, MemoryItem] = {}
        self.memory_vectors: Dict[str, np.ndarray] = {}
        self.agent_memories: Dict[str, Set[str]] = defaultdict(set)
        
        # 工作记忆队列（每个智能体）
        self.working_memory: Dict[str, deque] = defaultdict(lambda: deque(maxlen=max_working_memory))
        
        # 记忆衰减
        self.decay_interval = decay_interval
        self.last_decay_time = time.time()
        
        # 数据库连接
        self.db_path = self.data_dir / "memory.db"
        self._init_database()
        
        # 线程锁
        self.lock = threading.RLock()
        
        # 统计信息
        self.access_stats = defaultdict(int)
        self.query_stats = defaultdict(int)
        
        # 设置日志
        self.logger = logging.getLogger(__name__)
        
        # 启动后台任务
        self._start_background_tasks()
        
        self.logger.info("记忆管理器初始化完成")
    
    def _init_database(self):
        """初始化数据库"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS memories (
                    memory_id TEXT PRIMARY KEY,
                    agent_id TEXT NOT NULL,
                    content TEXT NOT NULL,
                    memory_type TEXT NOT NULL,
                    importance TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    last_accessed TEXT NOT NULL,
                    access_count INTEGER DEFAULT 0,
                    decay_rate REAL DEFAULT 0.1,
                    strength REAL DEFAULT 1.0,
                    associations TEXT DEFAULT '[]',
                    tags TEXT DEFAULT '[]',
                    context TEXT DEFAULT '{}',
                    metadata TEXT DEFAULT '{}'
                )
            ''')
            
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_agent_id ON memories(agent_id)
            ''')
            
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_memory_type ON memories(memory_type)
            ''')
            
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_importance ON memories(importance)
            ''')
            
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_created_at ON memories(created_at)
            ''')
    
    def _start_background_tasks(self):
        """启动后台任务"""
        def background_worker():
            while True:
                try:
                    # 记忆衰减
                    if time.time() - self.last_decay_time > self.decay_interval:
                        self._decay_memories()
                        self.last_decay_time = time.time()
                    
                    # 记忆整合
                    self._consolidate_memories()
                    
                    # 清理过期记忆
                    self._cleanup_expired_memories()
                    
                    time.sleep(300)  # 5分钟检查一次
                    
                except Exception as e:
                    self.logger.error(f"后台任务执行错误: {e}")
                    time.sleep(60)
        
        thread = threading.Thread(target=background_worker, daemon=True)
        thread.start()
    
    def store_memory(self, 
                    agent_id: str,
                    content: Any,
                    memory_type: MemoryType = MemoryType.SHORT_TERM,
                    importance: MemoryImportance = MemoryImportance.MEDIUM,
                    tags: List[str] = None,
                    context: Dict[str, Any] = None) -> str:
        """存储记忆"""
        with self.lock:
            # 生成记忆ID
            memory_id = self._generate_memory_id(agent_id, content)
            
            # 创建记忆项
            memory_item = MemoryItem(
                memory_id=memory_id,
                agent_id=agent_id,
                content=content,
                memory_type=memory_type,
                importance=importance,
                status=MemoryStatus.ACTIVE,
                created_at=datetime.now(),
                last_accessed=datetime.now(),
                tags=tags or [],
                context=context or {}
            )
            
            # 编码记忆内容
            memory_vector = self.encoder.encode(content)
            
            # 存储记忆
            self.memories[memory_id] = memory_item
            self.memory_vectors[memory_id] = memory_vector
            self.agent_memories[agent_id].add(memory_id)
            
            # 添加到工作记忆
            if memory_type == MemoryType.WORKING:
                self.working_memory[agent_id].append(memory_id)
            
            # 检查容量限制
            self._enforce_capacity_limits(agent_id)
            
            # 持久化到数据库
            self._save_memory_to_db(memory_item)
            
            # 更新统计
            self.access_stats[f"{agent_id}_store"] += 1
            
            self.logger.debug(f"存储记忆: {memory_id} for agent {agent_id}")
            
            return memory_id
    
    def retrieve_memory(self, memory_id: str) -> Optional[MemoryItem]:
        """检索特定记忆"""
        with self.lock:
            if memory_id not in self.memories:
                # 尝试从数据库加载
                memory_item = self._load_memory_from_db(memory_id)
                if memory_item:
                    self.memories[memory_id] = memory_item
                    self.memory_vectors[memory_id] = self.encoder.encode(memory_item.content)
                    self.agent_memories[memory_item.agent_id].add(memory_id)
                else:
                    return None
            
            memory_item = self.memories[memory_id]
            
            # 更新访问信息
            memory_item.last_accessed = datetime.now()
            memory_item.access_count += 1
            
            # 增强记忆强度
            memory_item.strength = min(1.0, memory_item.strength + 0.1)
            
            # 更新统计
            self.access_stats[f"{memory_item.agent_id}_retrieve"] += 1
            
            return memory_item
    
    def search_memories(self, agent_id: str, query: MemoryQuery) -> List[MemorySearchResult]:
        """搜索记忆"""
        with self.lock:
            # 编码查询
            query_vector = self.encoder.encode(query.query_text)
            
            # 获取候选记忆
            candidate_memories = []
            for memory_id in self.agent_memories[agent_id]:
                if memory_id in self.memories:
                    memory_item = self.memories[memory_id]
                    
                    # 过滤条件检查
                    if not self._matches_query_filters(memory_item, query):
                        continue
                    
                    candidate_memories.append(memory_item)
            
            # 计算相关性得分
            search_results = []
            for memory_item in candidate_memories:
                memory_vector = self.memory_vectors.get(memory_item.memory_id)
                if memory_vector is None:
                    continue
                
                # 计算各种得分
                similarity_score = self.encoder.similarity(query_vector, memory_vector)
                recency_score = self._calculate_recency_score(memory_item)
                importance_score = self._calculate_importance_score(memory_item)
                relevance_score = self._calculate_relevance_score(memory_item, query)
                
                # 综合得分
                final_score = (
                    similarity_score * 0.4 +
                    recency_score * 0.2 +
                    importance_score * 0.3 +
                    relevance_score * 0.1
                )
                
                if final_score >= query.similarity_threshold:
                    search_results.append(MemorySearchResult(
                        memory_item=memory_item,
                        relevance_score=relevance_score,
                        similarity_score=similarity_score,
                        recency_score=recency_score,
                        importance_score=importance_score,
                        final_score=final_score
                    ))
            
            # 排序并限制结果数量
            search_results.sort(key=lambda x: x.final_score, reverse=True)
            search_results = search_results[:query.max_results]
            
            # 更新访问统计
            self.query_stats[f"{agent_id}_search"] += 1
            
            return search_results
    
    def _matches_query_filters(self, memory_item: MemoryItem, query: MemoryQuery) -> bool:
        """检查记忆是否匹配查询过滤条件"""
        # 记忆类型过滤
        if query.memory_types and memory_item.memory_type not in query.memory_types:
            return False
        
        # 重要性过滤
        importance_levels = {
            MemoryImportance.TRIVIAL: 0,
            MemoryImportance.LOW: 1,
            MemoryImportance.MEDIUM: 2,
            MemoryImportance.HIGH: 3,
            MemoryImportance.CRITICAL: 4
        }
        if importance_levels[memory_item.importance] < importance_levels[query.importance_threshold]:
            return False
        
        # 时间范围过滤
        if query.time_range:
            start_time, end_time = query.time_range
            if not (start_time <= memory_item.created_at <= end_time):
                return False
        
        # 标签过滤
        if query.tags:
            if not any(tag in memory_item.tags for tag in query.tags):
                return False
        
        # 上下文过滤
        if query.context_filters:
            for key, value in query.context_filters.items():
                if memory_item.context.get(key) != value:
                    return False
        
        return True
    
    def _calculate_recency_score(self, memory_item: MemoryItem) -> float:
        """计算新近性得分"""
        now = datetime.now()
        time_diff = (now - memory_item.last_accessed).total_seconds()
        
        # 使用指数衰减函数
        decay_constant = 86400  # 1天
        recency_score = math.exp(-time_diff / decay_constant)
        
        return recency_score
    
    def _calculate_importance_score(self, memory_item: MemoryItem) -> float:
        """计算重要性得分"""
        importance_scores = {
            MemoryImportance.TRIVIAL: 0.1,
            MemoryImportance.LOW: 0.3,
            MemoryImportance.MEDIUM: 0.5,
            MemoryImportance.HIGH: 0.8,
            MemoryImportance.CRITICAL: 1.0
        }
        
        base_score = importance_scores[memory_item.importance]
        
        # 考虑访问频率
        access_bonus = min(0.2, memory_item.access_count * 0.01)
        
        # 考虑记忆强度
        strength_bonus = memory_item.strength * 0.1
        
        return min(1.0, base_score + access_bonus + strength_bonus)
    
    def _calculate_relevance_score(self, memory_item: MemoryItem, query: MemoryQuery) -> float:
        """计算相关性得分"""
        relevance_score = 0.0
        
        # 标签匹配
        if query.tags:
            matching_tags = set(query.tags) & set(memory_item.tags)
            tag_score = len(matching_tags) / len(query.tags)
            relevance_score += tag_score * 0.5
        
        # 上下文匹配
        if query.context_filters:
            matching_context = 0
            for key, value in query.context_filters.items():
                if memory_item.context.get(key) == value:
                    matching_context += 1
            context_score = matching_context / len(query.context_filters)
            relevance_score += context_score * 0.3
        
        # 记忆类型匹配
        if query.memory_types and memory_item.memory_type in query.memory_types:
            relevance_score += 0.2
        
        return min(1.0, relevance_score)
    
    def update_memory(self, memory_id: str, **updates) -> bool:
        """更新记忆"""
        with self.lock:
            if memory_id not in self.memories:
                return False
            
            memory_item = self.memories[memory_id]
            
            # 更新字段
            for field, value in updates.items():
                if hasattr(memory_item, field):
                    setattr(memory_item, field, value)
            
            # 如果内容更新，重新编码
            if 'content' in updates:
                self.memory_vectors[memory_id] = self.encoder.encode(memory_item.content)
            
            # 更新访问时间
            memory_item.last_accessed = datetime.now()
            
            # 持久化更新
            self._save_memory_to_db(memory_item)
            
            return True
    
    def delete_memory(self, memory_id: str) -> bool:
        """删除记忆"""
        with self.lock:
            if memory_id not in self.memories:
                return False
            
            memory_item = self.memories[memory_id]
            agent_id = memory_item.agent_id
            
            # 从内存中删除
            del self.memories[memory_id]
            if memory_id in self.memory_vectors:
                del self.memory_vectors[memory_id]
            
            self.agent_memories[agent_id].discard(memory_id)
            
            # 从工作记忆中删除
            if memory_id in self.working_memory[agent_id]:
                working_memory_list = list(self.working_memory[agent_id])
                working_memory_list.remove(memory_id)
                self.working_memory[agent_id] = deque(working_memory_list, maxlen=self.max_working_memory)
            
            # 从数据库删除
            self._delete_memory_from_db(memory_id)
            
            return True
    
    def get_working_memory(self, agent_id: str) -> List[MemoryItem]:
        """获取工作记忆"""
        with self.lock:
            working_memory_ids = list(self.working_memory[agent_id])
            working_memories = []
            
            for memory_id in working_memory_ids:
                if memory_id in self.memories:
                    working_memories.append(self.memories[memory_id])
            
            return working_memories
    
    def clear_working_memory(self, agent_id: str):
        """清空工作记忆"""
        with self.lock:
            self.working_memory[agent_id].clear()
    
    def consolidate_memory(self, agent_id: str, memory_ids: List[str], 
                          consolidated_content: Any, 
                          importance: MemoryImportance = MemoryImportance.HIGH) -> str:
        """整合记忆"""
        with self.lock:
            # 获取要整合的记忆
            memories_to_consolidate = []
            for memory_id in memory_ids:
                if memory_id in self.memories:
                    memories_to_consolidate.append(self.memories[memory_id])
            
            if not memories_to_consolidate:
                return None
            
            # 创建整合后的记忆
            consolidated_memory_id = self.store_memory(
                agent_id=agent_id,
                content=consolidated_content,
                memory_type=MemoryType.LONG_TERM,
                importance=importance,
                tags=list(set(tag for memory in memories_to_consolidate for tag in memory.tags)),
                context={
                    'consolidated_from': memory_ids,
                    'consolidation_time': datetime.now().isoformat(),
                    'original_count': len(memories_to_consolidate)
                }
            )
            
            # 标记原记忆为已归档
            for memory_id in memory_ids:
                if memory_id in self.memories:
                    self.memories[memory_id].status = MemoryStatus.ARCHIVED
                    self._save_memory_to_db(self.memories[memory_id])
            
            return consolidated_memory_id
    
    def _enforce_capacity_limits(self, agent_id: str):
        """强制执行容量限制"""
        # 短期记忆容量限制
        short_term_memories = [
            memory_id for memory_id in self.agent_memories[agent_id]
            if memory_id in self.memories and 
            self.memories[memory_id].memory_type == MemoryType.SHORT_TERM and
            self.memories[memory_id].status == MemoryStatus.ACTIVE
        ]
        
        if len(short_term_memories) > self.max_short_term_memory:
            # 按重要性和访问频率排序，删除最不重要的记忆
            memories_to_remove = sorted(
                short_term_memories,
                key=lambda mid: (
                    self.memories[mid].importance.value,
                    self.memories[mid].access_count,
                    self.memories[mid].strength
                )
            )[:-self.max_short_term_memory]
            
            for memory_id in memories_to_remove:
                self.memories[memory_id].status = MemoryStatus.ARCHIVED
                self._save_memory_to_db(self.memories[memory_id])
    
    def _decay_memories(self):
        """记忆衰减"""
        with self.lock:
            current_time = datetime.now()
            
            for memory_id, memory_item in self.memories.items():
                if memory_item.status != MemoryStatus.ACTIVE:
                    continue
                
                # 计算衰减
                time_since_access = (current_time - memory_item.last_accessed).total_seconds()
                decay_amount = memory_item.decay_rate * (time_since_access / 86400)  # 按天计算
                
                memory_item.strength = max(0.0, memory_item.strength - decay_amount)
                
                # 如果强度过低，标记为衰减状态
                if memory_item.strength < 0.1:
                    memory_item.status = MemoryStatus.DECAYING
                
                # 如果强度接近0，标记为遗忘
                if memory_item.strength < 0.01:
                    memory_item.status = MemoryStatus.FORGOTTEN
                
                # 持久化更新
                self._save_memory_to_db(memory_item)
    
    def _consolidate_memories(self):
        """自动记忆整合"""
        with self.lock:
            # 为每个智能体进行记忆整合
            for agent_id in self.agent_memories:
                self._consolidate_agent_memories(agent_id)
    
    def _consolidate_agent_memories(self, agent_id: str):
        """整合特定智能体的记忆"""
        # 获取短期记忆
        short_term_memories = [
            self.memories[memory_id] for memory_id in self.agent_memories[agent_id]
            if memory_id in self.memories and 
            self.memories[memory_id].memory_type == MemoryType.SHORT_TERM and
            self.memories[memory_id].status == MemoryStatus.ACTIVE and
            self.memories[memory_id].access_count > 3  # 访问次数超过3次
        ]
        
        if len(short_term_memories) < 3:
            return
        
        # 按相似性聚类
        memory_clusters = self._cluster_memories(short_term_memories)
        
        # 整合每个聚类
        for cluster in memory_clusters:
            if len(cluster) >= 3:  # 至少3个记忆才整合
                self._consolidate_memory_cluster(agent_id, cluster)
    
    def _cluster_memories(self, memories: List[MemoryItem]) -> List[List[MemoryItem]]:
        """聚类记忆"""
        clusters = []
        used_memories = set()
        
        for i, memory1 in enumerate(memories):
            if memory1.memory_id in used_memories:
                continue
            
            cluster = [memory1]
            used_memories.add(memory1.memory_id)
            
            for j, memory2 in enumerate(memories[i+1:], i+1):
                if memory2.memory_id in used_memories:
                    continue
                
                # 计算相似性
                vector1 = self.memory_vectors.get(memory1.memory_id)
                vector2 = self.memory_vectors.get(memory2.memory_id)
                
                if vector1 is not None and vector2 is not None:
                    similarity = self.encoder.similarity(vector1, vector2)
                    
                    if similarity > 0.7:  # 相似性阈值
                        cluster.append(memory2)
                        used_memories.add(memory2.memory_id)
            
            if len(cluster) > 1:
                clusters.append(cluster)
        
        return clusters
    
    def _consolidate_memory_cluster(self, agent_id: str, cluster: List[MemoryItem]):
        """整合记忆聚类"""
        # 提取共同主题和内容
        all_content = []
        all_tags = set()
        all_contexts = {}
        
        for memory in cluster:
            all_content.append(str(memory.content))
            all_tags.update(memory.tags)
            all_contexts.update(memory.context)
        
        # 创建整合内容
        consolidated_content = {
            'summary': f"整合了{len(cluster)}个相关记忆",
            'contents': all_content,
            'common_themes': list(all_tags),
            'consolidated_at': datetime.now().isoformat()
        }
        
        # 确定重要性
        max_importance = max(memory.importance for memory in cluster)
        
        # 执行整合
        memory_ids = [memory.memory_id for memory in cluster]
        self.consolidate_memory(
            agent_id=agent_id,
            memory_ids=memory_ids,
            consolidated_content=consolidated_content,
            importance=max_importance
        )
    
    def _cleanup_expired_memories(self):
        """清理过期记忆"""
        with self.lock:
            current_time = datetime.now()
            expired_threshold = current_time - timedelta(days=30)  # 30天前
            
            memories_to_delete = []
            
            for memory_id, memory_item in self.memories.items():
                # 删除遗忘状态且很久没访问的记忆
                if (memory_item.status == MemoryStatus.FORGOTTEN and 
                    memory_item.last_accessed < expired_threshold):
                    memories_to_delete.append(memory_id)
                
                # 删除琐碎且很久没访问的记忆
                elif (memory_item.importance == MemoryImportance.TRIVIAL and
                      memory_item.last_accessed < expired_threshold and
                      memory_item.access_count < 2):
                    memories_to_delete.append(memory_id)
            
            # 执行删除
            for memory_id in memories_to_delete:
                self.delete_memory(memory_id)
    
    def get_memory_statistics(self, agent_id: str) -> MemoryStatistics:
        """获取记忆统计"""
        with self.lock:
            agent_memory_ids = self.agent_memories[agent_id]
            agent_memories = [self.memories[mid] for mid in agent_memory_ids if mid in self.memories]
            
            if not agent_memories:
                return MemoryStatistics(
                    agent_id=agent_id,
                    total_memories=0,
                    memory_type_distribution={},
                    importance_distribution={},
                    status_distribution={},
                    avg_strength=0.0,
                    avg_access_count=0.0,
                    oldest_memory=None,
                    newest_memory=None,
                    memory_growth_rate=0.0,
                    forgetting_rate=0.0
                )
            
            # 统计分布
            type_dist = defaultdict(int)
            importance_dist = defaultdict(int)
            status_dist = defaultdict(int)
            
            total_strength = 0
            total_access = 0
            creation_times = []
            
            for memory in agent_memories:
                type_dist[memory.memory_type] += 1
                importance_dist[memory.importance] += 1
                status_dist[memory.status] += 1
                total_strength += memory.strength
                total_access += memory.access_count
                creation_times.append(memory.created_at)
            
            # 计算增长率和遗忘率
            now = datetime.now()
            recent_memories = [m for m in agent_memories if (now - m.created_at).days <= 7]
            forgotten_memories = [m for m in agent_memories if m.status == MemoryStatus.FORGOTTEN]
            
            growth_rate = len(recent_memories) / 7  # 每天新增记忆数
            forgetting_rate = len(forgotten_memories) / len(agent_memories) if agent_memories else 0
            
            return MemoryStatistics(
                agent_id=agent_id,
                total_memories=len(agent_memories),
                memory_type_distribution=dict(type_dist),
                importance_distribution=dict(importance_dist),
                status_distribution=dict(status_dist),
                avg_strength=total_strength / len(agent_memories),
                avg_access_count=total_access / len(agent_memories),
                oldest_memory=min(creation_times) if creation_times else None,
                newest_memory=max(creation_times) if creation_times else None,
                memory_growth_rate=growth_rate,
                forgetting_rate=forgetting_rate
            )
    
    def export_memories(self, agent_id: str, output_file: str, 
                       include_vectors: bool = False):
        """导出记忆"""
        with self.lock:
            agent_memory_ids = self.agent_memories[agent_id]
            agent_memories = [self.memories[mid] for mid in agent_memory_ids if mid in self.memories]
            
            export_data = {
                'agent_id': agent_id,
                'export_timestamp': datetime.now().isoformat(),
                'total_memories': len(agent_memories),
                'memories': [memory.to_dict() for memory in agent_memories],
                'statistics': asdict(self.get_memory_statistics(agent_id))
            }
            
            if include_vectors:
                export_data['memory_vectors'] = {
                    memory_id: vector.tolist() 
                    for memory_id, vector in self.memory_vectors.items()
                    if memory_id in agent_memory_ids
                }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"记忆数据已导出到: {output_file}")
    
    def import_memories(self, input_file: str) -> int:
        """导入记忆"""
        with open(input_file, 'r', encoding='utf-8') as f:
            import_data = json.load(f)
        
        imported_count = 0
        
        with self.lock:
            for memory_data in import_data.get('memories', []):
                try:
                    memory_item = MemoryItem.from_dict(memory_data)
                    
                    # 检查是否已存在
                    if memory_item.memory_id not in self.memories:
                        self.memories[memory_item.memory_id] = memory_item
                        self.memory_vectors[memory_item.memory_id] = self.encoder.encode(memory_item.content)
                        self.agent_memories[memory_item.agent_id].add(memory_item.memory_id)
                        
                        # 持久化
                        self._save_memory_to_db(memory_item)
                        
                        imported_count += 1
                
                except Exception as e:
                    self.logger.error(f"导入记忆失败: {e}")
        
        self.logger.info(f"成功导入 {imported_count} 个记忆")
        return imported_count
    
    def _generate_memory_id(self, agent_id: str, content: Any) -> str:
        """生成记忆ID"""
        content_str = str(content)
        timestamp = datetime.now().isoformat()
        combined = f"{agent_id}_{content_str}_{timestamp}"
        return hashlib.md5(combined.encode()).hexdigest()
    
    def _save_memory_to_db(self, memory_item: MemoryItem):
        """保存记忆到数据库"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT OR REPLACE INTO memories 
                    (memory_id, agent_id, content, memory_type, importance, status,
                     created_at, last_accessed, access_count, decay_rate, strength,
                     associations, tags, context, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    memory_item.memory_id,
                    memory_item.agent_id,
                    json.dumps(memory_item.content, ensure_ascii=False),
                    memory_item.memory_type.value,
                    memory_item.importance.value,
                    memory_item.status.value,
                    memory_item.created_at.isoformat(),
                    memory_item.last_accessed.isoformat(),
                    memory_item.access_count,
                    memory_item.decay_rate,
                    memory_item.strength,
                    json.dumps(memory_item.associations),
                    json.dumps(memory_item.tags),
                    json.dumps(memory_item.context),
                    json.dumps(memory_item.metadata)
                ))
        except Exception as e:
            self.logger.error(f"保存记忆到数据库失败: {e}")
    
    def _load_memory_from_db(self, memory_id: str) -> Optional[MemoryItem]:
        """从数据库加载记忆"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    'SELECT * FROM memories WHERE memory_id = ?',
                    (memory_id,)
                )
                row = cursor.fetchone()
                
                if row:
                    return MemoryItem(
                        memory_id=row[0],
                        agent_id=row[1],
                        content=json.loads(row[2]),
                        memory_type=MemoryType(row[3]),
                        importance=MemoryImportance(row[4]),
                        status=MemoryStatus(row[5]),
                        created_at=datetime.fromisoformat(row[6]),
                        last_accessed=datetime.fromisoformat(row[7]),
                        access_count=row[8],
                        decay_rate=row[9],
                        strength=row[10],
                        associations=json.loads(row[11]),
                        tags=json.loads(row[12]),
                        context=json.loads(row[13]),
                        metadata=json.loads(row[14])
                    )
        except Exception as e:
            self.logger.error(f"从数据库加载记忆失败: {e}")
        
        return None
    
    def _delete_memory_from_db(self, memory_id: str):
        """从数据库删除记忆"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('DELETE FROM memories WHERE memory_id = ?', (memory_id,))
        except Exception as e:
            self.logger.error(f"从数据库删除记忆失败: {e}")
    
    def close(self):
        """关闭记忆管理器"""
        with self.lock:
            # 保存所有未保存的记忆
            for memory_item in self.memories.values():
                self._save_memory_to_db(memory_item)
            
            self.logger.info("记忆管理器已关闭")