"""
AI Service - Hybrid OpenAI + Gemini
Provides fallback between OpenAI and Gemini for email classification.
"""

import logging
from typing import Dict, List
from flask import current_app

logger = logging.getLogger(__name__)

class AIService:
    """Hybrid AI service with OpenAI and Gemini fallback."""
    
    def __init__(self):
        self.openai_service = None
        self.gemini_service = None
        self.model = "hybrid"  # Add model attribute
        self._initialize_services()
    
    def _initialize_services(self):
        """Initialize both OpenAI and Gemini services."""
        try:
            # Try OpenAI first
            from .openai_service import OpenAIService
            self.openai_service = OpenAIService()
            if self.openai_service.client:
                logger.info("✅ OpenAI service initialized")
            else:
                logger.warning("⚠️ OpenAI service not available")
        except Exception as e:
            logger.warning(f"OpenAI service failed: {e}")
        
        try:
            # Try Gemini as fallback
            from .gemini_service import GeminiService
            self.gemini_service = GeminiService()
            if self.gemini_service.client:
                logger.info("✅ Gemini service initialized")
            else:
                logger.warning("⚠️ Gemini service not available")
        except Exception as e:
            logger.warning(f"Gemini service failed: {e}")
    
    def get_status(self):
        """Get service status."""
        status = {
            'service': 'AIService',
            'openai_available': self.openai_service and self.openai_service.client is not None,
            'gemini_available': self.gemini_service and self.gemini_service.client is not None,
            'primary_service': None
        }
        
        if status['openai_available']:
            status['primary_service'] = 'openai'
        elif status['gemini_available']:
            status['primary_service'] = 'gemini'
        else:
            status['primary_service'] = 'fallback'
        
        return status
    
    def classify_email(self, email_data: Dict) -> Dict:
        """Classify email using available AI service."""
        
        # Try OpenAI first
        if self.openai_service and self.openai_service.client:
            try:
                logger.info("Using OpenAI for classification")
                return self.openai_service.classify_email(email_data)
            except Exception as e:
                logger.warning(f"OpenAI classification failed: {e}")
        
        # Try Gemini as fallback
        if self.gemini_service and self.gemini_service.client:
            try:
                logger.info("Using Gemini for classification")
                return self.gemini_service.classify_email(email_data)
            except Exception as e:
                logger.warning(f"Gemini classification failed: {e}")
        
        # Use rule-based fallback
        logger.warning("All AI services failed, using rule-based classification")
        if self.openai_service:
            return self.openai_service._fallback_classification(email_data)
        elif self.gemini_service:
            return self.gemini_service._fallback_classification(email_data)
        else:
            # Basic fallback if no service available
            return {
                'urgency_category': 'medium',
                'confidence_score': 0.5,
                'reasoning': 'AI services not available - using basic classification',
                'sender_type': 'externo',
                'email_type': 'academico',
                'requires_immediate_action': False,
                'suggested_deadline': None
            }
    
    def classify_batch(self, emails_data: List[Dict], batch_size: int = 5) -> List[Dict]:
        """Classify multiple emails in batches."""
        
        results = []
        
        for i in range(0, len(emails_data), batch_size):
            batch = emails_data[i:i + batch_size]
            
            logger.info(f"Processing batch {i//batch_size + 1}, emails {i+1}-{min(i+batch_size, len(emails_data))}")
            
            batch_results = []
            for email_data in batch:
                try:
                    classification = self.classify_email(email_data)
                    batch_results.append(classification)
                    
                    # Delay between requests
                    import time
                    time.sleep(2)  # 2 seconds between requests
                    
                except Exception as e:
                    logger.error(f"Error classifying email: {str(e)}")
                    # Use fallback for this email
                    if self.openai_service:
                        batch_results.append(self.openai_service._fallback_classification(email_data))
                    else:
                        batch_results.append({
                            'urgency_category': 'medium',
                            'confidence_score': 0.5,
                            'reasoning': 'Classification failed',
                            'sender_type': 'externo',
                            'email_type': 'academico',
                            'requires_immediate_action': False,
                            'suggested_deadline': None
                        })
            
            results.extend(batch_results)
            
            # Delay between batches
            if i + batch_size < len(emails_data):
                import time
                time.sleep(5)  # 5 seconds between batches
        
        logger.info(f"Completed batch classification of {len(emails_data)} emails")
        return results
    
    def get_classification_stats(self, classifications: List[Dict]) -> Dict:
        """Generate statistics from classification results."""
        
        if not classifications:
            return {}
        
        stats = {
            'total_classified': len(classifications),
            'by_urgency': {'urgent': 0, 'high': 0, 'medium': 0, 'low': 0},
            'by_sender_type': {'estudiante': 0, 'profesor': 0, 'administracion': 0, 'externo': 0},
            'by_email_type': {'academico': 0, 'administrativo': 0, 'personal': 0, 'emergencia': 0},
            'avg_confidence': 0,
            'high_confidence_count': 0,
            'requires_immediate_action': 0
        }
        
        total_confidence = 0
        
        for classification in classifications:
            # Count by urgency
            urgency = classification.get('urgency_category', 'medium')
            if urgency in stats['by_urgency']:
                stats['by_urgency'][urgency] += 1
            
            # Count by sender type
            sender_type = classification.get('sender_type', 'externo')
            if sender_type in stats['by_sender_type']:
                stats['by_sender_type'][sender_type] += 1
            
            # Count by email type
            email_type = classification.get('email_type', 'academico')
            if email_type in stats['by_email_type']:
                stats['by_email_type'][email_type] += 1
            
            # Confidence stats
            confidence = classification.get('confidence_score', 0)
            total_confidence += confidence
            if confidence >= 0.8:
                stats['high_confidence_count'] += 1
            
            # Immediate action count
            if classification.get('requires_immediate_action', False):
                stats['requires_immediate_action'] += 1
        
        stats['avg_confidence'] = round(total_confidence / len(classifications), 3)
        stats['high_confidence_percentage'] = round((stats['high_confidence_count'] / len(classifications)) * 100, 1)
        
        return stats
