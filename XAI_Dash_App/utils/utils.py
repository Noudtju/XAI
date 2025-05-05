import pandas as pd
import numpy as np
import os
from datetime import datetime
import json

class DataLogger:
    def __init__(self, log_dir='../data/logs'):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(log_dir, f'study_logs_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx')
        
    def log_interaction(self, session_id, phase, event_type, data):
        """Log user interactions to Excel file"""
        timestamp = datetime.now().isoformat()
        log_data = {
            'session_id': session_id,
            'timestamp': timestamp,
            'phase': phase,
            'event_type': event_type,
            'data': json.dumps(data)
        }
        
        # Create or append to Excel file
        if not os.path.exists(self.log_file):
            df = pd.DataFrame([log_data])
            df.to_excel(self.log_file, index=False)
        else:
            df = pd.read_excel(self.log_file)
            df = pd.concat([df, pd.DataFrame([log_data])], ignore_index=True)
            df.to_excel(self.log_file, index=False)

def process_prediction_data(df):
    """Process the prediction data for display"""
    # Group by class_name and get top prototypes
    grouped = df.groupby('class_name').apply(
        lambda x: x.nlargest(5, 'activation_score')
    ).reset_index(drop=True)
    
    return grouped

def get_prototype_image_path(prototype_id):
    """Get the path to a prototype image"""
    base_path = '/Users/noudvansummeren/Documents/Directory/JADS/Semester_B/XAI/XAI/Database/visualized_prototypes'
    return os.path.join(base_path, str(prototype_id), 'prototype.png')

def calculate_metrics(log_file):
    """Calculate study metrics from logs"""
    if not os.path.exists(log_file):
        return {}
    
    df = pd.read_excel(log_file)
    metrics = {
        'total_participants': df['session_id'].nunique(),
        'avg_learning_time': None,  # To be implemented
        'avg_test_accuracy': None,  # To be implemented
        'avg_clarity_rating': None  # To be implemented
    }
    
    return metrics 