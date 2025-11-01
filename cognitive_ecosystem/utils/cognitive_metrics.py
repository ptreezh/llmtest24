import numpy as np

def calculate_cognitive_diversity_index(agents):
    """
    计算认知多样性指数 (CDI)
    CDI = (生态位分化度 × 0.3) + (功能互补度 × 0.3) + 
          (风格差异度 × 0.2) + (知识领域分布 × 0.2)
    """
    # This is a placeholder implementation.
    # A real implementation would require agent objects with niche, function, style, and knowledge attributes.
    if not agents:
        return 0.0
    
    # Placeholder values
    niche_differentiation = np.random.rand()
    functional_complementarity = np.random.rand()
    style_difference = np.random.rand()
    knowledge_distribution = np.random.rand()
    
    cdi = (niche_differentiation * 0.3) + \
          (functional_complementarity * 0.3) + \
          (style_difference * 0.2) + \
          (knowledge_distribution * 0.2)
          
    return cdi

def detect_emergence(group_performance, sum_individual_performance):
    """
    涌现检测: 群体表现 > 个体表现之和
    涌现指数 = (群体表现 - 个体表现之和) / 个体表现之和
    """
    if sum_individual_performance == 0:
        return 0.0
        
    emergence_index = (group_performance - sum_individual_performance) / sum_individual_performance
    return emergence_index

def calculate_resilience_score(pre_stress, post_stress, recovery_time):
    """
    韧性得分 = (恢复程度 × 0.5) + (恢复速度 × 0.3) + (适应能力 × 0.2)
    """
    # This is a placeholder implementation.
    # A real implementation would require more detailed metrics.
    recovery_level = post_stress / pre_stress if pre_stress > 0 else 0
    recovery_speed = 1 / (1 + recovery_time) # Simple inverse relationship
    adaptability = np.random.rand() # Placeholder for adaptability metric

    resilience_score = (recovery_level * 0.5) + (recovery_speed * 0.3) + (adaptability * 0.2)
    return min(1.0, max(0.0, resilience_score))
