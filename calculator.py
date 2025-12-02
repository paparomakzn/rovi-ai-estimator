# calculator.py - Расчет смет
from config import Config
from database import get_normatives

class Calculator:
    @staticmethod
    def calculate_estimate(work_type, area):
        """Рассчитать смету"""
        normatives = get_normatives(work_type)
        
        if not normatives:
            return None
        
        estimate_lines = []
        total_cost = 0
        
        for norm in normatives:
            quantity = area
            unit_price = norm['unit_price']
            line_total = quantity * unit_price
            
            estimate_lines.append({
                'work': norm['work'],
                'unit': norm['unit'],
                'quantity': quantity,
                'unit_price': unit_price,
                'total_price': line_total
            })
            
            total_cost += line_total
        
        # Добавляем накладные расходы (20%)
        overhead = total_cost * 0.2
        estimate_lines.append({
            'work': 'Накладные расходы',
            'unit': 'комплекс',
            'quantity': 1,
            'unit_price': overhead,
            'total_price': overhead
        })
        
        total_cost += overhead
        
        return {
            'lines': estimate_lines,
            'total': total_cost,
            'area': area,
            'work_type': work_type
        }
    
    @staticmethod
    def detect_work_type(text):
        """Определить тип работ из текста"""
        text = text.lower()
        
        if any(word in text for word in ['покраск', 'краск', 'окраск']):
            return 'wall_painting'
        elif any(word in text for word in ['плитк', 'кафел', 'укладк']):
            return 'tiling'
        elif any(word in text for word in ['обо', 'оклейк']):
            return 'wallpaper'
        elif any(word in text for word in ['штукатур', 'гипс']):
            return 'plaster'
        elif any(word in text for word in ['гипсокартон', 'гкл']):
            return 'drywall'
        
        return None