from collections import Counter
from typing import List, Dict, Set, Any

import numpy as np
from src.models.log_record import LogRecord


async def analyze_logs(logs: List[LogRecord]) -> Dict[str, Any]:
    """
    Анализирует список записей логов и возвращает словарь с результатами
    анализа.

    :param logs: Список записей логов.
    :return: Словарь с результатами анализа.
    """
    if not logs:
        return {
            'total_requests': 0,
            'resources': Counter(),
            'statuses': Counter(),
            'avg_size': 0.0,
            'p95_size': 0.0,
            'max_size': 0,
            'unique_ips': 0
        }

    total_requests: int = len(logs)
    resources: Counter = Counter(log.request for log in logs)
    statuses: Counter = Counter(log.status for log in logs)
    sizes: List[int] = [log.size for log in logs]
    unique_ips: Set[str] = {log.ip for log in logs}

    avg_size: float = sum(sizes) / len(sizes)
    p95_size: float = np.percentile(sizes, 95)
    max_size: int = max(sizes)

    return {
        'total_requests': total_requests,
        'resources': resources,
        'statuses': statuses,
        'avg_size': avg_size,
        'p95_size': p95_size,
        'max_size': max_size,
        'unique_ips': len(unique_ips)
    }
