from typing import List, Dict
from dataclasses import dataclass

@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int

@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int

def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Optimises the 3D printing queue according to priorities and printer constraints

    Args:
        print_jobs: List of print jobs
        constraints: Printer constraints

    Returns:
        Dict with the print order and total time
    """
    
    # Convert dicts into dataclass objects
    jobs = [PrintJob(**job) for job in print_jobs]
    printer = PrinterConstraints(**constraints)

    # Sort by priority
    jobs.sort(key=lambda x: x.priority)

    total_time = 0
    print_order = []

    i = 0
    while i < len(jobs):
        current_group = []
        current_volume = 0
        # Fill group while respecting constraints
        while (i < len(jobs) and 
               len(current_group) < printer.max_items and 
               current_volume + jobs[i].volume <= printer.max_volume):
            current_group.append(jobs[i])
            current_volume += jobs[i].volume
            i += 1

        # If current job doesn't fit, process it alone
        if not current_group:
            current_group.append(jobs[i])
            i += 1

        # Group print time = max of print times in the current group
        group_time = max(job.print_time for job in current_group)
        total_time += group_time
        print_order.extend([job.id for job in current_group])

    return {
        "print_order": print_order,
        "total_time": total_time
    }

# Testing
def test_printing_optimization():
    # Test 1: Models with the same priority
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    # Тест 2: Models with different priorities
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  # lab work
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},  # thesis
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}  # personal project
    ]

    # Тест 3: Exceeding volume constraints
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print("Test 1 (same priority):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Print order: {result1['print_order']}")
    print(f"Total time: {result1['total_time']} minutes")

    print("\nTest 2 (different priorities):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Print order: {result2['print_order']}")
    print(f"Total time: {result2['total_time']} minutes")

    print("\nTest 3 (exceeding constraints):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Print order: {result3['print_order']}")
    print(f"Total time: {result3['total_time']} minutes")

if __name__ == "__main__":
    test_printing_optimization()
