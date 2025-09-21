"""
Gemini Service
Handles AI-powered email classification using Google Gemini.
"""

import google.generativeai as genai
from flask import current_app
import logging
import json
from datetime import datetime
from typing import List, Dict

logger = logging.getLogger(__name__)

class GeminiService:
    """Service class for Gemini API operations with academic email classification."""
    
    def __init__(self, config=None):
        self.config = config or current_app.config
        self.api_key = self.config.get('GEMINI_API_KEY')
        self.model_name = 'gemini-pro'
        
        # Debug logging
        logger.info(f"Gemini API key configured: {bool(self.api_key)}")
        logger.info(f"Gemini API key value: {self.api_key[:10] if self.api_key else 'None'}...")
        
        self.client = None
        if self.api_key and self.api_key != 'your-gemini-api-key-here':
            try:
                # Configure Gemini
                genai.configure(api_key=self.api_key)
                self.client = genai.GenerativeModel(self.model_name)
                logger.info("✅ Gemini client initialized successfully")
            except Exception as e:
                logger.warning(f"❌ Failed to initialize Gemini client: {e}")
                self.client = None
        else:
            logger.warning("⚠️ Gemini API key not configured")
        
        # Academic context patterns - REAL urgent situations
        self.urgent_keywords = [
            'emergencia', 'accidente', 'hospital', 'ambulancia', 'lesion',
            'lesionado', 'herido', 'caída', 'golpe', 'sangre', 'desmayo',
            'crisis', 'problema grave', 'suspensión', 'expulsión', 'ayuda',
            'socorro', 'grave', 'inmediato', 'hoy mismo', 'crítico'
        ]
        
        # Non-urgent keywords that might be confused with urgent
        self.non_urgent_indicators = [
            'qué día', 'que dia', 'cuando', 'cuándo', 'horario', 'hora',
            'información', 'consulta', 'pregunta', 'duda', 'ayuda con',
            'necesito saber', 'podrías decirme', 'me puedes ayudar',
            'solo quería', 'solo queria', 'nada urgente', 'no es urgente',
            'cuando puedas', 'cuando tengas tiempo', 'no hay prisa'
        ]
        
        self.high_priority_keywords = [
            'reunión', 'junta', 'consejo', 'deadline', 'plazo', 'entrega',
            'examen', 'evaluación', 'presentación', 'defensa', 'tesis',
            'calificación', 'nota', 'reprobado', 'aprobado', 'suspensión',
            'expulsión', 'disciplinario', 'problema', 'conflicto', 'queja'
        ]
        
        self.academic_roles = {
            'estudiante': ['estudiante', 'alumno', 'alumna', '@uss.cl'],
            'profesor': ['profesor', 'profesora', 'docente', 'académico'],
            'administracion': ['secretaria', 'coordinador', 'director', 'decanato']
        }
    
    def get_status(self):
        """Get service status."""
        return {
            'service': 'GeminiService',
            'status': 'ready' if self.api_key else 'no_api_key',
            'model': self.model_name,
            'message': 'Gemini service ready for academic email classification' if self.api_key else 'Gemini API key not configured'
        }
    
    def _build_classification_prompt(self, email_data: Dict) -> str:
        """Build specialized prompt for academic email classification."""
        
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        # Smart content truncation - keep important parts
        content = email_data.get('body_preview', '')
        if len(content) > 400:
            # Keep first 200 chars and last 200 chars for context
            content = content[:200] + "..." + content[-200:]
        
        base_prompt = f"""Eres un asistente especializado en clasificar correos para Maritza Silva, Directora de ICIF en Universidad San Sebastián, Chile.

CONTEXTO: Directora universitaria que gestiona estudiantes, profesores y personal. Debe responder emergencias rápidamente.

NIVELES DE URGENCIA:
1. URGENTE (1 hora): Emergencias médicas, accidentes, crisis de seguridad, acción INMEDIATA
2. ALTA (3 horas): Problemas académicos graves, reuniones urgentes hoy, deadlines críticos
3. MEDIA (hoy/próximos días): Solicitudes académicas con plazo, cambios de horario, coordinación
4. BAJA (mañana+): Información general, invitaciones futuras, documentación no urgente

PALABRAS CLAVE CRÍTICAS para URGENTE:
- Emergencias: accidente, lesión, hospital, ambulancia, herido, sangre, desmayo, caída
- Crisis: ayuda, socorro, crítico, grave, urgente, emergencia
- Seguridad: peligro, amenaza, violencia, drogas, alcohol

EJEMPLOS:
- URGENTE: "Estudiante herido en laboratorio, necesita ambulancia"
- ALTA: "Reunión urgente hoy a las 3pm para resolver problema académico"
- MEDIA: "Solicitud cambio de horario con plazo viernes 20 septiembre"
- BAJA: "Consulta general sobre horarios del próximo semestre"

CORREO A CLASIFICAR:
Remitente: {email_data.get('sender_name', '')} <{email_data.get('sender_email', '')}>
Asunto: {email_data.get('subject', '')}
Fecha recibido: {email_data.get('received_at', '')}
Contenido: {content}

INSTRUCCIONES:
1. Analiza el contexto académico del remitente (estudiante/profesor/administración)
2. Identifica palabras clave de urgencia y deadlines
3. Considera la proximidad temporal de eventos
4. Evalúa el impacto en las responsabilidades de la directora

Responde SOLO en formato JSON válido:
{{
    "urgency_category": "urgent|high|medium|low",
    "confidence_score": 0.85,
    "reasoning": "Explicación breve de la clasificación",
    "sender_type": "estudiante|profesor|administracion|externo",
    "email_type": "academico|administrativo|personal|emergencia",
    "requires_immediate_action": true/false,
    "suggested_deadline": "2024-01-15T14:00:00" // o null
}}"""
        
        return base_prompt.strip()
    
    def classify_email(self, email_data: Dict) -> Dict:
        """Classify a single email using Gemini."""
        
        logger.info(f"Starting email classification with Gemini for: {email_data.get('subject', 'No subject')[:50]}...")
        logger.info(f"Gemini client status: {self.client is not None}")
        logger.info(f"API key configured: {bool(self.api_key)}")
        
        if not self.client:
            logger.warning("Gemini client not configured - using fallback")
            return self._fallback_classification(email_data)
        
        try:
            prompt = self._build_classification_prompt(email_data)
            logger.info(f"Prompt length: {len(prompt)} characters")
            
            logger.info("Making Gemini API call...")
            response = self.client.generate_content(prompt)
            
            if not response.text:
                raise Exception("Empty response from Gemini")
            
            logger.info("Gemini API call successful")
            
            content = response.text.strip()
            logger.info(f"Gemini response received: {content[:200]}...")
            
            # Clean response - remove markdown formatting if present
            if content.startswith('```json'):
                content = content[7:]  # Remove ```json
            if content.endswith('```'):
                content = content[:-3]  # Remove ```
            content = content.strip()
            
            # Parse JSON response
            try:
                classification = json.loads(content)
                logger.info(f"JSON parsed successfully: {classification}")
                
                # Validate required fields
                required_fields = ['urgency_category', 'confidence_score', 'reasoning']
                for field in required_fields:
                    if field not in classification:
                        raise ValueError(f"Missing required field: {field}")
                
                # Normalize urgency category
                urgency = classification['urgency_category'].lower()
                if urgency not in ['urgent', 'high', 'medium', 'low']:
                    urgency = 'medium'
                classification['urgency_category'] = urgency
                
                # Ensure confidence score is float between 0-1
                confidence = float(classification['confidence_score'])
                classification['confidence_score'] = max(0.0, min(1.0, confidence))
                
                logger.info(f"✅ Email classified as {urgency} with confidence {confidence}")
                return classification
                
            except (json.JSONDecodeError, ValueError, KeyError) as e:
                logger.error(f"❌ Error parsing Gemini response: {e}")
                logger.error(f"Raw response: {content}")
                logger.warning("Falling back to rule-based classification")
                return self._fallback_classification(email_data)
        
        except Exception as e:
            error_str = str(e)
            logger.error(f"❌ Gemini API error: {error_str}")
            logger.warning("Falling back to rule-based classification")
            return self._fallback_classification(email_data)
    
    def _fallback_classification(self, email_data: Dict) -> Dict:
        """Fallback classification when Gemini is unavailable."""
        
        subject = email_data.get('subject', '').lower()
        body = email_data.get('body_preview', '').lower()
        sender_email = email_data.get('sender_email', '').lower()
        text_content = f"{subject} {body}"
        
        # Rule-based classification - start with different defaults to avoid medium bias
        urgency = 'low'  # Start with low as default
        confidence = 0.6
        reasoning = "Clasificación basada en reglas (Gemini no disponible)"
        
        # Check for non-urgent indicators first (to avoid false positives)
        has_non_urgent_indicators = any(keyword in text_content for keyword in self.non_urgent_indicators)
        has_urgent_keywords = any(keyword in text_content for keyword in self.urgent_keywords)
        
        # If it has non-urgent indicators, it's likely not urgent even if it says "urgente"
        if has_non_urgent_indicators and not has_urgent_keywords:
            urgency = 'low'
            confidence = 0.8
            reasoning = "Contenido indica consulta no urgente (a pesar de palabras como 'urgente')"
        
        # Check for REAL urgent keywords (only if no non-urgent indicators)
        elif has_urgent_keywords and not has_non_urgent_indicators:
            urgency = 'urgent'
            confidence = 0.9
            reasoning = "Detectadas palabras clave de urgencia crítica real"
        
        # Check for high priority keywords
        elif any(keyword in text_content for keyword in self.high_priority_keywords):
            urgency = 'high'
            confidence = 0.8
            reasoning = "Detectadas palabras clave de alta prioridad académica"
        
        # Check for medium priority indicators
        elif any(keyword in text_content for keyword in ['consulta', 'pregunta', 'ayuda', 'información', 'horario', 'clase', 'materia', 'asignatura']):
            urgency = 'medium'
            confidence = 0.7
            reasoning = "Consulta académica que requiere respuesta"
        
        # Student emails from USS get medium priority only if they contain academic content
        elif '@uss.cl' in sender_email:
            if any(keyword in text_content for keyword in ['consulta', 'pregunta', 'ayuda', 'información', 'horario', 'clase', 'materia', 'asignatura', 'profesor', 'docente']):
                urgency = 'medium'
                confidence = 0.7
                reasoning = "Correo de estudiante USS con contenido académico"
            else:
                urgency = 'low'
                confidence = 0.6
                reasoning = "Correo de estudiante USS - contenido general"
        
        # External emails are generally low priority unless urgent keywords
        else:
            urgency = 'low'
            confidence = 0.5
            reasoning = "Correo externo - prioridad baja"
        
        # Determine sender type
        sender_type = 'externo'
        if '@uss.cl' in sender_email:
            sender_type = 'estudiante'
        elif any(keyword in text_content for keyword in self.academic_roles['profesor']):
            sender_type = 'profesor'
        elif any(keyword in text_content for keyword in self.academic_roles['administracion']):
            sender_type = 'administracion'
        
        return {
            'urgency_category': urgency,
            'confidence_score': confidence,
            'reasoning': reasoning,
            'sender_type': sender_type,
            'email_type': 'academico',
            'requires_immediate_action': urgency in ['urgent', 'high'],
            'suggested_deadline': None
        }
